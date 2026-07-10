import streamlit as st
from components.dashboard import show_dashboard
from utils.pdf_reader import extract_text_from_pdf
from utils.embeddings import generate_embedding
from utils.ranking import calculate_similarity
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
from utils.summary import generate_summary
from utils.recommendation import get_recommendation
from utils.degree_mapping import DEGREE_MAPPING
import plotly.express as px
from utils.feedback import generate_feedback
from utils.report_generator import generate_pdf_report
from components.dashboard import show_dashboard

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

            ranking_results = []

            progress = st.progress(0)
            status = st.empty()

            for i, candidate in enumerate(resume_data):
            
                progress.progress((i + 1) / len(resume_data))

                name = candidate["candidate_name"]

                if name == "Unknown Candidate":
                    name = candidate["filename"]

                status.text(f"Processing: {name}")

                if candidate["text"].strip():
                    resume_embedding = generate_embedding(candidate["text"])
                else:
                    st.warning(
                        f"{candidate['filename']} contains no extractable text."
                    )
                    continue

                similarity = calculate_similarity(
                    jd_embedding,
                    resume_embedding
                )
                
                skill_match = calculate_skill_match(
                    candidate["skills"],
                    jd_skills
                )
                
                ats_score = calculate_ats_score(
                    similarity,
                    skill_match
                )
                
                # Compare resume skills with JD skills
                matched_skills = list(
                    set(candidate["skills"]) &
                    set(jd_skills)
                )
                
                missing_skills = list(
                    set(jd_skills) -
                    set(candidate["skills"])
                )
                
                ranking_results.append({

                    "Candidate": candidate["candidate_name"],

                    "Degree": candidate["education"]["Degree"],

                    "Branch": candidate["education"]["Branch"],

                    "University/College": candidate["education"]["University"],

                    "Graduation Year": candidate["education"]["Graduation Year"],

                    "CGPA": candidate["education"]["CGPA"],

                    "Experience (Years)": candidate["experience"],

                    "ATS Score": ats_score,
                
                    "Semantic Score": round(similarity, 2),
                
                    "Skill Match (%)": round(skill_match, 2),

                    "Summary": generate_summary(candidate),
                
                    "Email": candidate["email"],
                
                    "Phone": candidate["phone"],
                
                    "Resume": candidate["filename"],
                
                    "Matched Skills": ", ".join(sorted(matched_skills)) if matched_skills else "None",
                
                    "Missing Skills": ", ".join(sorted(missing_skills)) if missing_skills else "None"
                
                })

            progress.empty()
            status.empty()

            st.success(
                f"Successfully analyzed {len(ranking_results)} resume(s)."
            )

            ranking_df = pd.DataFrame(ranking_results)

            ranking_df["Semantic Score"] = ranking_df["Semantic Score"].round(2)
            ranking_df["Skill Match (%)"] = ranking_df["Skill Match (%)"].round(2)
            ranking_df["ATS Score"] = ranking_df["ATS Score"].round(2)

            ranking_df = ranking_df.sort_values(
                by="ATS Score",
                ascending=False
            ).reset_index(drop=True)

            def get_candidate(df, name):
                return df[
                    df["Candidate"] == name
                ].iloc[0]

            # Dashboard Statistics

            candidate_count = len(ranking_df)

            average_ats = ranking_df["ATS Score"].mean()

            top_ats = ranking_df["ATS Score"].max()

            ranking_df["Experience (Years)"] = pd.to_numeric(
                ranking_df["Experience (Years)"],
                errors="coerce"
            )

            average_experience = ranking_df["Experience (Years)"].fillna(0).mean()

            st.subheader("Recruitment Dashboard")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Candidates", candidate_count)

            with col2:
                st.metric("Average ATS", f"{average_ats:.2f}%")

            with col3:
                st.metric("Top ATS", f"{top_ats:.2f}%")

            with col4:
                st.metric("Avg Experience", f"{average_experience:.1f} Years")

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

                st.header("Candidate Details")

                selected_candidate = st.selectbox(
                    "Select Candidate",
                    ranking_df["Candidate"],
                    key="candidate_details"
                )

                candidate = get_candidate(
                    ranking_df,
                    selected_candidate
                )

                st.divider()

                col1, col2 = st.columns(2)

                with col1:
                
                    st.subheader("Personal Information")

                    st.write(f"**Name:** {candidate['Candidate']}")
                    st.write(f"**Email:** {candidate['Email']}")
                    st.write(f"**Phone:** {candidate['Phone']}")

                    st.write(f"**Experience:** {candidate['Experience (Years)']}")

                with col2:
                
                    st.subheader("Education")

                    st.write(f"**Degree:** {candidate['Degree']}")
                    st.write(f"**Branch:** {candidate['Branch']}")
                    st.write(f"**University/College:** {candidate['University/College']}")
                    st.write(f"**Graduation Year:** {candidate['Graduation Year']}")
                    st.write(f"**CGPA:** {candidate['CGPA']}")

                st.divider()
                

                st.subheader("Candidate Performance")

                st.write(f"**ATS Score:** {candidate['ATS Score']}%")
                st.progress(int(candidate["ATS Score"]))

                st.write(f"**Semantic Score:** {candidate['Semantic Score']}%")
                st.progress(int(candidate["Semantic Score"]))

                st.write(f"**Skill Match:** {candidate['Skill Match (%)']}%")
                st.progress(int(candidate["Skill Match (%)"]))
                col1, col2 = st.columns(2)

                with col1:
                    
                        st.subheader("Matched Skills")

                        st.success(candidate["Matched Skills"])

                with col2:
                    
                    st.subheader("Missing Skills")

                    st.warning(candidate["Missing Skills"])

                st.divider()

                st.subheader("AI Candidate Summary")

                st.info(candidate["Summary"])

                st.divider()

                recommendation, message = get_recommendation(
                    candidate["ATS Score"]
                )

                st.subheader("Hiring Recommendation")

                if recommendation == "Strong Match":

                    st.success(
                        f"""
                ### Strong Match

                **Recommendation:** {message}

                **Decision:** Proceed with Interview
                """
                    )

                elif recommendation == "Good Match":
                
                    st.info(
                        f"""
                ### Good Match

                **Recommendation:** {message}

                **Decision:** Shortlist Candidate
                """
                    )

                elif recommendation == "Average Match":
                
                    st.warning(
                        f"""
                ### Average Match

                **Recommendation:** {message}

                **Decision:** Manual Review Required
                """
                    )

                else:
                
                    st.error(
                        f"""
                ### Weak Match

                **Recommendation:** {message}

                **Decision:** Not Recommended
                """
                    )

                st.divider()

                st.subheader("AI Resume Feedback")

                strengths, improvements, overall = generate_feedback(candidate)

                col1, col2 = st.columns(2)

                with col1:
                
                    st.markdown("Strengths")

                    if strengths:
                        for item in strengths:
                            st.success(item)
                    else:
                        st.info("No strengths identified.")

                with col2:
                
                    st.markdown("Areas for Improvement")

                    if improvements:
                        for item in improvements:
                            st.warning(item)
                    else:
                        st.success("No major improvements required.")

                st.markdown("Overall Assessment")
                st.info(overall)
            
            elif page == "Reports":
            
                st.header("Reports")

                selected_candidate = st.selectbox(
                    "Select Candidate",
                    ranking_df["Candidate"],
                    key="report_candidate"
                )

                candidate = get_candidate(
                    ranking_df,
                    selected_candidate
                )

                filename = "Candidate_Report.pdf"

                generate_pdf_report(
                    candidate,
                    filename
                )

                with open(filename, "rb") as pdf_file:
                
                    st.download_button(
                        label=":material/download: Download Candidate Report",
                        data=pdf_file,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )

            elif page == "Comparison":

                st.header("Candidate Comparison")

                if len(ranking_df) > 1:
                
                    comparison_col1, comparison_col2 = st.columns(2)
                
                    with comparison_col1:
                        candidate1_name = st.selectbox(
                            "Candidate 1",
                            ranking_df["Candidate"],
                            key="candidate1"
                        )
                
                    with comparison_col2:
                        candidate2_name = st.selectbox(
                            "Candidate 2",
                            ranking_df["Candidate"],
                            index=1,
                            key="candidate2"
                        )
                
                    candidate1 = get_candidate(
                        ranking_df,
                        candidate1_name
                    )

                    candidate2 = get_candidate(
                        ranking_df,
                        candidate2_name
                    ) 
                
                    st.subheader("Comparison Summary")
                
                    ats_winner = (
                        candidate1_name
                        if candidate1["ATS Score"] >= candidate2["ATS Score"]
                        else candidate2_name
                    )
                
                    exp_winner = (
                        candidate1_name
                        if candidate1["Experience (Years)"] >= candidate2["Experience (Years)"]
                        else candidate2_name
                    )
                
                    skill_winner = (
                        candidate1_name
                        if candidate1["Skill Match (%)"] >= candidate2["Skill Match (%)"]
                        else candidate2_name
                    )
                
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Higher ATS",
                            ats_winner
                        )
                    
                    with col2:
                        st.metric(
                            "Experience",
                            exp_winner
                        )
                    
                    with col3:
                        st.metric(
                            "Skill Match",
                            skill_winner
                        )
                
                    comparison_df = pd.DataFrame({
                        "Attribute": [
                            "ATS Score",
                            "Semantic Score",
                            "Skill Match",
                            "Experience",
                            "Degree",
                            "Branch",
                            "Matched Skills",
                            "Missing Skills"
                        ],
                        candidate1_name: [
                            f"{candidate1['ATS Score']}%",
                            f"{candidate1['Semantic Score']}%",
                            f"{candidate1['Skill Match (%)']}%",
                            f"{candidate1['Experience (Years)']} Years",
                            candidate1["Degree"],
                            candidate1["Branch"],
                            candidate1["Matched Skills"],
                            candidate1["Missing Skills"]
                        ],
                        candidate2_name: [
                            f"{candidate2['ATS Score']}%",
                            f"{candidate2['Semantic Score']}%",
                            f"{candidate2['Skill Match (%)']}%",
                            f"{candidate2['Experience (Years)']} Years",
                            candidate2["Degree"],
                            candidate2["Branch"],
                            candidate2["Matched Skills"],
                            candidate2["Missing Skills"]
                        ]
                    })
                
                    st.dataframe(
                        comparison_df,
                        use_container_width=True,
                        hide_index=True
                    )
                
                else:
                    st.info("Upload at least two resumes to compare candidates.")