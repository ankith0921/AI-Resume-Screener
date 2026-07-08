import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.embeddings import generate_embedding
from utils.ranking import calculate_similarity
import pandas as pd
from utils.parser import (
    extract_name,
    extract_email,
    extract_phone
)

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("📄 AI Resume Screening System")
st.markdown(
    """
    Upload a **Job Description** and multiple **Candidate Resumes**.
    
    The system will extract the text from each PDF. In the next phase,
    we will rank candidates using AI based on how well their resumes
    match the job description.
    """
)

st.divider()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.header("About")
st.sidebar.info(
    """
    **AI Resume Screening System**

    Features (Coming Soon):
    - Resume Ranking
    - AI Similarity Score
    - Skill Extraction
    - Missing Skills Analysis
    - Candidate Summary
    - CSV Export
    """
)

# -------------------------------------------------
# Upload Section
# -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Job Description")
    jd_file = st.file_uploader(
        "Upload Job Description (PDF)",
        type=["pdf"],
        key="jd"
    )



with col2:
    st.subheader("📑 Candidate Resumes")
    resume_files = st.file_uploader(
        "Upload Resume PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

st.divider()

# -------------------------------------------------
# Extract Job Description
# -------------------------------------------------
jd_text = ""
jd_embedding = None

if jd_file is not None:
    try:
        jd_text = extract_text_from_pdf(jd_file)

        st.success("✅ Job Description Uploaded Successfully")

        with st.expander("View Extracted Job Description", expanded=True):
            st.text_area(
                "Job Description Text",
                jd_text,
                height=300
            )

        # Generate embedding
        if jd_text.strip():
            jd_embedding = generate_embedding(jd_text)

    except Exception as e:
        st.error(f"Error reading Job Description:\n{e}")

# -------------------------------------------------
# Extract Resume Text
# -------------------------------------------------
resume_data = []

if resume_files:

    st.header("📂 Uploaded Resumes")

    for resume in resume_files:

        try:
            resume_text = extract_text_from_pdf(resume)


            resume_data.append({

                "filename": resume.name,
            
                "candidate_name": extract_name(resume_text),
            
                "email": extract_email(resume_text),
            
                "phone": extract_phone(resume_text),
            
                "text": resume_text
            
            })

            with st.expander(f"📄 {resume.name}"):

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
        with st.spinner("🤖 Ranking candidates..."):

            ranking_results = []

            progress = st.progress(0)

            for i, candidate in enumerate(resume_data):

                progress.progress((i + 1) / len(resume_data))

                if candidate["text"].strip():
                    resume_embedding = generate_embedding(candidate["text"])
                else:
                    st.warning(f"⚠️ {candidate['name']} contains no extractable text.")
                    continue

                similarity = calculate_similarity(
                    jd_embedding,
                    resume_embedding
                )

                ranking_results.append({

                    "Candidate": candidate["candidate_name"],

                    "Email": candidate["email"],

                    "Phone": candidate["phone"],

                    "Resume": candidate["filename"],

                    "Match Score (%)": similarity

                })

            progress.empty()

            ranking_results.sort(
                key=lambda x: x["Match Score (%)"],
                reverse=True
            )

            st.header("🏆 Candidate Rankings")

            ranking_df = pd.DataFrame(ranking_results)
            # Round scores to 2 decimal places
            ranking_df["Match Score (%)"] = ranking_df["Match Score (%)"].round(2)

            ranking_df.index = ranking_df.index + 1
            ranking_df.index.name = "Rank"

            st.dataframe(
                ranking_df,
                use_container_width=True
            )
# -------------------------------------------------
# Summary
# -------------------------------------------------
st.divider()

st.header("📊 Upload Summary")

col1, col2 = st.columns(2)

with col1:
    if jd_file:
        st.metric("Job Description", "Uploaded")
    else:
        st.metric("Job Description", "Not Uploaded")

with col2:
    st.metric("Total Resumes", len(resume_data))

# -------------------------------------------------
# Next Phase Placeholder
# -------------------------------------------------
if jd_text and len(resume_data) > 0:

    st.success("🎉 Everything is ready!")

    st.info(
        """
        **Next Phase**
        
        We will now:
        
        ✅ Generate embeddings
        
        ✅ Compare each resume with the Job Description
        
        ✅ Calculate similarity scores
        
        ✅ Rank candidates
        
        ✅ Display Top Candidates
        """
    )

else:

    st.warning(
        "Please upload one Job Description and at least one Resume."
    )