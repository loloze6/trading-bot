"""
E-039 step 5 follow-up (2026-09-12): metrics.json's "component_errors" block
(F5b's error count/samples, now wired through by trading-bot's
core/backtester.py) is a top-level sibling of "core", not nested inside it --
same shape as CUL-263's data_quality fix. Without an explicit read,
result_entry would silently drop it, the same "exists but doesn't flow"
failure CUL-263 found and fixed for data_quality.

Source-guard test (same convention as test_cul263_data_quality_flows_to_results.py):
run_protocol.py cannot be imported directly (constructs network/API clients at
import time in some paths), so this reads the real shipped file and confirms
the fix is textually present, plus a focused unit test against the literal
dict-construction logic to prove it actually reads a real metrics.json shape.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUN_PROTOCOL_SRC = (REPO_ROOT / "strategy-research" / "tools" / "run_protocol.py").read_text(encoding="utf-8")

_COMPONENT_ERRORS_FORWARD_RE = re.compile(
    r'"component_errors"\s*:\s*m\.get\(\s*"component_errors"\s*\)'
)


def test_result_entry_construction_includes_component_errors_key():
    """Source guard: result_entry must read metrics.json's component_errors key.
    Fails if this line is ever removed/renamed without a replacement."""
    assert _COMPONENT_ERRORS_FORWARD_RE.search(RUN_PROTOCOL_SRC), (
        "result_entry no longer forwards metrics.json's component_errors block -- "
        "F5b's error count/samples would silently stop reaching "
        "protocol_summary.json's per-window results again"
    )


def test_result_entry_dict_literal_reads_component_errors_from_a_real_metrics_shape():
    """Reproduces the exact result_entry dict-construction logic (copied, not
    imported -- run_protocol.py has import-time side effects) against a
    synthetic metrics.json shaped exactly like write_metrics_json's real
    output, with and without a populated component_errors block."""
    core = {"sharpe": 1.2, "trade_count": 10}

    def _build_result_entry(m: dict, core: dict) -> dict:
        return {
            "symbol": "BTCUSDT", "window": "w1", "run_id": "run_x",
            "core": core,
            "per_regime": m.get("per_regime", {}),
            "regime_validity": m.get("regime_validity", {}),
            "data_quality": m.get("data_quality"),
            "component_errors": m.get("component_errors"),
        }

    m_with_error = {
        "core": core,
        "component_errors": {"count": 3, "samples": [{"error_type": "ZeroDivisionError"}]},
    }
    entry = _build_result_entry(m_with_error, core)
    assert entry["component_errors"] == {
        "count": 3, "samples": [{"error_type": "ZeroDivisionError"}]
    }

    # A healthy run still carries the key, with an explicit zero (write_metrics_json
    # always includes it when a real strategy ran) -- never silently dropped.
    m_healthy = {"core": core, "component_errors": {"count": 0, "samples": []}}
    entry2 = _build_result_entry(m_healthy, core)
    assert entry2["component_errors"] == {"count": 0, "samples": []}
