"""
K3 kernel (B3 + B10, protocol pinning + stale-escalation hard-fail) regression
tests, 2026-07-15.
See docs/design/K3_protocol_pinning_design_20260714.md sections 3-6 and 9
(operator rulings A1-A5, Q1-Q4).

Sandboxing: relies on tests/conftest.py's autouse _sandbox_by_default fixture
for rpr.ROOT/rpr.CAMPAIGN_STATE_PATH (already redirected to a per-test
tmp_path sandbox before any test body runs) -- no bespoke sandboxing needed
for pure run_phase1_research.py calls. Tests exercising materialization
(run_campaign.py's lint call sites) or _route_escalate's own scaffolding
import the campaign_root fixture from test_k4_routing_registration.py, same
precedent test_k2_verdict_machinery.py already established.
"""
import asyncio
import json
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
import stamp_protocol  # noqa: E402

from test_k4_routing_registration import (  # noqa: E402
    campaign_root, _write_fresh_scaffold, _save_queue_entries, _write_campaign_state,
)


def _write_protocol(root: Path, name: str, obj: dict | None = None) -> Path:
    protocols_dir = root / "protocols"
    protocols_dir.mkdir(parents=True, exist_ok=True)
    path = protocols_dir / name
    path.write_text(
        json.dumps(obj or {"symbols": ["BTCUSDT"], "timeframe": "1d", "windows": []}),
        encoding="utf-8",
    )
    return path


