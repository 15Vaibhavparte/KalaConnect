import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from vertexai.preview.vision_models import ImageGenerationModel

# Load environment variables FIRST
load_dotenv()

# --- GCP Project Configuration ---
PROJECT_ID = "kalaconnect-hackathon"
LOCATION = "us-central1"

# Initialize the Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=LOCATION)

# --- Internal Helper Function for Image Generation ---
def _generate_product_image(full_image_prompt: str):
    """
    Generates a product image based on a full, detailed prompt.
    """
    try:
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002") 
        
        # We now pass the entire, pre-engineered prompt to this function
        response = model.generate_images(prompt=full_image_prompt, number_of_images=1)
        return response[0]._image_bytes
    except Exception as e:
        print(f"Image generation failed: {e}")
        return None

# --- Main Orchestration Function (Now with two-step prompting for better image accuracy) ---
def generate_all_content(product_input: str, image_data=None, image_style="Artistic Lifestyle", 
                        regenerate_image_only=False, regenerate_desc_only=False, regenerate_posts_only=False):
    """
    Generates all content based on text and/or an uploaded image using two-step prompting for better accuracy.
    
    Args:
        product_input: Text description of the product
        image_data: Binary image data if an image was uploaded
        image_style: "Artistic Lifestyle" or "Clean Studio Background"
        regenerate_image_only: If True, only regenerate the image
        regenerate_desc_only: If True, only regenerate the product description
        regenerate_posts_only: If True, only regenerate the social media posts
    """
    text_model = GenerativeModel("gemini-2.5-flash")
    
    # --- Step 1: Analyze the Input (Text or Image) ---
    if image_data:
        image_part = Part.from_data(data=image_data, mime_type="image/jpeg")
        
        # First, we ask Gemini to create a very detailed description of the uploaded image.
        detailed_desc_prompt = [
            "You are a meticulous product photographer's assistant. "
            "Describe the following image of a handcrafted product in extreme detail. "
            "Mention the exact type of product, "
            "the precise colors, the style of any patterns or designs, the material texture, "
            "and the overall aesthetic. Be very specific.",
            image_part
        ]
        response = text_model.generate_content(detailed_desc_prompt)
        detailed_description_from_image = response.text.strip()
        
        # Use this as the base for generating content
        base_content = detailed_description_from_image
    else:
        # Use the user's text input as the source
        base_content = product_input

    # --- Step 2: Generate Product Description (Separate Call) ---
    if not regenerate_image_only and not regenerate_posts_only:
        desc_prompt = f"""
        You are a marketing expert for handcrafted Indian products. 
        Based on this product: "{base_content}"
        
        Write a compelling and beautiful product description (around 100-150 words) for an e-commerce website.
        Make it warm, evocative, and appreciative of traditional craftsmanship.
        Do not include any introductory text or task labels - just provide the pure product description.
        """
        
        description_response = text_model.generate_content([desc_prompt])
        description = description_response.text.strip()
    else:
        # Skip generating description if only regenerating image or posts
        description = "Not regenerated"

    # --- Step 3: Generate Social Media Posts (Separate Call) ---
    if not regenerate_image_only and not regenerate_desc_only:
        social_prompt = f"""
        You are a social media manager for Indian handicraft brands.
        Based on this product: "{base_content}"
        
        Generate 3 Instagram post ideas. Format your response EXACTLY like this with proper line breaks:

## Instagram Post Idea 1: [Creative Title]

**Caption:** [Write an engaging caption here]

**Hashtags:** [List relevant hashtags]

---

## Instagram Post Idea 2: [Creative Title]

**Caption:** [Write an engaging caption here]

**Hashtags:** [List relevant hashtags]

---

## Instagram Post Idea 3: [Creative Title]

**Caption:** [Write an engaging caption here]

**Hashtags:** [List relevant hashtags]

Do not include any introductory text or task labels - start directly with the first post idea.
        """
        
        social_response = text_model.generate_content([social_prompt])
        social_posts = social_response.text.strip()
    else:
        # Skip generating social posts if only regenerating image or description
        social_posts = "Not regenerated"

    # --- Step 4: NEW - Identify Product Category for Scene-Aware Background ---
    category_prompt = f"""
    Based on the following product description, what is the single best category for this item?
    Also specify if it's a fabric pattern/swatch, small textile item, or full garment.
    Choose from: Pottery, Jewelry, Textile-Pattern, Textile-Small, Textile-Garment, Painting, Woodcraft, Metalwork, Other.
    Description: "{base_content}"
    
    Respond with just the category name.
    """
    category_response = text_model.generate_content([category_prompt])
    product_category = category_response.text.strip().lower()

    # --- Step 5: NEW - Select an Artistic Background Scene ---
    # Based on the category, we choose a beautiful, relevant setting.
    background_scene = "in a beautifully styled lifestyle setting that complements its colors and textures"  # Default
    
    if "pottery" in product_category:
        background_scene = "on a rustic wooden table, next to a window with soft, diffused morning light streaming in. A few dried flowers are artfully placed nearby"
    elif "jewelry" in product_category:
        background_scene = "delicately displayed on a natural piece of slate or dark marble, with a soft, out-of-focus background"
    elif "textile-pattern" in product_category or "textile-small" in product_category:
        background_scene = "professionally styled on a dress form mannequin in a bright, modern photography studio with clean white backdrop and professional lighting"
    elif "textile-garment" in product_category:  # Full garments like sarees, dresses
        background_scene = "beautifully styled on an elegant fashion mannequin in a sophisticated photography studio with soft, professional lighting and a clean, minimalist background"
    elif "painting" in product_category:
        background_scene = "hanging on a tastefully decorated, neutral-colored wall in a modern, minimalist living room, with a soft spotlight highlighting its details"
    elif "woodcraft" in product_category:
        background_scene = "placed on a clean, light-colored surface, with soft shadows and a hint of green foliage in the background"
    elif "metalwork" in product_category:
        background_scene = "artfully arranged on a textured stone surface with warm, golden lighting that highlights the metal's finish"

    # --- Step 6: Construct the Final Image Prompt Based on Selected Style ---
    if image_style == "Artistic Lifestyle":
        final_image_prompt = f"""
        A hyper-realistic, artistic lifestyle photograph of: {base_content}.
        The product is featured {background_scene}.
        The image should have a shallow depth of field, making the product the sharp focus.
        The mood is warm, serene, and authentic.
        Photographed with a professional DSLR camera, cinematic quality, 8k resolution.
        """
    else:  # Clean Studio Background
        final_image_prompt = f"""
        A clean, professional product photography of: {base_content}.
        The product is centered on a simple white or light gray background with subtle shadows.
        The lighting is bright, even, and highlights all details and textures of the product.
        The image has perfect focus and clarity, showing the craftsmanship in crisp detail.
        Commercial product photography style, perfect for e-commerce, 8k resolution.
        """

    # --- Step 7: Generate Image (Unless skipping for regenerate options) ---
    if not regenerate_desc_only and not regenerate_posts_only:
        generated_image_bytes = _generate_product_image(final_image_prompt)
    else:
        # Skip generating image if only regenerating description or posts
        generated_image_bytes = None

    # --- Step 8: Return all results ---
    return {
        "description": description,
        "social_posts": social_posts,
        "image": generated_image_bytes
    }

# --- For Testing ---
if __name__ == '__main__':
    # Test the functions
    test_input = "Blue pottery mug from Jaipur with floral designs"
    print("--- Generated Content ---")
    content = generate_all_content(test_input)
    print("Description:")
    print(content["description"])
    print("\nSocial Media Posts:")
    print(content["social_posts"])
    # Image content is in bytes, so we just confirm it's not None
    print("\nProduct Image:")
    print("Generated" if content["image"] is not None else "Failed to generate image")