"""
CUL-275 (route-mode tiebreak) regression tests.

Red-team finding on E-016 (fee-reduction autopsy): `evaluate_against_decision_rules()`
in `strategy-research/tools/run_protocol.py` used to compute
`post_backtest_route_real = statistics.mode(_routes_real) if _routes_real else None`.
`statistics.mode()` does not raise or flag a tie -- on equal counts it silently
returns whichever value appears FIRST in the input list, which depends purely on
`for symbol in symbols: for window in protocol["windows"]` iteration order. The
same underlying per-window routes, reordered, could therefore produce a
DIFFERENT `post_backtest_route_real` (and therefore a different
`cost_dominated_real`), with nothing anywhere signaling that the result was
actually a coin flip.

The fix, `_resolve_tied_route()`:
  - detects a genuine tie for most-common via collections.Counter
  - returns a `tied: bool` flag alongside the winning route
  - on a tie, resolves the winner via a documented, fixed precedence order
    (`_ROUTE_TIE_PRECEDENCE`) instead of list order

These tests prove:
  1. `_resolve_tied_route` directly, on the exact adversarial shape the
     reviewer found (a tie), in two different orderings: the tied flag is
     True in both, and the winning route is IDENTICAL in both -- i.e. the
     precedence rule is actually being applied, not just re-deriving
     Python's arbitrary first-element behavior under a different name.
  2. A non-tied, clear-majority case is unaffected (normal behavior).
  3. The wiring into `evaluate_against_decision_rules()`'s `diagnostics`
     dict: `post_backtest_route_real` and the new
     `post_backtest_route_real_tied` land correctly and are order-independent
     end-to-end, not just at the helper-function level.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
TOOLS_PATH = ROOT / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import run_protocol as rp  # noqa: E402 -- also puts trading-bot/ on sys.path


# ---------------------------------------------------------------------------
# 1. _resolve_tied_route -- the adversarial tie case, two orderings
# ---------------------------------------------------------------------------

def test_resolve_tied_route_2v2_tie_order_independent():
    """
    2-2 tie: kill_cost_hurdle x2, proceed_to_interpretation x2.

    Under the OLD `statistics.mode()` behavior this is exactly the reviewer's
    adversarial case: order A's first element is 'kill_cost_hurdle' (mode
    would return that), order B's first element is 'proceed_to_interpretation'
    (mode would return THAT instead) -- same data, different answer.

    _ROUTE_TIE_PRECEDENCE ranks kill_cost_hurdle (index 2) ahead of
    proceed_to_interpretation (index 4), so the fix must resolve to
    'kill_cost_hurdle' in BOTH orderings, and must report tied=True in both.
    """
    order_a = [
        "kill_cost_hurdle", "kill_cost_hurdle",
        "proceed_to_interpretation", "proceed_to_interpretation",
    ]
    order_b = [
        "proceed_to_interpretation", "proceed_to_interpretation",
        "kill_cost_hurdle", "kill_cost_hurdle",
    ]

    route_a, tied_a = rp._resolve_tied_route(order_a)
    route_b, tied_b = rp._resolve_tied_route(order_b)

    assert tied_a is True
    assert tied_b is True
    assert route_a == route_b == "kill_cost_hurdle"


def test_resolve_tied_route_2v1v1_tie_order_independent():
    """
    2-1-1(-ish) tie among the top two: refine_cost_hurdle x2 and
    proceed_to_interpretation x2 tie for most-common; kill_no_ic and
    refine_inverted_ic each appear once (below the tied top count, so they
    are not tie candidates, just noise proving the tie-detection isn't
    fooled by extra distinct values).

    _ROUTE_TIE_PRECEDENCE ranks refine_cost_hurdle (index 3) ahead of
    proceed_to_interpretation (index 4) -- both orderings must resolve to
    'refine_cost_hurdle' and report tied=True.
    """
    order_a = [
        "refine_cost_hurdle", "proceed_to_interpretation",
        "refine_cost_hurdle", "proceed_to_interpretation",
        "kill_no_ic", "refine_inverted_ic",
    ]
    order_b = [
        "refine_inverted_ic", "kill_no_ic",
        "proceed_to_interpretation", "refine_cost_hurdle",
        "proceed_to_interpretation", "refine_cost_hurdle",
    ]

    route_a, tied_a = rp._resolve_tied_route(order_a)
    route_b, tied_b = rp._resolve_tied_route(order_b)

    assert tied_a is True
    assert tied_b is True
    assert route_a == route_b == "refine_cost_hurdle"


def test_resolve_tied_route_kill_no_ic_outranks_kill_cost_hurdle():
    """
    Precedence is not simply 'kill_* beats refine_*/proceed_*' -- kill_no_ic
    also outranks the OTHER kill route, kill_cost_hurdle, since "no
    detectable signal at all" is a more fundamental problem than "signal is
    real but can't clear costs". Confirms the full precedence order, not
    just the kill-vs-non-kill boundary.
    """
    route, tied = rp._resolve_tied_route(["kill_cost_hurdle", "kill_no_ic"])
    assert tied is True
    assert route == "kill_no_ic"


def test_resolve_tied_route_clear_majority_unaffected():
    """Non-tied case: a clear 3-1 majority must resolve to the majority value
    with tied=False, matching plain-mode behavior (no regression)."""
    routes = ["kill_no_ic", "kill_no_ic", "kill_no_ic", "proceed_to_interpretation"]
    route, tied = rp._resolve_tied_route(routes)
    assert tied is False
    assert route == "kill_no_ic"


def test_resolve_tied_route_empty_list():
    assert rp._resolve_tied_route([]) == (None, False)


def test_resolve_tied_route_single_value_not_tied():
    assert rp._resolve_tied_route(["proceed_to_interpretation"]) == ("proceed_to_interpretation", False)


# ---------------------------------------------------------------------------
# 2. End-to-end wiring through evaluate_against_decision_rules()'s diagnostics
# ---------------------------------------------------------------------------

def _make_results(routes):
    """One minimal `results` row per route value, enough for
    evaluate_against_decision_rules() to run with an empty validation
    protocol and runs_root=None (skips the bootstrap-fallback file I/O
    path entirely -- see _pooled_ic_with_bootstrap_fallback)."""
    return [
        {"symbol": "BTCUSDT", "core": {"post_backtest_route_real": route}}
        for route in routes
    ]


def test_diagnostics_wiring_reports_tied_flag_and_precedence_winner():
    order_a = _make_results([
        "kill_cost_hurdle", "kill_cost_hurdle",
        "proceed_to_interpretation", "proceed_to_interpretation",
    ])
    order_b = _make_results([
        "proceed_to_interpretation", "proceed_to_interpretation",
        "kill_cost_hurdle", "kill_cost_hurdle",
    ])
    per_symbol_summary = {"BTCUSDT": {}}

    verdict_a = rp.evaluate_against_decision_rules(
        per_symbol_summary, order_a, validation_protocol={}, runs_root=None,
    )
    verdict_b = rp.evaluate_against_decision_rules(
        per_symbol_summary, order_b, validation_protocol={}, runs_root=None,
    )

    diag_a = verdict_a["diagnostics"]
    diag_b = verdict_b["diagnostics"]

    assert diag_a["post_backtest_route_real_tied"] is True
    assert diag_b["post_backtest_route_real_tied"] is True
    assert diag_a["post_backtest_route_real"] == diag_b["post_backtest_route_real"] == "kill_cost_hurdle"
    # cost_dominated_real must follow the precedence-resolved route, not flip
    # with ordering either.
    assert diag_a["cost_dominated_real"] is True
    assert diag_b["cost_dominated_real"] is True


def test_diagnostics_wiring_clear_majority_not_tied():
    results = _make_results([
        "proceed_to_interpretation", "proceed_to_interpretation",
        "proceed_to_interpretation", "kill_cost_hurdle",
    ])
    per_symbol_summary = {"BTCUSDT": {}}

    verdict = rp.evaluate_against_decision_rules(
        per_symbol_summary, results, validation_protocol={}, runs_root=None,
    )
    diag = verdict["diagnostics"]

    assert diag["post_backtest_route_real_tied"] is False
    assert diag["post_backtest_route_real"] == "proceed_to_interpretation"
    assert diag["cost_dominated_real"] is False
