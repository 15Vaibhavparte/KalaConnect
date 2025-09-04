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
def _generate_product_image(product_input: str):
    """Generates a product image based on the input description."""
    try:
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002") 
        
        image_prompt = f"""
        A hyper-realistic, professional product photograph of: {product_input}.
        The product should be the central focus, displayed on a clean, neutral background.
        The lighting should be soft and natural, highlighting the product's textures and details.
        8k resolution, photorealistic, cinematic lighting.
        """
        
        response = model.generate_images(prompt=image_prompt, number_of_images=1)
        return response[0]._image_bytes
    except Exception as e:
        print(f"Image generation failed: {e}")
        return None

# --- Main Orchestration Function (Now with two-step prompting for better image accuracy) ---
def generate_all_content(product_input: str, image_data=None):
    """
    Generates all content based on text and/or an uploaded image using two-step prompting for better accuracy.
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
    desc_prompt = f"""
    You are a marketing expert for handcrafted Indian products. 
    Based on this product: "{base_content}"
    
    Write a compelling and beautiful product description (around 100-150 words) for an e-commerce website.
    Make it warm, evocative, and appreciative of traditional craftsmanship.
    Do not include any introductory text or task labels - just provide the pure product description.
    """
    
    description_response = text_model.generate_content([desc_prompt])
    description = description_response.text.strip()

    # --- Step 3: Generate Social Media Posts (Separate Call) ---
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

    # --- Step 4: Generate an Image from Imagen (using the detailed description) ---
    generated_image_bytes = _generate_product_image(base_content)

    # --- Step 5: Return all results ---
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