from tabulate import tabulate

PYTHON_KEYWORDS = {"if", "else", "while", "for", "def", "return", "class", "try", "except", "import"}
PYTHON_OPERATORS = {"+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "and", "or", "not"}
PYTHON_PUNCTUATORS = {",", ":", ";", "(", ")", "{", "}", "[", "]"}

def is_identifier(token):
    return token.isidentifier()

def is_literal(token):
    try:
        float(token)
        return True
    except ValueError:
        pass
    if token.startswith(("'", '"')) and token.endswith(("'", '"')):
        return True
    if token in {"True", "False", "None", "true", "false", "nullptr"}:
        return True
    return False

def clean_line(line):
    cleaned = " ".join(line.split())
    return cleaned

def tokenize_line(line, keywords, operators, punctuators, literals, comments):
    tokens = []
    token = ""
    inside_string = False

    if "#" in line:
        comment_part = line.split("#", 1)[1].strip()
        comments.append(f"#{comment_part}")
        line = line.split("#", 1)[0]

    line = clean_line(line)

    i = 0
    while i < len(line):
        char = line[i]

        if char in ('"', "'"):
            if inside_string:
                token += char
                tokens.append(token.strip())
                token = ""
                inside_string = False
            else:
                if token:
                    tokens.append(token.strip())
                    token = ""
                token += char
                inside_string = True
        elif inside_string:
            token += char
        elif i < len(line) - 1 and line[i:i + 2] in operators:
            if token:
                tokens.append(token.strip())  
                token = ""
            tokens.append(line[i:i + 2])
            i += 2
            continue
        elif char in operators or char in punctuators:
            if token:
                tokens.append(token.strip())
                token = ""
            tokens.append(char)
        elif char.isspace():
            if token:
                tokens.append(token.strip())
                token = ""
        else:
            token += char

        i += 1

    if token:
        tokens.append(token.strip())

    return tokens

def categorize_tokens(tokens, keywords, operators, punctuators, literals, comments):
    categorized = {
        "Keywords": [],
        "Identifiers": [],
        "Literals": literals,
        "Operators": [],
        "Punctuators": [],
        "Comments": comments
    }

    total_token_count = 0

    for token in tokens:
        token = token.strip()
        if not token:
            continue
        if token in keywords:
            categorized["Keywords"].append(token)
            total_token_count += 1
        elif token in operators:
            categorized["Operators"].append(token)
            total_token_count += 1
        elif token in punctuators:
            categorized["Punctuators"].append(token)
            total_token_count += 1
        elif is_literal(token):
            categorized["Literals"].append(token)
            total_token_count += 1
        elif is_identifier(token):
            categorized["Identifiers"].append(token)
            total_token_count += 1

    return categorized, total_token_count

def display_table(categorized_tokens, total_count):
    print("Tokens for PYTHON:")
    categorized = [
        ["Keywords", ", ".join(categorized_tokens["Keywords"])],
        ["Identifiers", ", ".join(categorized_tokens["Identifiers"])],
        ["Literals", ", ".join(categorized_tokens["Literals"])],
        ["Operators", ", ".join(categorized_tokens["Operators"])],
        ["Punctuators", ", ".join(categorized_tokens["Punctuators"])],
        ["Comments", ", ".join(categorized_tokens["Comments"])],
        ["Total Tokens (excluding comments)", total_count]
    ]

    headers = ["Category", "Tokens"]
    table = tabulate(categorized, headers, tablefmt="fancy_grid")
    print(table)

def categorize_tokens(tokens, keywords, operators, punctuators, literals, comments):
    categorized = {
        "Keywords": [],
        "Identifiers": [],
        "Literals": literals,
        "Operators": [],
        "Punctuators": [],
        "Comments": comments
    }

    total_token_count = 0

    for token in tokens:
        token = token.strip()
        if not token:
            continue
        if token in keywords:
            categorized["Keywords"].append(token)
            total_token_count += 1
        elif token in operators:
            categorized["Operators"].append(token)
            total_token_count += 1
        elif token in punctuators:
            categorized["Punctuators"].append(token)
            total_token_count += 1
        elif is_literal(token):
            categorized["Literals"].append(token)
            total_token_count += 1
        elif is_identifier(token):
            categorized["Identifiers"].append(token)
            total_token_count += 1

    return categorized, total_token_count

def detect_language(line):
    if "def" in line or "if __name__" in line or "print(" in line:
        return "python"
    return None

def clean_code_and_ignore_comments(file_path):
    cleaned_code = []
    inside_multiline_comment = False

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if '"""' in line or "'''" in line:
                if inside_multiline_comment:
                    inside_multiline_comment = False
                    continue
                else:
                    inside_multiline_comment = True
                    continue

            if inside_multiline_comment:
                continue
            if "#" in line:
                line = line.split("#", 1)[0].strip()

            cleaned_line = clean_line(line)

            if cleaned_line:
                cleaned_code.append(cleaned_line)

        print("\n--- Cleaned Up Code (Comments Ignored) ---")
        for line in cleaned_code:
            print(line)

        return cleaned_code

    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Unable to read the file.")

def process_file(file_path):
    python_code = []
    python_tokens = []
    python_literals = []
    python_comments = []
    language = None

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            cleaned_line = clean_line(line)
            python_code.append(cleaned_line)
            python_tokens.extend(tokenize_line(line, PYTHON_KEYWORDS, PYTHON_OPERATORS, PYTHON_PUNCTUATORS, python_literals, python_comments))

        print("\n--- Original Code in File ---")
        print("\nPython:\n" + "\n".join(python_code))

        python_categorized, python_total = categorize_tokens(python_tokens, PYTHON_KEYWORDS, PYTHON_OPERATORS, PYTHON_PUNCTUATORS, python_literals, python_comments)

        return python_categorized, python_total

    except FileNotFoundError:
        print("File was not found.")
    except IOError:
        print("Not able to read the file.")

def display_table(categorized_tokens, total_count):
    print("Tokens for PYTHON:")
    categorized = [
        ["Keywords", ", ".join(categorized_tokens["Keywords"])],
        ["Identifiers", ", ".join(categorized_tokens["Identifiers"])],
        ["Literals", ", ".join(categorized_tokens["Literals"])],
        ["Operators", ", ".join(categorized_tokens["Operators"])],
        ["Punctuators", ", ".join(categorized_tokens["Punctuators"])],
        ["Comments", ", ".join(categorized_tokens["Comments"])],
        ["Total Tokens (excluding comments)", total_count]
    ]

    headers = ["Category", "Tokens"]
    table = tabulate(categorized, headers, tablefmt="fancy_grid")
    print(table)

def display_total_tokens(total_count):
    print(f"Total tokens (excluding comments) for PYTHON: {total_count}")

if __name__ == "__main__":
    file_path = "test.txt"
    cleaned_code = clean_code_and_ignore_comments(file_path)
    python_categorized, python_total = process_file(file_path)
    display_table(python_categorized, python_total)
    display_total_tokens(python_total)


