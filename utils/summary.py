def generate_summary(candidate):

    summary = []

    # Experience
    years = candidate["experience"]

    if years > 0:
        summary.append(
            f"{years} years of professional experience."
        )

    # Degree
    degree = candidate["education"]["Degree"]

    if degree != "Not Found":
        summary.append(
            f"Holds a {degree}."
        )

    # Branch
    branch = candidate["education"]["Branch"]

    if branch != "Not Found":
        summary.append(
            f"Specialized in {branch}."
        )

    # Skills
    if candidate["skills"]:

        top_skills = ", ".join(
            candidate["skills"][:5]
        )

        summary.append(
            f"Key skills include {top_skills}."
        )

    return " ".join(summary)