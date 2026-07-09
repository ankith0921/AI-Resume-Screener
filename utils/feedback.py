def generate_feedback(candidate):

    strengths = []
    improvements = []

    # ATS Score
    ats = candidate["ATS Score"]

    if ats >= 85:
        strengths.append("Excellent ATS score.")
    elif ats >= 70:
        strengths.append("Good ATS score.")
    else:
        improvements.append("Improve resume relevance to the job description.")

    # Skill Match
    if candidate["Skill Match (%)"] >= 80:
        strengths.append("Strong skill match with the job requirements.")
    elif candidate["Skill Match (%)"] >= 60:
        strengths.append("Reasonable skill alignment.")
    else:
        improvements.append("Add more job-relevant technical skills.")

    # Experience
    experience = candidate["Experience (Years)"]

    try:
        experience = float(experience)
    except:
        experience = 0

    if experience >= 3:
        strengths.append("Good professional experience.")
    elif experience > 0:
        strengths.append("Some relevant experience.")
    else:
        improvements.append("Gain more practical or internship experience.")

    # Missing Skills
    if candidate["Missing Skills"] != "None":
        improvements.append(
            f"Consider learning: {candidate['Missing Skills']}."
        )

    # Overall Assessment
    if ats >= 85:
        overall = (
            "This candidate is a strong match and is recommended "
            "for the interview process."
        )
    elif ats >= 70:
        overall = (
            "This candidate is a good fit but may require "
            "additional evaluation."
        )
    else:
        overall = (
            "This candidate may require significant improvements "
            "before proceeding."
        )

    return strengths, improvements, overall