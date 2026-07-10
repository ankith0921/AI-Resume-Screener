import streamlit as st
import pandas as pd
from utils.helpers import get_candidate


def show_comparison(
    ranking_df
):
    """
    Displays candidate comparison page.
    """

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