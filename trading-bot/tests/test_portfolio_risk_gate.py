"""
Unit tests for risk/portfolio_risk_gate.py (fix/risk-layer, PR-1 + PR-2).

PR-1 (cap): the absolute_allocation_cap clamp, the shared validate_portfolio_controls
rule set (fail-loud on bad shapes / ranges / unknown keys), and the gate ctor's
defense-in-depth validation. Pure units, no I/O.

PR-2 (stateful pair): max_drawdown_kill (peak tracking, boundary trip, terminal
latch) and daily_loss_limit (Europe/Paris day anchor, rollover re-arm, DST days),
their interaction ordering, fail-loud degenerate equity, and the kill-path routing
that bypasses the RiskManager min-Δ band -- the latter driven through
TradingBot._process_symbol_candle_completion over lightweight stubs (no engine, no
I/O), same technique as tests/test_funding_accrual.py. The end-to-end bit-identity,
cap-bite, and kill-bite-through-the-engine contracts live in
tests/test_risk_layer_bit_identical.py.

No-lookahead rationale (hard rule 3): apply() reads only its `target_allocation`
(this bar's forecast->allocation output) plus gate state that observe() folds from
this bar's close-derived equity and its own past state; observe() reads only the
bar's own timestamp and equity. Nothing timestamped after the bar is read, so the
gate cannot look ahead by construction.
"""

from pathlib import Path

import pytest

from risk.portfolio_risk_gate import PortfolioRiskGate, validate_portfolio_controls

# pytest.ini sets pythonpath = ., so trading-bot/ is importable without a sys.path hack.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

pytestmark = pytest.mark.unit


# --- validate_portfolio_controls ---


def test_empty_block_is_valid():
    assert validate_portfolio_controls({}) == []


def test_valid_cap_block_is_valid():
    assert validate_portfolio_controls({"absolute_allocation_cap": {"cap": 1.0}}) == []


def test_non_dict_block_fails():
    errs = validate_portfolio_controls([("absolute_allocation_cap", 1.0)])
    assert len(errs) == 1 and "must be a dict" in errs[0]


def test_unknown_control_key_fails():
    # A typo'd / unrecognised control must fail loud rather than silently arm a
    # do-nothing safety control.
    errs = validate_portfolio_controls({"maximum_drawdown_killl": {"threshold": 0.25}})
    assert any("unknown portfolio_controls key" in e for e in errs)


def test_unknown_cap_subkey_fails():
    errs = validate_portfolio_controls({"absolute_allocation_cap": {"capp": 1.0}})
    # "capp" is unknown AND "cap" is missing -> two distinct fail-loud signals.
    assert any("unknown absolute_allocation_cap key" in e for e in errs)
    assert any('requires a "cap"' in e for e in errs)


def test_cap_must_be_present():
    errs = validate_portfolio_controls({"absolute_allocation_cap": {}})
    assert any('requires a "cap"' in e for e in errs)


@pytest.mark.parametrize("bad", [0, -1.0, float("inf"), float("nan"), "1.0", True, None])
def test_cap_value_range_and_type(bad):
    errs = validate_portfolio_controls({"absolute_allocation_cap": {"cap": bad}})
    assert any("finite number > 0" in e for e in errs), f"{bad!r} should be rejected"


def test_cap_subblock_must_be_dict():
    errs = validate_portfolio_controls({"absolute_allocation_cap": 1.0})
    assert any("must be a dict" in e for e in errs)


# --- gate ctor ---


def test_ctor_rejects_invalid_config():
    with pytest.raises(ValueError, match="invalid portfolio_controls"):
        PortfolioRiskGate({"absolute_allocation_cap": {"cap": -1.0}})


def test_ctor_stores_effective_config_verbatim():
    cfg = {"absolute_allocation_cap": {"cap": 0.75}}
    gate = PortfolioRiskGate(cfg)
    assert gate.config == cfg
    # a copy, not the caller's dict (mutating the source must not change provenance)
    cfg["absolute_allocation_cap"]["cap"] = 9.0
    assert gate.config["absolute_allocation_cap"]["cap"] == 0.75


def test_ctor_no_cap_leaves_cap_none():
    gate = PortfolioRiskGate({})
    assert gate.cap is None


# --- apply: the cap clamp ---