def _minimal_run(root: Path, run_id: str) -> Path:
    run_dir = root / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    state = {
        "run_id": run_id, "status": "active", "pending_stage": "signal_prescreen",
        "flags": {}, "audit_log": {},
    }
    with open(run_dir / "pipeline_state.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, sort_keys=False)
    return run_dir


# ---------------------------------------------------------------------------
# _ensure_protocol_ref_pinned -- direct-call fixtures (§3, §9 A1)
# ---------------------------------------------------------------------------

def test_ensure_protocol_ref_pinned_pins_existing_protocol():
    root = rpr.ROOT
    _write_protocol(root, "foo.json")
    run_dir = _minimal_run(root, "run_500")
    constraints = {"protocol_ref": "protocols/foo.json"}

    result = rpr._ensure_protocol_ref_pinned(run_dir, "run_500", constraints)

    assert result == root / "protocols" / "foo.json"
    run_ctx = rpr.load_yaml(run_dir / "artifacts" / "run_context.yaml")
    assert run_ctx["run_type"] == "protocol_ref_pinned", "A3: must be a NEW, dedicated run_type"
    assert run_ctx["protocol"] == "foo.json", "A1.1: must write the BARE FILENAME, not the ROOT-relative ref"
    assert run_ctx["protocol_ref_pinned"] is True


def test_ensure_protocol_ref_pinned_missing_ref_raises_filenotfound():
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_501")
    constraints = {"protocol_ref": "protocols/does_not_exist.json"}
    with pytest.raises(FileNotFoundError):
        rpr._ensure_protocol_ref_pinned(run_dir, "run_501", constraints)


def test_ensure_protocol_ref_pinned_no_ref_returns_none():
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_502")
    assert rpr._ensure_protocol_ref_pinned(run_dir, "run_502", {}) is None


def test_ensure_protocol_ref_pinned_idempotent_short_circuits_on_bare_filename_match():
    """A1.3: the idempotency comparison must be against the BARE filename form
    actually written, not the full ref -- proven here by deleting the
    protocol file between calls: if the comparison used the full ref (the
    original, broken draft), it would never match, the short-circuit would
    never fire, and this second call would then re-check ref_path.exists()
    and raise FileNotFoundError."""
    root = rpr.ROOT
    proto_path = _write_protocol(root, "bar.json")
    run_dir = _minimal_run(root, "run_503")
    constraints = {"protocol_ref": "protocols/bar.json"}

    first = rpr._ensure_protocol_ref_pinned(run_dir, "run_503", constraints)
    assert first == proto_path

    proto_path.unlink()
    second = rpr._ensure_protocol_ref_pinned(run_dir, "run_503", constraints)
    assert second == proto_path


def test_ensure_protocol_ref_pinned_content_hash_mismatch_raises():
    root = rpr.ROOT
    _write_protocol(root, "hashed.json", {"symbols": ["BTCUSDT"], "windows": []})
    run_dir = _minimal_run(root, "run_504")
    constraints = {
        "protocol_ref": "protocols/hashed.json",
        "protocol_ref_content_hash": "sha256:" + "0" * 64,
    }
    with pytest.raises(RuntimeError, match="content hash"):
        rpr._ensure_protocol_ref_pinned(run_dir, "run_504", constraints)


def test_ensure_protocol_ref_pinned_content_hash_match_passes():
    root = rpr.ROOT
    proto_path = _write_protocol(root, "hashed2.json", {"symbols": ["BTCUSDT"], "windows": []})
    run_dir = _minimal_run(root, "run_505")
    actual_hash = rpr._compute_protocol_content_hash(proto_path)
    constraints = {"protocol_ref": "protocols/hashed2.json", "protocol_ref_content_hash": actual_hash}
    result = rpr._ensure_protocol_ref_pinned(run_dir, "run_505", constraints)
    assert result == proto_path


# ---------------------------------------------------------------------------
# _resolve_protocol_path -- consolidated resolver (§9 Q4), no path doubling (A1)
# ---------------------------------------------------------------------------

def test_resolve_protocol_path_replication_diagnostic():
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_510")
    rpr.save_yaml(run_dir / "artifacts" / "run_context.yaml", {"run_type": "replication_diagnostic"})
    _write_protocol(root, "baseline_v1.json")
    result = rpr._resolve_protocol_path(run_dir, "run_510")
    assert result == root / "protocols" / "baseline_v1.json"


def test_resolve_protocol_path_forced_diagnostic_generated():
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_511")
    _write_protocol(root, "run_511_generated.json")
    rpr.save_yaml(run_dir / "artifacts" / "run_context.yaml",
                   {"run_type": "forced_diagnostic", "protocol": "run_511_generated.json"})
    result = rpr._resolve_protocol_path(run_dir, "run_511")
    assert result == root / "protocols" / "run_511_generated.json"


def test_resolve_protocol_path_pinned_run_no_path_doubling():
    """A1: the exact bug class this amendment closes -- must resolve to a
    single, non-doubled protocols/ path."""
    root = rpr.ROOT
    _write_protocol(root, "pinned_v1.json")
    run_dir = _minimal_run(root, "run_512")
    constraints = {"protocol_ref": "protocols/pinned_v1.json"}
    rpr._ensure_protocol_ref_pinned(run_dir, "run_512", constraints)

    result = rpr._resolve_protocol_path(run_dir, "run_512")

    assert result == root / "protocols" / "pinned_v1.json"
    assert str(result).count("protocols") == 1, f"doubled path segment detected: {result}"


def test_resolve_protocol_path_pinned_run_malformed_missing_protocol_key_raises():
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_513")
    rpr.save_yaml(run_dir / "artifacts" / "run_context.yaml", {"run_type": "protocol_ref_pinned"})
    with pytest.raises(RuntimeError, match="protocol_ref_pinned"):
        rpr._resolve_protocol_path(run_dir, "run_513")


# ---------------------------------------------------------------------------
# B10 -- claim-checked last_escalation hard-fail (§4)
# ---------------------------------------------------------------------------

def test_resolve_protocol_path_stale_escalation_unclaimed_hard_fails():
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_520")
    rpr._save_campaign_state({
        "last_escalation": {
            "target": "timeframe", "detail": "15m",
            "protocol_path": str(root / "protocols" / "escalation_tf_15m.json"),
            "claimed_by_run": "run_049",
        }
    })
    with pytest.raises(RuntimeError, match="B10"):
        rpr._resolve_protocol_path(run_dir, "run_520")

    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["flags"]["stale_escalation_unclaimed"] is True, "Q2: flag must be set BEFORE raising"


def test_resolve_protocol_path_no_last_escalation_at_all_hard_fails():
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_521")
    with pytest.raises(RuntimeError, match="B10"):
        rpr._resolve_protocol_path(run_dir, "run_521")


def test_resolve_protocol_path_claimed_run_uses_fallback_legitimately():
    root = rpr.ROOT
    escalation_proto = _write_protocol(root, "escalation_tf_15m.json")
    run_dir = _minimal_run(root, "run_049")
    rpr._save_campaign_state({
        "last_escalation": {
            "target": "timeframe", "detail": "15m", "protocol_path": str(escalation_proto),
            "claimed_by_run": "run_049", "claimed_at": "2026-07-06",
        }
    })
    result = rpr._resolve_protocol_path(run_dir, "run_049")
    assert result == escalation_proto


def test_resolve_protocol_path_second_different_run_still_fails():
    """The claim is a ONE-HOP grant to its designated consumer, never
    transitively inherited by any later run."""
    root = rpr.ROOT
    escalation_proto = _write_protocol(root, "escalation_tf_15m.json")
    rpr._save_campaign_state({
        "last_escalation": {
            "target": "timeframe", "detail": "15m", "protocol_path": str(escalation_proto),
            "claimed_by_run": "run_049", "claimed_at": "2026-07-06",
        }
    })
    run_dir_other = _minimal_run(root, "run_050")
    with pytest.raises(RuntimeError, match="B10"):
        rpr._resolve_protocol_path(run_dir_other, "run_050")


# ---------------------------------------------------------------------------
# B10 negative-proof: the hard-fail fires BEFORE any subprocess spend (§9 A2)
# ---------------------------------------------------------------------------

def test_run_tool_worker_signal_prescreen_hard_fail_never_invokes_subprocess(monkeypatch):
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_530")
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")

    calls = []

    def _spy_subprocess_run(cmd, *args, **kwargs):
        calls.append(cmd)
        raise AssertionError("subprocess.run must never be invoked when protocol resolution hard-fails")
    monkeypatch.setattr(rpr.subprocess, "run", _spy_subprocess_run)

    with pytest.raises(RuntimeError, match="B10"):
        asyncio.run(rpr.run_tool_worker("signal_prescreen", "run_530"))

    assert calls == [], "subprocess.run must never be called before the hard-fail raises"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["flags"]["stale_escalation_unclaimed"] is True


# ---------------------------------------------------------------------------
# A2 -- mandatory end-to-end fixture: pin via _ensure_protocol_ref_pinned,
# THEN invoke run_tool_worker's selection path with subprocess.run CAPTURED
# (not executed, not merely "never called") -- the fixture shape that would
# have caught A1's path-doubling bug before Phase A approval.
# ---------------------------------------------------------------------------

def test_run_tool_worker_signal_prescreen_uses_pinned_protocol_exactly(monkeypatch):
    root = rpr.ROOT
    proto_path = _write_protocol(root, "e2e_pinned.json")
    run_dir = _minimal_run(root, "run_540")
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    constraints = {"protocol_ref": "protocols/e2e_pinned.json"}
    rpr._ensure_protocol_ref_pinned(run_dir, "run_540", constraints)

    captured = {}

    class _FakeCompletedProcess:
        returncode = 0
        stdout = ""
        stderr = ""

    def _fake_subprocess_run(cmd, *args, **kwargs):
        captured["cmd"] = cmd
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        rpr.save_yaml(out_dir / "prescreen_result.yaml", {
            "route": "kill", "ic_spearman_pooled": 0.0, "cost_check": {"pass": False},
        })
        return _FakeCompletedProcess()
    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)

    asyncio.run(rpr.run_tool_worker("signal_prescreen", "run_540"))

    cmd = captured["cmd"]
    protocol_arg = Path(cmd[3])
    assert protocol_arg == proto_path, f"expected exactly the pinned file (no doubling), got {protocol_arg}"


