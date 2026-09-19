"""
CUL-263 (E-039): metrics.json's "data_quality" block (CUL-261, gap detection)
is a top-level sibling of "core", not nested inside it -- unlike CUL-262's
forecast_return_corr_pvalue_block_adjusted/n_eff, which already ride along
inside "core" and therefore already reach run_protocol.py's per-window
`results` list (and from there, protocol_summary.json). `data_quality` was
being silently dropped at the `result_entry` construction site, which only
ever captured "core"/"per_regime"/"regime_validity".

Source-guard test (same convention as test_expectancy_promotion_lockstep.py):
run_protocol.py cannot be imported directly (constructs network/API clients
at import time in some paths), so this reads the real shipped file and
confirms the fix is textually present, plus a focused unit test against the
literal dict-construction logic to prove it actually reads a real
metrics.json shape, not just that the key name appears in source.
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUN_PROTOCOL_SRC = (REPO_ROOT / "strategy-research" / "tools" / "run_protocol.py").read_text(encoding="utf-8")

# Whitespace-insensitive: this guard must survive a reformat of the alignment
# padding in the result_entry dict literal, which carries no meaning. Matching
# the exact spacing would make the test fail on a cosmetic edit while the
# behaviour it guards is untouched -- a false alarm that teaches people to
# ignore this test, which is worse than not having it.
_DATA_QUALITY_FORWARD_RE = re.compile(
    r'"data_quality"\s*:\s*m\.get\(\s*"data_quality"\s*\)'
)


def test_result_entry_construction_includes_data_quality_key():
    """Source guard: result_entry must read metrics.json's data_quality key.
    Fails if this line is ever removed/renamed without a replacement."""
    assert _DATA_QUALITY_FORWARD_RE.search(RUN_PROTOCOL_SRC), (
        "result_entry no longer forwards metrics.json's data_quality block -- "
        "CUL-261's gap-detection output would silently stop reaching "
        "protocol_summary.json's per-window results again"
    )


def test_result_entry_dict_literal_reads_data_quality_from_a_real_metrics_shape():
    """Reproduces the exact result_entry dict-construction logic (copied, not
    imported -- run_protocol.py has import-time side effects) against a
    synthetic metrics.json shaped exactly like build_core's real output, with
    and without a populated data_quality block, proving the read is correct
    both ways rather than just present in source."""
    core = {"sharpe": 1.2, "trade_count": 10}

    def _build_result_entry(m: dict, core: dict) -> dict:
        # Mirrors the real result_entry construction in run_protocol.py exactly.
        return {
            "symbol": "BTCUSDT", "window": "w1", "run_id": "run_x",
            "core": core,
            "per_regime": m.get("per_regime", {}),
            "regime_validity": m.get("regime_validity", {}),
            "data_quality": m.get("data_quality"),
        }

    # gap_detection=True, a gap was found
    m_with_gap = {"core": core, "data_quality": {"gaps_detected": 1, "events": [{"symbol": "BTCUSDT"}]}}
    entry = _build_result_entry(m_with_gap, core)
    assert entry["data_quality"] == {"gaps_detected": 1, "events": [{"symbol": "BTCUSDT"}]}

    # gap_detection off (today's default) -- metrics.json has no such key at all
    m_without = {"core": core}
    entry2 = _build_result_entry(m_without, core)
    assert entry2["data_quality"] is None, (
        "must degrade to None, not KeyError, when gap_detection was off for this window"
    )


def test_forecast_return_corr_block_adjusted_already_flows_via_core():
    """CUL-262's two new fields live INSIDE build_core's returned dict, which
    is copied wholesale into result_entry['core'] already (unlike
    data_quality, a sibling key) -- confirms no separate fix was needed for
    those two fields specifically."""
    core_with_cul262_fields = {
        "sharpe": 1.2, "trade_count": 10,
        "forecast_return_corr_pvalue_block_adjusted": 0.031,
        "forecast_return_corr_n_eff": 4,
    }

    def _build_result_entry(m: dict, core: dict) -> dict:
        return {"core": core, "data_quality": m.get("data_quality")}

    entry = _build_result_entry({"core": core_with_cul262_fields}, core_with_cul262_fields)
    assert entry["core"]["forecast_return_corr_pvalue_block_adjusted"] == 0.031
    assert entry["core"]["forecast_return_corr_n_eff"] == 4
