# import streamlit as st
# import os
# import re
# import requests
# import tempfile
# from dotenv import load_dotenv
# from openai import OpenAI
# import gdown
#
# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# if not api_key:
#     raise ValueError("OPENAI_API_KEY missing")
#
# client = OpenAI(api_key=api_key)
#
# # === CONFIG: Your shared public Google Drive folder link ===
# GOOGLE_DRIVE_FOLDER_URL = "https://drive.google.com/drive/folders/10DoI0RRxjWpqFEFZwjE249Njt6QoJN5S?usp=sharing"
#
# # === Helper Functions ===
#
# def clean_html_preserve_paragraphs(raw_html):
#     raw_html = re.sub(r'<br\s*/?>', '\n', raw_html)
#     cleanr = re.compile('<.*?>')
#     clean_text = re.sub(cleanr, '', raw_html)
#     clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)
#     return clean_text.strip()
#
# def fetch_experience_details(experience_id):
#     url = f"https://api.xperio.travel/app/experience/public/{experience_id}"
#     res = requests.get(url)
#     if res.status_code != 200:
#         raise Exception(f"Failed to fetch experience details: {res.status_code}")
#     return res.json()
#
# def extract_text_content_from_details(details_data):
#     title = details_data.get("title") or "No Title"
#     fields = ["briefOverview", "keyAttraction", "whatToExpect"]
#     combined_text = ""
#     for field in fields:
#         val = details_data.get(field)
#         if val:
#             if isinstance(val, str):
#                 combined_text += val + "\n\n"
#             elif isinstance(val, dict):
#                 combined_text += " ".join(str(v) for v in val.values()) + "\n\n"
#     return title, combined_text.strip()
#
# def summarize_text(title, text):
#     prompt = f"""
# You are a travel content writer creating key highlights for a 30-second promotional video about the following travel experience.
#
# Title: {title}
#
# Description:
# {text}
#
# Please provide key highlights formatted with time stamps for a 30-second video, like this:
#
# Key Highlights for 30-Second Video Clip with Timings
# 0:00 - 0:10
# Highlight 1 description.
#
# 0:10 - 0:20
# Highlight 2 description.
#
# 0:20 - 0:30
# Highlight 3 description.
# """
#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.7,
#         max_tokens=250
#     )
#     return response.choices[0].message.content.strip()
#
# def get_music_theme(title, description):
#     prompt = f"""
# You are selecting background music for a travel promo video.
#
# Title: {title}
# Description: {description}
#
# Suggest a music theme (e.g., relaxing, energetic, romantic, adventurous, suspenseful) that best suits this content.
# Only return the theme.
# """
#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.5,
#         max_tokens=10
#     )
#     return response.choices[0].message.content.strip().lower()
#
# def download_music_file(theme):
#     """
#     Try to download a file from the shared folder based on theme name match (e.g., relaxing.mp3)
#     """
#     st.info("Looking for a matching music file...")
#
#     # Get folder ID from URL
#     match = re.search(r'/folders/([a-zA-Z0-9_-]+)', GOOGLE_DRIVE_FOLDER_URL)
#     if not match:
#         st.error("Invalid Google Drive folder URL.")
#         return None
#
#     folder_id = match.group(1)
#     folder_list_url = f"https://drive.google.com/drive/folders/{folder_id}"
#
#     # Scrape file links using gdown (this works only if public and indexed)
#     try:
#         files = gdown.download_folder(id=folder_id, quiet=True, use_cookies=False)
#         if not files:
#             st.error("No files found in the shared folder.")
#             return None
#         # Match by theme in filename
#         for file in files:
#             if theme in file.lower():
#                 return file
#     except Exception as e:
#         st.error(f"Failed to fetch or match music files: {e}")
#         return None
#
#     return None
#
#
# def main():
#     st.title(" Travel Promo Script + Auto-Music Selector")
#     experience_id = st.text_input("Enter Experience ID")
#
#     if st.button("Generate Video Script & Music"):
#         if not experience_id.strip():
#             st.error("Please enter a valid Experience ID.")
#             return
#
#         try:
#             with st.spinner("Fetching experience details..."):
#                 details_data = fetch_experience_details(experience_id)
#                 title, combined_text = extract_text_content_from_details(details_data)
#
#             if not combined_text:
#                 st.warning(f"Title: {title}")
#                 st.info("No descriptive content available to summarize.")
#                 return
#
#             with st.spinner("Generating key highlights..."):
#                 highlights = summarize_text(title, combined_text)
#
#             with st.spinner("Choosing matching music..."):
#                 theme = get_music_theme(title, combined_text)
#                 music_file = download_music_file(theme)
#
#             st.subheader(f" Title: {title}")
#             st.markdown(f"###  Key Highlights:\n{highlights}")
#
#             if music_file:
#                 st.audio(music_file)
#                 st.success(f" Matched theme: **{theme}**")
#             else:
#                 st.warning(f"No matching file found for theme: {theme}")
#
#         except Exception as e:
#             st.error(f"Error: {e}")
#
# if __name__ == "__main__":
#     main()
#
#





