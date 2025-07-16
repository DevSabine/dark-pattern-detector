import streamlit as st
import re
import requests
from bs4 import BeautifulSoup

# Function to extract text from a website URL
def extract_text_from_url(url):
    try:
        if not url.startswith("http"):
            url = "https://" + url
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)[:15000]
    except Exception as e:
        return f"Error fetching URL: {e}"

# Dark pattern definitions
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
        r"only\s*\d+\s*(left|remaining|available)",
        r"selling\s*out\s*(fast)?",
        r"last\s*chance",
        r"book(ed)?\s*now",
        r"limited\s*time\s*offer",
        r"low\s*stock"
    ],
    "Sneak into Basket": [
        r"pre-checked",
        r"add(ed)?\s+to\s+your\s+order\s+automatically",
        r"default\s+opt\s+in"
    ]
}

# Detection logic
def detect_dark_patterns(text):
    results = []
    for category, patterns in dark_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                results.append(f"🔍 **{category}** pattern found: `{pattern}`")
    return results

# Streamlit UI
st.set_page_config(page_title="Dark Pattern Detector", layout="centered")
st.title("🕵️‍♀️ Dark Pattern Detector")
st.markdown("""
> **Tired of websites tricking you into subscriptions, hidden fees, or shady “NO THANKS, I LOVE PAYING MORE” buttons?**  
> You’re not crazy — that stuff is real and it’s called a **dark pattern**. This app exposes it.

### 💥 How to Use It:
- 🔍 **Paste some shady text** from a site, email or app — you know, the stuff that makes you go “Wait, what did I just agree to?”
- 🌐 **Or just drop in a URL** — we’ll try to grab the visible text for you.
- 🧠 Hit **Analyze** and we’ll sniff out patterns like:
    - **“Free trial, auto-renews forever”**
    - **“Only 1 left in stock” panic bait**
    - **Hidden fees that show up last second**
    - **Those guilt-trip buttons you hate**

### ⚠️ Heads up:
It’s not magic. If a website hides the shady stuff in a popup, image or script — we might not catch it (yet). But we’re getting smarter.
""")

input_mode = st.radio("Choose input type:", ["Paste Text", "Enter URL"])
user_input = ""

# Session state for pasted text
if "text_input" not in st.session_state:
    st.session_state["text_input"] = ""

if input_mode == "Paste Text":
    col1, col2 = st.columns([4, 1])
    with col1:
        st.session_state["text_input"] = st.text_area(
            "Paste the plain text you'd like to analyze below:",
            value=st.session_state["text_input"],
            height=300
        )
    with col2:
        if st.button("🧹 Clear"):
            st.session_state["text_input"] = ""
    user_input = st.session_state["text_input"]

elif input_mode == "Enter URL":
    url = st.text_input("Enter a website URL", placeholder="https://example.com")
    if url:
        with st.spinner("Fetching and extracting text..."):
            user_input = extract_text_from_url(url)
        user_input = st.text_area("Extracted site text (editable):", user_input, height=200)

# Run detection
if st.button("🔎 Analyze"):
    if not user_input.strip():
        st.warning("Please enter text or a valid URL to analyze.")
    else:
        findings = detect_dark_patterns(user_input)
        if findings:
            st.success("✅ Potential dark patterns detected:")
            for match in findings:
                st.markdown(match)
        else:
            st.info("🚫 No obvious dark patterns detected.")


