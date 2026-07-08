import re

# Master skill list
SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "TypeScript",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "OpenCV",
    "NLP",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Git",
    "Linux",
    "FastAPI",
    "Flask",
    "Django",
    "REST API",
    "Spark",
    "Hadoop",
    "Power BI",
    "Tableau"
]


def extract_skills(text):

    found_skills = set()

    text = text.lower()

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.add(skill)

    return sorted(found_skills)