def test_cap_clamps_positive_over_limit():
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    # forecast +20 -> target +2.0 (the /10 map's default max) -> clamped to +1.0
    final, extras = gate.apply(2.0)
    assert final == 1.0
    assert extras == {"risk_target_raw": 2.0, "risk_cap_clamped": True}


def test_cap_clamps_negative_over_limit():
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    final, extras = gate.apply(-2.0)
    assert final == -1.0
    assert extras["risk_cap_clamped"] is True


def test_cap_passes_target_within_limit_untouched():
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    final, extras = gate.apply(0.5)
    assert final == 0.5
    assert extras == {"risk_target_raw": 0.5, "risk_cap_clamped": False}


def test_cap_boundary_is_not_clamped():
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    final, extras = gate.apply(1.0)
    assert final == 1.0
    assert extras["risk_cap_clamped"] is False


def test_apply_raises_on_nan_target():
    # Fail-loud on degenerate input: a NaN target would pass any clamp unchanged and
    # mislabel risk_cap_clamped True (nan != nan). Raises with or without a cap.
    for cfg in ({"absolute_allocation_cap": {"cap": 1.0}}, {}):
        gate = PortfolioRiskGate(cfg)
        with pytest.raises(ValueError, match="NaN target_allocation"):
            gate.apply(float("nan"))


def test_apply_clamps_inf_target_when_capped():
    # inf is NOT rejected -- the cap clamps it (reviewer-blessed). Guards against the
    # NaN check being widened to reject all non-finite values.
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    assert gate.apply(float("inf"))[0] == 1.0
    assert gate.apply(float("-inf"))[0] == -1.0


def test_apply_no_cap_is_identity():
    gate = PortfolioRiskGate({})
    final, extras = gate.apply(2.0)
    assert final == 2.0
    assert extras == {"risk_target_raw": 2.0, "risk_cap_clamped": False}


def test_apply_is_pure_function_of_its_argument():
    # No-lookahead / statelessness pin: repeated and interleaved calls never let one
    # bar's target influence another's result.
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    assert gate.apply(2.0)[0] == 1.0
    assert gate.apply(0.3)[0] == 0.3
    assert gate.apply(2.0)[0] == 1.0
    assert gate.apply(-5.0)[0] == -1.0


# --- provenance fold recipe (pure, no backtest) ---


def test_provenance_fold_changes_run_hash(tmp_path):
    """The 8-char config hash new_run_dir stamps on a run dir must differ once the
    risk_management block is folded in, and be deterministic for a fixed config -- the
    property the gate-on/gate-off distinguishability contract rests on."""
    from reporting.run_artifact import new_run_dir

    cfg = {"strategies": {"a": 1}, "regime_detector": {"b": 2}}
    folded = {
        **cfg,
        "risk_management": {"portfolio_controls": {"absolute_allocation_cap": {"cap": 1.0}}},
    }

    def _hash(root, c):
        return new_run_dir(str(tmp_path / root), c).name.split("_")[-1]

    h_base = _hash("a", cfg)
    h_base_again = _hash("b", cfg)
    h_folded = _hash("c", folded)

    assert h_base == h_base_again  # deterministic recipe
    assert h_base != h_folded  # the fold moves run identity


# --- validation wired into both entry points ---


def test_config_manager_validate_rejects_bad_portfolio_controls():
    """ConfigManager.validate (the config.json entry point) fails loud on a bad
    portfolio_controls block. Mutation: drop the validate_portfolio_controls call in
    settings.py -> this returns True."""
    from config.settings import ConfigManager

    cm = ConfigManager("config.json")
    cm.config = {
        "trading": {"symbols": ["BTCUSDT"]},
        "risk_management": {"portfolio_controls": {"absolute_allocation_cap": {"cap": -1.0}}},
    }
    assert cm.validate() is False

    cm.config["risk_management"]["portfolio_controls"] = {"absolute_allocation_cap": {"cap": 1.0}}
    assert cm.validate() is True


def test_run_backtest_rejects_bad_risk_controls_override(tmp_path):
    """run_backtest (the override entry point) raises fail-loud BEFORE any data load on
    an invalid risk_controls dict -- the override bypasses ConfigManager.validate, so it
    validates independently."""
    from core.launcher import run_backtest

    with pytest.raises(ValueError, match="Invalid risk_controls override"):
        run_backtest(
            config_path=str(PROJECT_ROOT / "strategy_config.json"),
            symbol="BTCUSDT",
            start="2024-04-01",
            end="2024-05-30",
            results_root=str(tmp_path),
            trades_log_file=str(tmp_path / "t.json"),
            risk_controls={"absolute_allocation_cap": {"cap": 0}},
        )


