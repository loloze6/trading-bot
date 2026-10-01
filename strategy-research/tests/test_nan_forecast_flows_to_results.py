"""
CUL-274: metrics.json's "nan_forecast" block (bars whose NaN forecast was held)
must reach run_protocol's per-window result_entry, like data_quality and
component_errors -- otherwise the research loop never sees the count.

Source guard, same convention as test_component_errors_flow_to_results.py
(run_protocol.py has import-time side effects, so the shipped file is read).
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUN_PROTOCOL_SRC = (REPO_ROOT / "strategy-research" / "tools" / "run_protocol.py").read_text(encoding="utf-8")


def test_result_entry_forwards_nan_forecast():
    assert re.search(r'"nan_forecast"\s*:\s*m\.get\(\s*"nan_forecast"\s*\)', RUN_PROTOCOL_SRC), (
        "result_entry no longer forwards metrics.json's nan_forecast block -- "
        "held NaN-forecast bars would silently stop reaching protocol_summary.json")
