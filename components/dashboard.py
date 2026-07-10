import streamlit as st
import pandas as pd
import plotly.express as px


def show_dashboard(
    ranking_df,
    resume_data,
    jd_file,
    DEGREE_MAPPING
):
    """
    Displays the dashboard page.
    """

    st.header("Candidate Ranking Results")

    candidate_count = len(ranking_df)
    average_ats = ranking_df["ATS Score"].mean()
    top_ats = ranking_df["ATS Score"].max()
    average_experience = (
        pd.to_numeric(ranking_df["Experience (Years)"], errors="coerce")
        .fillna(0)
        .mean()
    )

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

    st.header("Analysis Summary")

    col1, col2 = st.columns(2)

    with col1:
        if jd_file:
            st.metric("Job Description", "Uploaded")
        else:
            st.metric("Job Description", "Not Uploaded")

    with col2:
        st.metric("Total Resumes", len(resume_data))