# =========================================================================
# PR-2: max_drawdown_kill + daily_loss_limit (stateful pair)
# =========================================================================
#
# No-lookahead rationale (hard rule 3): observe() reads only `equity`
# (core/trading_bot.py's pre-rebalance mark-to-market, derived from THIS bar's
# close) and `data_time` (this bar's candle-close timestamp), plus the gate's own
# past state (running peak, day anchor). The Paris day key comes from the bar's own
# timestamp. Nothing timestamped after the bar is ever read, so the stateful
# controls cannot look ahead by construction.

from zoneinfo import ZoneInfo  # noqa: E402

import pandas as pd  # noqa: E402


def _ts(s):
    return pd.Timestamp(s)


# --- validation: the two new controls ---


def test_new_controls_are_known():
    assert validate_portfolio_controls({"max_drawdown_kill": {"threshold": 0.25}}) == []
    assert validate_portfolio_controls({"daily_loss_limit": {"threshold": 0.05}}) == []
    assert validate_portfolio_controls({"daily_loss_limit": {"threshold": 0.05, "tz": "Europe/Paris"}}) == []


@pytest.mark.parametrize("control", ["max_drawdown_kill", "daily_loss_limit"])
@pytest.mark.parametrize("bad", [0, 1, 1.5, -0.1, float("inf"), float("nan"), "0.2", True, None])
def test_threshold_range_and_type(control, bad):
    errs = validate_portfolio_controls({control: {"threshold": bad}})
    assert any("finite number in (0, 1)" in e for e in errs), f"{bad!r} should be rejected"


@pytest.mark.parametrize("control", ["max_drawdown_kill", "daily_loss_limit"])
def test_threshold_required(control):
    errs = validate_portfolio_controls({control: {}})
    assert any('requires a "threshold"' in e for e in errs)


def test_dd_unknown_subkey_fails():
    errs = validate_portfolio_controls({"max_drawdown_kill": {"threshold": 0.25, "tz": "x"}})
    assert any("unknown max_drawdown_kill key" in e for e in errs)


def test_dl_unknown_subkey_fails():
    errs = validate_portfolio_controls({"daily_loss_limit": {"threshold": 0.05, "cap": 1.0}})
    assert any("unknown daily_loss_limit key" in e for e in errs)


def test_dl_bad_tz_fails():
    errs = validate_portfolio_controls({"daily_loss_limit": {"threshold": 0.05, "tz": "Mars/Olympus"}})
    assert any("not a known timezone" in e for e in errs)


def test_dl_non_string_tz_fails():
    errs = validate_portfolio_controls({"daily_loss_limit": {"threshold": 0.05, "tz": 42}})
    assert any("must be a string" in e for e in errs)


def test_dl_tz_defaults_when_absent():
    gate = PortfolioRiskGate({"daily_loss_limit": {"threshold": 0.05}})
    assert gate.tz == "Europe/Paris"


def test_ctor_parses_thresholds():
    gate = PortfolioRiskGate(
        {"max_drawdown_kill": {"threshold": 0.3}, "daily_loss_limit": {"threshold": 0.04, "tz": "UTC"}}
    )
    assert gate.dd_threshold == 0.3
    assert gate.dl_threshold == 0.04
    assert gate.tz == "UTC"


# --- max_drawdown_kill ---


def test_monotone_series_never_trips():
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}})
    for h, eq in enumerate([100.0, 101.0, 105.0, 110.0]):
        gate.observe(_ts(f"2024-04-01 {h:02d}:00:00"), eq)
    assert gate.killed is False
    assert gate.peak_equity == 110.0


def test_drawdown_trips_at_exact_threshold():
    # Boundary is >=, not >. Mutation `>=` -> `>` is caught here: 25.0% drawdown
    # must trip.
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}})
    gate.observe(_ts("2024-04-01 00:00:00"), 100.0)
    gate.observe(_ts("2024-04-01 01:00:00"), 75.0)  # exactly 25% below peak
    assert gate.killed is True
    assert gate._bar_trip == "max_drawdown_kill"
    assert gate.kill_ts == "2024-04-01 01:00:00"