# ---------------------------------------------------------------------------
# Q4 -- duplication closed: BOTH run_tool_worker branches call the ONE
# shared resolver, no independent copy-pasted logic left in either branch.
# ---------------------------------------------------------------------------

def test_both_run_tool_worker_branches_call_the_shared_resolver(monkeypatch):
    root = rpr.ROOT
    proto_path = _write_protocol(root, "shared_resolver_check.json")

    calls = []

    def _spy_resolve(run_dir, run_id):
        calls.append((run_dir, run_id))
        return proto_path
    monkeypatch.setattr(rpr, "_resolve_protocol_path", _spy_resolve)

    class _FakeCompletedProcess:
        returncode = 0
        stdout = ""
        stderr = ""

    run_dir_a = _minimal_run(root, "run_550")
    (run_dir_a / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")

    def _fake_subprocess_run_prescreen(cmd, *a, **kw):
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        rpr.save_yaml(out_dir / "prescreen_result.yaml",
                      {"route": "kill", "ic_spearman_pooled": 0.0, "cost_check": {"pass": False}})
        return _FakeCompletedProcess()
    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run_prescreen)
    asyncio.run(rpr.run_tool_worker("signal_prescreen", "run_550"))

    run_dir_b = _minimal_run(root, "run_551")
    (run_dir_b / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    (run_dir_b / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")

    def _fake_subprocess_run_protocol(cmd, *a, **kw):
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "protocol_summary.json").write_text("{}", encoding="utf-8")
        return _FakeCompletedProcess()
    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run_protocol)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_551"))

    assert len(calls) == 2, "both branches must call the shared resolver exactly once each"
    assert calls[0] == (run_dir_a, "run_550")
    assert calls[1] == (run_dir_b, "run_551")


