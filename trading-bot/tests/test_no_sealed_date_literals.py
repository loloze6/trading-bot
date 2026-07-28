"""
No executable production date may sit at or beyond the sealed holdout — FORK-ONLY.

Threat model, measured not theoretical: a hardcoded window in production code
that reaches into holdout_range. `launcher.py`'s `visualize_data` ended
'2026-04-23' with localStorage=True and a 60-second interval — roughly 500k
sealed 1m bars fetched and written to disk per run, and the mode reported only
"Data visualization failed" afterwards. Nothing in the runtime could have caught
it, because the fetch was exactly what the code asked for.

The rule is "at or beyond the seal's START", not "inside the seal": a window
bound past the seal's end still fetches straight through the seal on its way
there. That straddle shape is the one that actually contaminated seven Binance
caches (last rows 2026-07-05 — both window literals outside the seal, the span
crossing it).

Only STRING literals are scanned (plus the two committed config JSONs): a
hardcoded window is a string, while comments and docstrings are prose and
legitimately name sealed dates when documenting incidents (upstream's
FetchGapError docstring does exactly that, which is how the first draft of this
test — a raw text scan — was found firing on the clean tree it exists to
protect). Docstrings are excluded by AST position, not by guesswork.

This is a filter for that incident shape, not a proof: a date built by code —
`datetime.date(2026, 4, 23)`, string concatenation, timestamp arithmetic,
`datetime.now()` drift — passes it, as does anything generated at runtime.
Those are the runtime/campaign gate's job (`strategy-research/tools/
holdout_date_gate.sh` is the deny-by-default whole-index scanner; wiring it
into the installed pre-commit hook is tracked separately). Test files are
excluded because fixtures legitimately simulate sealed-era timestamps to prove
the guards fire; markdown and prose are excluded because the seal cannot be
documented without naming it.

The seal moves with the policy: `holdout_range` is read, never assumed, so a
literal that becomes unsafe under a policy change fails on the same commit
that changes it.
"""
import ast
import datetime
import io
import re
import tokenize
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
_POLICY = PROJECT_ROOT.parent / "strategy-research" / "config" / "campaign_data_policy.yaml"

EXCLUDED_PARTS = ("tests", "venv", ".venv", "__pycache__", "results", "local_data")
# Positive control: the scan must at least reach the file where the incident
# lived. Guards against the exclusion filter (or a surprising checkout layout)
# silently emptying the scan — a seal check that examines nothing reports green.
SENTINEL = Path("core") / "launcher.py"
ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
_STRING_TOKENS = {tokenize.STRING, getattr(tokenize, "FSTRING_MIDDLE", tokenize.STRING)}


def _docstring_spans(source: str) -> list:
    """(first_line, last_line) of every docstring, located by AST position."""
    spans = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                spans.append((body[0].lineno, body[0].end_lineno))
    return spans


def _code_string_dates(path: Path):
    """Yield (lineno, literal) for ISO dates inside non-docstring string tokens."""
    source = path.read_text()
    docstrings = _docstring_spans(source)
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if tok.type not in _STRING_TOKENS:
            continue
        line = tok.start[0]
        if any(lo <= line <= hi for lo, hi in docstrings):
            continue
        for literal in ISO_DATE.findall(tok.string):
            yield line, literal


def test_no_executable_production_date_reaches_the_seal():
    with open(_POLICY) as fh:
        lo, hi = [datetime.date.fromisoformat(d)
                  for d in yaml.safe_load(fh)["holdout_range"]]   # hi is INCLUSIVE

    violations = []

    def record(rel, lineno, literal):
        try:
            found = datetime.date.fromisoformat(literal)
        except ValueError:
            return
        if found >= lo:
            violations.append(f"{rel}:{lineno}: {literal}")

    scanned = set()
    for path in sorted(PROJECT_ROOT.rglob("*.py")):
        rel = path.relative_to(PROJECT_ROOT)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        scanned.add(rel)
        for lineno, literal in _code_string_dates(path):
            record(rel, lineno, literal)

    assert SENTINEL in scanned, (
        f"seal scan never reached {SENTINEL} — the exclusion filter or checkout "
        f"layout emptied the scan, so a green result would be vacuous "
        f"({len(scanned)} files scanned)")

    for path in (PROJECT_ROOT / "config.json", PROJECT_ROOT / "strategy_config.json"):
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            for literal in ISO_DATE.findall(line):
                record(path.relative_to(PROJECT_ROOT), lineno, literal)

    assert not violations, (
        f"executable date literal(s) at or beyond the sealed holdout's start "
        f"{lo} (seal {lo}..{hi}, strategy-research/config/"
        f"campaign_data_policy.yaml). A window bound at or past the seal pulls "
        f"sealed rows on the way there; reading sealed data spends it "
        f"permanently:\n  " + "\n  ".join(violations))
