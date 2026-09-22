"""
E-033.1 Slice 4b (delivery_plan_v26.md Slice 4, sub-slice 2 of 2: "data gate +
conformance + grid/promotion wiring") -- unit + flag-off-identity tests.

Covers, per the dispatch's own build list (S1_FINDINGS.md items 3, 4, 7, 9;
4a already delivered items 1, 2, 5, 6, 8):

  1. run_tool_worker("data_availability_gate", ...) -> per-variant loop under
     orchestrator.variant_loop.enabled: each validated variant gets its own
     gate call; a refine/decline outcome marks THAT variant not_tested in
     index.yaml (without disturbing siblings) and appends a row to the new
     campaign_record/data_requests.yaml. Flag off: unchanged, single gate
     call against candidate_strategy_config.json.
  2. run_loop's own data_availability_gate elif-branch: after the per-variant
     gate has run, >=3 remaining validated variants advances to
     protocol_execution; <3 sets pipeline_state.flags.variant_gate_insufficient
     and routes to human_pause -- a DISTINCT flag from idea_status (S1
     Section 8's collision note).
  3. run_campaign._classify_human_pause / _PAUSE_FLAG_TO_REASON: the new
     variant_gate_insufficient branch and table entry.
  4. run_loop's own protocol_execution elif-branch (conformance): restructured
     into a per-variant loop reading each variant's own
     artifacts/variants/<variant_id>/protocol_result.yaml, calling the
     UNCHANGED _check_protocol_execution_conformance per variant, and
     invalidating ONLY the violating variant's own trial row via its compound
     trial_id -- siblings' trial rows and siblings' pass/fail status are
     untouched.
  5. _write_promotion_audit: under the flag, evaluates every variant's own
     protocol_result.yaml independently and PASSES overall if AT LEAST ONE
     variant clears the DSR/expectancy bar (existential OR; True beats None
     beats False). Flag off: byte-identical single-result shape, no
     "per_variant" key at all.

Sandboxing: relies on tests/conftest.py's autouse _sandbox_by_default fixture
(rpr.ROOT/camp.ROOT already redirected to a per-test tmp_path sandbox), same
precedent as test_e033_slice4a_variant_loop.py / test_k3_protocol_pinning.py.
"""
import asyncio
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(WORKFLOW_PATH))
sys.path.insert(0, str(TOOLS_PATH))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402

from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402
from test_e033_slice4a_variant_loop import (  # noqa: E402
    _set_flag, _write_three_variant_index, _summary_for,
)


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    """Same precedent as test_e033_slice4a_variant_loop.py / test_e056_config_
    direct_authoring.py: no resolvable trading-bot venv in this build
    environment; every subprocess-touching test here mocks subprocess.run."""
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


async def _noop_invoke(stage_name, run_id, retry_context=None):
    """FIX (interrupted-build recovery, 2026-09-22): every run_loop()-driven
    test in this file pre-seeds artifacts as if the CURRENT pending stage
    already completed, then asserts on the ROUTING decision run_loop makes
    next -- but run_loop() itself first calls async_invoke_agent() to
    actually EXECUTE the pending stage (real subprocess.run for a tool
    stage), which would overwrite/crash before the routing logic under test
    is ever reached, since subprocess isn't mocked in these run_loop-level
    tests. Same established precedent as test_anti_adjacency_retry_policy.py's
    own _noop_invoke: stub the stage-execution step out entirely so the
    pre-seeded artifacts stand as-is and only the routing decision is
    exercised."""
    return


def _write_handoff(run_dir: Path, name: str) -> None:
    """run_loop's own step 1 (`load_yaml(handoff_path)`) raises FileNotFoundError,
    UNCAUGHT, on a missing handoff file -- tests that drive run_loop() itself
    (rather than calling run_tool_worker directly, 4a's own precedent) need
    this scaffolding. Empty required_inputs/deliverables: nothing else in
    these tests depends on handoff content."""
    handoffs_dir = run_dir / "handoffs"
    handoffs_dir.mkdir(parents=True, exist_ok=True)
    rpr.save_yaml(handoffs_dir / name, {"required_inputs": [], "deliverables": []})


