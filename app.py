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

            st.header("Candidate Ranking Results")

            filter1, filter2, filter3, filter4 = st.columns(4)

            with filter1:
                search_candidate = st.text_input(
                    "Search Candidate",
                    placeholder="Enter candidate name..."
                )

            with filter2:
                minimum_ats = st.slider(
                    "Minimum ATS Score",
                    min_value=0,
                    max_value=100,
                    value=0
                )

            with filter3:
                degree_filter = st.selectbox(
                    "Degree",
                    ["All"] + list(DEGREE_MAPPING.keys())
                )

            with filter4:
                experience_filter = st.selectbox(
                    "Minimum Experience",
                    ["All", 0, 1, 2, 3, 5, 7, 10]
                )

            ranking_df.index += 1
            ranking_df.index.name = "Rank"

            display_df = ranking_df.copy()

            if search_candidate:
            
                display_df = display_df[
                    display_df["Candidate"].str.contains(
                        search_candidate,
                        case=False,
                        na=False
                    )
                ]

            display_df = display_df[
                display_df["ATS Score"] >= minimum_ats
            ]

            if degree_filter != "All":

                aliases = DEGREE_MAPPING[degree_filter]

                pattern = "|".join(aliases)

                display_df = display_df[
                    display_df["Degree"].str.contains(
                        pattern,
                        case=False,
                        na=False
                    )
                ]

            if experience_filter != "All":

                display_df = display_df[
                    display_df["Experience (Years)"] >= experience_filter
                ]

            table_df = display_df[
                [
                    "Candidate",
                    "ATS Score",
                    "Semantic Score",
                    "Skill Match (%)",
                    "Experience (Years)",
                    "Degree"
                ]
            ]

            st.dataframe(
                table_df,
                use_container_width=True
            )

            st.divider()

            st.subheader("Recruitment Analytics")

            col1, col2 = st.columns(2)

            with col1:

                fig = px.histogram(
                    display_df,
                    x="ATS Score",
                    nbins=8,
                    title="ATS Score Distribution"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
            with col2:

                degree_counts = (
                    display_df["Degree"]
                    .value_counts()
                    .reset_index()
                )

                degree_counts.columns = [
                    "Degree",
                    "Candidates"
                ]

                fig = px.pie(
                    degree_counts,
                    names="Degree",
                    values="Candidates",
                    title="Degree Distribution"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            col3, col4 = st.columns(2)

            with col3:

                experience_df = display_df.copy()

                experience_df["Experience (Years)"] = (
                    pd.to_numeric(
                        experience_df["Experience (Years)"],
                        errors="coerce"
                    )
                    .fillna(0)
                )

                fig = px.histogram(
                    experience_df,
                    x="Experience (Years)",
                    nbins=8,
                    title="Experience Distribution"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            with col4:

                all_skills = []

                for skills in display_df["Matched Skills"]:
                
                    if skills != "None":
                    
                        all_skills.extend(
                            [skill.strip() for skill in skills.split(",")]
                        )

                if all_skills:
                
                    skills_df = (
                        pd.Series(all_skills)
                        .value_counts()
                        .head(10)
                        .reset_index()
                    )

                    skills_df.columns = [
                        "Skill",
                        "Count"
                    ]

                    fig = px.bar(
                        skills_df,
                        x="Count",
                        y="Skill",
                        orientation="h",
                        title="Top Matched Skills"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                else:
                
                    st.info("No matched skills available.")

            csv = display_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Ranking Report",
                data=csv,
                file_name="candidate_ranking.csv",
                mime="text/csv"
            )

            st.divider()

            st.header("Candidate Details")

            selected_candidate = st.selectbox(
                "Select Candidate",
                display_df["Candidate"]
            )

            candidate = ranking_df[
                ranking_df["Candidate"] == selected_candidate
            ].iloc[0]

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

            st.divider()

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

# -------------------------------------------------
# Summary
# -------------------------------------------------
st.divider()

st.header("Analysis Summary")

col1, col2 = st.columns(2)

with col1:
    if jd_file:
        st.metric("Job Description", "Uploaded")
    else:
        st.metric("Job Description", "Not Uploaded")

with col2:
    st.metric("Total Resumes", len(resume_data))