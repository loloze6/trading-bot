"""
E-060 S3a code-review fix 1 -- a composite (block-combiner) config through the
REAL backtest path with warmup_prefetch=True (core/launcher.py asserts the
strategy is ready after 2 * required_bars prefetch bars).

Pins: the run does not raise; the composite is live (not NOT_READY, every
block standardised) from the window's first bar; and each block's final
forecast equals its own stand-alone backtest's forecast on every window bar.

SLOW: reads the committed SOLUSDT_1h.csv cache; skipped when it does not cover
the window.  pytest tests/test_e060_composite_prefetch_backtest.py -m slow --timeout=0
"""
import csv
import json
import sys
from pathlib import Path

import pytest
from _cache_guard import cache_skip_reason

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

SYMBOL, START, END = "SOLUSDT", "2024-03-01", "2024-03-08"
_CACHE_SKIP = cache_skip_reason(PROJECT_ROOT / "local_data", ("SOLUSDT_1h.csv",), "2024-01-15", END)
pytestmark = [pytest.mark.slow,
              pytest.mark.skipif(_CACHE_SKIP is not None, reason=_CACHE_SKIP or "cache usable")]

PE = "strategies.strategy_components.PriceEvolutionComponent"
EMA = "strategies.strategy_components.EMASpreadComponent"
UNGATED = {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"}


def _source(component):
    return {"regime_detector": UNGATED,
            "strategies": {"regimes": {"unknown": {"components": [component]},
                                       "trending": None, "mean_reversion": None, "chop": None}}}


SOURCES = {
    "b0": _source({"id": "sig", "class": PE, "params": {"period": 5}, "weight": 1.0,
                   "transforms": [{"op": "identity"}, {"op": "scale", "params": {"factor": 100}}]}),
    "b1": _source({"id": "sig", "class": EMA, "params": {"fast_period": 12, "slow_period": 150},
                   "weight": 1.0, "transforms": [{"op": "identity"}]}),
}


def _composite(paths):
    """What tools/composition.py writes for these two ungated blocks."""
    from strategies.main_strategy import AdvancedStrategy
    comps, blocks = [], []
    for bid, path in paths.items():
        src = AdvancedStrategy(config_path=str(path))
        spec = dict(SOURCES[bid]["strategies"]["regimes"]["unknown"]["components"][0])
        spec["lookback"] = src.strategy_engine._history["unknown"]["sig"].maxlen
        spec["id"] = f"{bid}__sig"
        comps.append(spec)
        blocks.append({"id": bid, "weight": 0.5, "components": [spec["id"]],
                       "source": {"required_bars": src.required_bars,
                                  "warmup": src.strategy_engine._warmup,
                                  "buffer_bars": src.data_buffer.max_size,
                                  "regime_detector": UNGATED,
                                  "parts": {"unknown": [spec["id"]]}}})
    return {"regime_detector": UNGATED,
            "strategies": {"regimes": {
                "unknown": {"components": comps, "blocks": blocks,
                            "block_standardisation": {"target": 10.0, "window": 500,
                                                      "min_periods": 30}},
                "trending": None, "mean_reversion": None, "chop": None}}}


def _bars(run_dir):
    with open(Path(run_dir) / "bars.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _run(config_path, out):
    from core.launcher import run_backtest
    return run_backtest(config_path=str(config_path), symbol=SYMBOL, start=START, end=END,
                        results_root=str(out), trades_log_file=str(out / "trades.json"),
                        warmup_prefetch=True)


def test_composite_backtest_with_warmup_prefetch_is_live_from_the_first_bar(tmp_path):
    paths = {}
    for bid, cfg in SOURCES.items():
        paths[bid] = tmp_path / f"{bid}.json"
        paths[bid].write_text(json.dumps(cfg), encoding="utf-8")
    comp_path = tmp_path / "composite.json"
    comp_path.write_text(json.dumps(_composite(paths)), encoding="utf-8")

    comp_rows = _bars(_run(comp_path, tmp_path / "comp"))
    alone = {bid: {r["timestamp"]: float(r["forecast"]) for r in _bars(_run(p, tmp_path / bid))}
             for bid, p in paths.items()}

    assert comp_rows and comp_rows[0]["regime"] != "NOT_READY"
    for bid in SOURCES:
        col = f"debug_info.components.{bid}"
        assert float(comp_rows[0][f"{col}.active"]) == 1.0  # standardised from bar one
        n = 0
        for r in comp_rows:
            assert r["regime"] == "unknown"
            assert float(r[f"{col}.last_history_value"]) == pytest.approx(
                alone[bid][r["timestamp"]], rel=1e-9, abs=1e-12)
            n += 1
        assert n == len(alone[bid]) > 100