def _minimal_run_at(root: Path, run_id: str, pending_stage: str) -> Path:
    """FIX (interrupted-build recovery, 2026-09-22): every run_loop()-driven
    test in this file reaches data_availability_gate or protocol_execution,
    both of which require a pinned protocol ref at run_loop's own top (B10)
    -- confirmed by direct reproduction, unrelated to variant-loop or
    conformance logic specifically, same requirement test_e033_slice4a_
    variant_loop.py's own run_loop-level tests already satisfy via
    _ensure_protocol_ref_pinned. Pin one here unconditionally so every test
    using this helper gets it automatically, instead of each test needing
    its own boilerplate."""
    run_dir = _minimal_run(root, run_id)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["pending_stage"] = pending_stage
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    _write_protocol(root, f"{run_id}_pinned.json")
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": f"protocols/{run_id}_pinned.json"})
    return run_dir


def _dag_ok(outcome: str, reasons=None):
    """A fake subprocess.run() result + data_availability_gate.yaml writer for
    one variant's data_availability_gate.py invocation."""
    def _write(out_dir: Path):
        out_dir.mkdir(parents=True, exist_ok=True)
        rpr.save_yaml(out_dir / "data_availability_gate.yaml",
                       {"outcome": outcome, "reasons": reasons or [f"{outcome} reason"]})
    return _write


# ---------------------------------------------------------------------------
# 1. run_tool_worker("data_availability_gate", ...) -- per-variant loop
# ---------------------------------------------------------------------------

def _setup_variant_loop_run(root: Path, run_id: str, protocol_name: str) -> Path:
    _write_protocol(root, protocol_name)
    run_dir = _minimal_run(root, run_id)
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": f"protocols/{protocol_name}"})
    return run_dir


def test_data_availability_gate_variant_loop_one_declines_others_continue(monkeypatch):
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}})
    root = rpr.ROOT
    run_dir = _setup_variant_loop_run(root, "run_970", "dag.json")
    _write_three_variant_index(run_dir)

    def _fake_subprocess_run(cmd, *args, **kwargs):
        config_path = cmd[2]
        variant_id = Path(config_path).parent.name
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        outcome = "decline" if variant_id == "design_v2" else "validate"
        _dag_ok(outcome)(out_dir)

        class _Result:
            returncode = {"validate": 0, "decline": 2, "refine": 3}[outcome]
            stdout = ""
            stderr = ""
        return _Result()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    asyncio.run(rpr.run_tool_worker("data_availability_gate", "run_970"))

    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")
    variants = index["variants"]
    assert variants["design_v2"]["status"] == "not_tested"
    assert "decline" in variants["design_v2"]["reason"]
    assert variants["base"]["status"] == "validated"
    assert variants["asset_v2"]["status"] == "validated"
    # 'not_pursued' was already not_tested before this stage ran -- must be untouched.
    assert variants["not_pursued"]["status"] == "not_tested"
    assert variants["not_pursued"]["reason"] == "manifest paths unresolved: [x]"

    requests = rpr.load_yaml(rpr.ROOT / "campaign_record" / "data_requests.yaml")
    rows = requests["requests"]
    assert len(rows) == 1
    assert rows[0]["run_id"] == "run_970"
    assert rows[0]["stage"] == "data_availability_gate"
    assert rows[0]["variant_id"] == "design_v2"
    assert rows[0]["outcome"] == "decline"

    # Per-variant artifact copies exist for every gated variant, not just the declined one.
    for vid in ("base", "design_v2", "asset_v2"):
        assert (run_dir / "artifacts" / "variants" / vid / "data_availability_gate.yaml").exists()


def test_data_availability_gate_flag_off_single_call_unchanged(monkeypatch):
    """Flag off: byte-identical to pre-4b -- exactly one gate call against the
    singular candidate_strategy_config.json, no artifacts/variants/ touched."""
    root = rpr.ROOT
    run_dir = _setup_variant_loop_run(root, "run_971", "dagoff.json")
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")

    calls = []

    def _fake_subprocess_run(cmd, *args, **kwargs):
        calls.append(cmd)
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        _dag_ok("validate")(out_dir)

        class _Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Result()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    asyncio.run(rpr.run_tool_worker("data_availability_gate", "run_971"))

    assert len(calls) == 1, "flag off must run exactly one gate call, not a per-variant loop"
    assert (run_dir / "artifacts" / "data_availability_gate.yaml").exists()
    assert not (run_dir / "artifacts" / "variants").exists()
    assert not (rpr.ROOT / "campaign_record" / "data_requests.yaml").exists()


