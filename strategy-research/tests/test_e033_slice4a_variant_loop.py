"""
E-033.1 Slice 4a (delivery_plan_v26.md Slice 4, sub-slice 1 of 2: "loop
restructure + trial accounting") -- unit + flag-off-identity tests.

Covers:
  1. orchestrator.variant_loop.enabled flag helper (on/off/absent, raises on
     non-bool, raises on the config_direct_authoring hard dependency).
  2. _route_post_config_direct_backtest_specification's restructure: flag
     off stays base-only (byte-identical to before this slice); flag on
     proceeds on ANY validated variant, pauses only when zero are validated.
  3. run_tool_worker("protocol_execution", ...) end to end under the flag
     (subprocess.run mocked): a real three-variant loop -- 3 per-variant
     protocol_result.yaml files, the singular artifacts/protocol_result.yaml
     matching the base variant's result exactly (Decision B), 3 distinct
     trial rows with the f"{run_id}:{variant_id}" shape (Decision A), and
     the grid receiving a real 3-column {variant_id: protocol_result} dict.
  4. Flag-off byte-identity for run_tool_worker("protocol_execution", ...):
     single config, single protocol_result.yaml, unchanged trial_id shape.
  5. _record_backtest_trial / _record_failed_backtest_trial's new optional
     trial_id parameter: defaults to run_id (byte-identical to every
     existing call site), and honors an explicit compound trial_id.
  6. _mark_trial_invalidated's renamed first parameter (Decision A): now
     compares by exact trial_id, so a compound trial_id invalidates only
     that one row, not a sibling sharing the same run_id prefix.
  7. Self-adversarial review scenarios named in this slice's own dispatch:
     zero validated variants at protocol_execution time raises loudly
     (race/staleness guard); a mid-loop variant failure does not stop
     remaining variants from running and does not disturb an
     already-recorded sibling trial.

Sandboxing: relies on tests/conftest.py's autouse _sandbox_by_default
fixture (rpr.ROOT already redirected to a per-test tmp_path sandbox), same
precedent as test_e056_config_direct_authoring.py / test_k3_protocol_pinning.py.
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

from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    """No resolvable trading-bot venv in this build environment
    (_resolve_tbot_python() raises RuntimeError otherwise) -- every
    run_tool_worker test in this file mocks subprocess.run, so the actual
    interpreter path is never really invoked. Same precedent as
    test_e056_config_direct_authoring.py's own fixture of the same name."""
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _set_flag(root: Path, orchestrator: dict) -> None:
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"orchestrator": orchestrator}, f)


# ---------------------------------------------------------------------------
# 1. Flag helper
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("enabled,expected", [(True, True), (False, False), (None, False)])
def test_variant_loop_enabled_reads_flag(enabled, expected):
    orchestrator = {"config_direct_authoring": {"enabled": True}}
    if enabled is None:
        orchestrator["variant_loop"] = {}
    else:
        orchestrator["variant_loop"] = {"enabled": enabled}
    _set_flag(rpr.ROOT, orchestrator)
    assert rpr._variant_loop_enabled() is expected


def test_variant_loop_enabled_false_when_config_file_absent():
    assert rpr._variant_loop_enabled() is False


def test_variant_loop_enabled_raises_on_non_bool_value():
    config_dir = rpr.ROOT / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"orchestrator": {
            "config_direct_authoring": {"enabled": True},
            "variant_loop": {"enabled": "false"},
        }}, f)
    with pytest.raises(ValueError, match="not a real"):
        rpr._variant_loop_enabled()


def test_variant_loop_enabled_raises_when_config_direct_authoring_off():
    """The hard dependency this slice's own dispatch required: variant_loop
    cannot be true while config_direct_authoring is false/absent --
    artifacts/variants/index.yaml structurally cannot exist without it."""
    _set_flag(rpr.ROOT, {"variant_loop": {"enabled": True}})
    with pytest.raises(ValueError, match="config_direct_authoring"):
        rpr._variant_loop_enabled()