import urllib.request
import streamlit as st
import os
import re
import requests
import random
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY missing")

client = OpenAI(api_key=api_key)

THEME_TO_URL = {
    "adventure": [
        "https://drive.google.com/uc?export=download&id=12pi77nxObzXn8pMhcaKz2som_-kHw_ws",
        "https://drive.google.com/uc?export=download&id=1pRLxw6x7ySmiV2AG_amOVRp3ouwGQZgy",
        "https://drive.google.com/uc?export=download&id=1zAe4QwoUORWj3b8wnzz6PeOFbJmN6_MK",
        "https://drive.google.com/uc?export=download&id=1soKHjY5u4MYFlXoMSeI7XPMZDGL94OfX",
        "https://drive.google.com/uc?export=download&id=1_8kZPZ42fLgIVOOx5MzFks98lRMhDimH",
    ],
    "spiritual": [
        "https://drive.google.com/uc?export=download&id=1GaLZ1_0DSZRjmm2ca2xiF2PsJ8lU0HbW",
        "https://drive.google.com/uc?export=download&id=19-nAJ4eiiucUERdphwBc3cwFGNjs0DDq",
        "https://drive.google.com/uc?export=download&id=1A2UCQpqiDyvsvhFS0_hsuPdJ6R1FCb_r",
        "https://drive.google.com/uc?export=download&id=1n353SamQfXFYW96YRi8nYLhXFxcA4OhG",
        "https://drive.google.com/uc?export=download&id=1hf2IZ936mJ7qvDXfl8ILO7beuRk9Sson",
    ],
    "eco tourism": [
        "https://drive.google.com/uc?export=download&id=1xEE_ldSEd7m7HOiGR994WtyayX4Fswhf",
        "https://drive.google.com/uc?export=download&id=1dKvNxFPpik40_mr6hmY7G_BpcjfwPdS2",
        "https://drive.google.com/uc?export=download&id=1fm4JMqxKrXGuaIwXSUrSQliLdJVAaVh4",
        "https://drive.google.com/uc?export=download&id=1vjTUVUvxNNwRFLdnwKIH-ZwkL2_RnCaK",
        "https://drive.google.com/uc?export=download&id=16K0Yo5vMizpypwzkg8gtstFivZ1mGVpV",
    ],
    "culinary": [
        "https://drive.google.com/uc?export=download&id=1bFIDxpbteMjwzMDD6erQ_wlR5Ghs6aEe",
        "https://drive.google.com/uc?export=download&id=1VxDljyIzKP3kqes9VNfXArO2p-vh9E1s",
        "https://drive.google.com/uc?export=download&id=1o2fOH7A16x_VRUTSlC6xZrA80oLGpa1_",
        "https://drive.google.com/uc?export=download&id=1x4uhOD5bLlknj8_ndEgZ77W75uAWNS_j",
        "https://drive.google.com/uc?export=download&id=12myZ4Qptpkz2VXXVUBYUCEbUNUgFbxJA",
    ],
    "agro tourism": [
        "https://drive.google.com/uc?export=download&id=12pi77nxObzXn8pMhcaKz2som_-kHw_ws",
        "https://drive.google.com/uc?export=download&id=12XwhGDa_LUkMPkYWDBYyHpptJxpLLuQ5",
        "https://drive.google.com/uc?export=download&id=1b2QaBFohxGRfgvXQoZBcjf1PW6FUyw7Z",
        "https://drive.google.com/uc?export=download&id=16KT32-90x3b4FPqGJDIUkyAJLt05SlNX",
        "https://drive.google.com/uc?export=download&id=1-w-rdsSLHromw0TKXbSekZyK--UhqTEL",
    ],
    "relaxing nature": [
        "https://drive.google.com/uc?export=download&id=1Njp5EiafOi9E5S1Jy9AYrbRdmm7sOnE2",
        "https://drive.google.com/uc?export=download&id=1OaVBybGoQdBuu_TeaKrGB9oeXKLqFwfb",
        "https://drive.google.com/uc?export=download&id=16vxsar28NhTi3nw_HSx5NwgpDnM3DKDt",
        "https://drive.google.com/uc?export=download&id=1HnjNmU_rXEbF9cbltQYNvnQhnv8i-Xwm",
        "https://drive.google.com/uc?export=download&id=YhfiiujKd2iRipYlQTjl-ZR9nTqW1h8X",
    ],
    "wellness": [
        "https://drive.google.com/uc?export=download&id=1vLTTWGutPdiVi-4juvYIrnXnhAPxo-Zz",
        "https://drive.google.com/uc?export=download&id=1WibjIQns9l5Q_blqmTKEVNzQ8mD9a6ie",
        "https://drive.google.com/uc?export=download&id=1nnga2oCoikKfRBXngP5Q_hKO494lD6w9",
        "https://drive.google.com/uc?export=download&id=13HvaBc-aWnfQnt1mniyeZ4bR6ofm82oq",
        "https://drive.google.com/uc?export=download&id=1fLFnlD6iN6jMDejpdmoDLyymiravOCE_",
    ],
    "culture": [
        "https://drive.google.com/uc?export=download&id=1oeJCYUI2pl_qphSPAIYMJTJTC-9phQqm",
        "https://drive.google.com/uc?export=download&id=1989KPg9DQsgTvPQKoWt-n6rdCjUFm9F3",
        "https://drive.google.com/uc?export=download&id=1lkP2PVlgHZOZcMsaR2DCfrc8wqE6Jzh3",
        "https://drive.google.com/uc?export=download&id=14Qh-camXcqFNpqupa4ic18hsMwO4kO5p",
        "https://drive.google.com/uc?export=download&id=1tsxsjWsTdxoCNbfV8FSpVPCrG1jUrG5L",
    ],
}


