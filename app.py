import streamlit as st
from backend import generate_all_content
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="KalaConnect AI Assistant",
    page_icon="🎨",
    layout="wide"
)

# --- Header Section ---
st.title("🎨 KalaConnect - The Artisan's Digital Storyteller")
st.image("img/artisan.png", caption="Empowering India's Artisans with the Power of AI", use_column_width=True)

# --- Sidebar Info ---
st.sidebar.info("This app is a prototype for the Google Cloud Gen AI Exchange Hackathon 2025.")

st.write("---")

# --- New Dual-Input UI ---
st.header("✨ Let's Create Some Magic!")
st.info("You can either describe your product with text OR upload an image for the AI to analyze.")

# Use columns for a clean side-by-side layout for text vs. image input
col1, col2 = st.columns(2)

with col1:
    st.subheader("Option 1: Describe with Text")
    product_input = st.text_area("Enter product details:", height=150, key="text_input")

with col2:
    st.subheader("Option 2: Upload an Image")
    uploaded_file = st.file_uploader("Choose a product image...", type=["jpg", "jpeg", "png"])

# --- Main Form and Submission Logic ---
with st.form("main_form"):
    # The button is now outside the columns
    submitted = st.form_submit_button("🚀 Generate All Content")

    if submitted:
        # Check if either text OR an image was provided
        if product_input or uploaded_file:
            image_data = None
            if uploaded_file is not None:
                # Read the image file into bytes, which the AI model needs
                image_data = uploaded_file.getvalue()

            with st.spinner("Generating a full marketing kit... This may take a moment."):
                # Pass both the text and image data to the backend
                results = generate_all_content(product_input, image_data)
                
                # --- Display Results ---
                st.write("---")
                st.header("Your AI-Generated Marketing Kit")
                
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    st.subheader("📸 AI-Generated Image")
                    if results["image"]:
                        st.image(results["image"], caption="Your AI-generated product image.")
                    else:
                        st.error("Sorry, the image could not be generated.")

                with res_col2:
                    st.subheader("✍️ Product Description")
                    st.markdown(f"> {results['description'].strip()}")
                    
                    st.write("---")
                    
                    st.subheader("📱 Social Media Posts")
                    st.markdown(results["social_posts"])
        else:
            # Error if neither input is provided
            st.error("Please describe your product OR upload an image to begin.")