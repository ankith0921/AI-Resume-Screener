import pandas as pd
from utils.embeddings import generate_embedding
from utils.ranking import calculate_similarity
from utils.ats_score import calculate_skill_match, calculate_ats_score
from utils.summary import generate_summary


def rank_candidates(resume_data, jd_embedding, jd_skills, progress=None, status=None):
    """
    Rank resumes against a job description and return a dataframe.
    """
    ranking_results = []

    for i, candidate in enumerate(resume_data):
        if progress is not None:
            progress.progress((i + 1) / len(resume_data))

        name = candidate["candidate_name"]
        if name == "Unknown Candidate":
            name = candidate["filename"]

        if status is not None:
            status.text(f"Processing: {name}")

        if candidate["text"].strip():
            resume_embedding = generate_embedding(candidate["text"])
        else:
            continue

        similarity = calculate_similarity(jd_embedding, resume_embedding)
        skill_match = calculate_skill_match(candidate["skills"], jd_skills)
        ats_score = calculate_ats_score(similarity, skill_match)

        matched_skills = list(set(candidate["skills"]) & set(jd_skills))
        missing_skills = list(set(jd_skills) - set(candidate["skills"]))

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
            "Missing Skills": ", ".join(sorted(missing_skills)) if missing_skills else "None",
        })

    ranking_df = pd.DataFrame(ranking_results)
    if ranking_df.empty:
        return ranking_df

    ranking_df["Semantic Score"] = ranking_df["Semantic Score"].round(2)
    ranking_df["Skill Match (%)"] = ranking_df["Skill Match (%)"].round(2)
    ranking_df["ATS Score"] = ranking_df["ATS Score"].round(2)

    ranking_df = ranking_df.sort_values(by="ATS Score", ascending=False).reset_index(drop=True)
    return ranking_df