def test_data_availability_gate_variant_loop_unknown_outcome_fails_closed(monkeypatch):
    """CODE-REVIEW REGRESSION: only 'refine'/'decline' outcomes marked a
    variant not_tested -- an 'unknown' (or any other malformed/missing)
    outcome silently fell through and left the variant 'validated',
    proceeding to a real backtest despite the gate never actually
    validating the data. Must fail CLOSED on anything that isn't the
    literal string 'validate', matching the sibling flag-off routing
    branch's own fail-closed default."""
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}})
    root = rpr.ROOT
    run_dir = _setup_variant_loop_run(root, "run_976", "unknown_outcome.json")
    _write_three_variant_index(run_dir)

    def _fake_subprocess_run(cmd, *args, **kwargs):
        config_path = cmd[2]
        variant_id = Path(config_path).parent.name
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        if variant_id == "design_v2":
            # Malformed/missing outcome -- gate ran (exit 0) but its own
            # output is degenerate.
            out_dir.mkdir(parents=True, exist_ok=True)
            rpr.save_yaml(out_dir / "data_availability_gate.yaml", {"reasons": []})
        else:
            _dag_ok("validate")(out_dir)

        class _Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Result()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    asyncio.run(rpr.run_tool_worker("data_availability_gate", "run_976"))

    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")
    variants = index["variants"]
    assert variants["design_v2"]["status"] == "not_tested", (
        "a missing/unknown gate outcome must fail closed (not_tested), "
        f"got {variants['design_v2']!r}"
    )
    assert "unknown" in variants["design_v2"]["reason"]
    assert variants["base"]["status"] == "validated"
    assert variants["asset_v2"]["status"] == "validated"


def test_data_availability_gate_variant_loop_zero_validated_raises(monkeypatch):
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}})
    run_dir = _minimal_run(rpr.ROOT, "run_972")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {
        "variants": {"base": {"status": "not_tested", "reason": "boom"}}
    })

    def _fail_if_called(*a, **kw):
        raise AssertionError("subprocess.run must never be invoked with zero validated variants")
    monkeypatch.setattr(rpr.subprocess, "run", _fail_if_called)

    with pytest.raises(RuntimeError, match="no validated variants"):
        asyncio.run(rpr.run_tool_worker("data_availability_gate", "run_972"))


# ---------------------------------------------------------------------------
# 2. run_loop's data_availability_gate elif-branch -- >=3 remain / <3 remain
# ---------------------------------------------------------------------------

def test_run_loop_data_gate_fewer_than_three_remain_pauses_and_sets_flag(monkeypatch):
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}})
    run_dir = _minimal_run_at(rpr.ROOT, "run_973", "data_availability_gate")
    _write_handoff(run_dir, "backtest_spec_to_data_availability_gate.yaml")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        "base": {"status": "validated", "config_path": "x"},
        "design_v2": {"status": "not_tested", "reason": "declined"},
        "asset_v2": {"status": "not_tested", "reason": "declined"},
    }})

    rpr.run_loop("run_973")

    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "paused_for_human"
    assert state["flags"]["variant_gate_insufficient"] is True
    # FIX (interrupted-build recovery, 2026-09-22): this test originally
    # asserted pending_stage == "human_pause", but no other pause path in
    # this codebase does that (confirmed against test_profit_bars_stop.py's
    # own established convention, which only ever asserts on `status`) --
    # pending_stage is deliberately left as the stage that triggered the
    # pause (here, "data_availability_gate"), so --resume re-enters at the
    # right stage rather than a literal "human_pause" stage name.
    assert state["pending_stage"] == "data_availability_gate"
    # Must NOT collide with the criteria-grid's own idea_status field (S1 §8).
    assert "idea_status" not in state


