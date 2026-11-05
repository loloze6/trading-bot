"""Structural check of an ideas file. Code only, no AI. Exit 1 on any problem."""
import sys, yaml, pathlib

REQUIRED_IDEA = ["id", "belief", "claim", "why_no_lookahead", "how_it_trades"]
REQUIRED_CLAIM = ["when", "then", "compared_to", "measure", "pass_if"]

def check(path: pathlib.Path) -> list[str]:
    problems = []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "ideas" not in data:
        return [f"{path}: no 'ideas' key"]
    ideas = data["ideas"] or []
    if len(ideas) < 3:
        problems.append(f"{path}: only {len(ideas)} ideas")
    seen = set()
    for i, idea in enumerate(ideas):
        tag = f"{path.name} idea {i}"
        for k in REQUIRED_IDEA:
            if k not in idea or idea[k] in (None, ""):
                problems.append(f"{tag}: missing {k}")
        claim = idea.get("claim") or {}
        for k in REQUIRED_CLAIM:
            if k not in claim or claim[k] in (None, ""):
                problems.append(f"{tag}: claim missing {k}")
        pass_if = str(claim.get("pass_if", ""))
        if not any(ch.isdigit() for ch in pass_if):
            problems.append(f"{tag}: pass_if has no number")
        if "window" not in pass_if.lower():
            problems.append(f"{tag}: pass_if has no window consistency rule")
        if idea.get("id") in seen:
            problems.append(f"{tag}: duplicate id {idea.get('id')}")
        seen.add(idea.get("id"))
    return problems

if __name__ == "__main__":
    paths = [pathlib.Path(p) for p in sys.argv[1:]]
    all_problems = []
    for p in paths:
        probs = check(p)
        n = len((yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("ideas") or [])
        print(f"{p}: {n} ideas, {len(probs)} problems")
        all_problems += probs
    for pr in all_problems:
        print("  -", pr)
    sys.exit(1 if all_problems else 0)
