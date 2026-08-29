"""
Integration tests for the model_funding wiring (fix/funding-accrual-wiring):
run_backtest(model_funding=...) -> BacktestEngine -> TradingBot's per-bar funding
hook -> execution/portfolio_info.py::apply_funding.

Two contracts, both driven end to end through the real engine and both needing the
local_data caches (hence slow + cache-guarded):

  FLAG OFF is byte-identical. Omitting model_funding must produce the same
  metrics.json AND portfolio_states.csv, byte for byte, as passing
  model_funding=False -- the off path builds no funding series and never enters the
  hook (core/trading_bot.py:205). Proven on the 1h reference window; the mutation
  bite is that flipping the default to True makes this run RAISE on 1h bars (the
  engine rejects sub-daily funding), which both fails the test and proves the flag
  reaches the engine.

  FLAG ON moves money in the funding direction. On a daily window that ends holding a
  LONG, turning model_funding on must change portfolio_states.csv, and at the first
  bar where the two runs diverge the change must carry the sign apply_funding dictates
  (-position_sign * funding_sign) -- a wiring check, not a re-derivation of the accrual
  math (that is unit-tested in test_funding_accrual.py).

SLOW INTEGRATION TEST. Run explicitly:
  pytest tests/test_model_funding_bit_identical.py -v -m slow
"""

import sys
from pathlib import Path

import pandas as pd
import pytest
from _cache_guard import cache_skip_reason

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Flag-off byte-identity runs on the 1h reference window (same scenario as
# test_bar_equity_bit_identical.py). 1h is deliberate: it is the timeframe on which
# model_funding=True is REJECTED, so the mutation bite (flip the default to True)
# turns this run red instead of silently changing output.
IDENT_START, IDENT_END = "2024-04-01", "2024-05-30"
# Flag-on wiring runs on a daily window that ends holding a LONG (found by probing
# bar-by-bar open-position state across 2024-2025; the default strategy_config.json
# holds +2.0 into 2025-03-31). warmup_prefetch warms the 1d strategy so it actually
# holds inside this short window. test_wiring_window_ends_holding_a_long fails loudly
# if that ever stops being true, since a flat window would make the direction check
# vacuous.
WIRE_START, WIRE_END = "2025-03-01", "2025-03-31"
SYMBOL = "BTCUSDT"

_NEEDED_1H = ("BTCUSDT_1h.csv", "BTCUSDT_funding_8h.csv", "fear_greed_daily.csv")
_NEEDED_1D = ("BTCUSDT_1d.csv", "BTCUSDT_funding_8h.csv", "fear_greed_daily.csv")
_CACHE_SKIP = cache_skip_reason(PROJECT_ROOT / "local_data", _NEEDED_1H, IDENT_START, IDENT_END) or cache_skip_reason(
    PROJECT_ROOT / "local_data", _NEEDED_1D, WIRE_START, WIRE_END
)
pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(_CACHE_SKIP is not None, reason=_CACHE_SKIP or "local_data caches usable"),
]


def _run(tmp_dir, **kwargs) -> Path:
    from core.launcher import run_backtest

    run_dir = run_backtest(
        config_path=str(PROJECT_ROOT / "strategy_config.json"),
        symbol=SYMBOL,
        results_root=str(tmp_dir),
        trades_log_file=str(Path(tmp_dir) / "interim_trades.json"),
        **kwargs,
    )
    return Path(run_dir)


# --- flag-off byte-identity (1h) ---


@pytest.fixture(scope="module")
def ident_default(tmp_path_factory):
    return _run(tmp_path_factory.mktemp("ident_default"), start=IDENT_START, end=IDENT_END)


@pytest.fixture(scope="module")
def ident_explicit_false(tmp_path_factory):
    return _run(
        tmp_path_factory.mktemp("ident_false"),
        start=IDENT_START,
        end=IDENT_END,
        model_funding=False,
    )


def test_default_omitted_matches_explicit_false_metrics(ident_default, ident_explicit_false):
    """model_funding omitted (default) must yield a BYTE-IDENTICAL metrics.json to
    model_funding=False -- compares raw file text, not parsed dicts."""
    assert (ident_default / "metrics.json").read_text() == (ident_explicit_false / "metrics.json").read_text()


def test_default_omitted_matches_explicit_false_portfolio_states(ident_default, ident_explicit_false):
    """Same byte-identity contract for the per-bar portfolio_states.csv -- the series
    the funding hook would perturb if the off path were not a true no-op."""
    assert (ident_default / "portfolio_states.csv").read_text() == (
        ident_explicit_false / "portfolio_states.csv"
    ).read_text()