def test_drawdown_just_under_threshold_does_not_trip():
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}})
    gate.observe(_ts("2024-04-01 00:00:00"), 100.0)
    gate.observe(_ts("2024-04-01 01:00:00"), 75.01)  # 24.99% < 25%
    assert gate.killed is False


def test_kill_latches_through_recovery():
    # Latch persists even when equity fully recovers past the old peak.
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}})
    gate.observe(_ts("2024-04-01 00:00:00"), 100.0)
    gate.observe(_ts("2024-04-01 01:00:00"), 70.0)  # trip
    gate.observe(_ts("2024-04-01 02:00:00"), 130.0)  # rally
    assert gate.killed is True
    assert gate.apply(2.0)[0] == 0.0  # still forced flat
    assert gate.n_bars_killed == 2  # trip bar + rally bar both in force


def test_peak_uses_current_bar_before_check():
    # peak includes the current bar, so a fresh all-time high never shows a drawdown.
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.01}})
    gate.observe(_ts("2024-04-01 00:00:00"), 100.0)
    gate.observe(_ts("2024-04-01 01:00:00"), 200.0)
    assert gate._bar_drawdown == 0.0
    assert gate.killed is False


# --- daily_loss_limit ---


def test_daily_trip_halts_rest_of_day_then_rearms():
    gate = PortfolioRiskGate({"daily_loss_limit": {"threshold": 0.05}})
    # Summer (Europe/Paris = UTC+2): the Paris day boundary is 22:00 UTC.
    gate.observe(_ts("2024-07-15 00:00:00"), 100.0)  # day anchor
    gate.observe(_ts("2024-07-15 05:00:00"), 96.0)  # 4% loss, no trip
    assert gate.daily_halted is False
    gate.observe(_ts("2024-07-15 10:00:00"), 94.0)  # 6% >= 5% -> trip
    assert gate.daily_halted is True
    assert gate._bar_trip == "daily_loss_limit"
    gate.observe(_ts("2024-07-15 12:00:00"), 99.0)  # recovered, still halted (day-scoped)
    assert gate.daily_halted is True
    # 22:00 UTC == 00:00 Paris next day -> rollover, re-arm, fresh anchor.
    gate.observe(_ts("2024-07-15 22:00:00"), 99.0)
    assert gate.daily_halted is False
    assert gate.day_key == pd.Timestamp("2024-07-16").date()
    assert gate.day_start_equity == 99.0


def test_daily_trip_at_exact_threshold():
    gate = PortfolioRiskGate({"daily_loss_limit": {"threshold": 0.05}})
    gate.observe(_ts("2024-07-15 00:00:00"), 100.0)
    gate.observe(_ts("2024-07-15 01:00:00"), 95.0)  # exactly 5%
    assert gate.daily_halted is True


def test_daily_first_bar_of_day_loss():
    # Anchor is the first bar of the Paris day; a big drop on the very next bar trips.
    gate = PortfolioRiskGate({"daily_loss_limit": {"threshold": 0.05}})
    gate.observe(_ts("2024-07-15 00:00:00"), 100.0)
    gate.observe(_ts("2024-07-15 01:00:00"), 80.0)
    assert gate.daily_halted is True
    assert gate._bar_daily_loss == pytest.approx(0.20)


def test_daily_two_consecutive_day_trips():
    gate = PortfolioRiskGate({"daily_loss_limit": {"threshold": 0.05}})
    gate.observe(_ts("2024-07-15 00:00:00"), 100.0)
    gate.observe(_ts("2024-07-15 02:00:00"), 90.0)  # day 1 trip
    gate.observe(_ts("2024-07-15 22:00:00"), 90.0)  # rollover to day 2, fresh anchor 90
    gate.observe(_ts("2024-07-16 02:00:00"), 80.0)  # day 2 trip (11% of 90)
    assert [e["day"] for e in gate.trip_log] == ["2024-07-15", "2024-07-16"]
    assert gate.stateful_summary()["daily_trips"] == ["2024-07-15", "2024-07-16"]