def test_run_loop_data_gate_three_or_more_remain_advances_to_protocol_execution(monkeypatch):
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}})
    run_dir = _minimal_run_at(rpr.ROOT, "run_974", "data_availability_gate")
    _write_handoff(run_dir, "backtest_spec_to_data_availability_gate.yaml")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        "base": {"status": "validated", "config_path": "x"},
        "design_v2": {"status": "validated", "config_path": "x"},
        "asset_v2": {"status": "validated", "config_path": "x"},
    }})

    # This test only cares about stage 1's (data_availability_gate) own routing
    # decision -- stage 2 (protocol_execution) is deliberately never reached.
    # data_availability_gate here isn't going through the per-variant SUBPROCESS
    # loop (no artifacts/variants/<vid>/strategy_config.json exist for these
    # bare index entries) -- routing only reads index.yaml's status column,
    # which run_tool_worker would normally have already updated; seeding it
    # directly here isolates the run_loop-level routing decision under test.
    real_update_state = rpr.update_state

    class _StopAfterCapture(Exception):
        pass

    def _spy_update_state(path, **kwargs):
        real_update_state(path=path, **kwargs)
        if kwargs.get("pending_stage") == "protocol_execution":
            raise _StopAfterCapture("captured the routing decision; stop before stage 2")

    monkeypatch.setattr(rpr, "update_state", _spy_update_state)

    rpr.run_loop("run_974")  # run_loop's own except-block swallows _StopAfterCapture

    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["pending_stage"] == "protocol_execution"
    assert "variant_gate_insufficient" not in state.get("flags", {})


def test_run_loop_data_gate_flag_off_still_routes_on_single_gate_outcome(monkeypatch):
    """Flag off: byte-identical to pre-4b -- routes on the SINGLE
    data_availability_gate.yaml's outcome, never consults index.yaml."""
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    run_dir = _minimal_run_at(rpr.ROOT, "run_975", "data_availability_gate")
    _write_handoff(run_dir, "backtest_spec_to_data_availability_gate.yaml")
    rpr.save_yaml(run_dir / "artifacts" / "data_availability_gate.yaml",
                   {"outcome": "decline", "reasons": ["no data"]})

    rpr.run_loop("run_975")

    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["pending_stage"] == "completed_rejected"
    assert "variant_gate_insufficient" not in state.get("flags", {})


# ---------------------------------------------------------------------------
# 3. run_campaign: variant_gate_insufficient flag/reason wiring
# ---------------------------------------------------------------------------

def test_classify_human_pause_returns_variant_gate_insufficient_when_flagged(tmp_path):
    run_dir = tmp_path / "run_test"
    (run_dir / "artifacts").mkdir(parents=True)
    state = {"flags": {"variant_gate_insufficient": True}}
    assert camp._classify_human_pause(run_dir, state) == "variant_gate_insufficient"


def test_pause_flag_to_reason_table_includes_variant_gate_insufficient():
    table = dict(camp._PAUSE_FLAG_TO_REASON)
    assert table.get("variant_gate_insufficient") == "variant_gate_insufficient"


def test_variant_gate_insufficient_does_not_outrank_earlier_sticky_flags(tmp_path):
    """Sanity: it must not accidentally jump to the front of the chain and
    mask a genuinely-earlier, higher-priority sticky flag."""
    run_dir = tmp_path / "run_test"
    (run_dir / "artifacts").mkdir(parents=True)
    state = {"flags": {"variant_gate_insufficient": True, "conformance_violation": True}}
    assert camp._classify_human_pause(run_dir, state) == "conformance_gate_failure"


# ---------------------------------------------------------------------------
# 4. run_loop's protocol_execution elif-branch -- per-variant conformance loop
# ---------------------------------------------------------------------------