def test_variant_loop_enabled_raises_when_config_direct_authoring_explicitly_false():
    _set_flag(rpr.ROOT, {
        "config_direct_authoring": {"enabled": False},
        "variant_loop": {"enabled": True},
    })
    with pytest.raises(ValueError, match="config_direct_authoring"):
        rpr._variant_loop_enabled()


def test_variant_loop_enabled_true_when_both_flags_on():
    _set_flag(rpr.ROOT, {
        "config_direct_authoring": {"enabled": True},
        "variant_loop": {"enabled": True},
    })
    assert rpr._variant_loop_enabled() is True


# ---------------------------------------------------------------------------
# 2. _route_post_config_direct_backtest_specification restructure
# ---------------------------------------------------------------------------

def test_route_flag_off_still_checks_base_only_byte_identical():
    """Flag off: behavior must be completely unchanged from before this
    slice -- a validated non-base variant with base missing/failed must
    still pause, exactly as test_e056_config_direct_authoring.py's own
    test_route_post_config_direct_backtest_specification_base_not_tested_pauses
    already proves for the base-not-tested case; this adds the "a SIBLING
    is validated but base isn't" case, which flag-off must ignore."""
    run_dir = _minimal_run(rpr.ROOT, "run_900")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {
        "variants": {
            "base": {"status": "not_tested", "reason": "boom"},
            "design_v2": {"status": "validated", "config_path": "artifacts/variants/design_v2/strategy_config.json"},
        }
    })
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "human_pause"


def test_route_flag_on_proceeds_on_any_validated_variant():
    _set_flag(rpr.ROOT, {
        "config_direct_authoring": {"enabled": True},
        "variant_loop": {"enabled": True},
        "data_availability_gate": {"enabled": False},
    })
    run_dir = _minimal_run(rpr.ROOT, "run_901")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {
        "variants": {
            "base": {"status": "not_tested", "reason": "boom"},
            "design_v2": {"status": "validated", "config_path": "artifacts/variants/design_v2/strategy_config.json"},
        }
    })
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "protocol_execution"


def test_route_flag_on_zero_validated_pauses():
    _set_flag(rpr.ROOT, {
        "config_direct_authoring": {"enabled": True},
        "variant_loop": {"enabled": True},
    })
    run_dir = _minimal_run(rpr.ROOT, "run_902")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {
        "variants": {
            "base": {"status": "not_tested", "reason": "boom"},
            "design_v2": {"status": "not_tested", "reason": "also boom"},
        }
    })
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "human_pause"


def test_route_flag_on_data_availability_gate_still_takes_priority():
    _set_flag(rpr.ROOT, {
        "config_direct_authoring": {"enabled": True},
        "variant_loop": {"enabled": True},
        "data_availability_gate": {"enabled": True},
    })
    run_dir = _minimal_run(rpr.ROOT, "run_903")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {
        "variants": {"design_v2": {"status": "validated", "config_path": "x"}}
    })
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "data_availability_gate"


# ---------------------------------------------------------------------------
# 3. run_tool_worker("protocol_execution", ...) -- flag-off byte identity
# ---------------------------------------------------------------------------

def test_protocol_execution_flag_off_single_config_unchanged(monkeypatch):
    """No orchestrator.variant_loop entry at all -- must behave exactly as
    before this slice: one subprocess call against
    candidate_strategy_config.json, one artifacts/protocol_result.yaml,
    trial_id == bare run_id."""
    root = rpr.ROOT
    _write_protocol(root, "flagoff.json")
    run_dir = _minimal_run(root, "run_910")
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, "run_910", {"protocol_ref": "protocols/flagoff.json"})

    calls = []

    def _fake_subprocess_run(cmd, *args, **kwargs):
        calls.append(cmd)
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "protocol_summary.json").write_text(
            rpr.json.dumps({"config_sha256": "x", "protocol_file": "p", "results": [],
                             "per_symbol_summary": {}, "verdict": "kill"}),
            encoding="utf-8",
        )

        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_910"))

    assert len(calls) == 1, "flag off must run exactly one subprocess call, not a per-variant loop"
    assert not (run_dir / "artifacts" / "variants").exists(), \
        "flag off must never create artifacts/variants/ -- that's the variant-loop's own territory"
    assert (run_dir / "artifacts" / "protocol_result.yaml").exists()

    state = rpr.load_campaign_state()
    trial_ids = [t["trial_id"] for t in state.get("trial_sharpes", [])]
    assert trial_ids == ["run_910"], "flag off must record the bare run_id as trial_id, unchanged"


