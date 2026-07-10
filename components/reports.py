import streamlit as st
from utils.report_generator import generate_pdf_report
from utils.helpers import get_candidate


def show_reports(
    ranking_df
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

    filename = f"{candidate['Candidate'].replace(' ', '_')}_Report.pdf"

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