def _write_conformance_fixture(run_dir: Path, run_id: str, violating_variant: str) -> None:
    """machine_constraints.significance_methodology=episode_blocked_a851a is
    checked PURELY against each variant's own protocol_result.yaml content --
    unlike a protocol/protocol_ref constraint, it never triggers
    _ensure_protocol_from_constraints/_ensure_protocol_ref_pinned at run_loop's
    own top (both gated on different constraint keys), so no real protocol
    file needs to exist for this fixture."""
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", {
        "machine_constraints": {"significance_methodology": "episode_blocked_a851a"}
    })
    for vid in ("base", "design_v2", "asset_v2"):
        vdir = run_dir / "artifacts" / "variants" / vid
        vdir.mkdir(parents=True, exist_ok=True)
        if vid == violating_variant:
            by_symbol = {}  # triggers "no episode_blocked_significance_by_symbol at all"
        else:
            by_symbol = {"BTCUSDT": "episode_block_bootstrap"}
        rpr.save_yaml(vdir / "protocol_result.yaml", {
            "protocol_file": "p", "episode_blocked_significance_by_symbol": by_symbol,
        })
    # FIX (interrupted-build recovery, 2026-09-22): the actual per-variant
    # conformance loop reads directories under artifacts/variants/ directly
    # (not index.yaml) -- confirmed by reading run_phase1_research.py's own
    # implementation -- but B7/other unconditional per-stage machinery in
    # run_loop expects artifacts/variants/index.yaml to exist whenever
    # artifacts/variants/ itself exists. Write a minimal one so those
    # unrelated checks don't fail before conformance is even reached.
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        vid: {"status": "validated", "config_path": f"artifacts/variants/{vid}/strategy_config.json"}
        for vid in ("base", "design_v2", "asset_v2")
    }})


def test_run_loop_protocol_execution_conformance_invalidates_only_violating_variant(monkeypatch):
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}})
    run_dir = _minimal_run_at(rpr.ROOT, "run_980", "protocol_execution")
    _write_handoff(run_dir, "backtest_spec_to_protocol_execution.yaml")
    _write_conformance_fixture(run_dir, "run_980", violating_variant="design_v2")

    campaign = rpr.load_campaign_state()
    campaign["trial_sharpes"] = [
        {"trial_id": "run_980:base", "source": "backtest", "sharpe": 0.1},
        {"trial_id": "run_980:design_v2", "source": "backtest", "sharpe": 0.2},
        {"trial_id": "run_980:asset_v2", "source": "backtest", "sharpe": 0.3},
    ]
    rpr._save_campaign_state(campaign)

    rpr.run_loop("run_980")

    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["flags"]["conformance_violation"] is True
    assert set(state["conformance_violations"].keys()) == {"design_v2"}
    assert state["pending_stage"] == "human_pause"

    campaign = rpr.load_campaign_state()
    by_id = {t["trial_id"]: t for t in campaign["trial_sharpes"]}
    assert by_id["run_980:design_v2"].get("invalidated_artifact") is True
    assert not by_id["run_980:base"].get("invalidated_artifact")
    assert not by_id["run_980:asset_v2"].get("invalidated_artifact")


def test_run_loop_protocol_execution_conformance_all_variants_violate_reports_all(monkeypatch):
    """Self-adversarial review item: if every variant violates, all must be
    recorded (no early exit after the first), and the run still just pauses
    once -- it must not crash trying to invalidate every one of them."""
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}})
    run_dir = _minimal_run_at(rpr.ROOT, "run_981", "protocol_execution")
    _write_handoff(run_dir, "backtest_spec_to_protocol_execution.yaml")
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", {
        "machine_constraints": {"significance_methodology": "episode_blocked_a851a"}
    })
    for vid in ("base", "design_v2", "asset_v2"):
        vdir = run_dir / "artifacts" / "variants" / vid
        vdir.mkdir(parents=True, exist_ok=True)
        rpr.save_yaml(vdir / "protocol_result.yaml", {
            "protocol_file": "p", "episode_blocked_significance_by_symbol": {},
        })
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        vid: {"status": "validated", "config_path": f"artifacts/variants/{vid}/strategy_config.json"}
        for vid in ("base", "design_v2", "asset_v2")
    }})
    campaign = rpr.load_campaign_state()
    campaign["trial_sharpes"] = [
        {"trial_id": f"run_981:{vid}", "source": "backtest", "sharpe": 0.1}
        for vid in ("base", "design_v2", "asset_v2")
    ]
    rpr._save_campaign_state(campaign)

    rpr.run_loop("run_981")

    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["flags"]["conformance_violation"] is True
    assert set(state["conformance_violations"].keys()) == {"base", "design_v2", "asset_v2"}

    campaign = rpr.load_campaign_state()
    assert all(t.get("invalidated_artifact") is True for t in campaign["trial_sharpes"])


