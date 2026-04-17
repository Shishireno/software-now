from pathlib import Path


# Convert input string into tokens (numbers, operators, brackets)
def tokenize(expr):
    tokens, i = [], 0
    while i < len(expr):
        ch = expr[i]

        # Ignore spaces
        if ch.isspace():
            i += 1

        # Handle numbers (including decimals)
        elif ch.isdigit() or ch == ".":
            start = i
            while i < len(expr) and (expr[i].isdigit() or expr[i] == "."):
                i += 1
            text = expr[start:i]

            # Check for invalid number format
            if text == "." or text.count(".") > 1:
                raise ValueError("Invalid number literal")

            tokens.append(("NUM", text))

        # Handle operators
        elif ch in "+-*/":
            tokens.append(("OP", ch))
            i += 1

        # Handle parentheses
        elif ch == "(":
            tokens.append(("LPAREN", ch))
            i += 1
        elif ch == ")":
            tokens.append(("RPAREN", ch))
            i += 1

        # Invalid character
        else:
            raise ValueError(f"Invalid character: {ch}")

    # Add END token to mark end of input
    return tokens + [("END", "")]


# Convert tokens into required output format
def format_tokens(tokens):
    return " ".join("[END]" if t == "END" else f"[{t}:{v}]" for t, v in tokens)


# Convert string number into int or float
def parse_number(text):
    return float(text) if "." in text else int(text)


# Get current token without moving forward
def current(state):
    return state["tokens"][state["index"]]


# Move to next token and return current one
def advance(state):
    tok = current(state)
    state["index"] += 1
    return tok


# Check if current token matches expected type/value
def match(state, kind, value=None):
    tok = current(state)
    return tok[0] == kind and (value is None or tok[1] == value)


# Check for implicit multiplication (e.g., 2(3+4))
def starts_factor(tok):
    return tok[0] in {"NUM", "LPAREN"}


# Parse addition and subtraction (lowest precedence)
def parse_expression(state):
    node = parse_term(state)
    while match(state, "OP", "+") or match(state, "OP", "-"):
        op = advance(state)[1]
        node = ("bin", op, node, parse_term(state))
    return node


# Parse multiplication, division, and implicit multiplication
def parse_term(state):
    node = parse_unary(state)
    while True:
        if match(state, "OP", "*") or match(state, "OP", "/"):
            op = advance(state)[1]
            node = ("bin", op, node, parse_unary(state))
        elif starts_factor(current(state)):  # implicit multiplication
            node = ("bin", "*", node, parse_unary(state))
        else:
            return node


# Handle unary minus (e.g., -5)
def parse_unary(state):
    if match(state, "OP", "-"):
        advance(state)
        return ("neg", parse_unary(state))

    # Unary plus is not allowed
    if match(state, "OP", "+"):
        raise ValueError("Unary plus is not supported")

    return parse_primary(state)


# Parse numbers and bracket expressions
def parse_primary(state):
    if match(state, "NUM"):
        return ("num", parse_number(advance(state)[1]))

    if match(state, "LPAREN"):
        advance(state)
        node = parse_expression(state)

        # Ensure closing bracket exists
        if not match(state, "RPAREN"):
            raise ValueError("Missing closing parenthesis")

        advance(state)
        return node

    raise ValueError("Expected a number or (")


# Build parse tree and ensure all tokens are used
def parse_tokens(tokens):
    state = {"tokens": tokens, "index": 0}
    tree = parse_expression(state)

    if not match(state, "END"):
        raise ValueError("Unexpected token after complete expression")

    return tree


# Format numbers nicely (remove .0 if integer)
def format_tree_number(value):
    return str(int(value)) if isinstance(value, float) and value.is_integer() else str(value)


# Convert parse tree into readable format
def format_tree(node):
    if node[0] == "num":
        return format_tree_number(node[1])

    if node[0] == "neg":
        return f"(neg {format_tree(node[1])})"

    _, op, left, right = node
    return f"({op} {format_tree(left)} {format_tree(right)})"


# Evaluate parse tree recursively
def evaluate_tree(node):
    if node[0] == "num":
        return float(node[1])

    if node[0] == "neg":
        return -evaluate_tree(node[1])

    _, op, left, right = node
    a, b = evaluate_tree(left), evaluate_tree(right)

    # Perform operation
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b

    raise ValueError("Unknown operator")


# Format final result for output
def format_result(value):
    return str(int(value)) if float(value).is_integer() else f"{value:.4f}"


# Process one expression (tokenize → parse → evaluate)
def process_expression(expr):
    try:
        tokens = tokenize(expr)
        token_str = format_tokens(tokens)
        tree = parse_tokens(tokens)
        tree_str = format_tree(tree)
        result = evaluate_tree(tree)

        return {"input": expr, "tree": tree_str, "tokens": token_str, "result": result}

    # Handle errors at any stage
    except Exception:
        try:
            return {"input": expr, "tree": "ERROR", "tokens": token_str, "result": "ERROR"}
        except UnboundLocalError:
            return {"input": expr, "tree": "ERROR", "tokens": "ERROR", "result": "ERROR"}


# Write results into output.txt
def write_output_file(path, results):
    with open(path, "w", encoding="utf-8") as f:
        for i, item in enumerate(results):
            f.write(f"Input: {item['input']}\n")
            f.write(f"Tree: {item['tree']}\n")
            f.write(f"Tokens: {item['tokens']}\n")

            # Show formatted result or ERROR
            f.write(f"Result: {'ERROR' if item['result'] == 'ERROR' else format_result(item['result'])}\n")

            if i < len(results) - 1:
                f.write("\n")


# Read input file, process all expressions, and generate output
def evaluate_file(input_path: str) -> list[dict]:
    input_file = Path(input_path)
    output_file = input_file.parent / "output.txt"

    with open(input_file, "r", encoding="utf-8") as f:
        expressions = [line.rstrip("\n") for line in f]

    results = [process_expression(expr) for expr in expressions]
    write_output_file(output_file, results)
    return results


# Program entry point
if __name__ == "__main__":
    evaluate_file("sample_input.txt")
    print("Output file generated successfully!")