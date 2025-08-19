import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# For Streamlit Cloud
if hasattr(st, 'secrets'):
    PROJECT_ID = st.secrets["gcp"]["PROJECT_ID"]
    LOCATION = st.secrets["gcp"]["LOCATION"]
    
    # Set up credentials from secrets
    import json
    import tempfile
    
    if "GOOGLE_APPLICATION_CREDENTIALS_JSON" in st.secrets["gcp"]:
        service_account_info = json.loads(st.secrets["gcp"]["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(service_account_info, f)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f.name
else:
    # Set credentials from .env file
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if credentials_path:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

try:
    from google.cloud import translate_v2 as translate
except ImportError:
    # Alternative import method
    from google.cloud import translate

# Load environment variables from .env file
load_dotenv()

# --- GCP Project Configuration ---
PROJECT_ID = "kalaconnect-hackathon" # Replace with your actual project ID
LOCATION = "us-central1"

# Initialize the Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=LOCATION)
# Initialize the Translation client (v2)
translate_client = translate.Client()

# --- Translation Function ---
def translate_text(text: str, target_language: str) -> str:
    """Translates text into the target language using v2 client."""
    if not text or target_language == "en":
        return text
    
    try:
        # Use v2 API syntax
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails

# --- AI Generation Functions ---
def generate_product_description(product_input: str, target_language: str = "en"):
    """
    Generates a marketing-focused product description in the target language.
    """
    # Step 1: Translate the user's input to English for the best AI performance
    input_in_english = translate_text(product_input, "en") if target_language != "en" else product_input

    # Load the Gemini 2.0 Flash model (updated model name)
    model = GenerativeModel("gemini-2.0-flash")

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
    input_in_english = translate_text(product_input, "en") if target_language != "en" else product_input

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
            reformatted_posts = reformat_translated_posts(translated_posts)
            return reformatted_posts
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

def reformat_translated_posts(text: str) -> str:
    """
    Takes a translated block of text and re-applies markdown formatting.
    """
    # Split the text into individual post ideas
    # Assuming the translator keeps "Post Idea" or a similar phrase
    # We use a common Hindi translation for "Post Idea" as a splitter
    posts = text.split('पोस्ट आइडिया')
    if len(posts) < 2: # If splitting didn't work, try the English phrase
        posts = text.split('Post Idea')

    formatted_posts = []
    for post in posts:
        if post.strip() == "":
            continue
        
        lines = post.strip().split('\n')
        
        # Make the title (Post Idea X) bold
        lines[0] = f"**Post Idea{lines[0]}**"
        
        # Reformat the rest of the lines
        reformatted_lines = [lines[0]]
        for line in lines[1:]:
            # Make keywords like 'Caption' and 'Hashtags' bold
            if ":" in line:
                parts = line.split(":", 1)
                line = f"**{parts[0].strip()}:**{parts[1]}"
            reformatted_lines.append(line)
        
        formatted_posts.append("\n".join(reformatted_lines))
        
    # Join the formatted posts with a double newline for spacing
    return "\n\n---\n\n".join(formatted_posts)