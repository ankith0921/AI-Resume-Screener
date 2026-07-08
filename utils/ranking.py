from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(jd_embedding, resume_embedding):
    """
    Calculate similarity score between job description
    and resume embeddings.
    """
    score = cosine_similarity(
        [jd_embedding],
        [resume_embedding]
    )[0][0]

    return round(score * 100, 2)