# KalaConnect Translation Feature

## Overview

KalaConnect now supports multi-language translation for generated content using Google Cloud Translate API. This feature allows users to translate product descriptions and social media posts into multiple Indian languages.

## Supported Languages

- **English** (default)
- **Hindi** (हिन्दी)
- **Bengali** (বাংলা)
- **Tamil** (தமிழ்)
- **Kannada** (ಕನ್ನಡ)
- **Urdu** (اردو)

## How It Works

1. **Content Generation**: The app first generates content in English using Vertex AI
2. **Translation**: If a non-English language is selected, the content is automatically translated using Google Cloud Translate API
3. **Display**: The translated content is displayed in the selected language

## Features

### Language Selection
- Located in the right sidebar under "🌐 Language Settings"
- Dropdown menu with all supported languages
- Real-time indication of selected language

### Automatic Translation
- **Product Descriptions**: Automatically translated after generation
- **Social Media Posts**: All three Instagram post ideas are translated
- **Regeneration**: New content is also translated when regenerated
- **Images**: Images remain unchanged (visual content doesn't need translation)

### Translation Process
- Original content is generated in English for accuracy
- High-quality translation using Google's Neural Machine Translation
- Preserves formatting and structure of the original content
- Handles special characters and emojis appropriately

## Technical Implementation

### Backend Functions
- `initialize_translate_client()`: Sets up Google Translate client
- `translate_text(text, target_language)`: Translates individual text pieces
- `translate_content(content_dict, target_language)`: Translates entire content dictionary

### Error Handling
- Graceful fallback to original English content if translation fails
- User-friendly warning messages for translation errors
- Maintains app functionality even if Translation API is unavailable

### Performance
- Translation happens after content generation to maintain quality
- Separate spinner indicators for generation vs. translation
- Efficient API usage with proper error handling

## Setup Requirements

### Google Cloud APIs
- **Cloud Translate API** must be enabled in your Google Cloud project
- Service account needs **Cloud Translate API User** role

### Dependencies
- `google-cloud-translate==3.15.3` added to requirements.txt
- Automatic initialization using existing credentials

## Usage Tips

1. **Language Selection**: Choose your preferred language before generating content
2. **Quality**: Content is first generated in English for optimal AI quality, then translated
3. **Regeneration**: When regenerating individual components, they will be translated to the selected language
4. **Copying**: Translated content can be copied using the standard copy buttons

## Limitations

- Translation quality depends on Google Translate API
- Some context-specific terms might not translate perfectly
- Image generation prompts remain in English for better AI understanding
- Complex formatting in social media posts might be affected by translation

This feature makes KalaConnect accessible to a broader audience of Indian artisans who prefer to work in their native languages.