# ---------------------------------------------------------------------------
# 4. run_tool_worker("protocol_execution", ...) -- real 3-variant loop
# ---------------------------------------------------------------------------

def _write_three_variant_index(run_dir: Path) -> None:
    variants_dir = run_dir / "artifacts" / "variants"
    for vid in ("base", "design_v2", "asset_v2"):
        (variants_dir / vid).mkdir(parents=True, exist_ok=True)
        (variants_dir / vid / "strategy_config.json").write_text(
            rpr.json.dumps({"variant": vid}), encoding="utf-8")
    rpr.save_yaml(variants_dir / "index.yaml", {"variants": {
        "base": {"status": "validated", "config_path": "artifacts/variants/base/strategy_config.json"},
        "design_v2": {"status": "validated", "config_path": "artifacts/variants/design_v2/strategy_config.json"},
        "asset_v2": {"status": "validated", "config_path": "artifacts/variants/asset_v2/strategy_config.json"},
        "not_pursued": {"status": "not_tested", "reason": "manifest paths unresolved: [x]"},
    }})


def _summary_for(variant_id: str) -> dict:
    return {
        "config_sha256": f"sha-{variant_id}", "protocol_file": "p", "verdict": "no_edge",
        "results": [], "per_symbol_summary": {"BTCUSDT": {"median_sharpe": 0.1}},
        "hypothesis_verdict": {"verdict": "refine", "diagnostics": {}},
    }


def test_protocol_execution_variant_loop_three_variants_end_to_end(monkeypatch):
    _set_flag(rpr.ROOT, {
        "config_direct_authoring": {"enabled": True},
        "variant_loop": {"enabled": True},
    })
    root = rpr.ROOT
    _write_protocol(root, "variant_loop.json")
    run_dir = _minimal_run(root, "run_920")
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, "run_920", {"protocol_ref": "protocols/variant_loop.json"})
    _write_three_variant_index(run_dir)

    calls = []

    def _fake_subprocess_run(cmd, *args, **kwargs):
        calls.append(cmd)
        config_path = cmd[2]
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        variant_id = Path(config_path).parent.name
        (out_dir / "protocol_summary.json").write_text(
            rpr.json.dumps(_summary_for(variant_id)), encoding="utf-8")

        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_920"))

    # Exactly 3 subprocess calls -- 'not_pursued' (not_tested) is skipped.
    assert len(calls) == 3

    # 3 per-variant protocol_result.yaml files.
    for vid in ("base", "design_v2", "asset_v2"):
        p = run_dir / "artifacts" / "variants" / vid / "protocol_result.yaml"
        assert p.exists(), f"missing per-variant protocol_result.yaml for {vid}"
        result = rpr.load_yaml(p)
        assert result["config_sha256"] == f"sha-{vid}"

    # Decision B: the singular file matches the BASE variant's result exactly.
    singular = rpr.load_yaml(run_dir / "artifacts" / "protocol_result.yaml")
    base_result = rpr.load_yaml(run_dir / "artifacts" / "variants" / "base" / "protocol_result.yaml")
    assert singular == base_result

    # Decision A: 3 distinct trial rows, correct compound trial_id shape.
    state = rpr.load_campaign_state()
    trial_ids = sorted(t["trial_id"] for t in state.get("trial_sharpes", []) if t.get("source") == "backtest")
    assert trial_ids == ["run_920:asset_v2", "run_920:base", "run_920:design_v2"]

    # pass_rule_evaluation.yaml still written (base-only, singular bridge).
    assert (run_dir / "artifacts" / "pass_rule_evaluation.yaml").exists()