def test_paris_day_matches_independent_zoneinfo():
    # Cross-check the gate's day key against an independent zoneinfo computation.
    gate = PortfolioRiskGate({"daily_loss_limit": {"threshold": 0.05}})
    for h in range(0, 24):
        t = _ts(f"2024-07-15 {h:02d}:00:00")
        expected = t.tz_localize("UTC").tz_convert(ZoneInfo("Europe/Paris")).date()
        assert gate._paris_day(t) == expected


def test_dst_spring_forward_2024_03_31():
    # Spring-forward day: Paris jumps UTC+1 -> UTC+2 at 01:00 UTC. Before the clock
    # change the day boundary sits at 23:00 UTC (winter); after, at 22:00 UTC.
    gate = PortfolioRiskGate({"daily_loss_limit": {"threshold": 0.9}})
    assert gate._paris_day(_ts("2024-03-30 23:00:00")) == pd.Timestamp("2024-03-31").date()
    assert gate._paris_day(_ts("2024-03-31 00:00:00")) == pd.Timestamp("2024-03-31").date()
    # 22:00 UTC 2024-03-31 is now UTC+2 -> 00:00 Paris on 2024-04-01.
    assert gate._paris_day(_ts("2024-03-31 22:00:00")) == pd.Timestamp("2024-04-01").date()


def test_dst_fall_back_2024_10_27():
    # Fall-back day: Paris drops UTC+2 -> UTC+1 at 01:00 UTC. The boundary INTO the
    # next day moves from 22:00 UTC (summer) to 23:00 UTC (winter).
    gate = PortfolioRiskGate({"daily_loss_limit": {"threshold": 0.9}})
    assert gate._paris_day(_ts("2024-10-26 22:00:00")) == pd.Timestamp("2024-10-27").date()
    assert gate._paris_day(_ts("2024-10-27 22:00:00")) == pd.Timestamp("2024-10-27").date()
    assert gate._paris_day(_ts("2024-10-27 23:00:00")) == pd.Timestamp("2024-10-28").date()


# --- interaction ordering (b before c) ---


def test_both_trip_same_bar_kill_is_recorded_cause():
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}, "daily_loss_limit": {"threshold": 0.05}})
    gate.observe(_ts("2024-07-15 00:00:00"), 100.0)
    gate.observe(_ts("2024-07-15 01:00:00"), 70.0)  # dd 30% AND daily 30% same bar
    assert gate.killed is True
    assert gate.daily_halted is False  # kill dominates; daily trip is not taken
    assert gate._bar_trip == "max_drawdown_kill"
    assert [e["control"] for e in gate.trip_log] == ["max_drawdown_kill"]


def test_daily_unreachable_once_killed():
    # A daily loss on a LATER day, after the kill has latched, never trips: the book
    # is already flat to run end.
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.1}, "daily_loss_limit": {"threshold": 0.05}})
    gate.observe(_ts("2024-07-15 00:00:00"), 100.0)
    gate.observe(_ts("2024-07-15 01:00:00"), 85.0)  # kill trips (15% dd)
    gate.observe(_ts("2024-07-16 00:00:00"), 60.0)  # new Paris day, huge loss, but killed
    assert gate.daily_halted is False
    assert gate._bar_trip is None
    assert gate.stateful_summary()["daily_trips"] == []


# --- apply: force-flat + extras shape ---


def test_apply_forces_flat_when_daily_halted():
    gate = PortfolioRiskGate({"daily_loss_limit": {"threshold": 0.05}})
    gate.observe(_ts("2024-07-15 00:00:00"), 100.0)
    gate.observe(_ts("2024-07-15 01:00:00"), 90.0)  # trip
    final, extras = gate.apply(2.0)
    assert final == 0.0
    assert extras["risk_daily_halted"] is True
    assert extras["risk_cap_clamped"] is False  # the halt, not the cap, zeroed it


def test_cap_only_extras_are_pr1_shape():
    # A cap-only gate must not leak the stateful columns -- its extras stay exactly
    # PR-1's pair so zoneinfo is never touched and PR-1 output is unchanged.
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    _, extras = gate.apply(2.0)
    assert set(extras) == {"risk_target_raw", "risk_cap_clamped"}


def test_dd_only_extras_have_no_daily_columns():
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}})
    gate.observe(_ts("2024-04-01 00:00:00"), 100.0)
    _, extras = gate.apply(0.5)
    assert set(extras) == {"risk_target_raw", "risk_cap_clamped", "risk_killed", "risk_drawdown", "risk_trip"}
    assert "risk_daily_halted" not in extras


