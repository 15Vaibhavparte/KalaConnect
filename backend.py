import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import translate_v2 as translate # Import the Translation library

# Load environment variables from .env file
load_dotenv()

# --- GCP Project Configuration ---
PROJECT_ID = "kalaconnect-hackathon" # Replace with your actual project ID
LOCATION = "us-central1"

# Initialize the Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=LOCATION)
# Initialize the Translation client
translate_client = translate.Client()

# --- New Translation Function ---
def translate_text(text: str, target_language: str) -> str:
    """Translates text into the target language."""
    if not text:
        return ""
    
    # The translation API returns a dictionary, we need the 'translatedText' value
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

# --- Updated AI Generation Functions ---
def generate_product_description(product_input: str, target_language: str = "en"):
    """
    Generates a marketing-focused product description in the target language.
    """
    # Step 1: Translate the user's input to English for the best AI performance
    input_in_english = translate_text(product_input, "en")

    # Load the Gemini 1.5 Flash model (updated model name)
    model = GenerativeModel("gemini-1.5-flash-latest")

    prompt = f"""
    You are a marketing expert specializing in helping local Indian artisans.
    Your tone is warm, evocative, and appreciative of traditional craftsmanship.
    An artisan has provided the following details about their product.
    Artisan's input: "{input_in_english}"

    Based on this, write a compelling and beautiful product description (around 100-150 words)
    in English that they can use on an e-commerce website.
    """

    try:
        # Step 2: Generate the content in English
        response = model.generate_content(prompt)
        english_description = response.text

        # Step 3: Translate the English output back to the user's target language
        if target_language != "en":
            translated_description = translate_text(english_description, target_language)
            return translated_description
        else:
            return english_description

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I'm having a little trouble connecting to the creative cloud right now. Please try again in a moment."


def generate_social_media_post(product_input: str, target_language: str = "en"):
    """
    Generates 3 engaging Instagram post ideas in the target language.
    """
    # Step 1: Translate input to English
    input_in_english = translate_text(product_input, "en")

    model = GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    You are a creative social media manager for Indian handicraft brands.
    Your goal is to create engaging, short-form content for Instagram in English.
    An artisan has provided the following details about their product: "{input_in_english}"

    Based on this, generate 3 distinct Instagram post ideas in English.
    Each post idea must include a caption and relevant hashtags.
    Format the output clearly using markdown.
    """
    try:
        # Step 2: Generate content in English
        response = model.generate_content(prompt)
        english_posts = response.text

        # Step 3: Translate the English output back to the target language
        if target_language != "en":
            translated_posts = translate_text(english_posts, target_language)
            return translated_posts
        else:
            return english_posts
            
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