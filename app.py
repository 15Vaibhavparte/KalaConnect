import streamlit as st
from backend import generate_product_description, generate_social_media_post

# --- Page Configuration ---
st.set_page_config(
    page_title="KalaConnect AI Assistant",
    page_icon="🎨",
    layout="wide"
)

# --- Application UI ---
st.title("🎨 KalaConnect - The Artisan's Digital Storyteller")

# Banner image below the title
st.image(
    "img/artisan.png",
    caption="Empowering India's Artisans with the Power of AI",
    use_column_width=True
)

# --- New Language Selector ---
# A dictionary of supported languages and their ISO 639-1 codes
LANGUAGES = {
    "English": "en",
    "हिन्दी (Hindi)": "hi",
    "বাংলা (Bengali)": "bn",
    "தமிழ் (Tamil)": "ta",
    "తెలుగు (Telugu)": "te",
    "मराठी (Marathi)": "mr"
}

# Add a selectbox to the sidebar for language selection
selected_language_name = st.sidebar.selectbox("Choose your language:", list(LANGUAGES.keys()))
selected_language_code = LANGUAGES[selected_language_name]

# Welcome text below the banner image
st.write("Welcome, creative soul! Describe your craft, and I'll help you write a beautiful story for it.")
st.write("Your creative partner for marketing your beautiful crafts.")
st.write("---")

# --- Create Tabs for Different Features ---
tab1, tab2 = st.tabs(["**✍️ Product Description Generator**", "**📱 Social Media Post Generator**"])

# --- Content for the First Tab (Product Description) ---
with tab1:
    st.header("Craft a Compelling Product Description")
    st.info("💡 **Pro-Tip:** For the best results, describe the material, the craft's name (e.g., 'blue pottery'), and any unique colors or patterns.")
    st.write("This tool will help you write a warm and evocative description for your product page or marketplace listing.")
    
    with st.form("product_form"):
        product_input_desc = st.text_area("Enter product details:", height=150, key="desc")
        submitted_desc = st.form_submit_button("✨ Generate Description")

    if submitted_desc:
        if product_input_desc:
            with st.spinner(f"Crafting the perfect description in {selected_language_name}..."):
                # Pass the selected language code to the backend function
                generated_description = generate_product_description(product_input_desc, selected_language_code)
                st.subheader("Your AI-Generated Product Description:")
                st.markdown(f"> {generated_description.strip()}")
        else:
            st.error("Please enter some details about your product first.")

# --- Content for the Second Tab (Social Media) ---
with tab2:
    st.header("Create Engaging Social Media Posts")
    st.info("💡 **Pro-Tip:** Mention what makes your product special. The AI will generate captions and hashtags to match your tone.")
    st.write("This tool will generate 3 different Instagram post ideas for your product, complete with captions and hashtags.")

    with st.form("social_form"):
        product_input_social = st.text_area("Enter product details:", height=150, key="social")
        submitted_social = st.form_submit_button("🚀 Generate Posts")

    if submitted_social:
        if product_input_social:
            with st.spinner(f"Brainstorming creative posts in {selected_language_name}..."):
                # Pass the selected language code to the backend function
                generated_posts = generate_social_media_post(product_input_social, selected_language_code)
                st.subheader("Your AI-Generated Social Media Ideas:")
                st.markdown(generated_posts) 
        else:
            st.error("Please enter some details about your product first.")

st.sidebar.info("This app is a prototype for the Google Cloud Gen AI Exchange Hackathon 2025.")