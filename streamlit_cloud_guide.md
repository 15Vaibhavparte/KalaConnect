# KalaConnect Streamlit Cloud Deployment Guide

This guide walks you through deploying your KalaConnect app to Streamlit Cloud, including setting up authentication for Google Cloud services.

## Quick Reference

| Step | Local Development | Streamlit Cloud |
|------|------------------|-----------------|
| Auth Method | `.env` file with path to JSON | Secrets manager with JSON content |
| File Needed | Service account JSON file | None (content in secrets) |
| Configuration | Environment variables | Streamlit secrets |

## Step-by-Step Deployment Guide

### 1️⃣ Create a Service Account in Google Cloud

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to your project: `kalaconnect-hackathon`
3. **Enable Required APIs:**
   - Go to **APIs & Services** > **Library**
   - Search for and enable:
     - Vertex AI API
     - Cloud Translate API
     - Cloud Storage API (if not already enabled)
4. Go to **IAM & Admin** > **Service Accounts**
5. Click **Create Service Account**
6. Name it `streamlit-deploy` (or any name you prefer)
7. Grant necessary roles:
   - **Vertex AI User** (for AI content generation)
   - **Cloud Translate API User** (for translation features)
   - **Storage Object Viewer** (if using cloud storage)
8. Click **Create and Continue**
9. Click **Done**

### 2️⃣ Generate a Key for Your Service Account

1. Find your service account in the list
2. Click the three dots menu (⋮) > **Manage keys**
3. Click **Add Key** > **Create new key**
4. Select **JSON** format
5. Click **Create** (this downloads the key file)
6. Keep this file secure and don't share it

### 3️⃣ Prepare Your App for Deployment

1. Ensure your code uses the updated `backend.py` with Streamlit secrets support
2. Create a `.streamlit` folder in your project (if not already there)
3. Create a placeholder `secrets.toml` file with this structure:

```toml
# API Key - REPLACE WITH REAL KEY IN STREAMLIT CLOUD ONLY
GOOGLE_API_KEY = "placeholder_value"

# Service Account - REPLACE WITH REAL VALUES IN STREAMLIT CLOUD ONLY
[gcp_service_account]
type = "service_account"
project_id = "placeholder"
private_key_id = "placeholder"
private_key = "placeholder"
client_email = "placeholder"
client_id = "placeholder"
auth_uri = "placeholder"
token_uri = "placeholder"
auth_provider_x509_cert_url = "placeholder"
client_x509_cert_url = "placeholder"
```

### 4️⃣ Deploy to Streamlit Cloud

1. Push your code to GitHub (with placeholder secrets only)
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click **New app**
4. Connect to your GitHub repository
5. Select the repository and main branch
6. Set the main file path to `app.py`
7. Click **Deploy**

### 5️⃣ Configure Secrets in Streamlit Cloud

1. Once deployed, go to your app settings
2. Click on **Secrets** in the sidebar
3. Click **Edit Secrets**
4. Add your secrets in TOML format:

```toml
# Add your real API key
GOOGLE_API_KEY = "Paste your API key here"

# Copy and paste the ENTIRE contents of your service account JSON file
[gcp_service_account]
type = "service_account"
project_id = "kalaconnect-hackathon"
private_key_id = "abc123def456"
private_key = """-----BEGIN PRIVATE KEY-----
COPY YOUR ENTIRE MULTI-LINE PRIVATE KEY HERE
INCLUDING ALL LINE BREAKS AND WHITESPACE
-----END PRIVATE KEY-----"""
client_email = "service-account-name@kalaconnect-hackathon.iam.gserviceaccount.com"
client_id = "123456789012345678901"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/service-account-name%40kalaconnect-hackathon.iam.gserviceaccount.com"
```

5. Click **Save**
6. Reboot your app by clicking the three dots menu (⋮) > **Reboot app**

## Security Best Practices

- ✅ Never commit real credentials to GitHub
- ✅ Use placeholder values in your `.streamlit/secrets.toml` file
- ✅ Only add real credentials in the Streamlit Cloud Secrets manager
- ✅ Restrict service account permissions to only what's needed
- ✅ Regenerate keys periodically for better security

## Troubleshooting

If your app fails to authenticate:

1. Check if your secrets are properly formatted in TOML
2. Ensure the private key includes all line breaks and is wrapped in triple quotes `"""`
3. Verify your service account has the necessary permissions
4. Check the app logs in Streamlit Cloud for specific error messages
5. Try rebooting the app after updating secrets

By following this guide, your KalaConnect app will authenticate properly with Google Cloud services when deployed to Streamlit Cloud.
