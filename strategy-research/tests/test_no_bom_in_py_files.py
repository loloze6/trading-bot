"""CUL-229: no tracked .py file under strategy-research/tests may carry a
UTF-8 BOM.

Python's source loader strips a BOM transparently, so a BOM-carrying test
file runs and passes like any other -- the bug is invisible to pytest. It
only bites a tool that AST-parses the file without a BOM-tolerant decode
(``ast.parse(open(f).read())`` raises ``SyntaxError`` on a BOM unless the
read uses ``utf-8-sig``), e.g. the AST sweeps in this same tests/ directory
(test_emoji_prints_cp1252_guarded.py, test_no_sealed_date_literals.py-style
scanners). The fix is mechanical (strip the 3 bytes) but silent regressions
come from Windows editors re-adding a BOM on save, hence this structural
guard rather than a one-time cleanup.
"""

from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_SCAN_ROOT = _REPO / "strategy-research" / "tests"


def test_no_py_file_under_sr_tests_starts_with_a_bom():
    offenders = [
        str(f.relative_to(_REPO))
        for f in sorted(_SCAN_ROOT.rglob("*.py"))
        if f.read_bytes()[:3] == b"\xef\xbb\xbf"
    ]
    assert not offenders, (
        "UTF-8 BOM found at the start of tracked .py file(s) under "
        "strategy-research/tests -- strip the 3 BOM bytes (keep UTF-8 "
        f"without BOM): {offenders}"
    )
