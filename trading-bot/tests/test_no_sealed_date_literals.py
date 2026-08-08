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
`datetime.now()` drift — passes it, as does anything generated at runtime; no
static string scan can catch a value that doesn't exist as a string until the
program runs. Six notations are now caught: dash-separated (zero-padded or
not), slash-separated, dotted, underscore-separated, compact
YYYY-MM-DD-with-no-separator, and compact-plus-time (a date immediately
followed by exactly 4 or 6 more digits — `202603150930` or
`20260315123456` — any other trailing digit count is a residual, see below).
Residuals that remain: a bare numeric literal (`end = 20260315` is a NUMBER
token, not a STRING — the JSON line-scan catches it because JSON has no
numeric-vs-string distinction at the text level, but the .py token scan only
looks at _STRING_TOKENS); mixed separators (`2026-03/15`); and day-first
European forms (`15-03-2026`), which this scanner has no way to distinguish
from a plausible YYYY-first date without a notation convention. The compact
patterns' digit-boundary guards also accept some fail-closed false positives
on purpose: a letter-flanked 8-, 12-, or 14-digit run inside a hex-ish
identifier, or a three-part CalVer string that happens to start at or past
2026, both extract as a date and both die at the seal check same as a real
one — a spurious failure that costs a manual look, not a silent miss. Those
residuals are the runtime/campaign gate's job
(`strategy-research/tools/holdout_date_gate.sh` is the deny-by-default
whole-index scanner; wiring it into the installed pre-commit hook is tracked
separately). Test files are excluded because fixtures legitimately simulate
sealed-era timestamps to prove the guards fire; markdown and prose are
excluded because the seal cannot be documented without naming it.

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
DATE_PATTERNS = (
    re.compile(r"(?<!\d)(\d{4})-(\d{1,2})-(\d{1,2})"),      # dash, non-padded ok
    re.compile(r"(?<!\d)(\d{4})/(\d{1,2})/(\d{1,2})"),      # slash
    re.compile(r"(?<!\d)(\d{4})\.(\d{1,2})\.(\d{1,2})"),    # dotted
    re.compile(r"(?<!\d)(\d{4})_(\d{1,2})_(\d{1,2})(?!\d)"),          # underscore — leading AND trailing guard
    re.compile(r"(?<!\d)(\d{4})(\d{2})(\d{2})(?!\d)"),                # compact — ONLY trailing guard
    re.compile(r"(?<!\d)(\d{4})(\d{2})(\d{2})(?:\d{6}|\d{4})(?!\d)"),  # compact + time, exactly 12 or 14 digits
)
_UNREADABLE_ERRORS = (OSError, UnicodeDecodeError, SyntaxError, tokenize.TokenError)
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


def _dates_in_text(text: str) -> list[str]:
    """Every date notation found in text, normalized to zero-padded
    YYYY-MM-DD, in pattern-major then left-to-right order. Seal-blind and
    validation-blind: an out-of-range calendar date is still returned, not
    filtered — that judgment belongs to _seal_violation. Not deduped."""
    dates = []
    for pattern in DATE_PATTERNS:
        for match in pattern.finditer(text):
            year, month, day = match.groups()
            dates.append(f"{year}-{int(month):02d}-{int(day):02d}")
    return dates


def _code_string_dates(path: Path):
    """Yield (lineno, literal) for dates inside non-docstring string tokens."""
    source = path.read_text(encoding="utf-8")
    docstrings = _docstring_spans(source)
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if tok.type not in _STRING_TOKENS:
            continue
        line = tok.start[0]
        if any(lo <= line <= hi for lo, hi in docstrings):
            continue
        for literal in _dates_in_text(tok.string):
            yield line, literal


def _config_json_dates(path: Path) -> list[tuple[int, str]]:
    """Line-scan a committed config JSON for dates in any notation."""
    dates = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for literal in _dates_in_text(line):
            dates.append((lineno, literal))
    return dates


def _seal_violation(rel: Path, lineno: int, literal: str, lo: datetime.date) -> str | None:
    try:
        found = datetime.date.fromisoformat(literal)
    except ValueError:
        return None
    return f"{rel}:{lineno}: {literal}" if found >= lo else None


def _scan_file(path: Path) -> tuple[list[tuple[int, str]] | None, str | None]:
    """(dates, None) on success, (None, reason) if the file could not be
    accessed, read, or tokenized — a caller must treat that as fail-closed,
    not skip."""
    try:
        return list(_code_string_dates(path)), None
    except _UNREADABLE_ERRORS as exc:
        return None, f"{type(exc).__name__}: {exc}"


