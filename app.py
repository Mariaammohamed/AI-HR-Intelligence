
import streamlit as st
import requests
import json


BASE_URL = "https://lucio-unincarnated-leonor.ngrok-free.dev"   

PARSE_URL = BASE_URL + "/parse"

st.set_page_config(
    page_title="AI HR Intelligence",
    layout="wide",
    page_icon="🧠"
)

st.title("🧠 AI HR Intelligence System")
st.markdown("Upload a resume and let AI analyze, structure, and rank candidates.")


uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])




if uploaded_file and st.button("🔍 Parse Resume"):
    with st.spinner("AI is extracting candidate profile..."):
        try:
            files = {
                "file": (uploaded_file.name, uploaded_file, "application/pdf")
            }
            response = requests.post(PARSE_URL, files=files, timeout=120)

            if response.status_code == 200:
                parsed = response.json()["result"]
                st.session_state["parsed_cv"] = parsed

                st.subheader("📄 Structured Candidate Profile")
                st.code(parsed, language="json")

            else:
                st.error("Error parsing resume")

        except Exception as e:
            st.error("Could not connect to AI server")
            st.write(e)


