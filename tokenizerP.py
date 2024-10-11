from tabulate import tabulate


PYTHON_KEYWORDS = {"if", "else", "while", "for", "def", "return", "class", "try", "except", "import"}
PYTHON_OPERATORS = {"+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "and", "or", "not"}
PYTHON_PUNCTUATORS = {",", ":", ";", "(", ")", "{", "}", "[", "]"}


CPP_KEYWORDS = {"int", "return", "if", "else", "for", "while", "do", "switch", "case", "break", "continue",
               "class", "public", "private", "protected", "virtual", "new", "delete", "using", "namespace", "#", "include", "iostream"}
CPP_OPERATORS = {"+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "!", "&", "|", "++", "--", "->", ".", "<<", ">>"}
CPP_PUNCTUATORS = {",", ":", ";", "(", ")", "{", "}", "[", "]", "<", ">", "#", "<<"}


def is_identifier(token):
   return token.isidentifier()


def is_literal(token):
   # Treat comments as literals
   if token.startswith("#") and token.startswith("#include ") or token.startswith("//"):
       return True
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


def tokenize_line(line, keywords, operators, punctuators, literals):
    tokens = []
    token = ""
    inside_string = False  # This flag will help us track if we're inside a string

    # Handle comments and add them to literals before cleaning the line
    if "#" in line and not line.strip().startswith("#include"):
        comment_part = line.split("#", 1)[1].strip()
        literals.append(f"#{comment_part}")  # Add comment as a literal
        line = line.split("#", 1)[0]  # Remove the comment part from the actual line

    if "//" in line:
        comment_part = line.split("//", 1)[1].strip()
        literals.append(f"//{comment_part}")  # Add comment as a literal
        line = line.split("//", 1)[0]  # Remove the comment part from the actual line

    line = clean_line(line)

    i = 0
    while i < len(line):
        char = line[i]

        # Check for string literals
        if char in ('"', "'"):  # Detect both single and double quotes
            if inside_string:
                # If we are already inside a string and encounter the same quote, we end the string
                token += char
                tokens.append(token.strip())  # Add the entire string as one token
                token = ""
                inside_string = False
            else:
                # If we're not inside a string and encounter a quote, we start the string
                if token:
                    tokens.append(token.strip())  # Add any completed token before starting the string
                    token = ""
                token += char  # Add the starting quote to the token
                inside_string = True
        elif inside_string:
            # If we're inside a string, keep adding characters until we find the closing quote
            token += char
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

def categorize_tokens(tokens, keywords, operators, punctuators, literals):
   categorized = {
       "Keywords": [],  # Changed to list to allow duplicates
       "Identifiers": [],  # Changed to list to allow duplicates
       "Literals": literals,  # Keep the literals from earlier (includes comments)
       "Operators": [],
       "Punctuators": []
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
           categorized["Literals"].append(token)  # Add non-comment literals
           if not (token.startswith("#") or token.startswith("//")):
               total_token_count += 1
       elif is_identifier(token):
           categorized["Identifiers"].append(token)
           total_token_count += 1


   return categorized, total_token_count


def detect_language(line):
   if "def" in line or "if __name__" in line or "print(" in line:
       return "python"
   elif "#include" in line or "int main()" in line or "cout" in line:
       return "cpp"
   return None

def clean_code_and_ignore_comments(file_path, language="python"):
    cleaned_code = []
    inside_multiline_comment = False  # Track whether we are inside a multiline comment

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            # Handle multiline comments for Python (triple quotes) or C++ (/* ... */)
            if language == "python":
                if '"""' in line or "'''" in line:
                    if inside_multiline_comment:
                        # If we were inside a multiline comment, end it and skip this line
                        inside_multiline_comment = False
                        continue
                    else:
                        # Start of a multiline comment
                        inside_multiline_comment = True
                        continue
            elif language == "cpp":
                if "/*" in line:
                    inside_multiline_comment = True
                if "*/" in line:
                    inside_multiline_comment = False
                    continue  # Skip the line with the end of the comment

            # If we're inside a multiline comment, skip the line
            if inside_multiline_comment:
                continue

            # Handle single-line comments and clean the line
            if "#" in line and not line.strip().startswith("#include") and language == "python":
                line = line.split("#", 1)[0].strip()
            if "//" in line and language == "cpp":
                line = line.split("//", 1)[0].strip()

            cleaned_line = clean_line(line)  # Use the clean_line function to clean spaces

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





def process_file(file_path):
   python_code = []
   cpp_code = []
   python_tokens = []
   cpp_tokens = []
   python_literals = []
   cpp_literals = []
   language = None


   try:
       with open(file_path, 'r') as file:
           lines = file.readlines()


       # Separate Python and C++ code and add comments to literals before cleaning them
       for line in lines:
           cleaned_line = clean_line(line)
           detected_language = detect_language(line)


           if detected_language:
               language = detected_language


           if language == "python":
               python_code.append(cleaned_line)
               python_tokens.extend(tokenize_line(line, PYTHON_KEYWORDS, PYTHON_OPERATORS, PYTHON_PUNCTUATORS, python_literals))
           elif language == "cpp":
               cpp_code.append(cleaned_line)
               cpp_tokens.extend(tokenize_line(line, CPP_KEYWORDS, CPP_OPERATORS, CPP_PUNCTUATORS, cpp_literals))


       # Print cleaned up code
       print("\n--- Original Code in File ---")
       if python_code:
           print("\nPython:\n" + "\n".join(python_code))
       if cpp_code:
           print("\nC++:\n" + "\n".join(cpp_code))


       python_categorized, python_total = categorize_tokens(python_tokens, PYTHON_KEYWORDS, PYTHON_OPERATORS, PYTHON_PUNCTUATORS, python_literals)
       cpp_categorized, cpp_total = categorize_tokens(cpp_tokens, CPP_KEYWORDS, CPP_OPERATORS, CPP_PUNCTUATORS, cpp_literals)


       return python_categorized, python_total, cpp_categorized, cpp_total


   except FileNotFoundError:
       print("File was not found.")
   except IOError:
       print("Not able to read the file.")


def display_table(categorized_tokens, total_count, language):
   print(f"Tokens for {language.upper()}:")
   categorized = [
       ["Keywords", ", ".join(categorized_tokens["Keywords"])],
       ["Identifiers", ", ".join(categorized_tokens["Identifiers"])],
       ["Literals (Comments Included)", ", ".join(categorized_tokens["Literals"])],  # Comments as literals
       ["Operators", ", ".join(categorized_tokens["Operators"])],
       ["Punctuators", ", ".join(categorized_tokens["Punctuators"])],
       ["Total Tokens (excluding comments)", total_count]
   ]


   headers = ["Category", "Tokens"]
   table = tabulate(categorized, headers, tablefmt="fancy_grid")
   print(table)


def display_total_tokens(total_count, language):
   print(f"Total tokens (excluding comments) for {language.upper()}: {total_count}")