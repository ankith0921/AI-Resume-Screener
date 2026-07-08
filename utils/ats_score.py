def calculate_skill_match(resume_skills, jd_skills):
    """
    Returns skill match percentage.
    """

    if not jd_skills:
        return 0

    matched = len(
        set(resume_skills) &
        set(jd_skills)
    )

    return (matched / len(jd_skills)) * 100


def calculate_ats_score(
    semantic_similarity,
    skill_match
):
    """
    Weighted ATS Score

    Semantic Similarity : 70%
    Skill Match         : 30%
    """

    ats_score = (
        semantic_similarity * 0.70
        +
        skill_match * 0.30
    )

    return round(ats_score, 2)