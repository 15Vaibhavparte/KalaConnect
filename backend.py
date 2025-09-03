import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel

# Load environment variables FIRST
load_dotenv()

# --- GCP Project Configuration ---
PROJECT_ID = "kalaconnect-hackathon"
LOCATION = "us-central1"

# Initialize the Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=LOCATION)

# --- AI Generation Functions (Translation Removed) ---
def generate_product_description(product_input: str, target_language: str = "en"):
    """Generates a marketing-focused product description."""
    # Translation logic is removed. The function now ignores the target_language parameter.
    
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
        print(f"An error occurred: {e}")
        return "Sorry, I'm having a little trouble connecting to the creative cloud right now. Please try again in a moment."


def generate_social_media_post(product_input: str, target_language: str = "en"):
    """
    Generates 3 engaging Instagram post ideas.
    """
    # Translation logic is removed.
    
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
        print(f"An error occurred: {e}")
        return "Sorry, I'm having a little trouble connecting to the creative cloud right now. Please try again in a moment."

# --- For Testing ---
if __name__ == '__main__':
    # Test the functions
    test_input = "Blue pottery mug from Jaipur with floral designs"
    print("--- Generated Description ---")
    print(generate_product_description(test_input))
    print("\n--- Generated Social Media Posts ---")
    print(generate_social_media_post(test_input))