def test_protocol_execution_variant_loop_grid_receives_three_column_dict(monkeypatch):
    """The grid call site (dispatch step 5) must build a real N-column
    {variant_id: protocol_result} dict from the N per-variant results, not
    the flag-off branch's single-entry {run_id: summary}."""
    _set_flag(rpr.ROOT, {
        "config_direct_authoring": {"enabled": True},
        "variant_loop": {"enabled": True},
        "grid_evaluation": {"enabled": True},
    })
    root = rpr.ROOT
    _write_protocol(root, "grid.json")
    run_dir = _minimal_run(root, "run_921")
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, "run_921", {"protocol_ref": "protocols/grid.json"})
    _write_three_variant_index(run_dir)
    # Menu-shaped pass_rule -- required for evaluate_grid to be reached at all.
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", {
        "pass_rule": {"criteria": [{"id": "c1", "source": "grid", "reducer": "unanimous"}]}
    })

    def _fake_subprocess_run(cmd, *args, **kwargs):
        config_path = cmd[2]
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        variant_id = Path(config_path).parent.name
        (out_dir / "protocol_summary.json").write_text(
            rpr.json.dumps(_summary_for(variant_id)), encoding="utf-8")

        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)

    captured = {}
    import verdict_criteria_evaluator as vce_mod
    real_evaluate_grid = vce_mod.evaluate_grid

    def _spy_evaluate_grid(protocol_results_by_variant, *a, **kw):
        captured["dict"] = protocol_results_by_variant
        captured["kw"] = kw
        return {"result": "INCONCLUSIVE", "idea_status": "inconclusive", "reason": "test spy"}

    monkeypatch.setattr(vce_mod, "evaluate_grid", _spy_evaluate_grid)
    try:
        asyncio.run(rpr.run_tool_worker("protocol_execution", "run_921"))
    finally:
        monkeypatch.setattr(vce_mod, "evaluate_grid", real_evaluate_grid)

    assert set(captured["dict"].keys()) == {"base", "design_v2", "asset_v2"}
    # E-061 C2 S2a: no variant failed -> the grid call is exactly today's (no
    # failed_variants keyword), so its output is byte-identical.
    assert "failed_variants" not in captured["kw"]
    assert (run_dir / "artifacts" / "grid_evaluation.yaml").exists()
    assert (run_dir / "artifacts" / "idea_status.yaml").exists()


def test_protocol_execution_variant_loop_zero_validated_raises(monkeypatch):
    """Self-adversarial review item: routing already refuses to reach this
    stage with zero validated variants, but this branch must not trust
    that silently -- a race/staleness case must raise loudly, not iterate
    over nothing."""
    _set_flag(rpr.ROOT, {
        "config_direct_authoring": {"enabled": True},
        "variant_loop": {"enabled": True},
    })
    run_dir = _minimal_run(rpr.ROOT, "run_922")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {
        "variants": {"base": {"status": "not_tested", "reason": "boom"}}
    })

    def _fail_if_called(*a, **kw):
        raise AssertionError("subprocess.run must never be invoked with zero validated variants")
    monkeypatch.setattr(rpr.subprocess, "run", _fail_if_called)

    with pytest.raises(RuntimeError, match="no validated variants"):
        asyncio.run(rpr.run_tool_worker("protocol_execution", "run_922"))


