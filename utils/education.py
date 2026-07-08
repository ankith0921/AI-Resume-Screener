import re

# -----------------------------------
# Degree Keywords
# -----------------------------------
DEGREES = [

    "Bachelor of Engineering",
    "Bachelor of Technology",
    "Bachelor of Science",
    "Bachelor of Computer Applications",
    "Bachelor of Business Administration",

    "B.E",
    "BE",
    "B.Tech",
    "BSc",
    "B.Sc",
    "BCA",
    "BBA",

    "Master of Engineering",
    "Master of Technology",
    "Master of Science",
    "Master of Computer Applications",
    "Master of Business Administration",

    "M.E",
    "M.Tech",
    "M.Sc",
    "MSc",
    "MBA",
    "MCA",

    "PhD",
    "Ph.D",
    "Doctorate"
]


# -----------------------------------
# Branch Keywords
# -----------------------------------
BRANCHES = [

    "Computer Science",
    "Computer Science and Engineering",

    "Information Technology",

    "Artificial Intelligence",

    "Artificial Intelligence and Machine Learning",

    "Machine Learning",

    "Data Science",

    "Cyber Security",

    "Software Engineering",

    "Electronics",

    "Electronics and Communication",

    "Electrical Engineering",

    "Mechanical Engineering",

    "Civil Engineering",

    "Chemical Engineering",

    "Biomedical Engineering"

]


# -----------------------------------
# University Extraction
# -----------------------------------
UNIVERSITY_PATTERN = r".*(University|Institute|College|School).*"


# -----------------------------------
# Main Parser
# -----------------------------------
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

            branch = b

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

        "Degree": degree,

        "Branch": branch,

        "University": university,

        "Graduation Year": graduation_year,

        "CGPA": cgpa

    }