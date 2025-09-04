import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.preview.vision_models import ImageGenerationModel

# Load environment variables FIRST
load_dotenv()

# --- GCP Project Configuration ---
PROJECT_ID = "kalaconnect-hackathon"
LOCATION = "us-central1"

# Initialize the Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=LOCATION)

# --- Internal Helper Functions for Content Generation ---

def _generate_product_description(product_input: str):
    """Generates a marketing-focused product description."""
    model = GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a marketing expert specializing in helping local Indian artisans.
    Your tone is warm, evocative, and appreciative of traditional craftsmanship.
    An artisan has provided the following details about their product.
    Artisan's input: "{product_input}"

    Based on this, write a compelling and beautiful product description (around 100-150 words)
    that they can use on an e-commerce website.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Description generation failed: {e}")
        return "Sorry, I'm having a little trouble writing the description right now."

def _generate_social_media_post(product_input: str):
    """Generates 3 engaging Instagram post ideas."""
    model = GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a creative social media manager for Indian handicraft brands.
    Your goal is to create engaging, short-form content for Instagram.
    An artisan has provided the following details about their product: "{product_input}"

    Based on this, generate 3 distinct Instagram post ideas.
    Each post idea must include a caption and relevant hashtags.
    Format the output clearly using markdown.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Social media post generation failed: {e}")
        return "Sorry, I'm having a little trouble brainstorming social media posts right now."

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

# --- Main Orchestration Function ---
def generate_all_content(product_input: str):
    """
    Generates product description, social media posts, and an image simultaneously.
    """
    # --- Generate all content ---
    description = _generate_product_description(product_input)
    social_posts = _generate_social_media_post(product_input)
    generated_image_bytes = _generate_product_image(product_input)

    # --- Return all results together in a dictionary ---
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