import streamlit as st
from google.cloud import vision
import pandas as pd
import re
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Alcohol Label Verification",
    page_icon="🤖",
    layout="wide"
)

# --- Authentication ---
# Supports both Streamlit Community Cloud (st.secrets) and local secrets.toml
try:
    if "gcp_service_account" in st.secrets:
        credentials_info = dict(st.secrets["gcp_service_account"])
    else:
        # Fallback dictionary access
        credentials_info = dict(st.secrets.gcp_service_account)

    # Ensure literal newlines in private key
    if "private_key" in credentials_info:
        credentials_info["private_key"] = credentials_info["private_key"].replace("\\n", "\n")

    client = vision.ImageAnnotatorClient(
        credentials=vision.Credentials.from_service_account_info(credentials_info)
    )
    auth_ok = True
except Exception as e:
    st.error(
        f"🔴 **Authentication Error:** Could not connect to Google Cloud Vision API. "
        f"Please verify your `secrets.toml` or Streamlit Cloud Secrets configuration.\n\nDetails: {e}"
    )

