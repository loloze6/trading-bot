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
crossing it). The rule is deliberately BROADER than that rationale: a literal
wholly after the seal (a post-2026-H1 analysis window whose start is also past
the seal) fires too, though such a window need not cross anything. Fail-closed
is the point — when a legitimately post-seal window is eventually hardcoded,
the exemption is a human edit here, not a cleverer scanner.

Only STRING literals are scanned (plus the two committed config JSONs): a
hardcoded window is a string, while comments and docstrings are prose and
legitimately name sealed dates when documenting incidents (upstream's
FetchGapError docstring does exactly that, which is how the first draft of this
test — a raw text scan — was found firing on the clean tree it exists to
protect). Docstrings are excluded by AST position, not by guesswork.

This is a filter for that incident shape, not a proof: a date built by code —
`datetime.date(2026, 4, 23)`, string concatenation, timestamp arithmetic,
`datetime.now()` drift — passes it, as does anything generated at runtime.
The notation matched is narrow too: only zero-padded, dash-separated
YYYY-MM-DD. Compact (`20260315`), slash-separated, dotted, and non-padded
forms are not caught (ticketed separately). Those are the runtime/campaign
gate's job (`strategy-research/tools/holdout_date_gate.sh` is the
deny-by-default whole-index scanner; wiring it into the installed pre-commit
hook is tracked separately). Test files are
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

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
_POLICY = PROJECT_ROOT.parent / "strategy-research" / "config" / "campaign_data_policy.yaml"

EXCLUDED_PARTS = ("tests", "venv", ".venv", "__pycache__", "results", "local_data")
# Positive control: the scan must at least reach the file where the incident
# lived. Guards against the exclusion filter (or a surprising checkout layout)
# silently emptying the scan — a seal check that examines nothing reports green.
SENTINEL = Path("core") / "launcher.py"
ISO_DATE = re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}")
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
    source = path.read_text(encoding="utf-8")
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
    with open(_POLICY, encoding="utf-8") as fh:
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
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for literal in ISO_DATE.findall(line):
                record(path.relative_to(PROJECT_ROOT), lineno, literal)

    assert not violations, (
        f"executable date literal(s) at or beyond the sealed holdout's start "
        f"{lo} (seal {lo}..{hi}, strategy-research/config/"
        f"campaign_data_policy.yaml). A window bound at or past the seal pulls "
        f"sealed rows on the way there; reading sealed data spends it "
        f"permanently:\n  " + "\n  ".join(violations))


@pytest.mark.parametrize(
    ("literal", "expected"),
    [
        ("2026-03-15", ["2026-03-15"]),
        ("2026-03-15T00:00:00", ["2026-03-15"]),
        ("2026-03-15T00:00:00Z", ["2026-03-15"]),
        ("run_2026-03-15T00:00:00", ["2026-03-15"]),
        ("BTCUSDT_2026-03-15_1h.csv", ["2026-03-15"]),
        ("12026-03-15", []),
    ],
)
def test_a_date_is_extracted_despite_adjacent_word_characters(tmp_path, literal, expected):
    """A word character (digit, letter, underscore) flanking the date on either
    side must not hide it — timestamps put 'T' after it, filename/run-id joins
    put '_' before and after it. A 5-digit year must still be refused."""
    fixture = tmp_path / "sample.py"
    fixture.write_text(f'end_date = "{literal}"\n', encoding="utf-8")
    extracted = [found for _, found in _code_string_dates(fixture)]
    assert extracted == expected, f"{literal!r} extracted {extracted}, expected {expected}"


def test_a_preseal_date_is_extracted_because_extraction_is_seal_blind(tmp_path):
    """Extraction doesn't know about the seal — record() does the lo comparison
    — so a plain pre-seal date must come out of extraction just like a sealed
    one; this isolates that property from any adjacent-word-character shape."""
    fixture = tmp_path / "sample.py"
    fixture.write_text('start_date = "2024-01-01"\n', encoding="utf-8")
    extracted = [found for _, found in _code_string_dates(fixture)]
    assert extracted == ["2024-01-01"]


def test_a_date_inside_an_fstring_literal_part_is_extracted(tmp_path):
    """FSTRING_MIDDLE (Python 3.12+ tokenizer) sits in _STRING_TOKENS alongside
    STRING — an f-string's literal text must be scanned too, not just plain
    string literals."""
    fixture = tmp_path / "sample.py"
    fixture.write_text('n = 1\nwindow_start = f"batch{n}: 2026-03-15"\n', encoding="utf-8")
    extracted = [found for _, found in _code_string_dates(fixture)]
    assert extracted == ["2026-03-15"]
