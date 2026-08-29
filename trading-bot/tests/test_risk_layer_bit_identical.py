"""
Integration tests for the fix/risk-layer PR-1 wiring: run_backtest(risk_controls=...)
-> BacktestEngine -> TradingBot per-bar gate -> provenance fold + metrics block.

Two contracts, both driven end to end through the real engine on the 1h reference
window (same scenario as test_bar_equity_bit_identical.py), hence slow + cache-guarded:

  GATE OFF is byte-identical. Omitting risk_controls (default), passing None
  explicitly, and passing {} (empty = no controls) must all produce the SAME
  metrics.json / portfolio_states.csv / bars.csv / trades.json, byte for byte, as
  today's behavior -- the off path builds no gate and the per-bar hook is never
  entered. The off run also reproduces the committed baseline dir hash 5ccbec42
  (reference_run.json), proving the provenance fold is a true no-op when off.
  Mutation bite: adding a risk_cap_clamped extra unconditionally (gate off) or
  folding risk_management into a gate-off run changes bars.csv / the dir hash and
  fails these.

  GATE ON bites and is distinguishable. A cap below the strategy's ~2.0 long
  exposure clamps it: metrics.json gains a risk_controls block, bars.csv gains a
  risk_cap_clamped column with >= 1 clamp, the manifest config_sha256 (and dir hash)
  differ from the off run, and post-rebalance exposure never exceeds the cap. The
  collision guard raises when a strategy config already carries a risk_management key
  and a gate is active (a silent fold would mask a real difference in run identity).

SLOW INTEGRATION TEST. Run explicitly:
  pytest tests/test_risk_layer_bit_identical.py -v -m slow --timeout=0
"""

import json
import sys
from pathlib import Path

import pandas as pd
import pytest
from _cache_guard import cache_skip_reason

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

START, END, SYMBOL = "2024-04-01", "2024-05-30", "BTCUSDT"
BASELINE_CONFIG_SHA8 = "5ccbec42"  # committed strategy_config.json canonical hash

_NEEDED_CACHES = ("BTCUSDT_1h.csv", "BTCUSDT_funding_8h.csv", "fear_greed_daily.csv")
_CACHE_SKIP = cache_skip_reason(PROJECT_ROOT / "local_data", _NEEDED_CACHES, START, END)
pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(
        _CACHE_SKIP is not None, reason=_CACHE_SKIP or "local_data caches usable"
    ),
]


def _run(tmp_dir, **kwargs):
    from core.launcher import run_backtest

    run_dir = run_backtest(
        config_path=str(PROJECT_ROOT / "strategy_config.json"),
        symbol=SYMBOL,
        start=START,
        end=END,
        results_root=str(tmp_dir),
        trades_log_file=str(Path(tmp_dir) / "interim_trades.json"),
        **kwargs,
    )
    return Path(run_dir)


# --- gate-off byte-identity ---


@pytest.fixture(scope="module")
def off_default(tmp_path_factory):
    return _run(tmp_path_factory.mktemp("off_default"))


@pytest.fixture(scope="module")
def off_explicit_none(tmp_path_factory):
    return _run(tmp_path_factory.mktemp("off_none"), risk_controls=None)


@pytest.fixture(scope="module")
def off_empty_block(tmp_path_factory):
    return _run(tmp_path_factory.mktemp("off_empty"), risk_controls={})


_IDENTITY_FILES = ("metrics.json", "portfolio_states.csv", "bars.csv", "trades.json")


@pytest.mark.parametrize("fname", _IDENTITY_FILES)
def test_explicit_none_matches_omitted(off_default, off_explicit_none, fname):
    """risk_controls=None must be byte-identical to omitting it (guards the default)."""
    assert (off_default / fname).read_text() == (off_explicit_none / fname).read_text()


@pytest.mark.parametrize("fname", _IDENTITY_FILES)
def test_empty_block_matches_omitted(off_default, off_empty_block, fname):
    """risk_controls={} (explicit no controls) must be byte-identical to omitting it --
    an empty block builds no gate, so no columns/keys are added."""
    assert (off_default / fname).read_text() == (off_empty_block / fname).read_text()


def test_gate_off_omits_risk_controls_key(off_default):
    """No gate -> metrics.json has NO risk_controls key at all (not empty/null)."""
    metrics = json.loads((off_default / "metrics.json").read_text())
    assert "risk_controls" not in metrics


def test_gate_off_bars_have_no_risk_columns(off_default):
    bars = pd.read_csv(off_default / "bars.csv")
    assert "risk_cap_clamped" not in bars.columns
    assert "risk_target_raw" not in bars.columns


def test_gate_off_reproduces_committed_baseline_hash(off_default):
    """The off run's provenance is byte-identical to today's: the dir-name config hash
    AND the manifest config_sha256 match the committed baseline (5ccbec42)."""
    assert off_default.name.split("_")[-1] == BASELINE_CONFIG_SHA8
    manifest = json.loads((off_default / "manifest.json").read_text())
    assert manifest["config_sha256"].startswith(BASELINE_CONFIG_SHA8)
    assert "risk_management" not in manifest["config"]


# --- gate-on: cap bites and is distinguishable ---


@pytest.fixture(scope="module")
def on_cap(tmp_path_factory):
    # cap 1.0 sits below the reference strategy's ~2.0 long exposure, so it must clamp.
    return _run(
        tmp_path_factory.mktemp("on_cap"),
        risk_controls={"absolute_allocation_cap": {"cap": 1.0}},
    )


def test_cap_run_has_risk_controls_metrics_block(on_cap):
    metrics = json.loads((on_cap / "metrics.json").read_text())
    block = metrics.get("risk_controls")
    assert block is not None
    assert block["portfolio_controls"] == {"absolute_allocation_cap": {"cap": 1.0}}
    assert block["n_cap_clamped_bars"] >= 1


