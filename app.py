import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.embeddings import generate_embedding
import pandas as pd
from utils.parser import (
    extract_name,
    extract_email,
    extract_phone
)
from utils.skills import extract_skills
from utils.ats_score import (
    calculate_skill_match,
    calculate_ats_score
)
from utils.experience import extract_experience
from utils.education import extract_education
from utils.degree_mapping import DEGREE_MAPPING
from utils.ranking_engine import rank_candidates
from components.dashboard import show_dashboard
from components.candidates import show_candidates
from components.reports import show_reports
from components.comparison import show_comparison

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="assets/logo.png",
    layout="wide"
)

# -------------------------------------------------
# Professional Header
# -------------------------------------------------

col1, col2 = st.columns([1.5, 5.5])

with col1:
    st.image("assets/logo.png", width=190)

with col2:
    st.title("AI Resume Screening System")
    st.caption("AI-Powered Resume Analysis and Candidate Ranking")
    st.caption(
    "Analyze resumes, rank candidates using AI, and streamline the hiring process."
)

st.divider()

# -------------------------------------------------
# Upload Section
# -------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        st.subheader("Job Description")

        st.caption(
            "Upload a PDF containing the job requirements."
        )

        jd_file = st.file_uploader(
            "Choose Job Description",
            type=["pdf"],
            key="jd",
            label_visibility="collapsed"
        )

        st.caption("Supported format: PDF")

with col2:

    with st.container(border=True):

        st.subheader("Candidate Resumes")

        st.caption(
            "Upload one or more candidate resumes."
        )

        resume_files = st.file_uploader(
            "Choose Resume PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        st.caption("Supported format: PDF")

st.divider()

# -------------------------------------------------
# Dashboard Statistics
# -------------------------------------------------

candidate_count = 0
average_ats = 0
top_ats = 0
average_experience = 0

# -------------------------------------------------
# Extract Job Description
# -------------------------------------------------
jd_text = ""
jd_embedding = None
jd_skills = []
if jd_file is not None:
    try:
        jd_text = extract_text_from_pdf(jd_file)

        st.success("Job description uploaded successfully.")

        with st.expander("View Extracted Job Description", expanded=True):
            st.text_area(
                "Job Description Text",
                jd_text,
                height=300
            )

        # Generate embedding
        if jd_text.strip():
            jd_embedding = generate_embedding(jd_text)
            jd_skills = extract_skills(jd_text)

            if jd_skills:
                st.subheader("Job Requirements")
                st.success(" | ".join(jd_skills))
            else:
                st.warning("No predefined skills detected in the Job Description.")

    except Exception as e:
        st.error(f"Error reading Job Description:\n{e}")

# -------------------------------------------------
# Extract Resume Text
# -------------------------------------------------
resume_data = []

if resume_files:

    st.header("Resume Preview")

    for resume in resume_files:

        try:
            resume_text = extract_text_from_pdf(resume)

            candidate_name = extract_name(resume_text)
            education = extract_education(resume_text)

            resume_data.append({
            
                "filename": resume.name,

                "candidate_name": candidate_name,

                "email": extract_email(resume_text),

                "phone": extract_phone(resume_text),

                "skills": extract_skills(resume_text),

                "experience": extract_experience(resume_text),

                "education": education,

                "text": resume_text

            })

            with st.expander(
                f"{candidate_name} ({resume.name})"
            ):

                st.text_area(
                    "Extracted Resume Text",
                    resume_text,
                    height=250,
                    key=resume.name
                )

        except Exception as e:

            st.error(f"Could not read {resume.name}")

    # -------------------------------
    # Rank Candidates
    # -------------------------------
    if jd_embedding is not None:
        with st.spinner("Generating embeddings and evaluating resumes..."):
            progress = st.progress(0)
            status = st.empty()

            ranking_df = rank_candidates(
                resume_data,
                jd_embedding,
                jd_skills,
                progress=progress,
                status=status
            )

            progress.empty()
            status.empty()

            st.success(
                f"Successfully analyzed {len(ranking_df)} resume(s)."
            )

            st.divider()
            st.subheader("Navigation")
            page = st.segmented_control(
                label="Navigation",
                options=[
                    "Dashboard",
                    "Candidates",
                    "Comparison",
                    "Reports"
                ],
                default="Dashboard",
                label_visibility="collapsed"
            )

            if page == "Dashboard":
                show_dashboard(
                    ranking_df=ranking_df,
                    resume_data=resume_data,
                    jd_file=jd_file,
                    DEGREE_MAPPING=DEGREE_MAPPING
                )

            elif page == "Candidates":
                show_candidates(ranking_df)

            elif page == "Comparison":
                show_comparison(ranking_df)

            elif page == "Reports":
                show_reports(ranking_df)