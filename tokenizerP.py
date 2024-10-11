from tabulate import tabulate

# Define Python keywords, operators, and punctuators
PYTHON_KEYWORDS = {"if", "else", "while", "for", "def", "return", "class", "try", "except", "import"}
PYTHON_OPERATORS = {"+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "and", "or", "not"}
PYTHON_PUNCTUATORS = {",", ":", ";", "(", ")", "{", "}", "[", "]"}

def is_identifier(token):
    return token.isidentifier()

def is_literal(token):
    # Treat actual literals (numbers, strings, etc.)
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

# Function to clean each line of code by removing extra spaces and unnecessary whitespace
def clean_line(line):
    cleaned = " ".join(line.split())
    return cleaned

# Function to tokenize a line of code
def tokenize_line(line, keywords, operators, punctuators, literals, comments):
    tokens = []
    token = ""
    inside_string = False  # Track if we're inside a string

    # Handle comments and add them to comments list
    if "#" in line:
        comment_part = line.split("#", 1)[1].strip()
        comments.append(f"#{comment_part}")  # Add comment as a literal
        line = line.split("#", 1)[0]  # Remove the comment part from the actual line

    line = clean_line(line)

    i = 0
    while i < len(line):
        char = line[i]

        # Check for string literals
        if char in ('"', "'"):  # Detect both single and double quotes
            if inside_string:
                token += char
                tokens.append(token.strip())  # Add the entire string as one token
                token = ""
                inside_string = False
            else:
                if token:
                    tokens.append(token.strip())  # Add any completed token before starting the string
                    token = ""
                token += char  # Add the starting quote to the token
                inside_string = True
        elif inside_string:
            token += char  # Keep adding characters until we find the closing quote
        elif i < len(line) - 1 and line[i:i + 2] in operators:
            if token:
                tokens.append(token.strip())  # Add any completed token before the operator
                token = ""
            tokens.append(line[i:i + 2])  # Add the multi-character operator as a single token
            i += 2
            continue
        elif char in operators or char in punctuators:
            if token:
                tokens.append(token.strip())  # Add any completed token before the operator or punctuator
                token = ""
            tokens.append(char)  # Add the single operator or punctuator
        elif char.isspace():
            if token:
                tokens.append(token.strip())  # Add any completed token
                token = ""
        else:
            token += char  # Build the token

        i += 1

    if token:  # Handle the last token if there is one
        tokens.append(token.strip())

    return tokens  # Return the tokens list


# Function to categorize tokens
def categorize_tokens(tokens, keywords, operators, punctuators, literals, comments):
    categorized = {
        "Keywords": [],
        "Identifiers": [],
        "Literals": literals,  # Keep the literals from earlier
        "Operators": [],
        "Punctuators": [],
        "Comments": comments  # Add comments separately
    }

    total_token_count = 0  # Initialize token counter (excluding comments)

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
            categorized["Literals"].append(token)  # Add non-comment literals
            total_token_count += 1
        elif is_identifier(token):
            categorized["Identifiers"].append(token)
            total_token_count += 1

    return categorized, total_token_count


# Display token table for Python, including comments in a separate row
def display_table(categorized_tokens, total_count):
    print("Tokens for PYTHON:")
    categorized = [
        ["Keywords", ", ".join(categorized_tokens["Keywords"])],
        ["Identifiers", ", ".join(categorized_tokens["Identifiers"])],
        ["Literals", ", ".join(categorized_tokens["Literals"])],  # No comments in literals
        ["Operators", ", ".join(categorized_tokens["Operators"])],
        ["Punctuators", ", ".join(categorized_tokens["Punctuators"])],
        ["Comments", ", ".join(categorized_tokens["Comments"])],  # New row for comments
        ["Total Tokens (excluding comments)", total_count]
    ]

    headers = ["Category", "Tokens"]
    table = tabulate(categorized, headers, tablefmt="fancy_grid")
    print(table)





# Function to categorize tokens
def categorize_tokens(tokens, keywords, operators, punctuators, literals, comments):
    categorized = {
        "Keywords": [],
        "Identifiers": [],
        "Literals": literals,  # Only actual literals here (no comments)
        "Operators": [],
        "Punctuators": [],
        "Comments": comments  # Comments in their own row
    }

    total_token_count = 0  # Initialize token counter (comments are excluded from this count)

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

# Detect language is simplified to only handle Python now
def detect_language(line):
    if "def" in line or "if __name__" in line or "print(" in line:
        return "python"
    return None

# Cleaning code for Python, ignoring comments
def clean_code_and_ignore_comments(file_path):
    cleaned_code = []
    inside_multiline_comment = False

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            # Handle Python multiline comments (triple quotes)
            if '"""' in line or "'''" in line:
                if inside_multiline_comment:
                    inside_multiline_comment = False
                    continue
                else:
                    inside_multiline_comment = True
                    continue

            if inside_multiline_comment:
                continue

            # Handle single-line comments and clean the line
            if "#" in line:
                line = line.split("#", 1)[0].strip()

            cleaned_line = clean_line(line)

            if cleaned_line:  # Only add non-empty lines after cleaning
                cleaned_code.append(cleaned_line)

        # Print cleaned-up code
        print("\n--- Cleaned Up Code (Comments Ignored) ---")
        for line in cleaned_code:
            print(line)

        return cleaned_code

    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Unable to read the file.")

# Process Python file only
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

# Display token table for Python
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

# Function to display total tokens for Python
def display_total_tokens(total_count):
    print(f"Total tokens (excluding comments) for PYTHON: {total_count}")

# Main function
if __name__ == "__main__":
    file_path = "test.txt"  # You can change this to the path of your file
    cleaned_code = clean_code_and_ignore_comments(file_path)
    python_categorized, python_total = process_file(file_path)
    display_table(python_categorized, python_total)
    display_total_tokens(python_total)


