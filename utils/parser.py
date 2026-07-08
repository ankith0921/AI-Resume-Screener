import re


# ----------------------------
# Extract Email
# ----------------------------
def extract_email(text):

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


# ----------------------------
# Extract Phone Number
# ----------------------------
def extract_phone(text):

    pattern = r"""
    (?:
        \+?\d{1,3}[\s\-]?
    )?
    (?:\(\d{3}\)|\d{3})
    [\s\-]?
    \d{3}
    [\s\-]?
    \d{4}
    """

    match = re.search(pattern, text, re.VERBOSE)

    if match:
        return match.group().strip()

    return "—"


# ----------------------------
# Extract Candidate Name
# ----------------------------
def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line) > 2 and len(line.split()) <= 4:

            if not any(char.isdigit() for char in line):

                return line

    return "Unknown Candidate"