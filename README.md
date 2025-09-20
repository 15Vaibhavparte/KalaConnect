# 🎨 KalaConnect - AI Marketing Assistant (Prototype)

> **Note:** This is a prototype submission for evaluation purposes. Not intended for production use.

## 🚀 Live Prototype Demo
**Try the prototype:** https://kalaconnect-4rjfnrzw3amnvmvwvinpxz.streamlit.app

## Project Overview

KalaConnect is an AI-powered digital marketing assistant designed to help Indian artisans create professional marketing content. Using Google Cloud's Vertex AI and Translation APIs, it generates product descriptions, social media posts, and scene-aware product images while supporting multiple Indian languages.

**Hackathon:** Google Cloud Gen AI Exchange Hackathon 2025 (Student Track)

## Prototype Functionalities

### ✅ Core Features
- **Multimodal Content Generation**: Product descriptions and social media posts from text or image input
- **AI Image Generation**: Scene-aware product photography with background removal
- **Multi-language Support**: Translation to Hindi, Bengali, Tamil, Kannada, and Urdu
- **Interactive UI**: Single-column layout with copy/download functionality
- **Per-section Regeneration**: Individual content refresh without full reload

### ⚠️ Current Limitations
- **Prototype Status**: Not production-ready, requires user review
- **Image Processing**: Basic background removal, may need manual refinement  
- **Translation Quality**: Automated translation may require human verification
- **Performance**: Processing time varies with content complexity
- **Error Handling**: Limited graceful degradation for API failures

## Quick Setup

### Prerequisites
- Python 3.11+
- Google Cloud Project with Vertex AI and Translation APIs enabled
- Service account with appropriate permissions

### Installation
```bash
# Clone repository
git clone https://github.com/15Vaibhavparte/KalaConnect.git
cd KalaConnect

# Setup environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure credentials (create service account and download JSON)
# Update .streamlit/secrets.toml with your credentials

# Run application
streamlit run app.py
```

### Usage
1. Upload product image or provide text description
2. Select language preference from sidebar
3. Choose image style (Artistic/Studio)
4. Generate content using form submission
5. Copy or download generated marketing materials

## Known Issues & Future Development

### Known Issues
- **Streamlit Version**: Compatibility issues with different Streamlit versions
- **API Quotas**: May hit rate limits during extensive testing
- **Image Upload**: Large images may cause timeout errors
- **Translation API**: Requires proper IAM role assignment

### Planned Improvements
- Enhanced error handling and user feedback
- Advanced image editing capabilities
- Batch processing for multiple products
- Performance optimization and caching
- Production-ready deployment configuration

## Technical Architecture

- **Frontend**: Streamlit web application
- **AI Models**: Vertex AI Gemini (text), Imagen (images)  
- **Translation**: Google Cloud Translate API v3
- **Image Processing**: Pillow, rembg for background removal
- **Authentication**: Service account-based Google Cloud credentials

## Acknowledgments

- **Google Cloud Platform**: Vertex AI and Translation APIs
- **Streamlit**: Web application framework  
- **Open Source Libraries**: Pillow, rembg, google-cloud-aiplatform
- **Google Cloud Gen AI Exchange Hackathon 2025** for the opportunity

---
**Disclaimer**: This prototype demonstrates AI-powered marketing content generation. All generated content should be reviewed before commercial use. 