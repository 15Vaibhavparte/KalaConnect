import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel

# Load environment variables from .env file
load_dotenv()

# --- Step 1: Initialize Vertex AI ---
# Get your project ID from the Google Cloud Console
PROJECT_ID = "kalaconnect-hackathon" # Replace with your actual project ID
LOCATION = "us-central1" # e.g., us-central1

# Initialize the Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=LOCATION)

# --- Step 2: Create the AI Model Function ---
def generate_product_description(product_input):
    """
    This function takes an artisan's product description and generates a marketing-focused one.
    """
    # Load the Gemini 2.0 Flash model
    model = GenerativeModel("gemini-2.0-flash")

    # --- Step 3: Engineer the Prompt ---
    # This is where you guide the AI. A good prompt is crucial!
    prompt = f"""
    You are a marketing expert specializing in helping local Indian artisans.
    Your tone is warm, evocative, and appreciative of traditional craftsmanship.
    An artisan has provided the following details about their product.
    Artisan's input: "{product_input}"

    Based on this, write a compelling and beautiful product description (around 100-150 words)
    that they can use on an e-commerce website. Highlight the handmade nature,
    the potential story behind the craft, and the materials used. Do not use generic phrases.
    Make it sound authentic and personal.
    """

    # --- Step 4: Generate the Content ---
    try:
        response = model.generate_content(prompt)
        return response.text
    # New, user-friendly error
    except Exception as e:
        print(f"An error occurred: {e}") # You can still see the technical error in your terminal
        return "Sorry, I'm having a little trouble connecting to the creative cloud right now. Please try again in a moment."

# --- For Testing ---
if __name__ == '__main__':
    # This block runs only when you execute backend.py directly
    test_input = "A handmade blue pottery mug from Jaipur. It is painted with a floral design. It is microwave safe."
    description = generate_product_description(test_input)
    print("--- Generated Description ---")
    print(description)

# This function uses Google Vertex AI's Gemini 2.0 Flash model to generate three Instagram post ideas for a given artisan product description.
# It crafts a detailed prompt instructing the AI to create engaging captions and relevant hashtags, formatted in markdown for clarity.
# The function handles errors gracefully and returns either the AI's response or an error message.
def generate_social_media_post(product_input):
    """
    Generates 3 engaging Instagram post ideas for a product.
    """
    # Load the Gemini 2.0 Flash model
    model = GenerativeModel("gemini-2.0-flash")

    # Engineer a new prompt specifically for social media
    prompt = f"""
    You are a creative social media manager for Indian handicraft brands.
    Your goal is to create engaging, short-form content for Instagram to drive sales and tell a story.
    An artisan has provided the following details about their product: "{product_input}"

    Based on this, generate 3 distinct Instagram post ideas.
    Each post idea must include:
    1. A captivating caption (around 30-50 words) that tells a small story or asks a question.
    2. A list of 5-7 relevant and popular hashtags (including #indianhandicraft, #handmade, #localartisan, #shopsmall, and others specific to the craft).

    Format the output clearly using markdown, with a heading for each post idea.
    For example:
    **Post Idea 1: The Making Of**
    *Caption:* ...
    *Hashtags:* ...
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"