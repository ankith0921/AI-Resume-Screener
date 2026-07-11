# AI Resume Screening System

An intelligent, AI-powered Applicant Tracking System (ATS) built with **Streamlit**, **Sentence Transformers**, and **Python**. This application automates resume screening by analyzing, ranking, and comparing candidate resumes against job descriptions using semantic similarity, skill matching, and comprehensive resume analysis. It generates professional PDF reports for recruiters to streamline hiring workflows.

---

## Features

- Upload Job Description (PDF)
- Upload Multiple Candidate Resumes (PDF)
- Automatic Resume Parsing
- Semantic Similarity Matching
- ATS Score Calculation
- Skill Match Analysis
- Missing Skills Identification
- Candidate Ranking Dashboard
- Candidate Search & Filters
- Side-by-Side Candidate Comparison
- AI-Generated Candidate Summaries
- Hiring Recommendations with Dynamic Scoring
- Professional PDF Report Generation
- Interactive Analytics Dashboard
- CSV Export Functionality
- Clean & Modular Streamlit Interface

---

## Tech Stack

| Category | Technologies |
|----------|---------------|
| **Language** | Python |
| **Framework** | Streamlit |
| **AI/NLP** | Sentence Transformers, Semantic Similarity, NLP |
| **Data Processing** | Pandas, Scikit-learn |
| **Visualization** | Plotly |
| **PDF Processing** | PyMuPDF, ReportLab |

---

## Project Structure

```
AI-Resume-Screener/
├── app.py                          # Main Streamlit application entry point
├── requirements.txt                # Project dependencies
├── README.md                       # This file
│
├── assets/
│   ├── logo.png                    # Application logo
│   └── screenshots/                # UI screenshots
│
├── components/                     # UI component modules
│   ├── dashboard.py                # Analytics dashboard
│   ├── candidates.py               # Individual candidate details
│   ├── comparison.py               # Side-by-side comparison
│   └── reports.py                  # PDF report generation
│
├── utils/                          # Utility modules
    ├── ats_score.py                # ATS scoring algorithm
    ├── degree_mapping.py           # Education degree normalization
    ├── education.py                # Education parsing & analysis
    ├── embeddings.py               # Semantic embedding generation
    ├── experience.py               # Experience analysis
    ├── feedback.py                 # System feedback logic
    ├── helpers.py                  # Shared utility functions
    ├── parser.py                   # Resume parsing logic
    ├── pdf_reader.py               # PDF text extraction
    ├── ranking.py                  # Candidate ranking algorithms
    ├── ranking_engine.py           # Main ranking orchestration
    ├── recommendation.py           # Hiring recommendations
    ├── report_generator.py         # Professional PDF generation
    ├── skills.py                   # Skill extraction & matching
    └── summary.py                  # AI-generated summaries

```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Steps

**1. Clone the repository**
```bash
git clone https://github.com/ankith0921/AI-Resume-Screener.git
cd AI-Resume-Screener
```

**2. Create a virtual environment**
```bash
python -m venv venv
```

**3. Activate the virtual environment**

*Windows:*
```bash
venv\Scripts\activate
```

*Linux / macOS:*
```bash
source venv/bin/activate
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Streamlit server:
```bash
streamlit run app.py
```

The application will automatically open in your browser at:
```
http://localhost:8501
```

---

## How It Works

1. **Upload Job Description** - Provide a PDF with job requirements
2. **Upload Resumes** - Add one or more candidate PDFs
3. **Automatic Parsing** - System extracts text and structured data
4. **Semantic Matching** - Uses Sentence Transformers for intelligent comparison
5. **ATS Scoring** - Calculates match based on skills, experience, and similarity
6. **Ranking Dashboard** - View candidates ranked by relevance
7. **Comparison** - Compare candidates side-by-side
8. **PDF Reports** - Generate professional hiring recommendation reports

---

## Scoring & Analysis

### ATS Score
The ATS score combines three key metrics:
- **Semantic Similarity**: How closely resume content matches job description
- **Skill Match**: Percentage of required skills candidate possesses
- **Experience Analysis**: Years of relevant experience

### Recommendation System
Based on ATS score thresholds:
- 🟩 **>= 75** → Recommended
- 🟨 **>= 55** → Consider
- 🟥 **< 55%** → Not Recommended

---

## PDF Report Features

Each generated report includes:
- Candidate Information (Name, Email, Phone)
- Education Details (Degree, Branch, University, CGPA)
- Performance Scores (ATS, Semantic, Skill Match, Experience)
- Skills Analysis (Matched & Missing Skills)
- AI-Generated Candidate Summary
- Dynamic Hiring Recommendation
- Professional Formatting with Page Numbers

---

## Future Roadmap

- LLM-powered candidate evaluation
- Resume improvement suggestions
- Recruiter authentication & access control
- Database integration for persistence
- Resume keyword highlighting
- Multi-language resume support
- Cloud deployment options

---

[![Live Demo](https://img.shields.io/badge/Live-Demo-success)]([YOUR_STREAMLIT_URL](https://ai-resume-screener-hcwkeqeyb8jvef8he7pivc.streamlit.app/))

## About the Author

**Ankith Kanthyappa Nataraj**

*Computer Science Engineer*

Passionate about **Artificial Intelligence**, **Applied Machine Learning**, **Natural Language Processing**, and **Data Science**.

- GitHub: [ankith0921](https://github.com/ankith0921)
- LinkedIn: *www.linkedin.com/in/ankith-kn-9b7a6329b*

---

## License

This project is licensed under the **MIT License** - see LICENSE file for details.