def generate_editing_tips(theme):
    prompt = f"""
You are a smart video editing assistant helping beginners create video, engaging social media videos it should be very beginner friendly so that every will be able to understand 
even if the user is not a  video editor.

The theme is: "{theme}"

Give 5 concise, beginner-friendly, data-driven tips to improve video quality, boost social media reach, and increase viewer engagement.

Focus on:
- Pacing
- Visuals
- Sound
- Format
- Calls-to-action

Keep it very practical and specific to {theme} content. Each tip should be one line.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()


def fetch_experience_details(experience_id):
    url = f"https://api.xperio.travel/app/experience/public/{experience_id}"
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception(f"Failed to fetch experience details: {res.status_code}")
    return res.json()


def extract_text_content_from_details(details_data):
    title = details_data.get("title") or "No Title"
    categories_raw = details_data.get("category") or details_data.get("categories") or ""
    categories = categories_raw if isinstance(categories_raw, str) else ""
    fields = ["briefOverview", "keyAttraction", "whatToExpect"]
    combined_text = ""
    for field in fields:
        val = details_data.get(field) or ""
        if val:
            combined_text += val + "\n"
    return title, categories, combined_text.strip()


def generate_highlights_and_music(experience_id, theme):
    # Fetch experience data
    details_data = fetch_experience_details(experience_id)
    title, categories, combined_text = extract_text_content_from_details(details_data)

    # Generate highlights text
    prompt = f"""
You are a video script generator for travel promos. 
Create engaging highlights for the experience titled: "{title}" with categories: {categories}.
Use the following details to inspire your highlights:

{combined_text}

Write 3-5 short, punchy bullet points (each 10-20 words) to use as video captions for Instagram reels or TikTok.
Make it very appealing and fun.
"""
    response_highlights = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=150,
    )
    highlights = response_highlights.choices[0].message.content.strip()

    # Generate music recommendations based on theme
    theme_lower = theme.lower()
    music_urls = THEME_TO_URL.get(theme_lower, [])
    music_url = random.choice(music_urls) if music_urls else "No music available for this theme."

    # Generate editing tips
    editing_tips = generate_editing_tips(theme)

    return highlights, music_url, editing_tips, combined_text


# Streamlit UI starts here

st.set_page_config(
    page_title="Travel Promo Video Script Builder",
    page_icon="✈️",
    layout="wide",
)

st.markdown(
    """
<style>
    .main {
        background-color: #f9f9f9;
        color: #333333;
    }
    h1 {
        color: #2c3e50;
        font-weight: 700;
        font-size: 2.5rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: 600;
        padding: 0.6em 1.2em;
        border-radius: 6px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>input {
        padding: 0.6em;
        font-size: 1.1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🧳 Travel Promo Video Script Builder")
st.write(
    "Welcome! Enter an Experience ID and select a theme to generate engaging travel video highlights, music, and editing tips."
)

col1, col2 = st.columns([3, 1])

with col1:
    experience_id = st.text_input("Enter Experience ID (e.g., EXP1234):")
    theme = st.selectbox(
        "Select a Theme:",
        options=[
            "Adventure",
            "Spiritual",
            "Eco Tourism",
            "Culinary",
            "Agro Tourism",
            "Relaxing Nature",
            "Wellness",
            "Culture",
        ],
    )
    generate_button = st.button("🎬 Generate Promo Script")

with col2:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/3064/3064197.png",
        width=100,
        caption="Travel Video",
    )

if generate_button:
    if not experience_id.strip():
        st.error("Please enter a valid Experience ID.")
    else:
        try:
            with st.spinner("Generating..."):
                highlights, music_url, editing_tips, combined_text = generate_highlights_and_music(
                    experience_id.strip(), theme
                )

            st.markdown("### 🎯 Highlights")
            st.write(highlights)

            st.markdown("### 🎵 Background Music (Sample Clip)")
            if music_url.startswith("http"):
                st.audio(music_url)
            else:
                st.write(music_url)

            st.markdown("### 🎬 Editing Tips")
            st.write(editing_tips)

            with st.expander("🔍 Experience Details Text"):
                st.text_area("Details used for generation:", combined_text, height=200)

        except Exception as e:
            st.error(f"Error: {e}")