def test_dl_only_extras_have_no_drawdown_columns():
    gate = PortfolioRiskGate({"daily_loss_limit": {"threshold": 0.05}})
    gate.observe(_ts("2024-07-15 00:00:00"), 100.0)
    _, extras = gate.apply(0.5)
    assert set(extras) == {"risk_target_raw", "risk_cap_clamped", "risk_daily_halted", "risk_daily_loss", "risk_trip"}
    assert "risk_killed" not in extras


# --- fail-loud degenerate equity ---


@pytest.mark.parametrize("bad", [0.0, -1.0, float("nan"), float("inf")])
def test_observe_raises_on_degenerate_equity(bad):
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}})
    with pytest.raises(ValueError, match="non-finite/non-positive equity"):
        gate.observe(_ts("2024-04-01 00:00:00"), bad)


def test_cap_only_observe_ignores_equity():
    # A cap-only gate never reads equity, so a degenerate equity must NOT raise
    # (observe is a no-op) -- guards against validating equity a control doesn't use.
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    gate.observe(_ts("2024-04-01 00:00:00"), float("nan"))  # no raise
    assert gate.apply(2.0)[0] == 1.0


# --- stateful_summary shape ---


def test_stateful_summary_empty_for_cap_only():
    assert PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}}).stateful_summary() == {}


def test_stateful_summary_no_trips():
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}})
    gate.observe(_ts("2024-04-01 00:00:00"), 100.0)
    s = gate.stateful_summary()
    assert s == {"n_bars_killed": 0, "first_trip": None, "daily_trips": []}


# =========================================================================
# PR-2: kill-path routing through TradingBot (the min-Δ bypass trap)
# =========================================================================
#
# Stub-driven (no backtest engine, no I/O): drives
# _process_symbol_candle_completion directly, same technique as
# tests/test_funding_accrual.py, to prove the forced flatten bypasses the RiskManager
# min-Δ band. The single most important mechanical trap for the kill switch
# (Phase-A Q1): a residual position smaller than the 0.2 min-Δ threshold must still be
# flattened.

import logging  # noqa: E402

from core.trading_bot import TradingBot  # noqa: E402
from execution.portfolio_info import MockPortfolioInfo  # noqa: E402
from risk.risk_manager import RiskManager  # noqa: E402


class _Signal:
    def __init__(self, forecast):
        self.forecast = forecast


class _Strategy:
    def __init__(self, forecast):
        self._f = forecast

    def update(self, data):
        pass

    def generate_signals(self):
        return _Signal(self._f)


class _Forecast:
    """The real forecast arithmetic: target = forecast/10, Δ = target - previous."""

    def forecast_to_allocation(self, forecast):
        return forecast / 10.0

    def calculate_allocation_change(self, target, previous):
        return target - previous


class _CaptureExec:
    """Records every _execute_portfolio_rebalance call; returns a configurable success."""

    def __init__(self, success=True):
        self.calls = []
        self.success = success

    def _execute_portfolio_rebalance(self, **kwargs):
        self.calls.append(kwargs)
        return self.success, {"stub": True}


class _FixedPortfolio(MockPortfolioInfo):
    """Reports a fixed decision-time equity and a fixed current allocation, so a bar
    can be posed with a chosen |previous_allocation| and a chosen drawdown."""

    def __init__(self, equity, allocation):
        super().__init__(initial_balance={"USDT": {"free": equity, "locked": 0.0}})
        self._equity = equity
        self._allocation = allocation

    def set_equity(self, equity):
        self._equity = equity

    def _calculate_total_portfolio_value(self, balances, close):
        return self._equity

    def _calculate_actual_allocation(self, close, balances, total_value, symbol):
        return self._allocation


class _Tracker:
    def __init__(self):
        self.rows = []

    def record_state(self, **kwargs):
        self.rows.append(kwargs)


def _bar_df(ts, close=20000.0):
    return pd.DataFrame({"timestamp": [pd.Timestamp(ts)], "close": [close]})


class _DM:
    def __init__(self):
        self.candle_builder = object()
        self._bar = None

    def set_bar(self, bar):
        self._bar = bar

    def get_data_history(self, symbol, count=1):
        return self._bar


