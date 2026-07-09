import re

# -----------------------------------
# Degree Keywords
# -----------------------------------
DEGREES = [

    # Bachelor's Degrees
    "Bachelor of Engineering",
    "Bachelor's of Engineering",
    "Bachelor of Technology",
    "Bachelor's of Technology",
    "Bachelor of Science",
    "Bachelor's of Science",
    "Bachelor of Computer Applications",
    "Bachelor's of Computer Applications",
    "Bachelor of Business Administration",
    "Bachelor's of Business Administration",

    # Common Abbreviations
    "B.E",
    "BE",
    "B E",

    "B.Tech",
    "BTech",
    "B Tech",

    "B.Sc",
    "BSc",
    "B Sc",

    "BCA",
    "B.C.A",

    "BBA",
    "B.B.A",

    # Master's Degrees
    "Master of Engineering",
    "Master's of Engineering",
    "Master of Technology",
    "Master's of Technology",
    "Master of Science",
    "Master's of Science",
    "Master of Computer Applications",
    "Master's of Computer Applications",
    "Master of Business Administration",
    "Master's of Business Administration",

    # Common Abbreviations
    "M.E",
    "ME",
    "M E",

    "M.Tech",
    "MTech",
    "M Tech",

    "M.Sc",
    "MSc",
    "M Sc",

    "MBA",

    "MCA",
    "M.C.A",

    # Doctoral
    "PhD",
    "Ph.D",
    "Doctorate",
    "Doctor of Philosophy"
]


# -----------------------------------
# Branch Keywords
# -----------------------------------
BRANCHES = [

    # Computer Science
    "Computer Science",
    "CS",

    # Computer Science & Engineering
    "Computer Science and Engineering",
    "Computer Engineering",
    "CSE",
    "C.S.E",

    # Information Technology
    "Information Technology",
    "IT",
    "I.T",

    # Artificial Intelligence
    "Artificial Intelligence",
    "AI",
    "A.I",

    # Artificial Intelligence & Machine Learning
    "Artificial Intelligence and Machine Learning",
    "Artificial Intelligence & Machine Learning",
    "AI and ML",
    "AI & ML",
    "AI/ML",
    "AIML",

    # Machine Learning
    "Machine Learning",
    "ML",
    "M.L",

    # Data Science
    "Data Science",
    "Data Analytics",
    "Data Engineering",
    "DS",

    # Cyber Security
    "Cyber Security",
    "Cybersecurity",
    "Cyber-Security",

    # Software Engineering
    "Software Engineering",
    "Software Development",

    # Electronics
    "Electronics",

    # Electronics & Communication
    "Electronics and Communication",
    "Electronics & Communication",
    "Electronics Communication",
    "ECE",
    "E.C.E",

    # Electrical Engineering
    "Electrical Engineering",
    "Electrical and Electronics Engineering",
    "EEE",
    "E.E.E",

    # Mechanical Engineering
    "Mechanical Engineering",
    "Mechanical",

    # Civil Engineering
    "Civil Engineering",
    "Civil",

    # Chemical Engineering
    "Chemical Engineering",
    "Chemical",

    # Biomedical Engineering
    "Biomedical Engineering",
    "Biomedical"

]


# -----------------------------------
# University Extraction
# -----------------------------------
UNIVERSITY_PATTERN = (
    r".*(University|Institute|College|School|Academy|"
    r"Polytechnic|Campus).*"
)

def standardize_degree(degree):

    degree = degree.lower().strip()

    degree_mapping = {

        "b.e": "B.E",
        "be": "B.E",
        "b e": "B.E",
        "bachelor of engineering": "B.E",
        "bachelor's of engineering": "B.E",

        "b.tech": "B.Tech",
        "btech": "B.Tech",
        "bachelor of technology": "B.Tech",
        "b tech": "B.Tech",
        "bachelor's of technology": "B.Tech",

        "b.sc": "B.Sc",
        "bsc": "B.Sc",
        "bachelor of science": "B.Sc",
        "b sc": "B.Sc",
        "bachelor's of science": "B.Sc",

        "b.c.a": "BCA",
        "bachelor's of computer applications": "BCA",
        "bca": "BCA",
        "bachelor of computer applications": "BCA",

        "m.tech": "M.Tech",
        "mtech": "M.Tech",
        "master of technology": "M.Tech",
        "m tech": "M.Tech",
        "master's of technology": "M.Tech",

        "b.b.a": "BBA",
        "bachelor's of business administration": "BBA",
        "bba": "BBA",
        "bachelor of business administration": "BBA",

        "m.sc": "M.Sc",
        "msc": "M.Sc",
        "master of science": "M.Sc",
        "m sc": "M.Sc",
        "master's of science": "M.Sc",

        "me": "M.E",
        "m e": "M.E",
        "master's of engineering": "M.E",
        "m.e": "M.E",
        "master of engineering": "M.E",

        "mba": "MBA",
        "master of business administration": "MBA",
        "master's of business administration": "MBA",

        "mca": "MCA",
        "master of computer applications": "MCA",
        "m.c.a": "MCA",
        "master's of computer applications": "MCA",

        "phd": "PhD",
        "doctorate": "PhD",
        "doctor of philosophy": "PhD",
        "ph.d": "PhD"
    }

    return degree_mapping.get(degree, "Not Found" if degree == "not found" else degree.title())

