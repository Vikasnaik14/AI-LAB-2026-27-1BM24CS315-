import itertools

def implies(a, b):
    return (not a) or b

def tf(x):
    return str(x).lower()

# Queries to check against the KB
queries = {
    'R':      lambda m: m['R'],
    'R -> P': lambda m: implies(m['R'], m['P']),
    'Q -> R': lambda m: implies(m['Q'], m['R']),
}

headers = ['P', 'Q', 'R', 'Q -> P', 'P -> ~Q', 'Q v R', 'KB'] + list(queries)

print("=== Truth Table: KB = {Q -> P, P -> ~Q, Q v R} ===")
header_str = " | ".join(f"{h:^8}" for h in headers)
print(header_str)
print("-" * (len(header_str) + 14))

kb_models = []
results = {name: [] for name in queries}   # query values over KB models

for values in itertools.product([False, True], repeat=3):
    m = dict(zip(['P', 'Q', 'R'], values))

    s1 = implies(m['Q'], m['P'])         # Q -> P
    s2 = implies(m['P'], not m['Q'])     # P -> ~Q
    s3 = m['Q'] or m['R']                # Q v R
    kb = s1 and s2 and s3

    q_vals = {name: fn(m) for name, fn in queries.items()}

    row = [m['P'], m['Q'], m['R'], s1, s2, s3, kb] + list(q_vals.values())
    row_str = " | ".join(f"{tf(v):^8}" for v in row)
    if kb:
        row_str += "  <-- KB model"
        kb_models.append(m)
        for name, v in q_vals.items():
            results[name].append((m, v))
    print(row_str)

print()
print(f"KB has {len(kb_models)} model(s). Verdicts (query must be true in ALL KB models):")
for name, vals in results.items():
    bad = [m for m, v in vals if not v]
    if not bad:
        print(f"  KB |= {name:<7} : YES")
    else:
        ce = ", ".join(f"{k}={tf(v)}" for k, v in bad[0].items())
        print(f"  KB |= {name:<7} : NO  (counterexample: {ce})")