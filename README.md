🎨 KalaConnect - The Artisan's Digital Storyteller
KalaConnect is an AI-powered web application designed to empower local Indian artisans by helping them with their digital marketing efforts. It provides easy-to-use tools to generate compelling product descriptions and engaging social media content, bridging the gap between traditional craftsmanship and the modern digital marketplace.

This project is a submission for the Google Cloud Gen AI Exchange Hackathon 2025 (Student Track).

Live Demo URL: [Insert Your Deployed Streamlit App URL Here]

1. Introduction
In the heart of India, millions of artisans create beautiful, handcrafted goods. However, they often face significant challenges in marketing their craft online, lacking the time, resources, or digital marketing expertise. KalaConnect was built to solve this problem. It acts as a personal marketing assistant, using the power of Google's Generative AI to craft beautiful stories and engaging content, allowing artisans to focus on what they do best: creating.

2. Installation and Setup
To run this project on your local machine, please follow these steps.

Prerequisites
Python 3.11

Git

A Google Cloud Platform (GCP) project with the Vertex AI API enabled and billing set up.

Step-by-Step Guide
Clone the Repository
Open your terminal and clone this repository to your local machine:

git clone https://github.com/YourUsername/KalaConnect.git
cd KalaConnect

Create and Activate a Python Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

# Create the environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate

Install Required Dependencies
Install all the necessary libraries using the requirements.txt file.

pip install -r requirements.txt

Set Up Google Cloud Credentials
This application uses Google's Application Default Credentials (ADC) for authentication.

Follow this Google Cloud ADC guide to set up your credentials locally.

Ensure your PROJECT_ID in backend.py is set to your actual Google Cloud Project ID.

3. Usage
Once the setup is complete, you can run the application with a single command.

Run the Streamlit App
In your terminal (with the virtual environment activated), run the following command from the project's root directory:

streamlit run app.py

Using the Application

Your web browser will automatically open to the application's UI.

Navigate between the "Product Description Generator" and "Social Media Post Generator" tabs.

In the appropriate tab, enter a simple description of your product in the text area.

Click the "Generate" button and wait for the AI to craft your content.

4. Features and Functionality
Key Features
AI Product Description Generator: Takes a basic user input and transforms it into a warm, evocative, and marketing-focused product description suitable for e-commerce sites like Etsy or a personal website.

AI Social Media Post Generator: Generates three distinct and creative Instagram post ideas based on a product description. Each idea includes an engaging caption and a list of relevant, high-traffic hashtags to maximize reach.

Simple & Intuitive UI: The application is built with Streamlit for a clean, user-friendly, and responsive interface that is accessible even to users with limited technical skills.

Limitations
This is a prototype. The AI's output, while generally high-quality, should be reviewed and edited by the user before publishing.

The application currently relies on a single Generative AI model (Gemini -2.0-Flash ) and does not yet incorporate multimodal features (image inputs).

5. Troubleshooting
If you encounter issues while running the app, here are a few common solutions:

ModuleNotFoundError: This usually means dependencies are not installed correctly. Ensure your virtual environment is active and you have run pip install -r requirements.txt.

Authentication Errors (e.g., PermissionDenied): This indicates a problem with your Google Cloud credentials. Re-run the ADC setup steps and ensure the Vertex AI API is enabled for your project.

Billing Disabled Error: The Vertex AI API requires billing to be enabled on your Google Cloud project. Please follow the link in the error message to enable it. (Note: You will likely not be charged due to Google Cloud's generous free tier and free trial credits).

Credits & Acknowledgements
Framework: Streamlit

AI Model: Google's Gemini on Vertex AI

Banner Image: [Pexels / Unsplash] 