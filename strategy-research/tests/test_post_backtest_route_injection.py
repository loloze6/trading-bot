"""
E-039 step 3 / CUL-264 (2026-09-11): _inject_post_backtest_route_into_handoff
surfaces the real, measured post-backtest go/no-go route to verdict_interpreter
as CONTEXT, never a gate -- per Jeremy's explicit decision, every backtest
still gets an LLM pass. Mirrors _inject_regime_context_into_handoff's own
pattern; no dedicated test existed for that precedent to model this on, so
this is a fresh, from-scratch pure-function test suite.
"""
import sys
from pathlib import Path

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402


def _write_handoff(path: Path, content: dict | None = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    rpr.save_yaml(path, content or {"handoff_version": 1, "to_stage": "verdict_interpreter"})


def test_noop_when_handoff_missing(tmp_path):
    handoff_path = tmp_path / "does_not_exist.yaml"
    protocol_result = {"results": [{"core": {"post_backtest_route": "kill_no_ic"}}]}
    rpr._inject_post_backtest_route_into_handoff(handoff_path, protocol_result, "run_x")
    assert not handoff_path.exists()  # never created out of nothing


def test_noop_when_protocol_result_is_none(tmp_path):
    """The prescreen-kill case: no real backtest ran, no protocol_result.yaml
    at all -- the handoff must be left completely untouched."""
    handoff_path = tmp_path / "protocol_to_verdict_interpreter.yaml"
    original = {"handoff_version": 1, "objective": "untouched"}
    _write_handoff(handoff_path, original)
    rpr._inject_post_backtest_route_into_handoff(handoff_path, None, "run_x")
    assert rpr.load_yaml(handoff_path) == original


def test_noop_when_no_window_carries_a_route(tmp_path):
    """protocol_result.yaml exists (a real backtest ran) but neither
    post_backtest_route nor post_backtest_route_real is present on any
    window's core block (e.g. an older run predating CUL-264) -- must not
    inject an empty/misleading context block."""
    handoff_path = tmp_path / "protocol_to_verdict_interpreter.yaml"
    original = {"handoff_version": 1}
    _write_handoff(handoff_path, original)
    protocol_result = {"results": [{"symbol": "BTCUSDT", "core": {"sharpe": 0.4}}]}
    rpr._inject_post_backtest_route_into_handoff(handoff_path, protocol_result, "run_x")
    assert rpr.load_yaml(handoff_path) == original


def test_injects_route_and_informational_constraint(tmp_path):
    handoff_path = tmp_path / "protocol_to_verdict_interpreter.yaml"
    _write_handoff(handoff_path)
    protocol_result = {
        "results": [
            {"symbol": "BTCUSDT", "window_label": "2024-01",
             "core": {"post_backtest_route": "kill_no_ic",
                       "post_backtest_route_rationale": "p_value=0.42 >= 0.10"}},
        ],
    }
    rpr._inject_post_backtest_route_into_handoff(handoff_path, protocol_result, "run_x")
    handoff = rpr.load_yaml(handoff_path)

    assert handoff["post_backtest_routes"] == [
        {"window": "2024-01", "symbol": "BTCUSDT", "route": "kill_no_ic",
         "rationale": "p_value=0.42 >= 0.10"},
    ]
    joined_constraints = " ".join(handoff["constraints"])
    assert "INFORMATIONAL ONLY, NEVER A GATE" in joined_constraints
    assert "Do NOT auto-adopt a kill_*/refine_* label" in joined_constraints


def test_prefers_real_route_over_estimated_when_both_present(tmp_path):
    """CUL-272's real-cost route supersedes CUL-264's estimated one once real
    trade data exists -- both may be present on the same window's core block."""
    handoff_path = tmp_path / "protocol_to_verdict_interpreter.yaml"
    _write_handoff(handoff_path)
    protocol_result = {
        "results": [
            {"symbol": "BTCUSDT", "window_label": "2024-01", "core": {
                "post_backtest_route": "kill_cost_hurdle",
                "post_backtest_route_rationale": "estimated edge too small",
                "post_backtest_route_real": "proceed_to_interpretation",
                "post_backtest_route_real_rationale": "real edge clears cost",
            }},
        ],
    }
    rpr._inject_post_backtest_route_into_handoff(handoff_path, protocol_result, "run_x")
    handoff = rpr.load_yaml(handoff_path)
    assert handoff["post_backtest_routes"][0]["route"] == "proceed_to_interpretation"
    assert handoff["post_backtest_routes"][0]["rationale"] == "real edge clears cost"


def test_multi_window_multi_symbol_all_carried(tmp_path):
    handoff_path = tmp_path / "protocol_to_verdict_interpreter.yaml"
    _write_handoff(handoff_path)
    protocol_result = {
        "results": [
            {"symbol": "BTCUSDT", "window_label": "2024-01", "core": {"post_backtest_route": "kill_no_ic"}},
            {"symbol": "ETHUSDT", "window_label": "2024-01", "core": {"post_backtest_route": "inconclusive_insufficient_data"}},
            {"symbol": "BTCUSDT", "window_label": "2024-02", "core": {"sharpe": 0.1}},  # no route -- skipped
        ],
    }
    rpr._inject_post_backtest_route_into_handoff(handoff_path, protocol_result, "run_x")
    handoff = rpr.load_yaml(handoff_path)
    assert len(handoff["post_backtest_routes"]) == 2
    assert {r["symbol"] for r in handoff["post_backtest_routes"]} == {"BTCUSDT", "ETHUSDT"}


def test_constraint_not_duplicated_on_repeated_call(tmp_path):
    """Idempotency, same discipline as the regime-injection precedent: calling
    this twice (e.g. a resumed run) must not duplicate the constraint text."""
    handoff_path = tmp_path / "protocol_to_verdict_interpreter.yaml"
    _write_handoff(handoff_path)
    protocol_result = {"results": [{"symbol": "BTCUSDT", "core": {"post_backtest_route": "kill_no_ic"}}]}
    rpr._inject_post_backtest_route_into_handoff(handoff_path, protocol_result, "run_x")
    rpr._inject_post_backtest_route_into_handoff(handoff_path, protocol_result, "run_x")
    handoff = rpr.load_yaml(handoff_path)
    assert len(handoff["constraints"]) == 1
