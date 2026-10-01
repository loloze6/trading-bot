"""
Gap rule on by default (operator 2026-10-01): research backtests get it only
because run_protocol.py calls run_backtest() WITHOUT gap_detection / gap_policy,
so trading-bot's default (on, DEFAULT_GAP_POLICY) applies. Source guard (same
convention as test_component_errors_flow_to_results.py): run_protocol.py has
import-time side effects, so the shipped file is read.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = (REPO_ROOT / "strategy-research" / "tools" / "run_protocol.py").read_text(encoding="utf-8")


def test_run_protocol_calls_run_backtest_and_never_overrides_the_gap_default():
    assert len(re.findall(r"\brun_backtest\(", SRC)) >= 2
    assert not re.search(r"\bgap_detection\s*=", SRC), (
        "run_protocol.py now sets gap_detection -- research runs would no longer "
        "inherit the gap-rule default; make that a declared decision")
    assert not re.search(r"\bgap_policy\s*=", SRC)