def test_protocol_execution_variant_loop_mid_loop_failure_continues_and_preserves_prior_trial(monkeypatch):
    """Self-adversarial review item: if run_protocol.py fails for one
    variant, the remaining variants must still run, and an already-recorded
    sibling trial must survive untouched."""
    _set_flag(rpr.ROOT, {
        "config_direct_authoring": {"enabled": True},
        "variant_loop": {"enabled": True},
    })
    root = rpr.ROOT
    _write_protocol(root, "midloop.json")
    run_dir = _minimal_run(root, "run_923")
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, "run_923", {"protocol_ref": "protocols/midloop.json"})
    _write_three_variant_index(run_dir)

    attempted = []

    def _fake_subprocess_run(cmd, *args, **kwargs):
        config_path = cmd[2]
        variant_id = Path(config_path).parent.name
        attempted.append(variant_id)
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)

        if variant_id == "design_v2":
            class _Fail:
                returncode = 1
                stdout = ""
                stderr = "boom"
            return _Fail()

        (out_dir / "protocol_summary.json").write_text(
            rpr.json.dumps(_summary_for(variant_id)), encoding="utf-8")

        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_923"))

    # All three variants were attempted -- design_v2's failure did not stop asset_v2.
    assert set(attempted) == {"base", "design_v2", "asset_v2"}

    state = rpr.load_campaign_state()
    backtest_rows = {t["trial_id"]: t for t in state.get("trial_sharpes", []) if t.get("source") == "backtest"}
    failed_rows = {t["trial_id"]: t for t in state.get("trial_sharpes", []) if t.get("source") == "backtest_failed"}

    assert "run_923:base" in backtest_rows, "base's trial must survive design_v2's failure"
    assert "run_923:asset_v2" in backtest_rows, "asset_v2 must still run after design_v2 failed"
    assert "run_923:design_v2" in failed_rows
    assert "run_923:design_v2" not in backtest_rows


# ---------------------------------------------------------------------------
# 5. _record_backtest_trial / _record_failed_backtest_trial -- trial_id param
# ---------------------------------------------------------------------------

def test_record_backtest_trial_defaults_trial_id_to_run_id():
    config_path = rpr.ROOT / "artifacts" / "candidate_strategy_config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text("{}", encoding="utf-8")
    summary = {"hypothesis_verdict": {"diagnostics": {}}, "per_symbol_summary": {}, "results": []}

    rpr._record_backtest_trial("run_930", summary, config_path)

    state = rpr.load_campaign_state()
    rows = [t for t in state["trial_sharpes"] if t["source"] == "backtest"]
    assert len(rows) == 1
    assert rows[0]["trial_id"] == "run_930"


def test_record_backtest_trial_honors_explicit_trial_id():
    config_path = rpr.ROOT / "artifacts" / "candidate_strategy_config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text("{}", encoding="utf-8")
    summary = {"hypothesis_verdict": {"diagnostics": {}}, "per_symbol_summary": {}, "results": []}

    rpr._record_backtest_trial("run_931", summary, config_path, trial_id="run_931:design_v2")

    state = rpr.load_campaign_state()
    rows = [t for t in state["trial_sharpes"] if t["source"] == "backtest"]
    assert len(rows) == 1
    assert rows[0]["trial_id"] == "run_931:design_v2"


def test_record_failed_backtest_trial_defaults_trial_id_to_run_id():
    config_path = rpr.ROOT / "artifacts" / "candidate_strategy_config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text("{}", encoding="utf-8")

    rpr._record_failed_backtest_trial("run_932", config_path, "boom")

    state = rpr.load_campaign_state()
    rows = [t for t in state["trial_sharpes"] if t["source"] == "backtest_failed"]
    assert len(rows) == 1
    assert rows[0]["trial_id"] == "run_932"


def test_record_failed_backtest_trial_honors_explicit_trial_id():
    config_path = rpr.ROOT / "artifacts" / "candidate_strategy_config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text("{}", encoding="utf-8")

    rpr._record_failed_backtest_trial("run_933", config_path, "boom", trial_id="run_933:asset_v2")

    state = rpr.load_campaign_state()
    rows = [t for t in state["trial_sharpes"] if t["source"] == "backtest_failed"]
    assert len(rows) == 1
    assert rows[0]["trial_id"] == "run_933:asset_v2"


# ---------------------------------------------------------------------------
# 6. _mark_trial_invalidated -- renamed param, exact-match semantics
# ---------------------------------------------------------------------------

