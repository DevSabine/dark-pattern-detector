import streamlit as st
import re

st.title("Dark Pattern Detector")
st.write("Paste website text below to check for dark patterns:")

user_input = st.text_area("Website text to analyze", height=300)

dark_patterns = {
    "Confirmshaming": r"(don’t|do not) (miss|leave|skip|go) (out|away).*", 
    "Hidden Subscription": r"(free trial).*(credit card|auto-renew|charge)",
    "Trick Questions": r"(double negatives|confusing choices)",
    "Obstruction": r"(make it hard|difficult to cancel|can’t find cancel)",
    "Forced Continuity": r"(auto-renew|keep charging|subscription continues)",
    "Nagging": r"(remind|are you sure|don’t leave yet)",
    "Bait and Switch": r"(click here).*(different result|not what expected)"
}

found_patterns = []

if st.button("Analyze Text"):
    for label, pattern in dark_patterns.items():
        if re.search(pattern, user_input, re.IGNORECASE):
            found_patterns.append(label)

    if found_patterns:
        st.error(f"⚠️ Detected potential dark patterns: {', '.join(found_patterns)}")
    else:
        st.success("✅ No obvious dark patterns detected.")
