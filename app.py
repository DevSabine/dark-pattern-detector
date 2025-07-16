import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Dark Pattern Detector", layout="centered")
st.title("🕵️ Dark Pattern Detector (Website Edition)")

st.write("Paste a website URL below and we'll scan for UI dark patterns:")

url = st.text_input("🔗 Website URL (e.g., https://shapermint.com)", "")

def find_dark_patterns(html):
    soup = BeautifulSoup(html, "html.parser")
    patterns_found = []

    # Text-based patterns
    text = soup.get_text(separator=" ").lower()
    text_patterns = {
        "Hidden Costs": [r"free trial.*\$\d+", r"\$?\d+.*after trial", r"auto[- ]?renew"],
        "Confirmshaming": [r"no thanks.*(miss|save|lose)", r"are you sure.*(miss|skip)"],
        "Forced Continuity": [r"cancel.*anytime", r"billed.*if you don.?t cancel"],
    }

    for category, patterns in text_patterns.items():
        for pat in patterns:
            if re.search(pat, text):
                patterns_found.append(f"{category}: `{pat}` matched")

    # Hidden or pre-checked inputs
    for checkbox in soup.find_all("input", {"type": "checkbox"}):
        if checkbox.has_attr("checked"):
            patterns_found.append("⚠️ Pre-checked opt-in checkbox")

    # Button shaming
    for btn in soup.find_all("button"):
        if btn and re.search(r"no thanks.*(miss|save|deal|money)", btn.get_text().lower()):
            patterns_found.append("⚠️ Confirmshaming button text")

    # Tiny font disclaimers
    for tag in soup.find_all(style=True):
        style = tag['style'].lower()
        if "font-size" in style and ("8px" in style or "7px" in style):
            if any(x in tag.get_text().lower() for x in ["terms", "subscription", "auto-renew"]):
                patterns_found.append("⚠️ Tiny font used for disclaimers or important terms")

    return patterns_found

if st.button("Analyze") and url:
    try:
        st.info(f"Scraping {url}...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            matches = find_dark_patterns(response.text)
            if matches:
                st.subheader("⚠️ Dark Patterns Detected:")
                for m in matches:
                    st.write(f"- {m}")
            else:
                st.success("✅ No obvious dark patterns found.")
        else:
            st.error(f"Failed to fetch page: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")