def test_run_loop_protocol_execution_flag_off_still_uses_bare_run_id(monkeypatch):
    """Flag off: byte-identical to pre-4b -- reads the singular
    artifacts/protocol_result.yaml and invalidates by bare run_id."""
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    run_dir = _minimal_run_at(rpr.ROOT, "run_982", "protocol_execution")
    _write_handoff(run_dir, "backtest_spec_to_protocol_execution.yaml")
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", {
        "machine_constraints": {"significance_methodology": "episode_blocked_a851a"}
    })
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", {
        "protocol_file": "p", "episode_blocked_significance_by_symbol": {},
    })
    campaign = rpr.load_campaign_state()
    campaign["trial_sharpes"] = [{"trial_id": "run_982", "source": "backtest", "sharpe": 0.1}]
    rpr._save_campaign_state(campaign)

    rpr.run_loop("run_982")

    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["flags"]["conformance_violation"] is True
    assert state["conformance_violations"], "flag-off shape is a flat list of strings, unchanged"
    assert isinstance(state["conformance_violations"], list)

    campaign = rpr.load_campaign_state()
    assert campaign["trial_sharpes"][0].get("invalidated_artifact") is True


# ---------------------------------------------------------------------------
# 5. _write_promotion_audit -- per-variant existential OR
# ---------------------------------------------------------------------------

def _sparse_pr(sharpe, mean, se):
    diagnostics = {"below_floor_pct": 80.0}
    if mean is not None:
        diagnostics["per_trade_expectancy_bps"] = {"mean": mean, "se": se}
    return {
        "per_symbol_summary": {"BTCUSDT": {"median_sharpe": sharpe}},
        "hypothesis_verdict": {"diagnostics": diagnostics},
    }


def _empty_campaign():
    campaign = rpr.load_campaign_state()
    campaign["trial_sharpes"] = []
    campaign["runs"] = []
    rpr._save_campaign_state(campaign)


def test_write_promotion_audit_flag_off_matches_pre_4b_shape():
    run_dir = rpr.ROOT / "runs" / "run_990"
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    rpr.save_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml", {"hypothesis_id": "run_990"})
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", _sparse_pr(0.4, 10.0, 2.0))
    _empty_campaign()

    rpr._write_promotion_audit(run_dir, "run_990")

    audit = rpr.load_yaml(run_dir / "artifacts" / "promotion_audit.yaml")
    assert "per_variant" not in audit
    assert "promoted_variant" not in audit
    assert audit["is_sparse_trading"] is True
    assert audit["raw_median_sharpe"] == 0.4
    assert audit["correction_method"] == "expectancy_t_stat_bonferroni"
    assert audit["expectancy_promotion"]["t_stat"] == 5.0
    assert audit["passes_deflated_threshold"] is True  # t_stat=5.0 > 2.0


def test_write_promotion_audit_variant_loop_passes_if_any_one_clears():
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}})
    run_dir = rpr.ROOT / "runs" / "run_991"
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    rpr.save_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml", {"hypothesis_id": "run_991"})
    variants_dir = run_dir / "artifacts" / "variants"
    rpr.save_yaml(variants_dir / "base" / "protocol_result.yaml", _sparse_pr(0.5, 10.0, 2.0))      # t=5.0 -> True
    rpr.save_yaml(variants_dir / "design_v2" / "protocol_result.yaml", _sparse_pr(0.1, 1.0, 2.0))   # t=0.5 -> False
    rpr.save_yaml(variants_dir / "asset_v2" / "protocol_result.yaml", _sparse_pr(0.2, None, None))  # t=None -> indeterminate
    _empty_campaign()

    rpr._write_promotion_audit(run_dir, "run_991")

    audit = rpr.load_yaml(run_dir / "artifacts" / "promotion_audit.yaml")
    assert audit["passes_deflated_threshold"] is True
    assert audit["promoted_variant"] == "base"
    assert audit["raw_median_sharpe"] == 0.5  # the winning variant's own value at top level
    assert set(audit["per_variant"].keys()) == {"base", "design_v2", "asset_v2"}
    assert audit["per_variant"]["base"]["passes_deflated_threshold"] is True
    assert audit["per_variant"]["design_v2"]["passes_deflated_threshold"] is False
    assert audit["per_variant"]["asset_v2"]["passes_deflated_threshold"] is None
    assert audit["per_variant"]["asset_v2"]["expectancy_promotion"]["t_stat"] is None