def test_no_executable_production_date_reaches_the_seal():
    with open(_POLICY, encoding="utf-8") as fh:
        lo, hi = [datetime.date.fromisoformat(d)
                  for d in yaml.safe_load(fh)["holdout_range"]]   # hi is INCLUSIVE

    violations = []
    unreadable = []

    def record(rel, lineno, literal):
        violation = _seal_violation(rel, lineno, literal, lo)
        if violation is not None:
            violations.append(violation)

    scanned = set()
    for path in sorted(PROJECT_ROOT.rglob("*.py")):
        rel = path.relative_to(PROJECT_ROOT)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        dates, reason = _scan_file(path)
        if dates is None:
            unreadable.append(f"{rel}: {reason}")
            continue
        scanned.add(rel)
        for lineno, literal in dates:
            record(rel, lineno, literal)

    for path in (PROJECT_ROOT / "config.json", PROJECT_ROOT / "strategy_config.json"):
        rel = path.relative_to(PROJECT_ROOT)
        try:
            dates = _config_json_dates(path)
        except _UNREADABLE_ERRORS as exc:
            unreadable.append(f"{rel}: {type(exc).__name__}: {exc}")
            continue
        for lineno, literal in dates:
            record(rel, lineno, literal)

    assert SENTINEL in scanned, (
        f"seal scan never reached {SENTINEL} — the exclusion filter or checkout "
        f"layout emptied the scan, so a green result would be vacuous "
        f"({len(scanned)} files scanned)")

    assert not unreadable, (
        "file(s) could not be read or tokenized — failing closed instead of "
        "skipping them unseen:\n  " + "\n  ".join(unreadable))

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


@pytest.mark.parametrize(
    ("literal", "expected"),
    [
        ("20260315", ["2026-03-15"]),
        ("run_20260315_1h", ["2026-03-15"]),
        ("20260315T00", ["2026-03-15"]),
        ("2026/03/15", ["2026-03-15"]),
        ("2026/3/5", ["2026-03-05"]),
        ("2026.03.15", ["2026-03-15"]),
        ("2026-3-5", ["2026-03-05"]),
        ("2026_03_15", ["2026-03-15"]),
        ("2026_3_5", ["2026-03-05"]),
        ("202603150930", ["2026-03-15"]),
        ("20260315123456", ["2026-03-15"]),
    ],
)
def test_each_notation_is_extracted_and_normalized(literal, expected):
    assert _dates_in_text(literal) == expected


@pytest.mark.parametrize(
    "literal",
    ["202603159", "120260315", "20260315123"],
)
def test_an_eight_digit_run_flanked_by_digits_is_not_a_date(literal):
    """Neither compact pattern may match a digit run of the wrong length: 9
    digits is one too many for the bare 8-digit pattern, and 11 digits is
    between the 8-digit pattern and the 12/14-digit compact-plus-time
    pattern — none of the three patterns claims it."""
    assert _dates_in_text(literal) == []


def test_a_date_prefixing_a_longer_digit_run_is_still_caught():
    """The dash pattern's non-greedy day group stops at 2 digits, so it finds
    the leading date even when 6 more digits follow with no separator. The
    compact pattern then independently walks the same text and picks up the
    trailing 8-digit run as its own (invalid) date — extraction doesn't
    dedupe or coordinate between patterns."""
    assert _dates_in_text("2026-03-15123456") == ["2026-03-15", "1512-34-56"]


def test_an_invalid_calendar_date_is_extracted_but_never_a_violation():
    assert _dates_in_text("20261399") == ["2026-13-99"]
    lo = datetime.date(2026, 1, 1)
    assert _seal_violation(Path("x"), 1, "2026-13-99", lo) is None


def test_the_seal_boundary_is_inclusive():
    lo = datetime.date(2026, 1, 1)
    assert _seal_violation(Path("x"), 1, "2026-01-01", lo) is not None
    assert _seal_violation(Path("x"), 1, "2025-12-31", lo) is None


@pytest.mark.parametrize(
    ("name", "content", "error_type"),
    [
        ("invalid_utf8.py", b"x = '\xff\xfe'\n", "UnicodeDecodeError"),
        ("unterminated_string.py", b"x = 'abc\n", "SyntaxError"),
        ("null_byte.py", b"x = 'a\x00b'\n", "SyntaxError"),
    ],
)
def test_an_unreadable_file_is_reported_not_skipped(tmp_path, name, content, error_type):
    fixture = tmp_path / name
    fixture.write_bytes(content)
    dates, reason = _scan_file(fixture)
    assert dates is None
    assert reason is not None and reason.startswith(error_type), reason


def test_a_readable_file_scans_clean_through_scan_file(tmp_path):
    fixture = tmp_path / "sample.py"
    fixture.write_text('end_date = "2026-03-15"\n', encoding="utf-8")
    dates, reason = _scan_file(fixture)
    assert reason is None
    assert dates == [(1, "2026-03-15")]


def test_an_os_unreadable_path_is_reported_not_crashed(tmp_path):
    """A directory named *.py (rglob("*.py") would yield it in the real scan)
    raises an OSError on read — IsADirectoryError on POSIX, PermissionError on
    Windows — not a content error. That must fail closed the same way a bad
    encoding does, not crash the scan."""
    fixture = tmp_path / "x.py"
    fixture.mkdir()
    dates, reason = _scan_file(fixture)
    assert dates is None
    assert reason is not None and reason.startswith(
        ("IsADirectoryError", "PermissionError")
    ), reason


def test_config_json_lines_are_scanned_with_all_notations(tmp_path):
    fixture = tmp_path / "config.json"
    fixture.write_text('{"end": "20260315"}\n', encoding="utf-8")
    assert _config_json_dates(fixture) == [(1, "2026-03-15")]
