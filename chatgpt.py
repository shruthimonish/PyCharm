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
        val = details_data.get(field)
        if val:
            if isinstance(val, str):
                combined_text += val + "\n\n"
            elif isinstance(val, dict):
                combined_text += " ".join(str(v) for v in val.values()) + "\n\n"
    return title, combined_text.strip(), categories


def summarize_text(title, text):
    prompt = f"""
You are a travel content writer creating key highlights for a 30-second promotional video about the following travel experience.

Title: {title}

Description:
{text}

Please provide key highlights formatted with time stamps for a 30-second video, like this:

Key Highlights for 30-Second Video Clip with Timings
0:00 - 0:10:
  Highlight 1 description.

0:10 - 0:20:
  Highlight 2 description.

0:20 - 0:30:
  Highlight 3 description.

Also, please suggest a single-word theme (e.g., nature, wellness, adventure) based on the above description.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=250
    )
    return response.choices[0].message.content.strip()


def extract_theme_from_summary(summary_text):
    lines = summary_text.lower().split("\n")
    for line in reversed(lines):
        for theme in THEME_TO_URL:
            if theme in line:
                return theme
    return None


def extract_direct_download_url(drive_url):
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", drive_url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return drive_url


def download_music_file(theme, category):
    categories = [c.strip().lower() for c in category.split(",") if c.strip()]
    for cat in categories:
        if cat in THEME_TO_URL:
            return cat, extract_direct_download_url(random.choice(THEME_TO_URL[cat]))
    if theme in THEME_TO_URL:
        return theme, extract_direct_download_url(random.choice(THEME_TO_URL[theme]))
    random_theme = random.choice(list(THEME_TO_URL.keys()))
    return random_theme, extract_direct_download_url(random.choice(THEME_TO_URL[random_theme]))


def main():
    st.title("Explore Edge SmartCut: AI Editing Assistant for Video Optimization")
    experience_id = st.text_input("Enter Experience ID")

    if st.button("Generate Highlights and Music"):
        if not experience_id.strip():
            st.error("Please enter a valid Experience ID.")
            return

        with st.spinner("Fetching experience details..."):
            try:
                details_data = fetch_experience_details(experience_id)
                title, combined_text, categories = extract_text_content_from_details(details_data)

                if not combined_text:
                    st.warning(f"Title: {title}")
                    st.info("No descriptive content available to summarize.")
                    return

                with st.spinner("Generating key highlights..."):
                    highlights = summarize_text(title, combined_text)

                ai_theme_raw = extract_theme_from_summary(highlights)
                music_theme, music_url = download_music_file(ai_theme_raw, categories)

                editing_tips = "No editing tips available."
                if music_theme:
                    with st.spinner("Generating smart editing tips..."):
                        try:
                            editing_tips = generate_editing_tips(music_theme)
                        except Exception as e:
                            editing_tips = f"Error generating tips: {e}"

                st.subheader(f"Title: {title}")
                st.markdown(f"### AI Suggested Theme: {music_theme}")
                st.markdown(f"### Key Highlights:\n{highlights}")
                st.markdown("###  Smart Editing Tips")
                st.markdown(editing_tips)

                st.title("Canva website")
                st.write("Click the link below to open the Canva for editing purpose:")
                st.markdown("[Open canva](https://www.canva.com/templates/?query=video-templates)", unsafe_allow_html=True)

                st.title("Video and Photo Selector")
                st.write("Click the link below to open the Google Drive folder and choose your videos/photos:")
                st.markdown("[Open Google Drive Folder](https://drive.google.com/drive/folders/1vloZ9mw9oynqHRkVq_DQFO6pHj_fl2gD?usp=sharing)", unsafe_allow_html=True)

                st.text(f"\U0001F3A7 Playing music from: {music_url}")
                with urllib.request.urlopen(music_url) as response:
                    audio_data = response.read()
                    st.audio(data=audio_data, format="audio/mp3")

            except Exception as e:
                st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