def test_write_promotion_audit_variant_loop_none_beats_false_with_no_true():
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}})
    run_dir = rpr.ROOT / "runs" / "run_992"
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    rpr.save_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml", {"hypothesis_id": "run_992"})
    variants_dir = run_dir / "artifacts" / "variants"
    rpr.save_yaml(variants_dir / "design_v2" / "protocol_result.yaml", _sparse_pr(0.1, 1.0, 2.0))   # t=0.5 -> False
    rpr.save_yaml(variants_dir / "asset_v2" / "protocol_result.yaml", _sparse_pr(0.2, None, None))  # t=None -> indeterminate
    _empty_campaign()

    rpr._write_promotion_audit(run_dir, "run_992")

    audit = rpr.load_yaml(run_dir / "artifacts" / "promotion_audit.yaml")
    assert audit["passes_deflated_threshold"] is None
    assert audit["promoted_variant"] is None


def test_write_promotion_audit_variant_loop_all_false():
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}})
    run_dir = rpr.ROOT / "runs" / "run_993"
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    rpr.save_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml", {"hypothesis_id": "run_993"})
    variants_dir = run_dir / "artifacts" / "variants"
    rpr.save_yaml(variants_dir / "base" / "protocol_result.yaml", _sparse_pr(0.1, 1.0, 2.0))
    rpr.save_yaml(variants_dir / "design_v2" / "protocol_result.yaml", _sparse_pr(0.1, 0.5, 2.0))
    _empty_campaign()

    rpr._write_promotion_audit(run_dir, "run_993")

    audit = rpr.load_yaml(run_dir / "artifacts" / "promotion_audit.yaml")
    assert audit["passes_deflated_threshold"] is False
    assert audit["promoted_variant"] is None


def test_write_promotion_audit_variant_loop_falls_back_to_singular_when_no_per_variant_files():
    """Defensive fallback (protocol_execution itself already raises if NO
    variant succeeded -- this is belt-and-braces, not the expected path):
    must never crash or emit an empty per_variant block."""
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}})
    run_dir = rpr.ROOT / "runs" / "run_994"
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    rpr.save_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml", {"hypothesis_id": "run_994"})
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", _sparse_pr(0.5, 10.0, 2.0))
    _empty_campaign()

    rpr._write_promotion_audit(run_dir, "run_994")

    audit = rpr.load_yaml(run_dir / "artifacts" / "promotion_audit.yaml")
    assert set(audit["per_variant"].keys()) == {"base"}
    assert audit["passes_deflated_threshold"] is True


def test_write_promotion_audit_picks_strongest_passing_variant_not_alphabetically_first():
    """CODE-REVIEW REGRESSION: when multiple variants pass, the promoted
    variant used to be picked by alphabetically-first variant_id rather
    than strongest evidence -- 'asset_v2' with a MUCH stronger t-stat would
    lose to 'base' purely by name ordering. Now ranked by evidence
    strength (DSR, or t_stat for the sparse/expectancy pathway)."""
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}})
    run_dir = rpr.ROOT / "runs" / "run_995"
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    rpr.save_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml", {"hypothesis_id": "run_995"})
    variants_dir = run_dir / "artifacts" / "variants"
    # Alphabetically FIRST but WEAKER evidence (t=5.0).
    rpr.save_yaml(variants_dir / "base" / "protocol_result.yaml", _sparse_pr(0.5, 10.0, 2.0))
    # Alphabetically LAST but STRONGER evidence (t=10.0) -- must win.
    rpr.save_yaml(variants_dir / "design_v2_stronger" / "protocol_result.yaml", _sparse_pr(0.6, 20.0, 2.0))
    _empty_campaign()

    rpr._write_promotion_audit(run_dir, "run_995")

    audit = rpr.load_yaml(run_dir / "artifacts" / "promotion_audit.yaml")
    assert audit["passes_deflated_threshold"] is True
    assert audit["promoted_variant"] == "design_v2_stronger", (
        f"expected the stronger-evidence variant to win, got {audit['promoted_variant']!r}"
    )
    assert audit["raw_median_sharpe"] == 0.6
