
import streamlit as st
import ollama

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Notes Summarizer",
    page_icon="📝",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("📝 AI Notes Summarizer")
st.write(
    "Paste your notes below and let AI create a clear, "
    "simple and exam-friendly summary."
)

# -----------------------------
# Notes Input
# -----------------------------
notes = st.text_area(
    "📚 Paste Your Notes",
    height=350,
    placeholder="Paste your lecture notes here..."
)

# -----------------------------
# Summary Length
# -----------------------------
summary_length = st.selectbox(
    "📌 Choose Summary Length",
    ["Short", "Medium", "Detailed"]
)

# -----------------------------
# Summarize Button
# -----------------------------
if st.button("✨ Summarize Notes", use_container_width=True):

    if not notes.strip():
        st.warning("⚠️ Please paste some notes first.")

    else:

        # Different instructions for different summary lengths
        if summary_length == "Short":
            instruction = """
Create a short summary.
Include only the most important points.
Use simple bullet points.
"""

        elif summary_length == "Medium":
            instruction = """
Create a medium-length summary.
Include important concepts, definitions and key points.
Use headings and bullet points.
"""

        else:
            instruction = """
Create a detailed summary.
Include important concepts, definitions, explanations,
examples and key points.
Organize the answer using clear headings and bullet points.
"""

        # -----------------------------
        # Prompt
        # -----------------------------
        prompt = f"""
You are an AI Notes Summarizer designed for college students.

Your job is to summarize the notes given below.

{instruction}

Important rules:
- Do not change the meaning of the notes.
- Do not add unrelated information.
- Use simple English.
- Make the summary easy to study.
- Highlight important terms.
- Make it useful for exam preparation.

Here are the notes:

{notes}
"""

        try:
            # -----------------------------
            # Send request to Ollama
            # -----------------------------
            with st.spinner("🤖 AI is summarizing your notes..."):

                response = ollama.chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

            # -----------------------------
            # Display Summary
            # -----------------------------
            summary = response["message"]["content"]

            st.success("✅ Summary generated successfully!")

            st.subheader("📌 AI Summary")

            st.markdown(summary)

            # -----------------------------
            # Download Summary
            # -----------------------------
            st.download_button(
                label="📥 Download Summary",
                data=summary,
                file_name="AI_Notes_Summary.txt",
                mime="text/plain"
            )

        except Exception as e:

            st.error(
                "❌ Could not connect to Ollama."
            )

            st.info(
                "Make sure Ollama is installed and running, "
                "and that the llama3.2 model is available."
            )

            st.code(str(e))

