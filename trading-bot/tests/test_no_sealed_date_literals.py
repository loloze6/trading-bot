"""
No executable production date may fall inside the sealed holdout — FORK-ONLY.

Threat model, measured not theoretical: a hardcoded window in production code
that reaches into holdout_range. `launcher.py`'s `visualize_data` ended
'2026-04-23' with localStorage=True and a 60-second interval — roughly 500k
sealed 1m bars fetched and written to disk per run, and the mode reported only
"Data visualization failed" afterwards. Nothing in the runtime could have caught
it, because the fetch was exactly what the code asked for.

Only STRING literals are scanned (plus the two committed config JSONs): a date
can reach a fetcher only through a string, never through bare code — while
comments and docstrings are prose, and legitimately name sealed dates when
documenting incidents (upstream's FetchGapError docstring does exactly that,
which is how the first draft of this test — a raw text scan — was found firing
on the clean tree it exists to protect). Docstrings are excluded by AST
position, not by guesswork.

Scope is deliberately narrow. Test files are excluded: fixtures legitimately
simulate sealed-era timestamps to prove the guards fire. Markdown and prose are
excluded: the seal cannot be documented without naming it. Configs generated at
runtime by an LLM cannot be scanned statically at all — that is the campaign
gate's job, not this file's.

The seal moves with the policy: `holdout_range` is read, never assumed, so a
literal that becomes sealed by a policy change fails on the same commit that
changes it.
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


def test_no_executable_production_date_falls_inside_the_seal():
    with open(_POLICY) as fh:
        lo, hi = [datetime.date.fromisoformat(d)
                  for d in yaml.safe_load(fh)["holdout_range"]]   # hi is INCLUSIVE

    violations = []

    def record(path, lineno, literal):
        try:
            found = datetime.date.fromisoformat(literal)
        except ValueError:
            return
        if lo <= found <= hi:
            violations.append(f"{path.relative_to(PROJECT_ROOT)}:{lineno}: {literal}")

    for path in sorted(PROJECT_ROOT.rglob("*.py")):
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        for lineno, literal in _code_string_dates(path):
            record(path, lineno, literal)

    for path in (PROJECT_ROOT / "config.json", PROJECT_ROOT / "strategy_config.json"):
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            for literal in ISO_DATE.findall(line):
                record(path, lineno, literal)

    assert not violations, (
        f"executable date literal(s) inside the sealed holdout {lo}..{hi} "
        f"(strategy-research/config/campaign_data_policy.yaml). Reading sealed "
        f"data spends it permanently:\n  " + "\n  ".join(violations))
