import streamlit as st
from backend import generate_all_content
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="KalaConnect AI Assistant",
    page_icon="🎨",
    layout="wide"
)

# Initialize session state for storing regenerated content
if 'regenerated_image' not in st.session_state:
    st.session_state.regenerated_image = None
if 'regenerated_description' not in st.session_state:
    st.session_state.regenerated_description = None
if 'regenerated_social_posts' not in st.session_state:
    st.session_state.regenerated_social_posts = None

# --- Header Section ---
st.title("🎨 KalaConnect - The Artisan's Digital Storyteller")
st.image("img/artisan.png", caption="Empowering India's Artisans with the Power of AI", use_column_width=True)

# --- Sidebar Info ---
st.sidebar.info("This app is a prototype for the Google Cloud Gen AI Exchange Hackathon 2025.")

st.write("---")

# --- Improved Single-Column UI ---
st.header("✨ Let's Create Some Magic!")
st.info("Upload a product image or provide a text description to generate your marketing content.")

# Single column layout with clearer hierarchy
uploaded_file = st.file_uploader("📸 Upload a product image (recommended)", type=["jpg", "jpeg", "png"])
product_input = st.text_area("📝 Or, add a text description (optional)", height=100, key="text_input")

# Image style selector
st.subheader("Image Style")
image_style = st.radio(
    "Choose your preferred image style:",
    options=["Artistic Lifestyle", "Clean Studio Background"],
    horizontal=True
)

# --- Main Form and Submission Logic ---
with st.form("main_form"):
    # What You'll Get Preview
    st.info("### What you'll receive: \n"
            "✍️ 1 Product Description • 📱 3 Social Media Posts • 📸 1 AI-Generated Image")
    
    # Generate button
    submitted = st.form_submit_button("🚀 Generate All Content")

# Process form submission (outside the form)
if submitted:
    # Check if either text OR an image was provided
    if product_input or uploaded_file:
        image_data = None
        if uploaded_file is not None:
            # Read the image file into bytes, which the AI model needs
            image_data = uploaded_file.getvalue()

        with st.spinner("Generating a full marketing kit... This may take a moment."):
            # Pass both the text and image data to the backend, along with the selected image style
            results = generate_all_content(product_input, image_data, image_style=image_style)
                
            # --- Display Results ---
            st.write("---")
            st.header("Your AI-Generated Marketing Kit")
    else:
        # Error if neither input is provided
        st.error("Please describe your product OR upload an image to begin.")
            
# Results section (outside the form)
if 'results' in locals():
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.subheader("📸 AI-Generated Image")
        if results["image"]:
            st.image(results["image"], caption="Your AI-generated product image.")
            # Download image button - now outside the form
            image_bytes = results["image"]
            st.download_button(
                label="⬇️ Download Image",
                data=image_bytes,
                file_name="kalaconnect_product_image.png",
                mime="image/png",
            )
            
            # Create a button for regenerating the image
            if st.button("🎲 Regenerate Image", key="regen_img"):
                with st.spinner("Regenerating image..."):
                    # Pass only the necessary parameters for image generation
                    new_results = generate_all_content(product_input, image_data, image_style=image_style, regenerate_image_only=True)
                    if new_results["image"]:
                        # Store the regenerated image in the session state
                        st.session_state.regenerated_image = new_results["image"]
                        st.success("Image regenerated successfully! Refreshing page...")
                        st.rerun()  # Refresh the page with new content
                    else:
                        st.error("Sorry, the image could not be regenerated.")
        else:
            st.error("Sorry, the image could not be generated.")

    with res_col2:
        st.subheader("✍️ Product Description")
        if results["description"] != "Not regenerated":
            st.markdown(f"> {results['description'].strip()}")
            
            # Create a container for the description buttons
            desc_buttons = st.container()
            
            # Copy button for description with a better approach
            desc_text = results['description'].strip()
            if desc_buttons.button("📋 Copy Description", key="copy_desc"):
                # Create a text area with the content that can be easily copied
                st.code(desc_text, language=None)
                st.toast("✅ Click in the box above, press Ctrl+A to select all, then Ctrl+C to copy")
                
            # Button for regenerating description
            if desc_buttons.button("🎲 Regenerate Description", key="regen_desc"):
                with st.spinner("Regenerating description..."):
                    new_results = generate_all_content(product_input, image_data, image_style=image_style, regenerate_desc_only=True)
                    if "description" in new_results and new_results["description"] != "Not regenerated":
                        # Store the regenerated description in the session state
                        st.session_state.regenerated_description = new_results["description"]
                        st.success("Description regenerated successfully! Refreshing page...")
                        st.rerun()
                    else:
                        st.error("Sorry, the description could not be regenerated.")
        else:
            st.error("Description was not generated during this operation.")
        
        st.write("---")
        
        st.subheader("📱 Social Media Posts")
        if results["social_posts"] != "Not regenerated":
            st.markdown(results["social_posts"])
            
            # Create a container for the social media buttons
            social_buttons = st.container()
            
            # Copy button for social media posts with a better approach
            social_text = results["social_posts"]
            if social_buttons.button("📋 Copy Social Posts", key="copy_posts"):
                # Create a text area with the content that can be easily copied
                st.code(social_text, language=None)
                st.toast("✅ Click in the box above, press Ctrl+A to select all, then Ctrl+C to copy")
                
            # Button for regenerating social media posts
            if social_buttons.button("🎲 Regenerate Social Posts", key="regen_posts"):
                with st.spinner("Regenerating social media posts..."):
                    new_results = generate_all_content(product_input, image_data, image_style=image_style, regenerate_posts_only=True)
                    if "social_posts" in new_results and new_results["social_posts"] != "Not regenerated":
                        # Store the regenerated social posts in the session state
                        st.session_state.regenerated_social_posts = new_results["social_posts"]
                        st.success("Social posts regenerated successfully! Refreshing page...")
                        st.rerun()
                    else:
                        st.error("Sorry, the social posts could not be regenerated.")
        else:
            st.error("Social media posts were not generated during this operation.")