# --- flag-on wiring (1d) ---


@pytest.fixture(scope="module")
def wire_off(tmp_path_factory):
    run_dir = _run(
        tmp_path_factory.mktemp("wire_off"),
        start=WIRE_START,
        end=WIRE_END,
        interval_seconds=86400,
        warmup_prefetch=True,
        holdout_start="2026-01-01",
    )
    return pd.read_csv(run_dir / "portfolio_states.csv")


@pytest.fixture(scope="module")
def wire_on(tmp_path_factory):
    run_dir = _run(
        tmp_path_factory.mktemp("wire_on"),
        start=WIRE_START,
        end=WIRE_END,
        interval_seconds=86400,
        warmup_prefetch=True,
        holdout_start="2026-01-01",
        model_funding=True,
    )
    return pd.read_csv(run_dir / "portfolio_states.csv")


def test_wiring_runs_produce_aligned_bar_series(wire_off, wire_on):
    """Both runs must cover the same bars, so a per-bar diff is meaningful."""
    assert len(wire_off) == len(wire_on) > 0
    assert (wire_off["timestamp"].values == wire_on["timestamp"].values).all()


def test_wiring_window_ends_holding_a_long(wire_off):
    """Anti-vacuity: the funding hook only bites while a position is open, so this
    window must hold one (a LONG here). A flat window would make the direction check
    below pass on an empty diff -- re-probe for a holding window if this fails."""
    held = wire_off["previous_allocation"][wire_off["previous_allocation"].abs() > 1e-9]
    assert len(held) >= 1 and (held > 0).all(), (
        f"{WIRE_START}..{WIRE_END} no longer holds a long position; re-probe for a "
        f"daily window that ends holding one (held allocations: {held.tolist()})"
    )


def test_model_funding_on_changes_portfolio_states(wire_off, wire_on):
    """Wiring proof: with nothing changed but the flag, the per-bar total-value series
    must differ -- the flag reaches apply_funding and moves USDT. If the hook were not
    wired, the two runs would be identical (the flag-off byte-identity contract above)."""
    off = wire_off["total_portfolio_value"].to_numpy()
    on = wire_on["total_portfolio_value"].to_numpy()
    assert (off != on).any(), (
        "model_funding=True produced an identical total_portfolio_value series to "
        "model_funding=False -- the funding hook never moved USDT"
    )


def test_model_funding_moves_value_in_the_funding_direction(wire_off, wire_on):
    """Direction proof at the first divergence bar. Up to it the two runs are identical,
    so the whole gap is that bar's funding cash flow: sign(on - off) must equal
    -position_sign * funding_sign (apply_funding's rule). Robust to mixed funding signs
    because it reads only the first funded bar, and coarse (sign, not magnitude) -- the
    accrual arithmetic is unit-tested in test_funding_accrual.py."""
    from data.feed_registry import build_daily_funding_series

    off = wire_off["total_portfolio_value"].to_numpy()
    on = wire_on["total_portfolio_value"].to_numpy()
    diverged = [i for i in range(len(off)) if abs(on[i] - off[i]) > 1e-9]
    assert diverged, "no divergence bar -- covered by test_model_funding_on_changes_portfolio_states"
    i = diverged[0]

    pos = wire_off["previous_allocation"].iloc[i]
    assert pos != 0.0, "first-divergence bar holds no position; funding cannot have moved it"

    series = build_daily_funding_series([SYMBOL], str(PROJECT_ROOT / "local_data"), WIRE_START, WIRE_END)[SYMBOL]
    day = pd.Timestamp(wire_off["timestamp"].iloc[i]).normalize()
    f_bar = series.get(day)
    assert f_bar is not None and f_bar != 0.0, (
        f"no funding settlement for {SYMBOL} on {day.date()}; cannot predict direction"
    )

    expected = -(1 if pos > 0 else -1) * (1 if f_bar > 0 else -1)
    observed = 1 if (on[i] - off[i]) > 0 else -1
    assert observed == expected, (
        f"funding moved total_portfolio_value the wrong way at {day.date()}: "
        f"position {pos:+.4f}, f_bar {f_bar:+.6f} -> expected sign {expected}, "
        f"got {observed} (on - off = {on[i] - off[i]:+.6f})"
    )
