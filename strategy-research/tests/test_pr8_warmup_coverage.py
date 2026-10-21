"""
PR-8 (D-169): the data gates count a window as covered only when the coin has the
strategy's warm-up bars BEFORE the window start.

run_098's ADA on fold B: both gates looked only at the test window, so a window with
about 95 daily bars of history before it was "fully available" and then crashed the
launcher's warm-up probe (`assert probe.is_ready()` after a 2 x required_bars prefetch).

Covers:
  1. The number: strategy_required_bars equals AdvancedStrategy.required_bars, the
     strategy is ready only between required_bars and 2 x required_bars bars (so
     required_bars alone would let the probe crash), warmup_bars_needed = 2 x.
  2. layer1_warmup_check / layer1_price_precheck: a coin whose history starts inside the
     warm-up is excluded with the reason; a full-history coin is unchanged; the exact
     boundary; warmup_bars=None is byte-identical to the structural precheck.
  3. The data gate (evaluate_variant): the window is excluded with the reason in its
     record; a config with no strategy sections is judged as before.
  4. D-042 (variant_coin.window_coverage / coverage_decision): the excluded windows are
     counted against the 60 percent; the 60 percent outcome when exclusions push coverage
     below it.
  5. Wiring: run_phase1_research._variant_coin_context applies the warm-up from the run's
     backtest_spec.yaml config and leaves the precheck untouched without one.

Sandbox: synthetic Layer-1 audits and configs only. No local_data read, no network, no
market data. Windows are 2019-2021 (no sealed-range date).
"""
import copy
import datetime
import functools
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
REPO_ROOT = SR_ROOT.parent
TRADING_BOT = REPO_ROOT / "trading-bot"
for _p in (str(TRADING_BOT / "tools"), str(TRADING_BOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import data_availability_gate as dag  # noqa: E402
import variant_coin as vc  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

from test_e061_c2_s2b_one_coin_per_variant import (  # noqa: E402
    _asset, _copy_coin_configs, _ctx, _months, _set_flags, _source, _synthetic)
from test_k3_protocol_pinning import _minimal_run  # noqa: E402

COMP = "strategies.strategy_components."
STANDARDISE = {"op": "standardise", "params": {"window": 60, "min_periods": 20}}


def _config(period: int) -> dict:
    """One PriceEvolution component of lookback `period`, standardised 60/20: required_bars is
    period + 21 (measured below; run_098's ADA config had required_bars 270)."""
    return {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                            "default_regime": "unknown"},
        "strategies": {"regimes": {
            "unknown": {"components": [
                {"id": "a", "class": COMP + "PriceEvolutionComponent", "params": {"period": period},
                 "weight": 1.0, "transforms": [STANDARDISE]}]},
            "trending": None, "mean_reversion": None, "chop": None}},
    }


SLOW = _config(249)
REQUIRED = 270
NEEDED = 2 * REQUIRED  # 540, the launcher's prefetch (core/launcher.py:950-955)
DAY = datetime.timedelta(days=1)


# ---------------------------------------------------------------------------
# 1. The number
# ---------------------------------------------------------------------------

def _strategy(tmp_path, config):
    import json
    from strategies.main_strategy import AdvancedStrategy
    path = tmp_path / "strategy_config.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    return AdvancedStrategy(config_path=str(path))


def test_required_bars_matches_the_strategy_and_the_prefetch_doubles_it(tmp_path):
    strategy = _strategy(tmp_path, SLOW)
    assert strategy.required_bars == REQUIRED
    assert dag.strategy_required_bars(SLOW) == strategy.required_bars
    assert dag.warmup_bars_needed(SLOW) == 2 * strategy.required_bars == NEEDED
    # the 24-bar floor of main_strategy.py
    fast = _config(1)
    assert dag.strategy_required_bars(fast) == _strategy(tmp_path, fast).required_bars == 24


def test_ready_only_after_required_bars_so_required_bars_alone_would_not_do(tmp_path):
    """Why the rule needs 2 x required_bars and not required_bars (the component lookback plus
    the standardise min_periods): the strategy is not ready at required_bars bars; it is ready
    somewhere before the launcher's 2 x required_bars prefetch. A coin with required_bars bars
    would pass a required_bars rule and still fail the launcher's probe."""
    strategy = _strategy(tmp_path, SLOW)
    rng = np.random.default_rng(3)
    n = NEEDED
    close = 100.0 * np.exp(np.cumsum(rng.normal(0.0, 0.01, n)))
    bars = pd.DataFrame({
        "timestamp": pd.date_range("2019-01-01", periods=n, freq="D"),
        "open": close, "high": close * 1.01, "low": close * 0.99, "close": close,
        "volume": rng.uniform(50.0, 150.0, n)})
    first_ready, ready_at_required = None, None
    for t in range(n):
        strategy.update(bars.iloc[t:t + 1])
        if t + 1 == REQUIRED:
            ready_at_required = strategy.is_ready()
        if first_ready is None and strategy.is_ready():
            first_ready = t + 1
    assert ready_at_required is False
    assert first_ready is not None and REQUIRED < first_ready <= NEEDED
    assert strategy.is_ready()  # the probe's assertion, after exactly the prefetch


@pytest.mark.parametrize("config", [{}, {"aux_feeds": []}, {"strategies": {"regimes": {}}},
                                    {"regime_detector": {"mode": "threshold_rules"}}])
def test_a_config_without_strategy_sections_has_no_warmup_number(config):
    assert dag.strategy_required_bars(config) is None
    assert dag.warmup_bars_needed(config) is None


# ---------------------------------------------------------------------------
# 2. layer1_warmup_check / layer1_price_precheck
# ---------------------------------------------------------------------------

def _layer1(earliest: str, symbol: str = "ADAUSD", exchange: str = "kraken") -> dict:
    return {"venues": {exchange: {"spot": {
        "timeframes": {"live_rest_api": {"intervals_minutes": [1440]},
                       "downloadable_archive": {"intervals_minutes": [1440]}},
        "symbols": {"confirmed_universe": [symbol], "earliest_ohlcv_utc": {symbol: earliest}}}}}}


WINDOW_START = datetime.datetime(2019, 1, 1)
WINDOW_END = datetime.datetime(2019, 5, 1)


def _earliest_before(bars: int) -> str:
    return (WINDOW_START - bars * DAY).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_a_coin_whose_history_starts_inside_the_warmup_is_excluded_with_the_reason():
    # run_098's ADA: about 95 daily bars before the window, 540 needed
    layer1 = _layer1(_earliest_before(95))
    ok, reason = dag.layer1_price_precheck(layer1, "kraken", "ADAUSD", "1d", WINDOW_START, WINDOW_END,
                                           warmup_bars=NEEDED)
    assert ok is False
    assert reason.startswith("warm-up: 95 bars before the window start, 540 needed")
    # the same coin, same window, passes the structural precheck: the gap this PR closes
    assert dag.layer1_price_precheck(layer1, "kraken", "ADAUSD", "1d", WINDOW_START, WINDOW_END) == (True, "ok")


def test_a_full_history_coin_is_unchanged():
    layer1 = _layer1(_earliest_before(2000))
    base = dag.layer1_price_precheck(layer1, "kraken", "ADAUSD", "1d", WINDOW_START, WINDOW_END)
    assert base == (True, "ok")
    assert dag.layer1_price_precheck(layer1, "kraken", "ADAUSD", "1d", WINDOW_START, WINDOW_END,
                                     warmup_bars=NEEDED) == base


def test_the_boundary_exactly_k_bars_before_is_covered_one_fewer_is_not():
    ok, _ = dag.layer1_price_precheck(_layer1(_earliest_before(NEEDED)), "kraken", "ADAUSD", "1d",
                                      WINDOW_START, WINDOW_END, warmup_bars=NEEDED)
    assert ok is True
    ok, reason = dag.layer1_price_precheck(_layer1(_earliest_before(NEEDED - 1)), "kraken", "ADAUSD", "1d",
                                           WINDOW_START, WINDOW_END, warmup_bars=NEEDED)
    assert ok is False and reason.startswith(f"warm-up: {NEEDED - 1} bars before the window start, {NEEDED} needed")


def test_a_window_starting_before_the_first_bar_has_zero_warmup_bars():
    layer1 = _layer1("2019-03-01T00:00:00Z")
    ok, reason = dag.layer1_price_precheck(layer1, "kraken", "ADAUSD", "1d", WINDOW_START, WINDOW_END,
                                           warmup_bars=NEEDED)
    assert ok is False and reason.startswith("warm-up: 0 bars before the window start")


def test_a_structural_decline_keeps_its_own_reason_and_no_date_means_not_judged():
    layer1 = _layer1(_earliest_before(95))
    ok, reason = dag.layer1_price_precheck(layer1, "kraken", "NOTLISTED", "1d", WINDOW_START, WINDOW_END,
                                           warmup_bars=NEEDED)
    assert ok is False and "confirmed_universe" in reason and "warm-up" not in reason
    no_date = copy.deepcopy(layer1)
    no_date["venues"]["kraken"]["spot"]["symbols"]["earliest_ohlcv_utc"] = {}
    assert dag.layer1_price_precheck(no_date, "kraken", "ADAUSD", "1d", WINDOW_START, WINDOW_END,
                                     warmup_bars=NEEDED)[0] is True


def test_the_warmup_is_counted_in_bars_of_the_timeframe():
    # 1h strategy: 540 bars is 22.5 days, not 540 days
    layer1 = {"venues": {"binance": {"spot": {
        "timeframes": {"available": ["1h"]},
        "symbols": {"earliest_ohlcv_utc": {"BTCUSDT": (WINDOW_START - datetime.timedelta(hours=539)).isoformat() + "Z"}}}}}}
    ok, reason = dag.layer1_price_precheck(layer1, "binance", "BTCUSDT", "1h", WINDOW_START, WINDOW_END,
                                           warmup_bars=NEEDED)
    assert ok is False and reason.startswith("warm-up: 539 bars before the window start, 540 needed")


# ---------------------------------------------------------------------------
# 3. The data gate (evaluate_variant)
# ---------------------------------------------------------------------------

def _gate_protocol(windows):
    return {"symbols": ["ADAUSD"], "timeframe": "1d", "exchange": "kraken", "windows": windows}


@pytest.fixture
def layer2_validates(monkeypatch):
    calls = []

    def _fake(symbol, exchange, timeframe, start, end, gap_tolerance=0.05, **kw):
        calls.append((symbol, start))
        return {"outcome": "validate", "missing_fraction": 0.0, "reason": "fully available", "rows": 1}
    monkeypatch.setattr(dag, "check_price_window", _fake)
    return calls


def test_the_data_gate_excludes_a_window_without_warmup_and_records_the_reason(layer2_validates):
    # ADA-like: first bar 95 days before 2019-01; the 2020-07 window has plenty
    layer1 = _layer1(_earliest_before(95))
    windows = [{"label": "2019-01", "test": {"start": "2019-01-01", "end": "2019-05-01"}},
               {"label": "2020-07", "test": {"start": "2020-07-01", "end": "2020-11-01"}}]
    result = dag.evaluate_variant(SLOW, _gate_protocol(windows), layer1=layer1)
    first, second = result["windows"]
    assert first["layer"] == 1 and first["outcome"] == "decline" and first["missing_fraction"] == 1.0
    assert first["reason"].startswith("warm-up: 95 bars before the window start, 540 needed")
    assert second["layer"] == 2 and second["outcome"] == "validate"
    assert result["outcome"] == "refine"
    assert any("2019-01" in r and "warm-up" in r for r in result["reasons"])
    assert layer2_validates == [("ADAUSD", "2020-07-01")]  # the excluded window never reaches the data touch


def test_the_data_gate_declines_when_every_window_lacks_the_warmup(layer2_validates):
    layer1 = _layer1(_earliest_before(95))
    windows = [{"label": "2019-01", "test": {"start": "2019-01-01", "end": "2019-05-01"}},
               {"label": "2019-06", "test": {"start": "2019-06-01", "end": "2019-09-01"}}]
    result = dag.evaluate_variant(SLOW, _gate_protocol(windows), layer1=layer1)
    assert result["outcome"] == "decline"
    assert all("warm-up" in w["reason"] for w in result["windows"])
    assert layer2_validates == []


def test_the_data_gate_is_unchanged_for_a_full_history_coin(layer2_validates):
    layer1 = _layer1(_earliest_before(2000))
    windows = [{"label": "2019-01", "test": {"start": "2019-01-01", "end": "2019-05-01"}}]
    with_warmup = dag.evaluate_variant(SLOW, _gate_protocol(windows), layer1=layer1)
    without = dag.evaluate_variant({}, _gate_protocol(windows), layer1=layer1)  # no strategy sections
    for key in ("outcome", "reasons", "windows"):
        assert with_warmup[key] == without[key]
    assert with_warmup["outcome"] == "validate"


def test_a_config_without_strategy_sections_is_judged_as_before(layer2_validates):
    layer1 = _layer1(_earliest_before(95))
    windows = [{"label": "2019-01", "test": {"start": "2019-01-01", "end": "2019-05-01"}}]
    result = dag.evaluate_variant({"aux_feeds": []}, _gate_protocol(windows), layer1=layer1)
    assert result["outcome"] == "validate"


# ---------------------------------------------------------------------------
# 4. D-042: window coverage and the 60 percent
# ---------------------------------------------------------------------------

def _protocol_1d(starts):
    return {"symbols": ["ADAUSD"], "timeframe": "1d", "exchange": "kraken",
            "windows": [{"label": s, "test": {"start": s, "end": f"{s[:7]}-28"}} for s in starts]}


def _era_of(ts):
    return "era_a"


FIVE = ["2019-01-01", "2019-07-01", "2020-01-01", "2020-07-01", "2021-01-01"]


def _coverage(protocol, layer1, warmup_bars):
    precheck = (dag.layer1_price_precheck if warmup_bars is None
                else functools.partial(dag.layer1_price_precheck, warmup_bars=warmup_bars))
    return vc.window_coverage(protocol, exchange="kraken", symbol="ADAUSD", layer1=layer1,
                              precheck=precheck, era_of=_era_of)


def test_excluded_windows_are_counted_against_the_60_percent():
    # first bar 2018-06-01 + 540 days = 2019-11-24: the windows from 2020-01 on have the
    # warm-up (2019-01 has 214 bars, 2019-07 has 395)
    layer1 = _layer1("2018-06-01T00:00:00Z")
    cov = _coverage(_protocol_1d(FIVE), layer1, NEEDED)
    assert cov["windows_run"] == ["2020-01-01", "2020-07-01", "2021-01-01"]
    assert cov["windows_total"] == 5 and cov["fraction"] == 0.6
    assert [u["label"] for u in cov["uncovered"]] == ["2019-01-01", "2019-07-01"]
    assert all(u["reason"].startswith("warm-up:") for u in cov["uncovered"])
    # the same coin without the rule covered every window: the gap this PR closes
    assert _coverage(_protocol_1d(FIVE), layer1, None)["windows_run"] == FIVE
    # exactly 3/5 = 60 percent: D-042 admits it
    assert vc.coverage_decision(cov) is None


def test_the_60_percent_outcome_when_exclusions_push_coverage_below_it():
    layer1 = _layer1("2019-06-01T00:00:00Z")  # first bar + 540 days = 2020-11-22: only 2021-01 has them
    cov = _coverage(_protocol_1d(FIVE), layer1, NEEDED)
    assert cov["windows_run"] == ["2021-01-01"] and cov["fraction"] == 0.2
    why = vc.coverage_decision(cov)
    assert why is not None and why.startswith(vc.COVERAGE_REASON_PREFIX)
    assert "1/5 protocol windows" in why and "60%" in why
    # and none left: also not run
    none = _coverage(_protocol_1d(FIVE[:2]), layer1, NEEDED)
    assert none["windows_run"] == [] and vc.coverage_decision(none).startswith(vc.COVERAGE_REASON_PREFIX)


def test_a_full_history_coin_has_full_coverage_with_the_rule():
    layer1 = _layer1("2015-01-01T00:00:00Z")
    cov = _coverage(_protocol_1d(FIVE), layer1, NEEDED)
    assert cov == _coverage(_protocol_1d(FIVE), layer1, None)
    assert cov["windows_run"] == FIVE and vc.coverage_decision(cov) is None


# ---------------------------------------------------------------------------
# 5. Wiring: _variant_coin_context
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _spec_run(run_id, config):
    """A run dir whose artifacts/backtest_spec.yaml carries `config` (the shape 1b writes)."""
    _set_flags(config_direct_authoring=True, variant_loop=True)
    _copy_coin_configs()
    run_dir = _minimal_run(rpr.ROOT, run_id)
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (run_dir / "artifacts" / "backtest_spec.yaml").write_text(
        yaml.safe_dump({"status": "spec_ready", "config": config}), encoding="utf-8")
    return run_dir


def test_the_coin_context_applies_the_warmup_from_the_runs_base_config():
    run_dir = _spec_run("run_981", SLOW)
    ctx = rpr._variant_coin_context(run_dir, "run_981", source=_source(_months("2022-01", 6)))
    assert isinstance(ctx["precheck"], functools.partial)
    assert ctx["precheck"].func is dag.layer1_price_precheck
    assert ctx["precheck"].keywords == {"warmup_bars": NEEDED}


def test_the_coin_context_is_unchanged_without_a_base_config():
    run_dir = _minimal_run(rpr.ROOT, "run_982")  # no artifacts/backtest_spec.yaml
    _set_flags(config_direct_authoring=True, variant_loop=True)
    _copy_coin_configs()
    ctx = rpr._variant_coin_context(run_dir, "run_982", source=_source(_months("2022-01", 6)))
    assert ctx["precheck"] is dag.layer1_price_precheck


def test_an_asset_variant_without_warmup_is_not_run_through_the_real_resolver():
    """5a's resolve_variant, with the warm-up the coin context carries: XRPUSDT listed 95 days
    before the first window and the strategy needing 540 bars -> every window excluded ->
    not run (insufficient_coverage); the same coin without the rule would have run."""
    run_dir = _spec_run("run_983", SLOW)
    source = {**_source(_months("2022-01", 6)), "timeframe": "1d"}
    ctx = rpr._variant_coin_context(run_dir, "run_983", source=source)
    universe, layer1 = _synthetic("2021-09-28T00:00:00Z")
    ctx = {**ctx, "universe": universe, "layer1": layer1}
    res = vc.resolve_variant(_asset(), **ctx)
    assert res["ok"] is False and res["reason"].startswith(vc.COVERAGE_REASON_PREFIX)
    assert res["coverage"]["windows_run"] == []
    assert all(u["reason"].startswith("warm-up:") for u in res["coverage"]["uncovered"])
    plain = vc.resolve_variant(_asset(), **{**ctx, "precheck": dag.layer1_price_precheck})
    assert plain["ok"] is True
