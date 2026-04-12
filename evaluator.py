from pathlib import Path


# This function converts one input expression string into a list of tokens.
# It recognises numbers, operators, parentheses, and the END token.
# If it finds any invalid character, it raises an error immediately.
def tokenize(expression):
    tokens = []
    i = 0

    while i < len(expression):
        ch = expression[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit() or ch == ".":
            start = i
            dot_count = 0

            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                if expression[i] == ".":
                    dot_count += 1
                i += 1

            number_text = expression[start:i]

            if dot_count > 1 or number_text == ".":
                raise ValueError("Invalid number literal")

            tokens.append(("NUM", number_text))
            continue

        if ch in "+-*/":
            tokens.append(("OP", ch))
            i += 1
            continue

        if ch == "(":
            tokens.append(("LPAREN", ch))
            i += 1
            continue

        if ch == ")":
            tokens.append(("RPAREN", ch))
            i += 1
            continue

        raise ValueError(f"Invalid character: {ch}")

    tokens.append(("END", ""))
    return tokens


# This function converts the token list into the exact text format
# required for the Tokens line in output.txt.
def format_tokens(tokens):
    parts = []

    for token_type, token_value in tokens:
        if token_type == "END":
            parts.append("[END]")
        else:
            parts.append(f"[{token_type}:{token_value}]")

    return " ".join(parts)


# This function converts the text of a number token into an int or float
# so that calculations can be done correctly.
def parse_number_text(number_text):
    if "." in number_text:
        return float(number_text)
    return int(number_text)


# This function returns the current token without moving forward.
def current_token(state):
    return state["tokens"][state["index"]]


# This function returns the current token and then moves to the next token.
def advance(state):
    token = state["tokens"][state["index"]]
    state["index"] += 1
    return token


# This function checks whether the current token matches a required type
# and optional value.
def match_token(state, token_type, token_value=None):
    token = current_token(state)

    if token[0] != token_type:
        return False

    if token_value is not None and token[1] != token_value:
        return False

    return True


# This function checks whether a token can begin a factor that allows
# implicit multiplication, such as 2(3+4).
def token_starts_implicit_factor(token):
    token_type, _ = token
    return token_type in {"NUM", "LPAREN"}


# This function parses the lowest-precedence level of the grammar.
# It handles addition and subtraction from left to right.
def parse_expression(state):
    node = parse_term(state)

    while match_token(state, "OP", "+") or match_token(state, "OP", "-"):
        operator = advance(state)[1]
        right = parse_term(state)
        node = ("bin", operator, node, right)

    return node


# This function parses the medium-precedence level of the grammar.
# It handles multiplication, division, and implicit multiplication.
def parse_term(state):
    node = parse_unary(state)

    while True:
        if match_token(state, "OP", "*") or match_token(state, "OP", "/"):
            operator = advance(state)[1]
            right = parse_unary(state)
            node = ("bin", operator, node, right)
            continue

        if token_starts_implicit_factor(current_token(state)):
            right = parse_unary(state)
            node = ("bin", "*", node, right)
            continue

        break

    return node


# This function parses unary negation such as -5, --5, or -(3+4).
# Unary plus is not allowed, so it raises an error if unary + is found.
def parse_unary(state):
    if match_token(state, "OP", "-"):
        advance(state)
        operand = parse_unary(state)
        return ("neg", operand)

    if match_token(state, "OP", "+"):
        raise ValueError("Unary plus is not supported")

    return parse_primary(state)


# This function parses the highest-precedence basic values.
# It handles number literals and parenthesised expressions.
def parse_primary(state):
    if match_token(state, "NUM"):
        number_text = advance(state)[1]
        return ("num", parse_number_text(number_text))

    if match_token(state, "LPAREN"):
        advance(state)
        node = parse_expression(state)

        if not match_token(state, "RPAREN"):
            raise ValueError("Missing closing parenthesis")

        advance(state)
        return node

    raise ValueError("Expected a number or (")


# This function parses a full token list into a parse tree and checks
# that no extra tokens remain after parsing is finished.
def parse_tokens(tokens):
    state = {"tokens": tokens, "index": 0}
    tree = parse_expression(state)

    if not match_token(state, "END"):
        raise ValueError("Unexpected token after complete expression")

    return tree


# This function formats a number for tree display.
# Whole numbers are shown without .0.
def format_tree_number(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


# This function converts the internal parse tree structure into the

def format_tree(node):
    node_type = node[0]

    if node_type == "num":
        return format_tree_number(node[1])

    if node_type == "neg":
        return f"(neg {format_tree(node[1])})"

    operator = node[1]
    left = format_tree(node[2])
    right = format_tree(node[3])
    return f"({operator} {left} {right})"


# This function evaluates the parse tree recursively.
# If division by zero occurs, it raises an error.
def evaluate_tree(node):
    node_type = node[0]

    if node_type == "num":
        return float(node[1])

    if node_type == "neg":
        return -evaluate_tree(node[1])

    operator = node[1]
    left_value = evaluate_tree(node[2])
    right_value = evaluate_tree(node[3])

    if operator == "+":
        return left_value + right_value

    if operator == "-":
        return left_value - right_value

    if operator == "*":
        return left_value * right_value

    if operator == "/":
        if right_value == 0:
            raise ZeroDivisionError("Division by zero")
        return left_value / right_value

    raise ValueError("Unknown operator")


# This function formats the final numeric result for output.
# Whole numbers are shown as integers, otherwise values are rounded
# to 4 decimal places.
def format_result_for_output(value):
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.4f}"


# This function processes one expression and returns the required
# dictionary containing input, tree, tokens, and result.
def process_expression(expression):
    try:
        tokens = tokenize(expression)
        token_string = format_tokens(tokens)
    except Exception:
        return {
            "input": expression,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }

    try:
        tree = parse_tokens(tokens)
        tree_string = format_tree(tree)
    except Exception:
        return {
            "input": expression,
            "tree": "ERROR",
            "tokens": token_string,
            "result": "ERROR"
        }

    try:
        result_value = evaluate_tree(tree)
        return {
            "input": expression,
            "tree": tree_string,
            "tokens": token_string,
            "result": result_value
        }
    except Exception:
        return {
            "input": expression,
            "tree": tree_string,
            "tokens": token_string,
            "result": "ERROR"
        }


# This function writes all processed expression results into output.txt

def write_output_file(output_path, results):
    with open(output_path, "w", encoding="utf-8") as file:
        for index, item in enumerate(results):
            file.write(f"Input: {item['input']}\n")
            file.write(f"Tree: {item['tree']}\n")
            file.write(f"Tokens: {item['tokens']}\n")

            if item["result"] == "ERROR":
                result_text = "ERROR"
            else:
                result_text = format_result_for_output(item["result"])

            file.write(f"Result: {result_text}\n")

            if index != len(results) - 1:
                file.write("\n")


# This function reads expressions from the input file, writes output.txt
# in the same directory, and returns a list of result dictionaries.
def evaluate_file(input_path: str) -> list[dict]:
    input_file = Path(input_path)
    output_file = input_file.parent / "output.txt"

    with open(input_file, "r", encoding="utf-8") as file:
        expressions = [line.rstrip("\n") for line in file]

    results = [process_expression(expression) for expression in expressions]
    write_output_file(output_file, results)
    return results

if __name__ == "__main__":
    evaluate_file("sample_input.txt")
    print("Output file generated successfully!")