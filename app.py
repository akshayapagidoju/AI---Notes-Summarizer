
import streamlit as st
from google import genai

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="AI Notes Summarizer",
    page_icon="📚",
    layout="centered"
)

# -----------------------------
# Get Gemini API key
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Gemini API key is not configured.")
    st.info("Add GEMINI_API_KEY in Streamlit Cloud → Settings → Secrets.")
    st.stop()

# -----------------------------
# Gemini client
# -----------------------------
client = genai.Client(api_key=api_key)

# -----------------------------
# Title
# -----------------------------
st.title("📚 AI Notes Summarizer")
st.write("Upload your notes or paste text and get a clear, concise summary using AI.")

st.divider()

# -----------------------------
# Text input
# -----------------------------
notes = st.text_area(
    "📝 Paste your notes here",
    height=300,
    placeholder="Paste your class notes, study material, or any text here..."
)

# -----------------------------
# File upload
# -----------------------------
uploaded_file = st.file_uploader(
    "📄 Or upload a text file",
    type=["txt"]
)

if uploaded_file is not None:
    file_text = uploaded_file.read().decode("utf-8")
    notes = file_text
    st.success("File uploaded successfully!")

# -----------------------------
# Summary options
# -----------------------------
summary_type = st.selectbox(
    "Choose summary type",
    [
        "Short Summary",
        "Detailed Summary",
        "Exam Notes",
        "Key Points"
    ]
)

# -----------------------------
# Summarize button
# -----------------------------
if st.button("✨ Summarize Notes", use_container_width=True):

    if not notes.strip():
        st.warning("Please paste some notes or upload a text file.")
        st.stop()

    if summary_type == "Short Summary":
        instruction = """
        Summarize the notes briefly.
        Include only the most important information.
        """

    elif summary_type == "Detailed Summary":
        instruction = """
        Create a detailed but easy-to-understand summary.
        Cover all important concepts from the notes.
        """

    elif summary_type == "Exam Notes":
        instruction = """
        Convert the notes into exam preparation notes.
        Use headings, definitions, important points, and examples where useful.
        Keep the language simple and easy to remember.
        """

    else:
        instruction = """
        Extract the most important key points from the notes.
        Present them as clear bullet points.
        """

    prompt = f"""
You are an AI Notes Summarizer.

{instruction}

Rules:
- Do not change the meaning of the original notes.
- Use simple English.
- Organize the answer clearly.
- Use headings and bullet points where appropriate.

Notes:

{notes}
"""

    with st.spinner("🤖 AI is summarizing your notes..."):

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.success("Summary generated successfully!")

            st.subheader("📖 Summary")
            st.write(response.text)

        except Exception as e:
            st.error("Unable to generate the summary.")
            st.write("Please check your Gemini API key and try again.")

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("AI Notes Summarizer | Built with Streamlit and Gemini AI")


