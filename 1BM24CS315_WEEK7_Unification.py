import re


def is_variable(x):
    return isinstance(x, str) and len(x) > 0 and x[0].islower()


def apply_substitution(expr, subst):
    """Apply existing substitutions recursively."""
    if is_variable(expr):
        if expr in subst:
            return apply_substitution(subst[expr], subst)
        return expr
    if isinstance(expr, tuple):
        return tuple(apply_substitution(arg, subst) for arg in expr)
    return expr


def occurs_check(variable, expr, subst):
    """Check whether variable occurs inside expression."""
    expr = apply_substitution(expr, subst)
    if variable == expr:
        return True
    if isinstance(expr, tuple):
        return any(occurs_check(variable, arg, subst) for arg in expr)
    return False


def unify_variable(var, expr, subst):
    if var in subst:
        return unify(subst[var], expr, subst)
    if is_variable(expr) and expr in subst:
        return unify(var, subst[expr], subst)
    if occurs_check(var, expr, subst):
        return None
    subst[var] = expr
    return subst


def unify(x, y, subst=None):
    if subst is None:
        subst = {}

    x = apply_substitution(x, subst)
    y = apply_substitution(y, subst)

    if x == y:
        return subst
    if is_variable(x):
        return unify_variable(x, y, subst)
    if is_variable(y):
        return unify_variable(y, x, subst)
    if isinstance(x, tuple) and isinstance(y, tuple):
        if len(x) != len(y) or x[0] != y[0]:
            return None
        for a, b in zip(x[1:], y[1:]):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    return None


def parse(text):
    """Parse text like Knows(x, FatherOf(y)) into nested tuples."""
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|[(),]", text)
    pos = 0

    def term():
        nonlocal pos
        name = tokens[pos]
        pos += 1
        if name in "(),":
            raise ValueError(f"Unexpected '{name}'")
        if pos < len(tokens) and tokens[pos] == "(":
            pos += 1
            args = [term()]
            while tokens[pos] == ",":
                pos += 1
                args.append(term())
            if tokens[pos] != ")":
                raise ValueError("Expected ')'")
            pos += 1
            return (name, *args)
        return name

    try:
        result = term()
    except IndexError:
        raise ValueError("Incomplete expression")
    if pos != len(tokens):
        raise ValueError("Extra characters after expression")
    return result


# Main program
print("Enter expressions like: Knows(x, FatherOf(y))")
print("Variables start with a lowercase letter; constants/predicates with uppercase.\n")

while True:
    try:
        expr1 = parse(input("Expression 1: ").strip())
        expr2 = parse(input("Expression 2: ").strip())
    except ValueError as e:
        print("Invalid input:", e, "\n")
        continue

    result = unify(expr1, expr2)

    if result is None:
        print("Unification Failed")
    else:
        print("Unification Successful")
        print("MGU:", result)
        print("Final Expression 1:", apply_substitution(expr1, result))
        print("Final Expression 2:", apply_substitution(expr2, result))

    if input("\nTry another? (y/n): ").strip().lower() != "y":
        break
    print()