def test_mark_trial_invalidated_matches_exact_trial_id_not_run_id_prefix():
    """A compound trial_id must invalidate ONLY that one row -- not a
    sibling row sharing the same run_id prefix (Decision A)."""
    state = rpr.load_campaign_state()
    state.setdefault("trial_sharpes", []).extend([
        {"trial_id": "run_940:base", "source": "backtest", "sharpe": 0.1},
        {"trial_id": "run_940:design_v2", "source": "backtest", "sharpe": 0.2},
    ])
    rpr._save_campaign_state(state)

    marked = rpr._mark_trial_invalidated("run_940:design_v2", "conformance violation")
    assert marked is True

    state = rpr.load_campaign_state()
    by_id = {t["trial_id"]: t for t in state["trial_sharpes"]}
    assert by_id["run_940:design_v2"].get("invalidated_artifact") is True
    assert not by_id["run_940:base"].get("invalidated_artifact")


def test_mark_trial_invalidated_bare_run_id_still_works_for_non_variant_trials():
    """Today's one real call site (run_loop's conformance branch) still
    passes a bare run_id-shaped value -- must still work exactly as before
    for a trial recorded under the old bare-run_id shape."""
    state = rpr.load_campaign_state()
    state.setdefault("trial_sharpes", []).append(
        {"trial_id": "run_941", "source": "backtest", "sharpe": 0.1}
    )
    rpr._save_campaign_state(state)

    marked = rpr._mark_trial_invalidated("run_941", "conformance violation")
    assert marked is True

    state = rpr.load_campaign_state()
    assert state["trial_sharpes"][0].get("invalidated_artifact") is True


# ---------------------------------------------------------------------------
# CODE-REVIEW REGRESSIONS (2026-09-22)
# ---------------------------------------------------------------------------

def test_bridge_file_written_when_base_fails_but_a_sibling_succeeds(monkeypatch):
    """CODE-REVIEW REGRESSION: Decision B's singular artifacts/protocol_result.yaml
    bridge file used to be written ONLY inside the per-variant loop's own
    base-success branch. If base's protocol run failed while a sibling
    variant succeeded, the bridge file was never written at all -- breaking
    every existing singular-file reader (run_loop's conformance branch,
    build_reports.py, verdict-interpreter/SKILL.md) that Decision B exists
    to keep working."""
    _set_flag(rpr.ROOT, {
        "config_direct_authoring": {"enabled": True},
        "variant_loop": {"enabled": True},
    })
    root = rpr.ROOT
    _write_protocol(root, "bridge_fail.json")
    run_dir = _minimal_run(root, "run_950")
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, "run_950", {"protocol_ref": "protocols/bridge_fail.json"})
    _write_three_variant_index(run_dir)

    def _fake_subprocess_run(cmd, *args, **kwargs):
        config_path = cmd[2]
        variant_id = Path(config_path).parent.name
        if variant_id == "base":
            class _Fail:
                returncode = 1
                stdout = ""
                stderr = "base config rejected"
            return _Fail()
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "protocol_summary.json").write_text(
            rpr.json.dumps(_summary_for(variant_id)), encoding="utf-8")

        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_950"))

    bridge_path = run_dir / "artifacts" / "protocol_result.yaml"
    assert bridge_path.exists(), (
        "the singular protocol_result.yaml bridge file must exist whenever ANY "
        "variant succeeded, even when base specifically failed"
    )
    bridge = rpr.load_yaml(bridge_path)
    assert bridge["config_sha256"] in ("sha-design_v2", "sha-asset_v2")

    state = rpr.load_campaign_state()
    trial_ids = {t["trial_id"] for t in state.get("trial_sharpes", [])}
    assert "run_950:design_v2" in trial_ids
    assert "run_950:asset_v2" in trial_ids


