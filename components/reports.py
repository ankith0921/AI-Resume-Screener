import streamlit as st

from utils.report_generator import generate_pdf_report


def show_reports(
    ranking_df,
    get_candidate
):
    """
    Displays report generation page.
    """
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