def _bot(portfolio, gate, exec_handler, tracker):
    # Real RiskManager with the production band (min 0.2 / max 4.0): the mutation that
    # routes the forced flatten through approve_allocation_change is rejected by this
    # min control, which is exactly what the trap test detects.
    rm = RiskManager(
        controls_cfg={
            "max_allocation_change": {"max": 4.0},
            "min_allocation_change": {"threshold": 0.2},
        }
    )
    return TradingBot(
        data_manager=_DM(),
        strategy=_Strategy(forecast=20.0),  # wants +2.0; the kill overrides it to 0
        execution_handler=exec_handler,
        logger=logging.getLogger("test_risk_gate_routing"),
        portfolio_info=portfolio,
        portfolio_state_tracker=tracker,
        forecast_manager=_Forecast(),
        risk_manager=rm,
        performance_tracker=None,
        symbols=["BTCUSDT"],
        risk_gate=gate,
    )


def _drive(bot, ts, equity, close=20000.0):
    bot.portfolio_info.set_equity(equity)
    bot.data_manager.set_bar(_bar_df(ts, close))
    bot._process_symbol_candle_completion("BTCUSDT")


def test_kill_flattens_residual_below_min_delta_band():
    """THE TRAP (Phase-A Q1): |previous_allocation| = 0.1 < the 0.2 min-Δ threshold.
    When the drawdown kill trips, the forced flatten (Δ = -0.1) MUST execute via the
    direct path. Mutation: route it through approve_allocation_change -> the real
    RiskManager min control rejects |Δ|=0.1 -> no exec call -> this test fails, proving
    the bypass is load-bearing."""
    portfolio = _FixedPortfolio(equity=100.0, allocation=0.1)
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}})
    execn = _CaptureExec(success=True)
    bot = _bot(portfolio, gate, execn, _Tracker())

    _drive(bot, "2024-04-01 00:00:00", equity=100.0)  # sets peak, no trip
    assert gate.killed is False
    execn.calls.clear()  # only the TRIP bar matters; discard the pre-trip rebalance

    _drive(bot, "2024-04-01 01:00:00", equity=70.0)  # 30% drawdown -> kill trips
    assert gate.killed is True
    assert len(execn.calls) == 1, "forced flatten must execute despite |Δ|=0.1 < 0.2"
    assert execn.calls[0]["target_allocation"] == 0.0
    assert execn.calls[0]["allocation_change"] == pytest.approx(-0.1)


def test_failed_flatten_retries_next_bar_through_bypass():
    """A flatten that returns success=False on the trip bar retries on the next bar
    through the same direct bypass (routing keys off the latch, not 'tripped this
    bar'). Mutation: gate the retry on 'tripped this bar' -> the second bar does not
    re-attempt -> this fails."""
    portfolio = _FixedPortfolio(equity=100.0, allocation=0.1)
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}})
    execn = _CaptureExec(success=False)  # flatten keeps failing
    bot = _bot(portfolio, gate, execn, _Tracker())

    _drive(bot, "2024-04-01 00:00:00", equity=100.0)
    execn.calls.clear()
    _drive(bot, "2024-04-01 01:00:00", equity=70.0)  # trip -> flatten attempt (fails)
    _drive(bot, "2024-04-01 02:00:00", equity=72.0)  # still latched -> retry
    assert len(execn.calls) == 2
    assert all(c["target_allocation"] == 0.0 for c in execn.calls)


def test_kill_records_flatten_success_not_none():
    """The forced-flatten path records the bypass call's real success (not None, which
    the per-bar ternary would give since approved_rebalance stays None). Mutation: drop
    'or risk_forced_flat' from the record ternary -> succcess reads None -> fails."""
    portfolio = _FixedPortfolio(equity=100.0, allocation=0.1)
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}})
    execn = _CaptureExec(success=True)
    tracker = _Tracker()
    bot = _bot(portfolio, gate, execn, tracker)

    _drive(bot, "2024-04-01 00:00:00", equity=100.0)
    _drive(bot, "2024-04-01 01:00:00", equity=70.0)  # kill trips + flatten
    trip_row = tracker.rows[-1]
    assert trip_row["succcess_execute_portfolio_rebalance"] is True
    assert trip_row["approved_rebalance"] is None  # approval was never consulted
    assert trip_row["risk_killed"] is True
