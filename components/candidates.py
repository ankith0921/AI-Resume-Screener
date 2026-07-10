import streamlit as st

from utils.feedback import generate_feedback
from utils.recommendation import get_recommendation


def show_candidates(
    ranking_df,
    get_candidate
):
    """
    Displays candidate details page.
    """
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