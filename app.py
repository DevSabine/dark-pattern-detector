import streamlit as st

# Define known dark patterns
dark_patterns = {
    "confirmshaming": "Guilt-tripping language",
    "sneak into basket": "Adding extra items without consent",
    "roach motel": "Easy sign-up, hard cancellation",
    "privacy zuckering": "Tricking into sharing data",
    "misdirection": "Distracting from important information",
    "trick questions": "Confusing language to mislead",
    "forced continuity": "Ongoing charges after free trial",
    "hidden costs": "Undisclosed fees at checkout",
    "disguised ads": "Ads that look like content"
}

# Streamlit App
st.set_page_config(page_title="Dark Pattern Detector", layout="centered")
st.title("🕵️‍♀️ Dark Pattern Detector")
st.write("Paste in some text from a website, email, or app and we’ll scan it for shady design tricks.")

# Input
user_input = st.text_area("Paste the text to analyze:")

if st.button("Scan for Dark Patterns"):
    st.subheader("🧠 Results:")
    found = False
    for phrase, pattern_type in dark_patterns.items():
        if phrase.lower() in user_input.lower():
            st.error(f"⚠️ Detected **{pattern_type}**: \"{phrase}\"")
            found = True
    if not found:
        st.success("✅ No known dark patterns found in your input.")