def test_c7_failure_does_not_crash_the_stage_or_misrecord_already_successful_trials(monkeypatch):
    """CODE-REVIEW REGRESSION: the C7 pass-rule evaluation block used to run
    completely unguarded -- unlike the grid/reports blocks right below it in
    the same branch. A crash there used to propagate uncaught out of
    run_tool_worker even though every succeeded variant's trial was already
    recorded, leaving clean trial rows with a permanently-missing required
    artifact and no error signal beyond the crash itself. Must now log
    loudly, never re-raise, and never touch the already-recorded trials."""
    _set_flag(rpr.ROOT, {
        "config_direct_authoring": {"enabled": True},
        "variant_loop": {"enabled": True},
    })
    root = rpr.ROOT
    _write_protocol(root, "c7_crash.json")
    run_dir = _minimal_run(root, "run_951")
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, "run_951", {"protocol_ref": "protocols/c7_crash.json"})
    _write_three_variant_index(run_dir)

    def _fake_subprocess_run(cmd, *args, **kwargs):
        config_path = cmd[2]
        variant_id = Path(config_path).parent.name
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "protocol_summary.json").write_text(
            rpr.json.dumps(_summary_for(variant_id)), encoding="utf-8")

        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)

    import verdict_criteria_evaluator as _vce
    def _raise(*args, **kwargs):
        raise RuntimeError("simulated C7 crash")
    monkeypatch.setattr(_vce, "evaluate_pass_rule_criteria", _raise)

    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_951"))

    assert not (run_dir / "artifacts" / "pass_rule_evaluation.yaml").exists(), (
        "C7 genuinely failed -- the file must not exist, but the stage must not crash either"
    )
    state = rpr.load_campaign_state()
    trial_ids = {t["trial_id"] for t in state.get("trial_sharpes", [])
                 if t.get("source") == "backtest"}
    assert {"run_951:base", "run_951:design_v2", "run_951:asset_v2"} <= trial_ids, (
        "all 3 already-succeeded variant trials must remain recorded as successful, "
        "unaffected by the downstream C7 crash"
    )


def test_variant_missing_config_path_recorded_as_failed_trial_not_uncaught_keyerror(monkeypatch):
    """CODE-REVIEW REGRESSION: a validated index.yaml entry missing
    'config_path' (e.g. a corrupted/hand-edited index between routing and
    this stage running) used to raise an uncaught KeyError with ZERO
    trial-ledger accounting -- the one failure mode in this loop that
    wasn't wrapped like every other one."""
    _set_flag(rpr.ROOT, {
        "config_direct_authoring": {"enabled": True},
        "variant_loop": {"enabled": True},
    })
    root = rpr.ROOT
    _write_protocol(root, "missing_config_path.json")
    run_dir = _minimal_run(root, "run_952")
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, "run_952", {"protocol_ref": "protocols/missing_config_path.json"})

    variants_dir = run_dir / "artifacts" / "variants"
    (variants_dir / "base").mkdir(parents=True, exist_ok=True)
    (variants_dir / "base" / "strategy_config.json").write_text(rpr.json.dumps({"variant": "base"}), encoding="utf-8")
    rpr.save_yaml(variants_dir / "index.yaml", {"variants": {
        "base": {"status": "validated", "config_path": "artifacts/variants/base/strategy_config.json"},
        "corrupted": {"status": "validated"},
    }})

    calls = []

    def _fake_subprocess_run(cmd, *args, **kwargs):
        calls.append(cmd)
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "protocol_summary.json").write_text(
            rpr.json.dumps(_summary_for("base")), encoding="utf-8")
        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)

    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_952"))

    assert len(calls) == 1, "only 'base' should reach subprocess.run -- 'corrupted' has no config_path"

    state = rpr.load_campaign_state()
    failed = {t["trial_id"]: t for t in state.get("trial_sharpes", [])
              if t.get("source") == "backtest_failed"}
    assert "run_952:corrupted" in failed, (
        "the missing-config_path variant must be recorded as a failed trial, "
        "not silently dropped with an uncaught KeyError"
    )
    successful = {t["trial_id"] for t in state.get("trial_sharpes", [])
                  if t.get("source") == "backtest"}
    assert "run_952:base" in successful
