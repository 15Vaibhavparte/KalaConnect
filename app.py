import streamlit as st
from backend import generate_all_content # Import the new master function

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

# --- Single Input Form ---
st.header("✨ Let's Create Some Magic!")
st.info("Describe your product below. I will generate a product description, social media posts, and a unique product image for you all at once.")

with st.form("main_form"):
    product_input = st.text_area("Enter product details (e.g., 'A hand block-printed cotton saree from Bagru with floral motifs'):", height=150)
    submitted = st.form_submit_button("🚀 Generate All Content")

# --- Output Section ---
if submitted:
    if product_input:
        # A more descriptive spinner message
        with st.spinner("Generating a full marketing kit... This might take a moment."):
            # Call the single backend function
            results = generate_all_content(product_input)
            
            st.write("---")
            st.header("Your AI-Generated Marketing Kit")
            
            # Use columns for a professional layout to display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📸 AI-Generated Image")
                if results["image"]:
                    st.image(results["image"], caption="Your AI-generated product image.")
                else:
                    st.error("Sorry, the image could not be generated at this time.")

            with col2:
                st.subheader("✍️ Product Description")
                st.markdown(f"> {results['description'].strip()}")
                
                st.write("---")
                
                st.subheader("📱 Social Media Posts")
                st.markdown(results["social_posts"])
    else:
        st.error("Please enter some details about your product first.")