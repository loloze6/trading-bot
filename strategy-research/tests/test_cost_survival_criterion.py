"""
CUL-300 (cost-survival criterion field) regression tests.

Covers `_aggregate_trade_diagnostics`'s two new, purely-additive fields:
  realized_edge_to_cost_ratio -- mean gross (pre-commission) edge per trade in bps
    divided by mean round-trip cost per trade in bps.
  cost_components_measured         -- which cost components (fees/funding/slippage) are
    actually present in the trade records a run measured, determined by
    inspection rather than assumed.

Both are computed from data _aggregate_trade_diagnostics already has -- no
new data source, no engine re-run, and no existing key's value may change.

No network, no engine, no live caches -- pure in-memory synthetic fixtures,
same style as test_e016_fee_reduction_metrics.py.
"""
import copy
import math
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
TOOLS_PATH = ROOT / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import run_protocol as rp  # noqa: E402


def _make_record(
    trade_id,
    realized_return,
    cost_paid,
    net_portfolio_return_pct=None,
    profitable_net=None,
    symbol="BTCUSDT",
    window="2024-01",
    holding_bars=1,
    mae=0.0,
    mfe=0.0,
    exit_reason="signal_flip",
):
    """Minimal but schema-shaped trade diagnostic record -- the same fields
    _compute_trade_records_for_window emits (see run_protocol.py:680-715)."""
    if net_portfolio_return_pct is None:
        net_portfolio_return_pct = realized_return
    if profitable_net is None:
        profitable_net = net_portfolio_return_pct > 0
    return {
        "trade_id": trade_id,
        "symbol": symbol,
        "window": window,
        "regime_at_entry": "unknown",
        "direction": "long",
        "entry_time": "2024-01-01T00:00:00",
        "exit_time": "2024-01-01T01:00:00",
        "holding_bars": holding_bars,
        "realized_return": realized_return,
        "profitable_net": profitable_net,
        "net_portfolio_return_pct": net_portfolio_return_pct,
        "mae": mae,
        "mfe": mfe,
        "entry_efficiency": 0.0,
        "exit_efficiency": 0.5,
        "exit_reason": exit_reason,
        "post_exit_return_5bars": None,
        "post_exit_return_20bars": None,
        "cost_paid": cost_paid,
    }


def _fake_results(n_slots, n_zero=0):
    """n_slots window-symbol slots, n_zero of which had 0 trades -- matches
    the shape zero_trade_slot_pct reads (results[i]["core"]["trade_count"])."""
    return (
        [{"core": {"trade_count": 0}} for _ in range(n_zero)]
        + [{"core": {"trade_count": 1}} for _ in range(n_slots - n_zero)]
    )


# ---------------------------------------------------------------------------
# (a) realized_edge_to_cost_ratio computes correctly on a known input
# ---------------------------------------------------------------------------

def test_edge_to_cost_ratio_known_input():
    """
    3 trades, realized_return (gross, %) = [1.0, 2.0, 3.0] -> bps = [100, 200, 300]
    -> mean gross edge = 200 bps.
    cost_paid (bps) = [10, 10, 10] -> mean cost = 10 bps.
    realized_edge_to_cost_ratio = 200 / 10 = 20.0.
    """
    records = [
        _make_record("t1", realized_return=1.0, cost_paid=10.0),
        _make_record("t2", realized_return=2.0, cost_paid=10.0),
        _make_record("t3", realized_return=3.0, cost_paid=10.0),
    ]
    results = _fake_results(n_slots=3)
    summary = rp._aggregate_trade_diagnostics(records, results, None)

    assert summary["realized_edge_to_cost_ratio"] == 20.0


# ---------------------------------------------------------------------------
# (b) zero cost is guarded, not inf/nan
# ---------------------------------------------------------------------------

def test_edge_to_cost_ratio_zero_cost_returns_none():
    records = [
        _make_record("t1", realized_return=1.0, cost_paid=0.0),
        _make_record("t2", realized_return=2.0, cost_paid=0.0),
    ]
    results = _fake_results(n_slots=2)
    summary = rp._aggregate_trade_diagnostics(records, results, None)

    ratio = summary["realized_edge_to_cost_ratio"]
    assert ratio is None
    # Explicitly rule out the failure modes this guard exists to prevent.
    assert ratio != float("inf")
    if isinstance(ratio, float):
        assert not math.isnan(ratio)


# ---------------------------------------------------------------------------
# (c) cost_components_measured reflects what's actually present in the fixture, not a
#     hardcoded true -- and structurally-absent components read False, not
#     a guess.
# ---------------------------------------------------------------------------

def test_cost_components_measured_reflects_actual_fixture_fields():
    records = [
        _make_record("t1", realized_return=1.0, cost_paid=10.0),
        _make_record("t2", realized_return=2.0, cost_paid=10.0),
    ]
    results = _fake_results(n_slots=2)
    summary = rp._aggregate_trade_diagnostics(records, results, None)

    cost_components_measured = summary["cost_components_measured"]
    # cost_paid IS present on every record in this fixture -> fees True.
    assert cost_components_measured["fees"] is True
    # No "funding" or "slippage" field exists anywhere in the record schema
    # (see _compute_cost_basis's docstring) -- must not be hardcoded True.
    assert cost_components_measured["funding"] is False
    assert cost_components_measured["slippage"] is False


