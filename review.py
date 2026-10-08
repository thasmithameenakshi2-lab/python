import ast
import re


# ==========================================
# AI-POWERED CODE REVIEW ASSISTANT
# ==========================================

def check_syntax(code):
    try:
        tree = ast.parse(code)
        return tree, None

    except SyntaxError as error:
        return None, error


# ==========================================
# CODE ANALYSIS
# ==========================================

def review_code(code):

    issues = []
    suggestions = []

    tree, error = check_syntax(code)

    # --------------------------------------
    # Syntax Check
    # --------------------------------------

    if error:

        issues.append(
            "Syntax Error - Line "
            + str(error.lineno)
            + ": "
            + error.msg
        )

        suggestions.append(
            "Correct the syntax error before running the program."
        )

        return issues, suggestions

    # --------------------------------------
    # AST Analysis
    # --------------------------------------

    for node in ast.walk(tree):

        # Bare except
        if isinstance(node, ast.ExceptHandler):

            if node.type is None:

                issues.append(
                    "Line "
                    + str(node.lineno)
                    + ": Bare except detected."
                )

                suggestions.append(
                    "Use a specific exception type such as "
                    "ValueError or ZeroDivisionError."
                )

        # Empty exception handler
        if isinstance(node, ast.ExceptHandler):

            if len(node.body) == 1:

                if isinstance(node.body[0], ast.Pass):

                    issues.append(
                        "Line "
                        + str(node.lineno)
                        + ": Empty exception handler."
                    )

                    suggestions.append(
                        "Handle the exception properly instead of using pass."
                    )

        # Global variable
        if isinstance(node, ast.Global):

            issues.append(
                "Line "
                + str(node.lineno)
                + ": Global variable detected."
            )

            suggestions.append(
                "Avoid unnecessary global variables."
            )

        # Nested loops
        if isinstance(node, (ast.For, ast.While)):

            for child in ast.walk(node):

                if child is node:
                    continue

                if isinstance(child, (ast.For, ast.While)):

                    issues.append(
                        "Line "
                        + str(node.lineno)
                        + ": Nested loop detected."
                    )

                    suggestions.append(
                        "Consider optimizing nested loops "
                        "for better performance."
                    )

                    break

    # --------------------------------------
    # Line Analysis
    # --------------------------------------

    lines = code.splitlines()

    for number, line in enumerate(lines, start=1):

        # Long line
        if len(line) > 100:

            issues.append(
                "Line "
                + str(number)
                + ": Line is longer than 100 characters."
            )

            suggestions.append(
                "Break long lines into smaller lines."
            )

        # TODO
        if "TODO" in line.upper():

            issues.append(
                "Line "
                + str(number)
                + ": TODO comment found."
            )

            suggestions.append(
                "Complete or remove the TODO item."
            )

        # Hardcoded password
        password_pattern = re.compile(
            r"(password|passwd|pwd)"
            r"\s*=\s*[\"'][^\"']+[\"']",
            re.IGNORECASE
        )

        if password_pattern.search(line):

            issues.append(
                "Line "
                + str(number)
                + ": Possible hardcoded password."
            )

            suggestions.append(
                "Do not store passwords directly in source code."
            )

        # SQL injection
        if "SELECT" in line.upper() and "+" in line:

            issues.append(
                "Line "
                + str(number)
                + ": Possible SQL injection risk."
            )

            suggestions.append(
                "Use parameterized SQL queries."
            )

    # --------------------------------------
    # General Suggestions
    # --------------------------------------

    if "input(" in code:

        suggestions.append(
            "Validate user input before processing it."
        )

    if "print(" in code:

        suggestions.append(
            "For larger applications, consider using logging "
            "instead of print()."
        )

    if len(lines) > 20 and "def " not in code:

        suggestions.append(
            "Divide large code into functions "
            "for better maintainability."
        )

    # --------------------------------------
    # Final Result
    # --------------------------------------

    if not issues:

        issues.append(
            "No major issues detected."
        )

    if not suggestions:

        suggestions.append(
            "Code looks good. Continue following clean-code practices."
        )

    return issues, suggestions


# ==========================================
# COMPLEXITY
# ==========================================

def calculate_complexity(code):

    try:
        tree = ast.parse(code)

    except SyntaxError:
        return 0

    complexity = 1

    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.If,
                ast.For,
                ast.While,
                ast.Try
            )
        ):

            complexity += 1

    return complexity


# ==========================================
# DISPLAY REVIEW
# ==========================================

def display_review(code):

    print("\n==========================================")
    print("   AI-POWERED CODE REVIEW ASSISTANT")
    print("==========================================")

    issues, suggestions = review_code(code)

    complexity = calculate_complexity(code)

    print("\n--- ISSUES FOUND ---")

    for issue in issues:

        if "No major issues" in issue:
            print("[OK] " + issue)
        else:
            print("[WARNING] " + issue)

    print("\n--- SUGGESTIONS ---")

    for suggestion in suggestions:

        print("[TIP] " + suggestion)

    print("\n--- CODE STATISTICS ---")

    print("Number of lines :", len(code.splitlines()))
    print("Complexity      :", complexity)

    print("\n==========================================")
    print("          REVIEW COMPLETED")
    print("==========================================")


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("\nAI-Powered Code Review Assistant")
    print("--------------------------------")

    print("\nPaste your Python code below.")
    print("Type END on a new line when finished.\n")

    code_lines = []

    while True:

        line = input()

        if line == "END":
            break

        code_lines.append(line)

    code = "\n".join(code_lines)

    if not code.strip():

        print("\nNo code entered.")
        return

    display_review(code)


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":
    main()
