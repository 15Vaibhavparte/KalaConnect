import streamlit as st
from backend import generate_product_description # Import our AI function

# --- Page Configuration ---
st.set_page_config(
    page_title="KalaConnect AI Assistant",
    page_icon="🎨", # You can use emojis as icons
    layout="centered"
)

# --- Application UI ---
st.title("🎨 KalaConnect - The Artisan's Digital Storyteller")
st.write("Welcome! Describe your craft, and I'll help you write beautiful descriptions for it.")

# --- Step 1: Create the Input Form ---
with st.form("product_form"):
    st.subheader("Tell me about your product:")
    product_input = st.text_area("Enter a few details (e.g., materials used, craft name, special features):")

    # --- Step 2: Create the Submission Button ---
    submitted = st.form_submit_button("✨ Generate Description")

# --- Step 3: Handle the Submission ---
if submitted:
    if product_input:
        # Show a loading spinner while the AI is working
        with st.spinner("Crafting the perfect description for you..."):
            # Call the backend function
            generated_description = generate_product_description(product_input)
            
            # Display the result
            st.subheader("Here's your AI-Generated Product Description:")
            st.markdown(f"> {generated_description.strip()}") # Using markdown for a blockquote style
    else:
        st.error("Please enter some details about your product first.")

st.sidebar.info("This app is a prototype for the Google Cloud Gen AI Exchange Hackathon 2025.")