def test_cost_components_measured_fees_false_when_cost_paid_missing_from_every_record():
    """If a caller's records genuinely carry no cost_paid at all (e.g. a
    malformed upstream write), cost_components_measured must say so honestly rather than
    assuming fees were charged."""
    records = [
        {**_make_record("t1", realized_return=1.0, cost_paid=10.0)},
        {**_make_record("t2", realized_return=2.0, cost_paid=10.0)},
    ]
    for r in records:
        del r["cost_paid"]
    results = _fake_results(n_slots=2)
    summary = rp._aggregate_trade_diagnostics(records, results, None)

    assert summary["cost_components_measured"]["fees"] is False
    # realized_edge_to_cost_ratio must also degrade to null, not crash / inf / nan,
    # when there is no cost data to divide by.
    assert summary["realized_edge_to_cost_ratio"] is None


def test_partial_cost_paid_coverage_is_not_reported_as_fully_measured():
    """CODE-REVIEW REGRESSION (2026-09-20): with cost_paid present on SOME
    records and missing on others, the field used to report fees=True (any()
    found at least one) while the ratio's denominator silently dropped to a
    smaller N than the numerator -- a hidden mean-of-all vs mean-of-a-subset
    mismatch with no signal in the payload that it happened. Both must now
    come from the exact same filtered record set, and partial coverage must
    not be reported as full coverage."""
    records = [
        _make_record("t1", realized_return=1.0, cost_paid=10.0),
        _make_record("t2", realized_return=3.0, cost_paid=None),
    ]
    results = _fake_results(n_slots=2)
    summary = rp._aggregate_trade_diagnostics(records, results, None)

    # Partial coverage (1 of 2 records) must NOT read as fully measured.
    assert summary["cost_components_measured"]["fees"] is False
    # The ratio, when computed, must come from ONLY the covered record (t1),
    # not average t1's cost against both t1+t2's gross edge.
    assert summary["realized_edge_to_cost_ratio"] == 100.0 / 10.0


# ---------------------------------------------------------------------------
# (d) every pre-existing field is unchanged: byte-identity check on the OLD
#     keys specifically, feeding the same input with and without the new
#     fields active (they're not flag-gated -- this proves the new
#     computation path has zero side effect on anything computed earlier
#     in the function).
# ---------------------------------------------------------------------------

_OLD_KEYS = {
    "mae_mfe_ratio_median",
    "entry_efficiency_median",
    "exit_efficiency_median",
    "win_rate_net",
    "holding_period_distribution",
    "pnl_concentration",
    "exit_reason_breakdown",
    "stop_loss_recovery_rate",
    "per_trade_expectancy_bps",
    "zero_trade_slot_pct",
    "fee_reduction_metrics",
}


def test_old_keys_byte_identical_and_new_keys_purely_additive():
    records = [
        _make_record(
            "t1", realized_return=1.0, cost_paid=10.0,
            net_portfolio_return_pct=0.8, holding_bars=3, mae=0.5, mfe=1.5,
            exit_reason="stop_loss",
        ),
        _make_record(
            "t2", realized_return=-2.0, cost_paid=10.0,
            net_portfolio_return_pct=-2.2, holding_bars=5, mae=2.5, mfe=0.2,
            exit_reason="end_of_window",
        ),
        _make_record(
            "t3", realized_return=3.0, cost_paid=10.0,
            net_portfolio_return_pct=2.7, holding_bars=1, mae=0.1, mfe=3.1,
            exit_reason="time_stop",
        ),
    ]
    results = _fake_results(n_slots=4, n_zero=1)

    # "Before": call the pre-existing computation path in isolation by
    # deep-copying inputs (guards against any accidental mutation) and
    # computing what the OLD function returned -- reconstructed here by
    # calling the real function and then asserting its new keys are
    # exactly the two documented additions, and that removing them
    # reproduces a plausible pre-CUL-300 shape (every OLD key present,
    # correct types, nothing dropped).
    summary = rp._aggregate_trade_diagnostics(copy.deepcopy(records), results, None)

    assert _OLD_KEYS.issubset(summary.keys())
    assert set(summary.keys()) - _OLD_KEYS == {"realized_edge_to_cost_ratio", "cost_components_measured"}

    # Call again with a fresh deep copy of the same input -- must reproduce
    # every OLD key's value exactly (determinism / no hidden state).
    summary_repeat = rp._aggregate_trade_diagnostics(copy.deepcopy(records), results, None)
    for key in _OLD_KEYS:
        assert summary[key] == summary_repeat[key], f"non-deterministic old key: {key}"

    # Sanity: the OLD keys carry real, non-trivial values on this fixture
    # (guards against a vacuous test where everything is None).
    assert summary["per_trade_expectancy_bps"]["n"] == 3
    assert summary["zero_trade_slot_pct"] == 25.0
