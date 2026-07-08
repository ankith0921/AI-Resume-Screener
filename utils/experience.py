import re


def extract_experience(text):
    """
    Extract total years of experience from resume text.
    """

    patterns = [

        r'(\d+)\+?\s+years',

        r'(\d+)\+?\s+yrs',

        r'(\d+)\+?\s+year',

        r'(\d+)\+?\s+yr'

    ]

    text = text.lower()

    years = []

    for pattern in patterns:

        matches = re.findall(pattern, text)

        for match in matches:
            years.append(int(match))

    if years:
        return max(years)

    return 0