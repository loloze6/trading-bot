"""
Known-answer shakedown for prescreen_signal.py's degenerate-active-forecast fallback
(2026-07-07, P4_ts_trend). SmaTrendLongOnlyComponent (long-only, single constant
magnitude when active) makes ic_active_bars mathematically undefined -- Spearman IC
has zero variance to correlate against returns when every active-bar forecast is
identical. The naive route (kill_no_ic on "not significant") is a guaranteed false
negative for this signal SHAPE, independent of whether real edge exists.

These two tests prove the gate's block-bootstrap fallback on pooled all-bars IC can
BOTH kill a genuine null AND pass a genuine positive for this exact signal shape,
end-to-end through run_prescreen() on the 1d path, using the actual production
SmaTrendLongOnlyComponent -- before trusting the gate to judge the real
SMA(100)-daily registration. Only the underlying synthetic price series differs
between the two tests; the component/config is identical.
"""
import json
import random
import sys
from pathlib import Path

import pandas as pd
import pytest

TOOLS_PATH = Path(__file__).parent.parent / "tools"
TBOT_PATH = Path(__file__).parent.parent.parent / "trading-bot"
for p in (TOOLS_PATH, TBOT_PATH):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import prescreen_signal as ps

N_BARS = 1000
PHASE_LEN = 500  # >> lookback_L=100, so SMA(100) has time to catch up with each phase
LOOKBACK_L = 100

_CONFIG = {
    "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
    "strategies": {"warmup": LOOKBACK_L + 1, "regimes": {
        "unknown": {"components": [{
            "id": "sma_trend_long_only",
            "class": "strategies.strategy_components.SmaTrendLongOnlyComponent",
            "weight": 1.0, "transforms": [{"op": "identity"}],
            "params": {"lookback_L": LOOKBACK_L, "scaling_factor": 10.0},
        }]},
        "trending": None, "mean_reversion": None, "chop": None,
    }},
}

_PROTOCOL = {
    "symbols": ["SYNTHUSDT"],
    "timeframe": "1d",
    "windows": [{"label": "test", "test": {"start": "2018-01-01", "end": "2020-09-27"}}],
}


def _make_bars(mode: str) -> pd.DataFrame:
    """
    mode='null': i.i.d. random-sign daily returns (seeded) -- no persistent regime,
    so SMA(100) crossings carry no genuine forward-return information (classic
    no-free-lunch-on-a-random-walk null).
    mode='positive': deterministic multi-hundred-day up/down phases, each much
    longer than the SMA(100) lookback -- once the SMA catches up with a phase
    change (a lag of roughly LOOKBACK_L bars), "price > SMA(100)" genuinely,
    persistently precedes the phase's own continuing drift. A real, known-by-
    construction relationship, without the component ever reading future data.
    """
    rng = random.Random(20260707)
    rows = []
    price = 100.0
    for i in range(N_BARS):
        ts = pd.Timestamp("2018-01-01") + pd.Timedelta(i, unit="D")
        if mode == "positive":
            phase_up = (i // PHASE_LEN) % 2 == 0
            ret = 0.0015 if phase_up else -0.0015
        else:
            ret = rng.choice([-0.005, 0.005])
        open_ = price
        price = price * (1.0 + ret)
        rows.append({
            "timestamp": ts, "open": open_, "high": max(open_, price),
            "low": min(open_, price), "close": price, "volume": 1000.0,
        })
    return pd.DataFrame(rows)


def _run(mode: str, monkeypatch, tmp_path) -> dict:
    bars = _make_bars(mode)
    monkeypatch.setattr(ps, "_load_ohlcv", lambda symbol, start, end, timeframe="1h": bars.copy())

    config_path = tmp_path / "candidate_strategy_config.json"
    protocol_path = tmp_path / "protocol.json"
    config_path.write_text(json.dumps(_CONFIG), encoding="utf-8")
    protocol_path.write_text(json.dumps(_PROTOCOL), encoding="utf-8")

    return ps.run_prescreen(str(config_path), str(protocol_path),
                             run_id=f"test_synthetic_{mode}", out_dir=tmp_path)


def test_synthetic_null_routes_kill_no_ic(monkeypatch, tmp_path):
    result = _run("null", monkeypatch, tmp_path)

    assert result["active_n_bars"] > 0, "signal must actually activate on this fixture"
    assert result["ic_active_bars"] is None, "long-only constant magnitude -- must be undefined, not 0.0"
    assert result["degenerate_active_forecast"] is True
    assert result["significance_methodology_used"] == "block_bootstrap_all_bars_v1"
    assert result["ic_significance"]["significant"] is False, (
        "a genuinely unrelated (random-walk) null must NOT pass the bootstrap fallback"
    )
    assert result["route"] == "kill_no_ic"


def test_synthetic_positive_routes_proceed_to_backtest(monkeypatch, tmp_path):
    result = _run("positive", monkeypatch, tmp_path)

    assert result["active_n_bars"] > 0
    assert result["ic_active_bars"] is None
    assert result["degenerate_active_forecast"] is True
    assert result["significance_methodology_used"] == "block_bootstrap_all_bars_v1"
    assert result["ic_significance"]["significant"] is True, (
        "a genuine, constructed multi-phase trend relationship must be detected "
        "by the bootstrap fallback"
    )
    assert result["ic_significance"]["pooled_ic"] > 0
    assert result["route"] == "proceed_to_backtest", (
        f"expected the gate to pass a real signal of this shape; got route="
        f"{result['route']!r} rationale={result['route_rationale']!r}"
    )
