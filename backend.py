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
    # Load the Gemini 1.0 Flash model
    model = GenerativeModel("gemini-1.0-flash")

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
    except Exception as e:
        # Handle potential errors, e.g., safety blocks, API issues
        return f"An error occurred: {e}"

# --- For Testing ---
if __name__ == '__main__':
    # This block runs only when you execute backend.py directly
    test_input = "A handmade blue pottery mug from Jaipur. It is painted with a floral design. It is microwave safe."
    description = generate_product_description(test_input)
    print("--- Generated Description ---")
    print(description)