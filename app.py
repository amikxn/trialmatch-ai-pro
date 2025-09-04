import streamlit as st
import openai
from PyPDF2 import PdfReader

# Load API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("📄 Clinical Trial PDF Analyzer")

uploaded_file = st.file_uploader("Upload a clinical trial PDF", type="pdf")

if uploaded_file is not None:
    # Extract text from the PDF
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    st.subheader("PDF Extracted Text (first 1000 chars)")
    st.text(text[:1000])  # preview only

    # Send to OpenAI for analysis
    if st.button("Analyze PDF"):
        with st.spinner("Analyzing..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert in analyzing clinical trial studies."},
                    {"role": "user", "content": f"Summarize the following clinical trial: {text[:6000]}"}
                ]
            )
            st.success("✅ Analysis complete")
            st.write(response["choices"][0]["message"]["content"])