def standardize_branch(branch):

    branch = branch.lower().strip()

    branch_mapping = {

    # Computer Science
    "computer science": "Computer Science",
    "cs": "Computer Science",

    # Computer Science & Engineering
    "computer science and engineering": "Computer Science and Engineering",
    "computer engineering": "Computer Science and Engineering",
    "cse": "Computer Science and Engineering",
    "c.s.e": "Computer Science and Engineering",

    # Information Technology
    "information technology": "Information Technology",
    "it": "Information Technology",
    "i.t": "Information Technology",

    # Artificial Intelligence
    "artificial intelligence": "Artificial Intelligence",
    "ai": "Artificial Intelligence",
    "a.i": "Artificial Intelligence",

    # Artificial Intelligence & Machine Learning
    "artificial intelligence and machine learning":
        "Artificial Intelligence and Machine Learning",
    "artificial intelligence & machine learning":
        "Artificial Intelligence and Machine Learning",
    "ai and ml":
        "Artificial Intelligence and Machine Learning",
    "ai & ml":
        "Artificial Intelligence and Machine Learning",
    "ai/ml":
        "Artificial Intelligence and Machine Learning",
    "aiml":
        "Artificial Intelligence and Machine Learning",

    # Machine Learning
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "m.l": "Machine Learning",

    # Data Science
    "data science": "Data Science",
    "data analytics": "Data Science",
    "data engineering": "Data Science",
    "ds": "Data Science",

    # Cyber Security
    "cyber security": "Cyber Security",
    "cybersecurity": "Cyber Security",
    "cyber-security": "Cyber Security",

    # Software Engineering
    "software engineering": "Software Engineering",
    "software development": "Software Engineering",

    # Electronics
    "electronics": "Electronics",

    # Electronics & Communication
    "electronics and communication": "Electronics and Communication",
    "electronics & communication": "Electronics and Communication",
    "electronics communication": "Electronics and Communication",
    "ece": "Electronics and Communication",
    "e.c.e": "Electronics and Communication",

    # Electrical Engineering
    "electrical engineering": "Electrical Engineering",
    "electrical and electronics engineering": "Electrical Engineering",
    "eee": "Electrical Engineering",
    "e.e.e": "Electrical Engineering",

    # Mechanical Engineering
    "mechanical engineering": "Mechanical Engineering",
    "mechanical": "Mechanical Engineering",

    # Civil Engineering
    "civil engineering": "Civil Engineering",
    "civil": "Civil Engineering",

    # Chemical Engineering
    "chemical engineering": "Chemical Engineering",
    "chemical": "Chemical Engineering",

    # Biomedical Engineering
    "biomedical engineering": "Biomedical Engineering",
    "biomedical": "Biomedical Engineering"
}

    return branch_mapping.get(branch, branch.title())

def extract_education(text):

    lines = text.split("\n")

    degree = "Not Found"

    branch = "Not Found"

    university = "Not Found"

    graduation_year = "Not Found"

    cgpa = "Not Found"

    # Degree
    for d in DEGREES:

        if d.lower() in text.lower():

            degree = d

            break

    # Branch

    for b in BRANCHES:

        if b.lower() in text.lower():

            branch = standardize_branch(b)

            break

    # University

    for line in lines:

        if re.search(
            UNIVERSITY_PATTERN,
            line,
            re.IGNORECASE
        ):

            university = line.strip()

            break

    # Graduation Year

    years = re.findall(r"(19\d{2}|20\d{2})", text)

    if years:

        graduation_year = max(years)

    # CGPA

    cgpa_match = re.search(
        r"(CGPA|GPA)\s*[:\-]?\s*(\d+(\.\d+)?)",
        text,
        re.IGNORECASE
    )

    if cgpa_match:

        cgpa = cgpa_match.group(2)

    return {

        "Degree": standardize_degree(degree),

        "Branch": branch,

        "University": university,

        "Graduation Year": graduation_year,

        "CGPA": cgpa

    }