# ---------------------------------------------------------------------------
# Materialization-time lint: _lint_machine_constraints_protocol_selection (§3, §9 Q1)
# ---------------------------------------------------------------------------

def test_lint_rejects_both_protocol_and_protocol_ref():
    violations = rpr._lint_machine_constraints_protocol_selection({
        "protocol": {"symbols": ["BTCUSDT"], "start": "2024-01-01", "end": "2024-06-01"},
        "protocol_ref": "protocols/foo.json",
    })
    assert violations
    assert any("protocol" in v and "protocol_ref" in v for v in violations)


def test_lint_rejects_empty_protocol_ref():
    assert rpr._lint_machine_constraints_protocol_selection({"protocol_ref": ""})


def test_lint_rejects_non_string_protocol_ref():
    assert rpr._lint_machine_constraints_protocol_selection({"protocol_ref": 12345})


def test_lint_rejects_nested_protocol_ref_path():
    """A1.2: protocol_ref must resolve FLAT under protocols/ -- no subdirectory nesting."""
    violations = rpr._lint_machine_constraints_protocol_selection({"protocol_ref": "protocols/nested/foo.json"})
    assert violations
    assert any("FLAT" in v for v in violations)


def test_lint_rejects_protocol_ref_outside_protocols_dir():
    assert rpr._lint_machine_constraints_protocol_selection({"protocol_ref": "other_dir/foo.json"})


def test_lint_accepts_flat_protocol_ref_with_no_pass_rule():
    assert rpr._lint_machine_constraints_protocol_selection({"protocol_ref": "protocols/foo.json"}) == []


def test_lint_q1_hard_rejects_window_set_ref_mismatch():
    """Q1 ruling: DIFFERENT protocol_ref/window_set_ref names is a HARD REJECT,
    not the WARNING originally proposed in §3."""
    violations = rpr._lint_machine_constraints_protocol_selection(
        {"protocol_ref": "protocols/foo.json"},
        pass_rule={"window_set_ref": "protocols/some_other.json"},
    )
    assert violations
    assert any("foo.json" in v and "some_other.json" in v for v in violations)


