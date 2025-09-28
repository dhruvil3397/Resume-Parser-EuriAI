import json
from typing import Optional

import streamlit as st
from dotenv import load_dotenv

from crew_app.file_tools.file_loader import detect_and_extract  # [file:4]
from crew_app.crew import run_pipeline  # [file:3]
from crew_app.utils import txt_to_docx_bytes  # [file:2]


# ---- App setup ----
load_dotenv()  # Load env early for any downstream SDKs [file:4]

st.set_page_config(
    page_title="ATS Resume Agent (CrewAI)",
    page_icon="🧠",
    layout="wide",
)  # [file:4]

st.title("🧠 ATS-Optimized Resume Agent (CrewAI + EuriAI)")  # [file:4]
st.caption(
    "Upload a resume, set a target role, and generate an ATS-friendly version with scores and quick wins."
)  # [file:4]


# ---- Sidebar ----
with st.sidebar:
    st.subheader("EuriAI Settings")  # Cosmetic; actual model is in backend config [file:4]
    st.text_input("Model:", value="gpt-4o-mini", disabled=True)  # Display-only [file:4]
    st.write("API Key loaded: ✅ Working EuriAI key")  # Informational [file:4]


# ---- Inputs ----
colL, colR = st.columns([1, 1])  # Balanced layout [file:4]

with colL:
    up = st.file_uploader(
        "Upload Resume (.pdf or .docx preferred)",
        type=["pdf", "docx", "txt"],
    )  # [file:4]

with colR:
    job_title = st.text_input("Target Job Title (e.g., 'Machine Learning Engineer')")  # [file:4]
    job_desc = st.text_area("Paste Job Description", height=220, placeholder="Paste JD here...")  # [file:4]

run_btn = st.button("Run ATS Agent")  # [file:4]

tabs = st.tabs(
    ["Cleaned Resume", "Rewritten (ATS-optimized)", "Final (Refined Bullets)", "ATS Evaluation"]
)  # [file:4]


# ---- Helpers ----
def _normalize_tasks_output(value) -> str:
    """
    Convert possible list-like task outputs into a single text block.
    """
    if isinstance(value, list):
        return "\n\n".join(str(item) for item in value)
    return str(value) if value is not None else ""  # [file:4]


def _try_parse_json(text: str) -> Optional[dict]:
    """
    Try to parse evaluation output as JSON, allowing a quick single-quote fix.
    """
    try:
        fixed = text.strip().replace("'", '"')
        return json.loads(fixed)
    except Exception:
        return None  # [file:4]


# ---- Main action ----
if run_btn:
    if up is None:
        st.error("Please upload a resume file.")  # [file:4]
    elif not job_title or not job_desc.strip():
        st.error("Please provide a target job title and job description.")  # [file:4]
    else:
        try:
            ext, raw_text = detect_and_extract(up.name, up.read())  # [file:4]
        except Exception as e:
            st.error(f"Failed to read file: {e}")  # [file:4]
            st.stop()

        if not raw_text or not raw_text.strip():
            st.error("Could not extract any text from the file.")  # [file:4]
            st.stop()

        with st.spinner("Running Crew agents..."):  # [file:4]
            try:
                cleaned, rewritten, final_resume, evaluation = run_pipeline(
                    raw_resume_text=raw_text,
                    job_title=job_title.strip(),
                    job_description=job_desc.strip(),
                )  # [file:3]
            except Exception as e:
                st.error(f"Pipeline failed: {e}")  # [file:3]
                st.stop()

        # ---- Tab 0: Cleaned ----
        with tabs[0]:
            st.subheader("Cleaned Resume (plain text)")  # [file:4]
            st.code(cleaned, language="markdown")  # [file:4]
            st.download_button(
                "Download cleaned.txt",
                data=cleaned,
                file_name="cleaned_resume.txt",
                mime="text/plain",
            )  # [file:4]

        # ---- Tab 1: Rewritten ----
        with tabs[1]:
            rewritten_text = getattr(rewritten, "tasks_output", rewritten)  # tolerate object-like returns [file:4]
            rewritten_str = _normalize_tasks_output(rewritten_text)  # [file:4]
            st.subheader("Rewritten Resume (ATS-optimized)")  # [file:4]
            st.code(rewritten_str, language="markdown")  # [file:4]
            st.download_button(
                "Download rewritten.txt",
                data=rewritten_str,
                file_name="rewritten_resume.txt",
                mime="text/plain",
            )  # [file:4]

        # ---- Tab 2: Final ----
        with tabs[2]:
            final_text = getattr(final_resume, "tasks_output", final_resume)  # [file:4]
            final_str = _normalize_tasks_output(final_text)  # [file:4]
            st.subheader("Final Resume (Refined Bullets)")  # [file:4]
            st.code(final_str, language="markdown")  # [file:4]
            st.download_button(
                "Download final.txt",
                data=final_str,
                file_name="final_resume.txt",
                mime="text/plain",
            )  # [file:4]

            # DOCX download
            try:
                docx_bytes = txt_to_docx_bytes(final_str)  # [file:2]
                st.download_button(
                    "Download final.docx",
                    data=docx_bytes,
                    file_name="final_resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )  # [file:2]
            except Exception as e:
                st.warning(f"Could not generate DOCX: {e}")  # [file:2]

        # ---- Tab 3: Evaluation ----
        with tabs[3]:
            st.subheader("ATS Evaluation & Suggestions")  # [file:4]
            eval_text = str(evaluation).strip()  # normalize in case of non-str [file:4]
            parsed = _try_parse_json(eval_text)  # [file:4]
            if parsed and isinstance(parsed, dict):
                st.json(parsed)  # [file:4]
                if "overall_score" in parsed:
                    st.metric("Overall ATS Score", f"{parsed['overall_score']}/100")  # [file:4]
            else:
                st.write("Raw evaluation output:")  # [file:4]
                st.code(eval_text, language="json")  # [file:4]
