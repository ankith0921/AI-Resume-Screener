def get_recommendation(ats_score):

    if ats_score >= 85:
        return (
            "Strong Match",
            "Recommended for Interview"
        )

    elif ats_score >= 70:
        return (
            "Good Match",
            "Consider for Interview"
        )

    elif ats_score >= 50:
        return (
            "Average Match",
            "Review Before Deciding"
        )

    else:
        return (
            "Weak Match",
            "Not Recommended"
        )