def test_cap_run_records_clamp_column_matching_metrics(on_cap):
    bars = pd.read_csv(on_cap / "bars.csv")
    assert "risk_cap_clamped" in bars.columns
    n_clamped = int(bars["risk_cap_clamped"].sum())
    metrics = json.loads((on_cap / "metrics.json").read_text())
    assert n_clamped == metrics["risk_controls"]["n_cap_clamped_bars"] >= 1


def test_cap_run_never_exceeds_cap(on_cap):
    """The whole point: post-rebalance exposure is held at or below the cap."""
    bars = pd.read_csv(on_cap / "bars.csv")
    assert bars["postRebalance_current_allocation"].abs().max() <= 1.0 + 1e-9


def test_cap_run_provenance_differs_from_off(on_cap, off_default):
    """Two runs differing only in risk controls are DISTINGUISHABLE (closes the #54
    defect class for this feature): different dir hash and different config_sha256."""
    assert on_cap.name.split("_")[-1] != off_default.name.split("_")[-1]
    man_on = json.loads((on_cap / "manifest.json").read_text())
    man_off = json.loads((off_default / "manifest.json").read_text())
    assert man_on["config_sha256"] != man_off["config_sha256"]
    assert man_on["config"]["risk_management"] == {
        "portfolio_controls": {"absolute_allocation_cap": {"cap": 1.0}}
    }


# --- fold-collision guard ---


def test_fold_collision_guard_raises(tmp_path):
    """A strategy config that already carries a risk_management key, run with a gate
    active, must raise rather than silently overwrite it in run identity. Mutation:
    delete the guard in backtester._end_of_backtest -> the planted key is silently
    folded over and this run completes without raising -> test fails."""
    from core.launcher import run_backtest

    base = json.loads((PROJECT_ROOT / "strategy_config.json").read_text())
    base["risk_management"] = {
        "portfolio_controls": {"absolute_allocation_cap": {"cap": 9.9}}
    }
    planted = tmp_path / "planted_strategy_config.json"
    planted.write_text(json.dumps(base))

    with pytest.raises(ValueError, match="already carries a risk_management key"):
        run_backtest(
            config_path=str(planted),
            symbol=SYMBOL,
            start=START,
            end=END,
            results_root=str(tmp_path / "run"),
            trades_log_file=str(tmp_path / "run_t.json"),
            risk_controls={"absolute_allocation_cap": {"cap": 1.0}},
        )


# --- PR-2: cap-only run carries NO stateful columns (new keys' absence) ---


def test_cap_only_run_has_no_stateful_columns(on_cap):
    """A cap-only gate must not leak the PR-2 stateful columns/metrics -- proof the new
    keys' absence is byte-clean end to end, so PR-1's cap behaviour is unchanged under
    PR-2 code."""
    bars = pd.read_csv(on_cap / "bars.csv")
    for col in (
        "risk_killed",
        "risk_daily_halted",
        "risk_drawdown",
        "risk_daily_loss",
        "risk_trip",
    ):
        assert col not in bars.columns, col
    block = json.loads((on_cap / "metrics.json").read_text())["risk_controls"]
    for key in ("n_bars_killed", "n_bars_daily_halted", "first_trip", "daily_trips"):
        assert key not in block, key


# --- PR-2: max_drawdown_kill bites end to end ---


@pytest.fixture(scope="module")
def on_kill(tmp_path_factory):
    # The reference window draws down ~24%, so a 5% kill trips well inside it.
    return _run(
        tmp_path_factory.mktemp("on_kill"),
        risk_controls={"max_drawdown_kill": {"threshold": 0.05}},
    )


def test_kill_run_metrics_block(on_kill):
    block = json.loads((on_kill / "metrics.json").read_text())["risk_controls"]
    assert block["portfolio_controls"] == {"max_drawdown_kill": {"threshold": 0.05}}
    assert block["n_bars_killed"] >= 1
    assert block["first_trip"]["control"] == "max_drawdown_kill"
    assert block["daily_trips"] == []  # no daily control configured


def test_kill_run_latches_and_flattens(on_kill):
    """Once risk_killed goes True it stays True (latch) and exposure is held flat for
    the rest of the run."""
    bars = pd.read_csv(on_kill / "bars.csv")
    assert "risk_killed" in bars.columns
    killed = bars["risk_killed"].astype(bool)
    assert bool(killed.any()), "the kill must trip on this drawdown window"
    first = killed.idxmax()
    assert bool(killed.loc[first:].all()), "kill must latch (never un-set) once tripped"
    # From the trip bar onward the book is forced flat: exposure collapses from the
    # strategy's ~2.0 long toward 0 and stays there.
    assert bars.loc[first:, "postRebalance_current_allocation"].abs().max() < 0.1


def test_kill_run_metrics_matches_bars_count(on_kill):
    """The gate-owned n_bars_killed equals the recorded risk_killed count (the book is
    flat at run end, so no end-of-run row replacement perturbs the last bar)."""
    bars = pd.read_csv(on_kill / "bars.csv")
    block = json.loads((on_kill / "metrics.json").read_text())["risk_controls"]
    assert int(bars["risk_killed"].astype(bool).sum()) == block["n_bars_killed"]


def test_kill_run_provenance_differs_from_off(on_kill, off_default):
    assert on_kill.name.split("_")[-1] != off_default.name.split("_")[-1]
    man_on = json.loads((on_kill / "manifest.json").read_text())
    assert man_on["config"]["risk_management"] == {
        "portfolio_controls": {"max_drawdown_kill": {"threshold": 0.05}}
    }