def test_lint_accepts_matching_window_set_ref():
    violations = rpr._lint_machine_constraints_protocol_selection(
        {"protocol_ref": "protocols/foo.json"},
        pass_rule={"window_set_ref": "protocols/foo.json"},
    )
    assert violations == []


def test_lint_skips_legacy_string_pass_rule_for_window_set_ref_check():
    violations = rpr._lint_machine_constraints_protocol_selection(
        {"protocol_ref": "protocols/foo.json"}, pass_rule="PASS iff x."
    )
    assert violations == []


# ---------------------------------------------------------------------------
# Materialization wiring: the lint actually blocks _materialize_run /
# _materialize_refinement_run, not just as a standalone function
# ---------------------------------------------------------------------------

def test_materialize_run_rejects_incoherent_protocol_selection(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_900")
    brief = {
        "strategy_domain": "test",
        "machine_constraints": {
            "protocol": {"symbols": ["BTCUSDT"], "start": "2024-01-01", "end": "2024-06-01"},
            "protocol_ref": "protocols/foo.json",
        },
    }
    with pytest.raises(ValueError, match="K3 protocol-selection lint"):
        camp._materialize_run("run_900", brief)
    assert not (runs_dir / "run_900" / "artifacts" / "pre_registration.yaml").exists()


# ---------------------------------------------------------------------------
# B4/B7 rider (2026-07-16): pass_rule copy-through on _materialize_run's
# fresh_launch path, mirroring _materialize_refinement_run's own extraction
# (brief["evaluation"]["pass_rule"] -> pre_registration["pass_rule"], same
# key-path and shape) -- closes the documented gap in _materialize_run's own
# prior comment ("machine_constraints-only briefs don't carry a pass_rule
# block yet").
# ---------------------------------------------------------------------------

def _fresh_launch_brief_with_pass_rule(protocol_ref: str = "protocols/foo.json") -> dict:
    return {
        "strategy_domain": "test",
        "machine_constraints": {"protocol_ref": protocol_ref},
        "evaluation": {
            "pass_rule": {
                "statement": "PASS iff x.",
                "window_set_ref": protocol_ref,
                "criteria": [
                    {"id": "a", "metric": "median_sharpe", "metric_basis": "bar_level",
                     "comparator": ">=", "per_symbol_threshold": {"BTCUSDT": 0.1},
                     "null_handling": "fails_threshold"},
                ],
                "outcomes": [
                    {"branch": "PASS", "hypothesis_verdict": "promote", "lineage_routing": None},
                    {"branch": "FAIL-a", "hypothesis_verdict": "kill", "lineage_routing": "terminate"},
                ],
            },
        },
    }


def test_materialize_run_fresh_launch_pass_rule_copy_through(campaign_root):
    """A fresh-launch brief's evaluation.pass_rule must reach
    pre_registration.yaml['pass_rule'] verbatim -- the exact gap this rider
    closes, proven by round-tripping through the real _materialize_run call,
    not just asserting the code exists."""
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_901")
    _write_protocol(root, "foo.json")

    brief = _fresh_launch_brief_with_pass_rule()
    camp._materialize_run("run_901", brief)

    pre_reg_path = runs_dir / "run_901" / "artifacts" / "pre_registration.yaml"
    assert pre_reg_path.exists()
    pre_registration = camp.orch.load_yaml(pre_reg_path)
    assert pre_registration["pass_rule"] == brief["evaluation"]["pass_rule"]


def test_materialize_run_fresh_launch_rejects_non_total_pass_rule_mapping(campaign_root):
    """A fresh-launch brief with a deliberately non-total outcomes mapping
    (a FAIL branch missing both hypothesis_verdict and lineage_routing, no
    discretion opt-in) must be rejected by the SAME B11 lint the refinement
    path already enforces -- one gate, not two divergent ones."""
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_902")
    _write_protocol(root, "foo.json")

    brief = _fresh_launch_brief_with_pass_rule()
    brief["evaluation"]["pass_rule"]["outcomes"][1]["hypothesis_verdict"] = None
    brief["evaluation"]["pass_rule"]["outcomes"][1]["lineage_routing"] = None

    with pytest.raises(ValueError, match="B11 total-mapping lint"):
        camp._materialize_run("run_902", brief)
    assert not (runs_dir / "run_902" / "artifacts" / "pre_registration.yaml").exists()


def test_materialize_refinement_run_rejects_nested_protocol_ref(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_910")
    brief = {
        "brief_id": "BAD_PIN",
        "lineage": {"parent_queue_entry": "X", "parent_run": "run_910",
                    "relation": "refine", "parent_verdict": "refine"},
        "hypothesis": {"primary": "test"},
        "gate_definition": {"indicator": "test"},
        "evaluation": {},
        "machine_constraints": {"protocol_ref": "protocols/nested/foo.json"},
    }
    brief_path = root / "brief.yaml"
    brief_path.write_text(yaml.safe_dump(brief, sort_keys=False), encoding="utf-8")

    with pytest.raises(ValueError, match="K3 protocol-selection lint"):
        camp._materialize_refinement_run("run_911", brief, brief_path)
    assert not (runs_dir / "run_911" / "artifacts" / "pre_registration.yaml").exists()


# ---------------------------------------------------------------------------
# B10 Part 1 -- _route_escalate's record_escalation writes claimed_by_run (§4)
# ---------------------------------------------------------------------------

def test_route_escalate_instrument_writes_claimed_by_run(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_600")
    run_dir = runs_dir / "run_600"

    (root / "protocols").mkdir()
    (root / "protocols" / "baseline_v1.json").write_text(
        '{"symbols": ["BTCUSDT"], "timeframe": "1h", "windows": []}', encoding="utf-8"
    )
    (root / "coin_universe.yaml").write_text(yaml.safe_dump({
        "escalation_order": {"sequence": [{"category": "majors", "priority": 1}]},
        "categories": {"majors": {"coins": [{"symbol": "ETHUSDT", "data_cached": True}],
                                   "strategy_affinity": []}},
    }), encoding="utf-8")
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_600"])

    next_stage = rpr._route_escalate(run_dir, "run_600", {}, {})

    assert next_stage == "completed_escalated"
    state = rpr.load_campaign_state()
    last_escalation = state["last_escalation"]
    assert last_escalation["claimed_by_run"] == "run_601"
    assert "claimed_at" in last_escalation


# ---------------------------------------------------------------------------
# Q2 -- run_campaign.py's classifier recognizes the stale_escalation_unclaimed flag
# ---------------------------------------------------------------------------

def test_hard_pause_reason_classifies_stale_escalation_unclaimed_flag(tmp_path):
    run_dir = tmp_path / "runs" / "run_570"
    (run_dir / "artifacts").mkdir(parents=True)
    state = {"status": "failed", "last_error": "boom", "flags": {"stale_escalation_unclaimed": True}}
    reason, detail = camp._hard_pause_reason(run_dir, state)
    assert reason == "stale_escalation_unclaimed"
    assert detail == "boom"


def test_hard_pause_reason_generic_unhandled_exception_without_flag(tmp_path):
    run_dir = tmp_path / "runs" / "run_571"
    (run_dir / "artifacts").mkdir(parents=True)
    state = {"status": "failed", "last_error": "boom", "flags": {}}
    reason, detail = camp._hard_pause_reason(run_dir, state)
    assert reason == "unhandled_exception"


# ---------------------------------------------------------------------------
# A4 -- runtime mutual-exclusion guard at run_loop()'s own top
# ---------------------------------------------------------------------------

def test_run_loop_top_hard_fails_on_both_protocol_keys_before_anything_else(monkeypatch):
    """Protects a hand-authored/hand-edited pre_registration.yaml fed directly
    to this script, bypassing run_campaign.py's materialization-time lint
    entirely (§9 A4) -- independent of, and in addition to, that lint."""
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_560")
    pre_reg = {
        "machine_constraints": {
            "protocol": {"symbols": ["BTCUSDT"], "start": "2024-01-01", "end": "2024-06-01"},
            "protocol_ref": "protocols/foo.json",
        }
    }
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", pre_reg)

    def _fail_if_called(*a, **kw):
        raise AssertionError("must never reach _ensure_protocol_from_constraints/_ensure_protocol_ref_pinned")
    monkeypatch.setattr(rpr, "_ensure_protocol_from_constraints", _fail_if_called)
    monkeypatch.setattr(rpr, "_ensure_protocol_ref_pinned", _fail_if_called)

    with pytest.raises(RuntimeError, match=r"K3/A4"):
        rpr.run_loop("run_560")


# ---------------------------------------------------------------------------
# K3 rider (2026-07-15) -- protocol_ref post-hoc conformance extension of
# _check_prescreen_conformance (operator ruling overturning Phase B deviation 1:
# A4/Q1 are registration-time only and never catch an EXECUTED prescreen that
# silently ran against a different file than the one pinned).
# ---------------------------------------------------------------------------

def test_check_prescreen_conformance_protocol_ref_mismatch_names_both():
    prescreen_result = {"protocol_version": str(Path("C:/somewhere/protocols/actually_used.json"))}
    constraints = {"protocol_ref": "protocols/pinned_expected.json"}
    violations = rpr._check_prescreen_conformance(prescreen_result, constraints, {})
    assert violations
    assert any("actually_used.json" in v and "pinned_expected.json" in v for v in violations)


def test_check_prescreen_conformance_protocol_ref_match_no_violation():
    prescreen_result = {"protocol_version": str(Path("/anywhere/protocols/pinned_expected.json"))}
    constraints = {"protocol_ref": "protocols/pinned_expected.json"}
    violations = rpr._check_prescreen_conformance(prescreen_result, constraints, {})
    assert violations == []


def test_check_prescreen_conformance_protocol_ref_content_hash_mismatch():
    protocol_obj = {"symbols": ["BTCUSDT"], "timeframe": "1d", "windows": []}
    prescreen_result = {"protocol_version": "/anywhere/protocols/pinned.json"}
    constraints = {
        "protocol_ref": "protocols/pinned.json",
        "protocol_ref_content_hash": "sha256:" + "0" * 64,
    }
    violations = rpr._check_prescreen_conformance(prescreen_result, constraints, protocol_obj)
    assert violations
    assert any("content hash" in v for v in violations)


def test_check_prescreen_conformance_protocol_ref_content_hash_match():
    protocol_obj = {"symbols": ["BTCUSDT"], "timeframe": "1d", "windows": []}
    expected_hash = stamp_protocol.compute_protocol_content_hash(protocol_obj)
    prescreen_result = {"protocol_version": "/anywhere/protocols/pinned.json"}
    constraints = {
        "protocol_ref": "protocols/pinned.json",
        "protocol_ref_content_hash": expected_hash,
    }
    violations = rpr._check_prescreen_conformance(prescreen_result, constraints, protocol_obj)
    assert violations == []


def test_check_prescreen_conformance_no_protocol_ref_skips_new_branch():
    """No protocol_ref on the brief -- the new branch must never fire, existing
    generation-shape checks unaffected."""
    violations = rpr._check_prescreen_conformance({"protocol_version": "/x/protocols/whatever.json"}, {}, {})
    assert violations == []


# ---------------------------------------------------------------------------
# Q3 -- tools/stamp_protocol.py round-trip
# ---------------------------------------------------------------------------

def test_stamp_protocol_round_trip_matches_rpr_hash_formula(tmp_path):
    proto_path = tmp_path / "sample.json"
    proto_path.write_text(json.dumps({"symbols": ["BTCUSDT"], "timeframe": "1d", "windows": []}), encoding="utf-8")

    written_hash = stamp_protocol.stamp(proto_path, "2026-07-15")

    stamped = json.loads(proto_path.read_text(encoding="utf-8"))
    assert stamped["protocol_version"] == "2026-07-15"
    assert stamped["protocol_content_hash"] == written_hash

    # Must never diverge from run_phase1_research.py's own runtime content-hash
    # guard (§5) -- see stamp_protocol.py's own module docstring.
    recomputed = rpr._compute_protocol_content_hash(proto_path)
    assert recomputed == written_hash


def test_stamp_protocol_hash_stable_across_key_reordering():
    a = {"symbols": ["BTCUSDT"], "timeframe": "1d", "windows": []}
    b = {"timeframe": "1d", "windows": [], "symbols": ["BTCUSDT"]}
    assert stamp_protocol.compute_protocol_content_hash(a) == stamp_protocol.compute_protocol_content_hash(b)


# ---------------------------------------------------------------------------
# SDK result-misclassification retry rider (2026-07-16): claude_agent_sdk
# 0.2.82's query loop can raise a bare Exception whose message is the exact
# string "Claude Code returned an error result: success" (an SDK-internal
# is_error=True/subtype="success" contradiction, verified against the
# installed package -- see _invoke_agent_with_yaml_retry's own comment).
# _invoke_agent_with_yaml_retry now retries exactly once on this exact
# message before re-raising unchanged.
# ---------------------------------------------------------------------------

def test_invoke_agent_with_yaml_retry_recovers_from_sdk_error_result_success(monkeypatch, capsys):
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_600")
    expected_output = run_dir / "artifacts" / "deliverable.yaml"
    expected_output.write_text("key: value\n", encoding="utf-8")

    calls = {"n": 0}

    async def _fake_async_invoke_agent(stage_name, run_id, retry_context=None):
        calls["n"] += 1
        if calls["n"] == 1:
            raise Exception(rpr._SDK_ERROR_RESULT_SUCCESS_MSG)
        # second call: succeed -- deliverable is already on disk, nothing to write

    monkeypatch.setattr(rpr, "async_invoke_agent", _fake_async_invoke_agent)

    rpr._invoke_agent_with_yaml_retry("some_stage", "run_600", run_dir, [expected_output], {})

    assert calls["n"] == 2, "must retry exactly once on the exact SDK message"
    captured = capsys.readouterr()
    assert captured.out.count("[SDK-RETRY]") == 1, "warning line must be emitted exactly once"


def test_invoke_agent_with_yaml_retry_reraises_on_second_sdk_error_result_success(monkeypatch):
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_601")
    expected_output = run_dir / "artifacts" / "deliverable.yaml"
    expected_output.write_text("key: value\n", encoding="utf-8")

    calls = {"n": 0}

    async def _always_fails(stage_name, run_id, retry_context=None):
        calls["n"] += 1
        raise Exception(rpr._SDK_ERROR_RESULT_SUCCESS_MSG)

    monkeypatch.setattr(rpr, "async_invoke_agent", _always_fails)

    with pytest.raises(Exception) as exc_info:
        rpr._invoke_agent_with_yaml_retry("some_stage", "run_601", run_dir, [expected_output], {})

    assert str(exc_info.value) == rpr._SDK_ERROR_RESULT_SUCCESS_MSG
    assert calls["n"] == 2, "must attempt exactly twice before re-raising unchanged"


def test_invoke_agent_with_yaml_retry_does_not_catch_other_messages(monkeypatch):
    """Any OTHER exception message -- including a different 'error result:'
    text -- must propagate immediately, no retry."""
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_602")
    expected_output = run_dir / "artifacts" / "deliverable.yaml"
    expected_output.write_text("key: value\n", encoding="utf-8")

    calls = {"n": 0}

    async def _different_error(stage_name, run_id, retry_context=None):
        calls["n"] += 1
        raise Exception("Claude Code returned an error result: error_during_execution")

    monkeypatch.setattr(rpr, "async_invoke_agent", _different_error)

    with pytest.raises(Exception) as exc_info:
        rpr._invoke_agent_with_yaml_retry("some_stage", "run_602", run_dir, [expected_output], {})

    assert str(exc_info.value) == "Claude Code returned an error result: error_during_execution"
    assert calls["n"] == 1, "a different message must never be retried"
