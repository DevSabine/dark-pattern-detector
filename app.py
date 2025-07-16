import streamlit as st
import re
import requests
from bs4 import BeautifulSoup

import streamlit as st
import re

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)[:15000]  # Limit to 15,000 chars
    except Exception as e:
        return f"Error fetching URL: {e}"



st.set_page_config(page_title="Dark Pattern Detector", layout="centered")
st.title("🕵️‍♀️ Dark Pattern Detector")
st.markdown("Analyze website or email text for **dark UX patterns** like hidden opt-outs, forced subscriptions, confirmshaming, etc.")

# Input text
user_input = st.text_area("Paste the plain text you'd like to analyze below:", height=300)

# Define patterns to look for
dark_patterns = {
    "Forced Continuity": [
        r"automatically\s*renew",
        r"free\s+trial.*\$\d+.*month",
        r"\$\d+\s*/\s*month\s*after\s*trial",
        r"free\s+for\s+\d+\s+days.*\$\d+.*month",
        r"charged\s*after\s*trial",
        r"\$\d+\s*/\s*month\s*.*terms\s*apply"
    ],
    "Confirmshaming": [
        r"no,\s*i\s*don'?t\s*want\s*to\s*save\s*money",
        r"i\s*prefer\s*to\s*pay\s*full\s*price",
        r"i'?m\s*not\s*interested\s*in\s*better\s*health"
    ],
    "Hidden Costs": [
        r"service\s*fee",
        r"processing\s*fee",
        r"added\s*at\s*checkout"
    ],
    "Scarcity Pressure": [
        r"only\s+\d+\s+left",
        r"selling\s*out\s*fast",
        r"last\s*chance"
    ],
    "Sneak into Basket": [
        r"pre-checked",
        r"add(ed)?\s+to\s+your\s+order\s+automatically",
        r"default\s+opt\s+in"
    ]
}

def detect_dark_patterns(text):
    results = []
    for category, patterns in dark_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                results.append(f"🔍 **{category}** pattern found: `{pattern}`")
    return results

if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("Please paste some text to analyze.")
    else:
        findings = detect_dark_patterns(user_input)
        if findings:
            st.success("✅ Potential dark patterns detected:")
            for match in findings:
                st.markdown(match)
        else:
            st.info("🚫 No obvious dark patterns detected.")

