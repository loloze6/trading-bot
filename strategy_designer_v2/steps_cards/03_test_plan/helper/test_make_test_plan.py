"""Tests of step 3's code rules: the sizing block and the holding period every config gets, and the windows of a
period."""
import math
import pytest
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[3] / "trading-bot"))
import make_test_plan as m  # noqa: E402
from strategies.registry import sizing_block_errors  # noqa: E402


def test_sizing_is_60_days_and_2_percent_a_day_on_any_bar_size():
    for bar, window in (("1d", 60), ("4h", 360), ("1h", 1440)):
        s = m.add_sizing({"strategies": {"regimes": {}}}, bar)["strategies"]["sizing"]
        assert s["window"] == window and s["periods_per_year"] == 365 * m.bars_per_day(bar)
        assert math.isclose(s["target_annual_vol"], 0.02 * math.sqrt(365), rel_tol=1e-5)
        assert s["kind"] == "vol_target" and s["max_allocation"] == 2
        assert sizing_block_errors(s) == []


def test_sizing_overwrites_a_block_the_model_wrote():
    cfg = {"strategies": {"regimes": {}, "sizing": {"kind": "vol_target", "window": 5, "target_annual_vol": 9,
                                                    "periods_per_year": 365}}}
    assert m.add_sizing(cfg, "1d")["strategies"]["sizing"]["window"] == 60


def test_the_holding_period_is_the_plan_s_horizon():
    assert m.add_holding({"strategies": {"regimes": {}}}, "24 bars")["strategies"]["min_holding_bars"] == 24
    cfg = {"strategies": {"regimes": {}, "min_holding_bars": 3}}                 # the model's value is replaced
    assert m.add_holding(cfg, "72")["strategies"]["min_holding_bars"] == 72
    for bad in ("", "about a day", "0 bars"):
        try:
            m.add_holding({"strategies": {}}, bad)
            assert False, bad
        except ValueError:
            pass


def test_the_prompt_has_no_placeholder_left():
    assert "{{" not in (HERE / "system_prompt.md").read_text()


def test_the_brief_side_is_enforced_by_code_on_every_component():
    """Operator, 2026-11-22: a short-only brief's book never goes long (each component capped at 0 from above), a long-only
    brief's never goes short; any other side adds nothing; applying it twice adds one cap."""
    import copy
    cfg = {"strategies": {"regimes": {"unknown": {"components": [
        {"id": "a", "class": "X", "transforms": [{"op": "standardise", "params": {"window": 60, "min_periods": 20}}]},
        {"id": "b", "class": "Y"}]}, "trending": None}}}
    short = m.add_side(m.add_side(copy.deepcopy(cfg), "short only"), "short only")
    for c in short["strategies"]["regimes"]["unknown"]["components"]:
        assert c["transforms"][-1] == {"op": "clip", "params": {"max": 0}} and sum(t["op"] == "clip" for t in c["transforms"]) == 1
    long_ = m.add_side(copy.deepcopy(cfg), "long only")
    assert all(c["transforms"][-1] == {"op": "clip", "params": {"min": 0}} for c in long_["strategies"]["regimes"]["unknown"]["components"])
    assert m.add_side(copy.deepcopy(cfg), "long and short") == cfg and m.add_side(copy.deepcopy(cfg), None) == cfg
    assert m.brief_side("---\nbar: 1d\nside: short only\n---\nA theory.") == "short only"
    assert m.brief_side("---\n---\nA theory.") is None


def test_the_idea_s_profile_is_built_by_code_and_holds_nothing_outside_it():
    """Topic 49: an idea naming a market profile gets it as vetoes to a flat regime, with the definition's settings in
    bars; run by the engine's own detector on made-up closes, a bar is in the idea's regime exactly when its 60-day return
    and the rank of its 30-day swing over 365 days put it in the profile (common/market_profile.md)."""
    import copy
    import numpy as np, pandas as pd
    from strategies.regime_engine import ConfigDrivenRegimeEngine
    cfg = {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
           "strategies": {"regimes": {"unknown": {"components": [{"id": "a", "class": "X"}]},
                                      "trending": None, "mean_reversion": None, "chop": None}}}
    assert m.add_profile(copy.deepcopy(cfg), None, "1d") == cfg and m.add_profile(copy.deepcopy(cfg), "none", "1d") == cfg
    hourly = m.add_profile(copy.deepcopy(cfg), "rising calm", "1h")["regime_detector"]
    assert hourly["components"][0]["params"] == {"period": 1440, "scaling_factor": 1.0}
    assert hourly["components"][1]["params"] == {"vol_period": 720, "lookback_period": 8760, "smooth_period": 1}
    trend_only = m.add_profile(copy.deepcopy(cfg), "choppy", "1d")["regime_detector"]     # one element: that element only
    assert [c["id"] for c in trend_only["components"]] == ["profile_trend"] and len(trend_only["vetoes"]) == 2
    rng = np.random.default_rng(7)
    rets = np.concatenate([rng.normal(0.004, 0.01, 300), rng.normal(-0.004, 0.05, 300), rng.normal(0, 0.02, 300)])
    close = pd.Series(100 * np.cumprod(1 + rets))
    seen = set()
    for profile in ("rising calm", "falling agitated", "choppy agitated", "choppy calm", "choppy", "agitated"):
        rd = m.add_profile(copy.deepcopy(cfg), profile, "1d")["regime_detector"]
        assert all(v["result"] == "chop" for v in rd["vetoes"])
        eng = ConfigDrivenRegimeEngine(rd)
        for t in range(400, len(close)):
            data = pd.DataFrame({"close": close[:t + 1].values})
            eng.update(data)
            regime, _ = eng.classify()
            trend = (close[t] / close[t - 60] - 1) * 100
            c = close.values[t - 394:t + 1]                              # the last 365 + 30 closes, as the component reads them
            r = np.diff(c) / c[1:]
            vols = pd.Series(r).rolling(30).std().dropna().values
            rank = (vols <= vols[-1]).mean()
            want = (("rising" if trend > 10 else "falling" if trend < -10 else "choppy") + " "
                    + ("agitated" if rank > 0.5 else "calm"))
            inside = all(w in want.split() for w in profile.split())
            assert (regime.value == "unknown") == inside, (profile, t, trend, rank, regime)
            seen.add(inside)
    assert seen == {True, False}
    full = {"strategies": {"regimes": {r: {"components": []} for r in ("unknown", "trending", "mean_reversion", "chop")}}}
    with pytest.raises(ValueError):
        m.add_profile(full, "rising calm", "1d")
