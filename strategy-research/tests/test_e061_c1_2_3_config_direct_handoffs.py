"""
E-061 C1.2 + C1.3 (delivery_plan_v26_continuation.md C1; review findings A1, A2;
C2_S1_FINDINGS.md G14), with the code-review fixes -- targeted unit tests. The
joined-up proof is tests/test_e061_end_to_end_wiring.py (A1, A2, A5 and the two
joined-up tests).

C1.2 -- the handoff contract under config-direct authoring:
  * 5a / data gate / protocol_execution / verdict_interpreter load their own
    code-written handoff, rebuilt at every stage entry from the current flags,
    whose required inputs never name validation_protocol.yaml;
  * a stage's outputs are cleared at each attempt's start (moved to
    .previous_attempts/) and must exist after it: step 2's variant_patches.yaml
    (a deliverable in memory only), 5a's variants/index.yaml, the variant-loop
    gate's file for every variant still validated after it;
  * hypothesis_to_innovation_expansion.yaml has one required_inputs key.
C1.3 -- the validation protocol is optional under config-direct:
  * run_tool_worker passes --validation-protocol only when the file exists,
    else --diagnostics-only (config-direct only);
  * run_protocol.py dry-runs the rule evaluator on a passed file before any
    backtest and refuses exactly when it would crash (exit 3, the "no data
    touched" token opening stderr); the orchestrator records such a refusal
    with no trial row only when no window result was written, per variant;
    --diagnostics-only writes the diagnostics block with no rule set; with
    neither flag hypothesis_verdict stays null (composite_cache, manual calls).
Flag off: the legacy handoffs are loaded, nothing new is written, the argv
still carries --validation-protocol, run_protocol.py's output with a validation
protocol is the rule evaluator's for that file, and without one it is null.

Sandboxing: tests/conftest.py's autouse _sandbox_by_default (rpr.ROOT, sr.ROOT
in a per-test tmp_path). No real subprocess, no real backtest, no LLM.
"""
import asyncio
import json
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))
if str(_SR.parent / "trading-bot") not in sys.path:
    sys.path.insert(0, str(_SR.parent / "trading-bot"))

import run_phase1_research as rpr  # noqa: E402
import run_protocol as rp  # noqa: E402
import setup_run as sr  # noqa: E402
import composite_cache as cc  # noqa: E402
import protocol_refusal  # noqa: E402

from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402

_TEMPLATES = _SR / "workflow_artifacts" / "templates" / "handoffs"
_CD_STAGES = ("backtest_specification", "data_availability_gate", "protocol_execution")


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _set_flags(**flags) -> None:
    config_dir = rpr.ROOT / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    rpr.save_yaml(config_dir / "campaign_config.yaml",
                  {"orchestrator": {k: {"enabled": v} for k, v in flags.items()}})


_CD_VL = dict(config_direct_authoring=True, variant_loop=True)


# ---------------------------------------------------------------------------
# C1.2 -- the duplicated required_inputs key
# ---------------------------------------------------------------------------

def test_innovation_expansion_template_has_one_required_inputs_key():
    text = (_TEMPLATES / "hypothesis_to_innovation_expansion.yaml").read_text(encoding="utf-8")
    assert sum(1 for line in text.splitlines() if line.startswith("required_inputs:")) == 1


def test_innovation_expansion_template_parses_as_before():
    """The parse is unchanged: PyYAML kept the LAST duplicate key, which is the
    one left in place (the four inputs, indicator_library.yaml included)."""
    doc = yaml.safe_load((_TEMPLATES / "hypothesis_to_innovation_expansion.yaml")
                         .read_text(encoding="utf-8"))
    assert [x["path"] for x in doc["required_inputs"]] == [
        "artifacts/research_brief.yaml", "artifacts/hypothesis_card.yaml",
        "../../config/available_feeds.yaml", "../../config/indicator_library.yaml"]
    assert doc["deliverables"] == ["expanded_hypothesis_card.yaml", "innovation_notes.yaml"]


# ---------------------------------------------------------------------------
# C1.2 -- the config-direct handoffs
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("variant_loop", [True, False])
@pytest.mark.parametrize("stage", _CD_STAGES + ("verdict_interpreter",))
def test_config_direct_handoff_never_requires_validation_protocol(stage, variant_loop):
    doc = rpr._config_direct_handoff_doc(stage, "run_001", variant_loop)
    paths = [x["path"] for x in doc["required_inputs"]]
    assert "artifacts/validation_protocol.yaml" not in paths
    assert doc["to_stage"] == stage
    assert doc["run_id"] == "run_001" and doc["config_direct_authoring"] is True


def test_config_direct_verdict_interpreter_handoff_is_the_template_minus_the_protocol():
    """Review fix 8 (config-direct + specialist_readers off, outside the target
    flag set -- C1.5 may refuse the combination at launch)."""
    template = yaml.safe_load((_TEMPLATES / "protocol_to_verdict_interpreter.yaml")
                              .read_text(encoding="utf-8"))
    doc = rpr._config_direct_handoff_doc("verdict_interpreter", "run_001", True)
    assert doc["assigned_engine"] == "claude"
    assert [x["path"] for x in doc["required_inputs"]] == [
        x["path"] for x in template["required_inputs"]
        if x["path"] != "artifacts/validation_protocol.yaml"]
    assert doc["deliverables"] == template["deliverables"]


def test_config_direct_handoff_path_is_none_off_the_flag_or_the_stages():
    run_dir = _minimal_run(rpr.ROOT, "run_001")
    (run_dir / "handoffs").mkdir()
    assert rpr._config_direct_handoff_path("verdict_interpreter", "run_001", run_dir,
                                           rebuild=True) is None  # flag off
    _set_flags(config_direct_authoring=True)
    assert rpr._config_direct_handoff_path("validation", "run_001", run_dir,
                                           rebuild=True) is None
    assert not list((run_dir / "handoffs").iterdir())
    path = rpr._config_direct_handoff_path("verdict_interpreter", "run_001", run_dir,
                                           rebuild=False)  # created when missing
    assert path == run_dir / "handoffs" / "config_direct_verdict_interpreter.yaml"
    assert path.exists()


@pytest.mark.parametrize("variant_loop,inputs,deliverables", [
    (True, ["artifacts/variants/index.yaml"], ["variants/index.yaml"]),
    (False, ["artifacts/candidate_strategy_config.json"], ["data_availability_gate.yaml"]),
])
def test_config_direct_gate_handoff_matches_what_the_gate_writes(variant_loop, inputs,
                                                                 deliverables):
    doc = rpr._config_direct_handoff_doc("data_availability_gate", "run_001", variant_loop)
    assert [x["path"] for x in doc["required_inputs"]] == inputs
    assert doc["deliverables"] == deliverables


def test_config_direct_5a_and_protocol_handoffs():
    bs = rpr._config_direct_handoff_doc("backtest_specification", "run_001", True)
    assert [x["path"] for x in bs["required_inputs"]] == [
        "artifacts/backtest_spec.yaml", "artifacts/variant_patches.yaml"]
    assert bs["deliverables"] == ["variants/index.yaml"]
    for vl, want in ((True, "artifacts/variants/index.yaml"),
                     (False, "artifacts/candidate_strategy_config.json")):
        pe = rpr._config_direct_handoff_doc("protocol_execution", "run_001", vl)
        assert [x["path"] for x in pe["required_inputs"]] == [want]
        assert pe["deliverables"] == ["protocol_result.yaml"]


def test_config_direct_handoff_unknown_stage_raises():
    with pytest.raises(ValueError, match="no config-direct handoff"):
        rpr._config_direct_handoff_doc("validation", "run_001", True)


def test_config_direct_handoff_path_rebuilds_from_the_current_flags():
    """Review fix 6: run_loop's rebuild=True rewrites it at every entry; the
    rebuild=False read (async_invoke_agent) never overwrites run_loop's file."""
    _set_flags(**_CD_VL)
    run_dir = _minimal_run(rpr.ROOT, "run_001")
    (run_dir / "handoffs").mkdir()
    path = rpr._config_direct_handoff_path("protocol_execution", "run_001", run_dir,
                                           rebuild=True)
    assert path == run_dir / "handoffs" / "config_direct_protocol_execution.yaml"
    assert rpr.load_yaml(path) == rpr._config_direct_handoff_doc("protocol_execution",
                                                                  "run_001", True)
    _set_flags(config_direct_authoring=True)  # variant loop switched off
    rpr._config_direct_handoff_path("protocol_execution", "run_001", run_dir, rebuild=True)
    assert rpr.load_yaml(path) == rpr._config_direct_handoff_doc("protocol_execution",
                                                                  "run_001", False)
    rpr.save_yaml(path, {"injected": True})
    assert rpr._config_direct_handoff_path("protocol_execution", "run_001", run_dir,
                                           rebuild=False) == path
    assert rpr.load_yaml(path) == {"injected": True}


def test_config_direct_step2_deliverables():
    assert rpr._config_direct_step2_deliverables("innovation_expansion") == []  # flag off
    _set_flags(config_direct_authoring=True)
    assert rpr._config_direct_step2_deliverables("validation") == []
    assert rpr._config_direct_step2_deliverables("innovation_expansion") == [
        "variant_patches.yaml"]
    handoff = {"deliverables": ["expanded_hypothesis_card.yaml", "innovation_notes.yaml"]}
    run_dir = _minimal_run(rpr.ROOT, "run_001")
    rpr._apply_config_direct_authoring_context("innovation_expansion", handoff, run_dir)
    rpr._apply_config_direct_authoring_context("innovation_expansion", handoff, run_dir)
    assert handoff["deliverables"] == ["expanded_hypothesis_card.yaml", "innovation_notes.yaml",
                                       "variant_patches.yaml"]


# ---- run_loop: which handoff each stage loads ------------------------------

class _Stop(RuntimeError):
    pass


def _run_at(run_id: str, pending_stage: str) -> Path:
    if not (rpr.ROOT / "runs" / run_id).exists():
        sr.setup_run(run_id)
    run_dir = rpr.ROOT / "runs" / run_id
    rpr.update_state(path=run_dir, pending_stage=pending_stage, status="active",
                     last_error=None)
    return run_dir


def _drive(monkeypatch, run_id: str, body=None) -> list:
    """run_loop with the stage body replaced: `body(stage_name)` (default: stop
    the run). Returns [(handoff name, loaded doc)] for every handoff loaded."""
    loaded = []
    real_load = rpr.load_yaml

    def _spy(path):
        doc = real_load(path)
        p = Path(path)  # a run's handoffs/ dir (not the templates' handoffs/ dir)
        if p.parent.name == "handoffs" and p.parent.parent.parent.name == "runs":
            loaded.append((Path(path).name, doc))
        return doc

    async def _invoke(stage_name, rid, retry_context=None):
        if body is None or body(stage_name) is _Stop:
            raise _Stop(f"stopped at {stage_name}")

    monkeypatch.setattr(rpr, "load_yaml", _spy)
    monkeypatch.setattr(rpr, "async_invoke_agent", _invoke)
    rpr.run_loop(run_id)
    return loaded


def _last_error(run_dir: Path):
    return rpr.load_yaml(run_dir / "pipeline_state.yaml").get("last_error") or ""


_LEGACY = {"backtest_specification": "validation_to_backtest_specification.yaml",
           "data_availability_gate": "backtest_spec_to_data_availability_gate.yaml",
           "protocol_execution": "backtest_spec_to_protocol_execution.yaml",
           "verdict_interpreter": "protocol_to_verdict_interpreter.yaml"}


@pytest.mark.parametrize("stage", _CD_STAGES)
def test_run_loop_flag_off_loads_the_legacy_handoff(monkeypatch, stage):
    """Flag off: the STAGE_CONFIGS handoff, and no config-direct file is written."""
    run_dir = _run_at("run_001", stage)
    arts = run_dir / "artifacts"
    for rel in ("expanded_hypothesis_card.yaml", "validation_protocol.yaml"):
        (arts / rel).write_text("{}", encoding="utf-8")
    (arts / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    if stage == "data_availability_gate":
        rpr._create_remaining_handoffs("run_001", run_dir)
    before = sorted(p.name for p in (run_dir / "handoffs").iterdir())
    loaded = _drive(monkeypatch, "run_001")
    assert loaded[0][0] == _LEGACY[stage]
    assert f"stopped at {stage}" in _last_error(run_dir)
    assert sorted(p.name for p in (run_dir / "handoffs").iterdir()) == before
    assert not list((run_dir / "handoffs").glob("config_direct_*"))


@pytest.mark.parametrize("stage", _CD_STAGES)
def test_run_loop_config_direct_loads_its_own_handoff(monkeypatch, stage):
    _set_flags(**_CD_VL)
    run_dir = _run_at("run_001", stage)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "backtest_spec.yaml", {"status": "spec_ready", "config": {}})
    rpr.save_yaml(arts / "variant_patches.yaml", {"variants": []})
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {}})
    assert not (arts / "validation_protocol.yaml").exists()
    loaded = _drive(monkeypatch, "run_001")
    assert loaded[0][0] == rpr._CONFIG_DIRECT_HANDOFFS[stage]
    assert f"stopped at {stage}" in _last_error(run_dir)


def test_run_loop_config_direct_verdict_interpreter_needs_no_validation_protocol(monkeypatch):
    """Review fix 8: config-direct + specialist_readers off reaches verdict_interpreter;
    its handoff no longer requires validation_protocol.yaml."""
    _set_flags(config_direct_authoring=True)
    run_dir = _run_at("run_001", "verdict_interpreter")
    arts = run_dir / "artifacts"
    for rel in ("protocol_result.yaml", "backtest_spec.yaml", "research_brief.yaml"):
        (arts / rel).write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr(rpr, "_ensure_regime_detector_report", lambda rid, rd: None)
    monkeypatch.setattr(rpr, "_inject_regime_context_into_handoff", lambda *a, **k: None)
    loaded = _drive(monkeypatch, "run_001")
    assert loaded[0][0] == "config_direct_verdict_interpreter.yaml"
    assert "stopped at verdict_interpreter" in _last_error(run_dir)


def test_run_loop_handoff_shape_follows_the_flags_across_a_resume(monkeypatch):
    """Review fix 6: variant loop on -> stop -> off -> resume loads the non-loop shape."""
    _set_flags(**_CD_VL)
    run_dir = _run_at("run_001", "protocol_execution")
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {}})
    (arts / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    first = _drive(monkeypatch, "run_001")
    assert [x["path"] for x in first[0][1]["required_inputs"]] == [
        "artifacts/variants/index.yaml"]
    _set_flags(config_direct_authoring=True)
    _run_at("run_001", "protocol_execution")
    second = _drive(monkeypatch, "run_001")
    assert second[0][0] == "config_direct_protocol_execution.yaml"
    assert [x["path"] for x in second[0][1]["required_inputs"]] == [
        "artifacts/candidate_strategy_config.json"]


# ---- step 2: variant_patches.yaml, in memory and fresh ----------------------

def _step2_run(run_id="run_001") -> Path:
    run_dir = _run_at(run_id, "innovation_expansion")
    arts = run_dir / "artifacts"
    for rel in ("research_brief.yaml", "hypothesis_card.yaml", "backtest_spec.yaml"):
        (arts / rel).write_text("{}\n", encoding="utf-8")
    for rel in ("available_feeds.yaml", "indicator_library.yaml"):
        (rpr.ROOT / "config" / rel).write_text("{}\n", encoding="utf-8")
    return run_dir


def _writes(arts: Path, names):
    def _body(stage_name):
        if stage_name != "innovation_expansion":
            return _Stop
        for rel in names:
            (arts / rel).write_text("{}\n", encoding="utf-8")
    return _body


_TWO = ("expanded_hypothesis_card.yaml", "innovation_notes.yaml")


def test_step2_without_variant_patches_fails_the_stage(monkeypatch):
    _set_flags(config_direct_authoring=True)
    run_dir = _step2_run()
    _drive(monkeypatch, "run_001", _writes(run_dir / "artifacts", _TWO))
    st = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert st["status"] == "failed" and "variant_patches.yaml" in st["last_error"]


def test_step2_previous_variant_patches_is_cleared_and_fails_the_stage(monkeypatch):
    """Review round 3 (fixes 4/5): a previous attempt's variant_patches.yaml is
    moved aside at the attempt's start, so it can never satisfy the check."""
    _set_flags(config_direct_authoring=True)
    run_dir = _step2_run()
    old = run_dir / "artifacts" / "variant_patches.yaml"
    old.write_text("variants: []\n", encoding="utf-8")
    _drive(monkeypatch, "run_001", _writes(run_dir / "artifacts", _TWO))
    assert "variant_patches.yaml" in _last_error(run_dir)
    assert not old.exists()
    kept = list((run_dir / ".previous_attempts").rglob("variant_patches.yaml"))
    assert [k.read_text(encoding="utf-8") for k in kept] == ["variants: []\n"]


def test_step2_composition_mode_in_process_write_passes(monkeypatch):
    """Composition mode writes variant_patches.yaml in-process (code, no LLM):
    cleared at entry, written by the attempt, the check passes."""
    _set_flags(config_direct_authoring=True)
    run_dir = _step2_run()
    arts = run_dir / "artifacts"
    (arts / "variant_patches.yaml").write_text("variants: [previous]\n", encoding="utf-8")
    monkeypatch.setattr(rpr, "_composition_mode", lambda rd: True)
    monkeypatch.setattr(rpr, "_composition_variant_patches", lambda rd: rpr.save_yaml(
        Path(rd) / "artifacts" / "variant_patches.yaml", {"variants": ["this attempt"]}))
    _drive(monkeypatch, "run_001")  # step 2 is code; the next (tool) stage stops
    assert "stopped at backtest_specification" in _last_error(run_dir)
    assert rpr.load_yaml(arts / "variant_patches.yaml") == {"variants": ["this attempt"]}


def test_step2_deliverable_is_never_persisted_and_a_flag_off_resume_ignores_it(monkeypatch):
    """Review fix 7: after a flag-on attempt the run's handoff file does not list
    variant_patches.yaml, so a flag-off resume does not require it."""
    _set_flags(config_direct_authoring=True)
    run_dir = _step2_run()
    _drive(monkeypatch, "run_001", _writes(run_dir / "artifacts", _TWO))
    assert "variant_patches.yaml" in _last_error(run_dir)  # flag on: required
    on_disk = rpr.load_yaml(run_dir / "handoffs" / "hypothesis_to_innovation_expansion.yaml")
    assert "variant_patches.yaml" not in on_disk["deliverables"]
    _set_flags()  # flag off
    _step2_run()
    _drive(monkeypatch, "run_001", _writes(run_dir / "artifacts", _TWO))
    st = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert "stopped at validation" in st["last_error"]  # step 2 passed, next stage reached


def test_step2_writes_all_three_passes(monkeypatch):
    _set_flags(config_direct_authoring=True)
    run_dir = _step2_run()
    _drive(monkeypatch, "run_001",
           _writes(run_dir / "artifacts", _TWO + ("variant_patches.yaml",)))
    assert "stopped at strategy_config_authoring" not in _last_error(run_dir)
    assert "stopped at backtest_specification" in _last_error(run_dir)


# ---- 5a and the variant-loop gate: outputs of this attempt ------------------

def _gate_or_5a_run(stage: str) -> Path:
    _set_flags(**_CD_VL)
    run_dir = _run_at("run_001", stage)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "backtest_spec.yaml", {"status": "spec_ready", "config": {}})
    rpr.save_yaml(arts / "variant_patches.yaml", {"variants": []})
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {
        "base": {"status": "validated", "config_path": "x"},
        "design": {"status": "validated", "config_path": "y"}}})
    for vid in ("base", "design"):  # a previous attempt's gate files
        rpr.save_yaml(arts / "variants" / vid / "data_availability_gate.yaml",
                      {"outcome": "validate", "attempt": "previous"})
    return run_dir


def test_5a_previous_index_is_cleared_and_fails(monkeypatch):
    run_dir = _gate_or_5a_run("backtest_specification")
    _drive(monkeypatch, "run_001", lambda s: None if s == "backtest_specification" else _Stop)
    assert "index.yaml" in _last_error(run_dir)
    assert not (run_dir / "artifacts" / "variants" / "index.yaml").exists()
    assert list((run_dir / ".previous_attempts").rglob("index.yaml"))


def test_gate_that_writes_nothing_fails(monkeypatch):
    """The previous attempt's gate files are cleared; a gate that writes nothing
    leaves every still-validated variant without one."""
    run_dir = _gate_or_5a_run("data_availability_gate")
    _drive(monkeypatch, "run_001", lambda s: None if s == "data_availability_gate" else _Stop)
    err = _last_error(run_dir)
    assert "did not write" in err and "base" in err and "design" in err


def test_gate_missing_a_validated_variants_file_fails(monkeypatch):
    run_dir = _gate_or_5a_run("data_availability_gate")
    arts = run_dir / "artifacts"

    def _body(stage):
        if stage != "data_availability_gate":
            return _Stop
        rpr.save_yaml(arts / "variants" / "base" / "data_availability_gate.yaml",
                      {"outcome": "validate"})  # design's file is not written

    _drive(monkeypatch, "run_001", _body)
    err = _last_error(run_dir)
    assert "did not write" in err
    assert "design" in err and "\\base\\" not in err and "/base/" not in err


def test_gate_checks_exactly_the_variants_still_validated(monkeypatch):
    """A variant whose gate crashed is marked not_tested and is not required."""
    run_dir = _gate_or_5a_run("data_availability_gate")
    arts = run_dir / "artifacts"

    def _body(stage):
        if stage != "data_availability_gate":
            return _Stop
        rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {
            "base": {"status": "validated", "config_path": "x"},
            "design": {"status": "not_tested", "reason": "data_availability_gate.py crashed"}}})
        rpr.save_yaml(arts / "variants" / "base" / "data_availability_gate.yaml",
                      {"outcome": "validate"})

    _drive(monkeypatch, "run_001", _body)
    assert "did not write" not in _last_error(run_dir)


# ---------------------------------------------------------------------------
# C1.3 -- run_tool_worker
# ---------------------------------------------------------------------------

def test_one_definition_of_the_refusal_signal():
    """Review round 3 fix 9: both sides use tools/protocol_refusal.py."""
    assert rp.EXIT_NO_DATA_TOUCHED is protocol_refusal.EXIT_NO_DATA_TOUCHED
    assert rp.NO_DATA_TOUCHED_TOKEN is protocol_refusal.NO_DATA_TOUCHED_TOKEN
    assert rpr._protocol_refusal is protocol_refusal
    assert not hasattr(rpr, "_RUN_PROTOCOL_NO_DATA_EXIT")


def test_validation_protocol_args(tmp_path):
    vp = tmp_path / "validation_protocol.yaml"
    assert rpr._validation_protocol_args(vp) == ["--validation-protocol", str(vp)]  # flag off
    _set_flags(config_direct_authoring=True)
    assert rpr._validation_protocol_args(vp) == ["--diagnostics-only"]
    vp.write_text("{}", encoding="utf-8")
    assert rpr._validation_protocol_args(vp) == ["--validation-protocol", str(vp)]


class _Done:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


def _fake_protocol_run(calls: list, result=None):
    def _run(cmd, *a, **k):
        calls.append([str(c) for c in cmd])
        if result is not None:
            return result
        out = Path(cmd[cmd.index("--out-dir") + 1])
        out.mkdir(parents=True, exist_ok=True)
        (out / "protocol_summary.json").write_text(json.dumps({
            "config_sha256": "x", "protocol_file": "p", "results": [],
            "per_symbol_summary": {"BTCUSDT": {"median_sharpe": 0.1}}, "verdict": "refine",
            "hypothesis_verdict": None}), encoding="utf-8")
        return _Done()
    return _run


def _pinned_run(run_id: str) -> Path:
    _write_protocol(rpr.ROOT, "p.json")
    run_dir = _minimal_run(rpr.ROOT, run_id)
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": "protocols/p.json"})
    return run_dir


def _variant_loop_run(run_id: str) -> Path:
    run_dir = _pinned_run(run_id)
    arts = run_dir / "artifacts"
    (arts / "variants" / "base").mkdir(parents=True)
    (arts / "variants" / "base" / "strategy_config.json").write_text("{}", encoding="utf-8")
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {"base": {
        "status": "validated", "config_path": "artifacts/variants/base/strategy_config.json"}}})
    return run_dir


def test_flag_off_protocol_execution_argv_unchanged(monkeypatch):
    """Flag off: exactly the pre-C1.3 argv -- --validation-protocol passed, in the
    same position, even when the file is absent; never --diagnostics-only."""
    run_dir = _pinned_run("run_910")
    arts = run_dir / "artifacts"
    (arts / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    calls = []
    monkeypatch.setattr(rpr.subprocess, "run", _fake_protocol_run(calls))
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_910"))
    assert calls == [[
        "stub-python", str(rpr.ROOT / "tools" / "run_protocol.py"),
        str(arts / "candidate_strategy_config.json"),
        str(rpr._resolve_protocol_path(run_dir, "run_910")),
        "--validation-protocol", str(arts / "validation_protocol.yaml"),
        "--out-dir", str(run_dir)]]


@pytest.mark.parametrize("with_file", [False, True])
def test_variant_loop_argv(monkeypatch, with_file):
    _set_flags(**_CD_VL)
    run_dir = _variant_loop_run("run_911")
    arts = run_dir / "artifacts"
    if with_file:
        (arts / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    calls = []
    monkeypatch.setattr(rpr.subprocess, "run", _fake_protocol_run(calls))
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_911"))
    (argv,) = calls
    assert argv == [
        "stub-python", str(rpr.ROOT / "tools" / "run_protocol.py"),
        str(arts / "variants" / "base" / "strategy_config.json"),
        str(rpr._resolve_protocol_path(run_dir, "run_911")),
        *(["--validation-protocol", str(arts / "validation_protocol.yaml")] if with_file
          else ["--diagnostics-only"]),
        "--out-dir", str(run_dir / "variants" / "base")]


def test_config_direct_without_variant_loop_argv(monkeypatch):
    _set_flags(config_direct_authoring=True)
    run_dir = _pinned_run("run_912")
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    calls = []
    monkeypatch.setattr(rpr.subprocess, "run", _fake_protocol_run(calls))
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_912"))
    (argv,) = calls
    assert "--validation-protocol" not in argv and "--diagnostics-only" in argv


_TOKEN_LINE = f"{protocol_refusal.NO_DATA_TOUCHED_TOKEN}: bad validation protocol\n"
_REFUSED = _Done(protocol_refusal.EXIT_NO_DATA_TOUCHED, stderr=_TOKEN_LINE)


def _legacy_run(run_id: str) -> Path:
    run_dir = _pinned_run(run_id)
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    return run_dir


def test_refusal_before_any_backtest_legacy_branch_records_no_trial(monkeypatch):
    """Exit 3, the token opening stderr, no window written -> engineering failure."""
    _legacy_run("run_913")
    monkeypatch.setattr(rpr.subprocess, "run", _fake_protocol_run([], _REFUSED))
    with pytest.raises(RuntimeError, match="no data touched"):
        asyncio.run(rpr.run_tool_worker("protocol_execution", "run_913"))
    assert rpr.load_campaign_state().get("trial_sharpes", []) == []


def _abc_run(run_id: str) -> Path:
    run_dir = _pinned_run(run_id)
    arts = run_dir / "artifacts"
    index = {}
    for vid in ("a", "b", "c"):
        (arts / "variants" / vid).mkdir(parents=True)
        (arts / "variants" / vid / "strategy_config.json").write_text("{}", encoding="utf-8")
        index[vid] = {"status": "validated",
                      "config_path": f"artifacts/variants/{vid}/strategy_config.json"}
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": index})
    return run_dir


def test_variant_loop_one_refused_variant_the_others_run(monkeypatch):
    """Review round 3 fix 6: variant a is refused before any backtest -> not_tested,
    no trial row; b and c run and record their trials; the post-loop artifacts
    (the protocol_result.yaml bridge) are written."""
    _set_flags(**_CD_VL)
    run_dir = _abc_run("run_915")
    ok = _fake_protocol_run([])

    def _run(cmd, *a, **k):
        if Path(cmd[cmd.index("--out-dir") + 1]).name == "a":
            return _REFUSED
        return ok(cmd, *a, **k)

    monkeypatch.setattr(rpr.subprocess, "run", _run)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_915"))
    rows = rpr.load_campaign_state().get("trial_sharpes", [])
    assert sorted((r["trial_id"], r["source"]) for r in rows) == [
        ("run_915:b", "backtest"), ("run_915:c", "backtest")]
    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]
    assert index["a"]["status"] == "not_tested"
    assert "no data touched" in index["a"]["reason"]
    assert index["b"]["status"] == index["c"]["status"] == "validated"
    assert (run_dir / "artifacts" / "protocol_result.yaml").exists()


def _writes_a_window_then(result):
    """A fake run_protocol.py that writes one window result, then exits `result`."""
    def _run(cmd, *a, **k):
        out = Path(cmd[cmd.index("--out-dir") + 1])
        (out / "results" / "win_1").mkdir(parents=True, exist_ok=True)
        return result
    return _run


@pytest.mark.parametrize("variant_loop", [True, False])
@pytest.mark.parametrize("case", ["exit1", "exit3_no_token", "token_not_first_line",
                                  "spoofed_after_windows"])
def test_real_backtest_failure_still_records_its_trial(monkeypatch, variant_loop, case):
    """Anything but exit 3 + the token opening stderr + no window written by the
    call is a real (data-touching) failure: a backtest_failed row."""
    if variant_loop:
        _set_flags(**_CD_VL)
        _variant_loop_run("run_914")
    else:
        _legacy_run("run_914")
    fake = {
        "exit1": _fake_protocol_run([], _Done(1, stderr="Traceback: boom")),
        "exit3_no_token": _fake_protocol_run([], _Done(3, stderr="exit 3 without the token")),
        "token_not_first_line": _fake_protocol_run([], _Done(3, stderr="window log\n" +
                                                             _TOKEN_LINE)),
        "spoofed_after_windows": _writes_a_window_then(_REFUSED),
    }[case]
    monkeypatch.setattr(rpr.subprocess, "run", fake)
    with pytest.raises(RuntimeError):
        asyncio.run(rpr.run_tool_worker("protocol_execution", "run_914"))
    rows = rpr.load_campaign_state().get("trial_sharpes", [])
    assert [r["source"] for r in rows] == ["backtest_failed"]


def test_stderr_declares_no_data_touched_is_anchored():
    t = protocol_refusal.NO_DATA_TOUCHED_TOKEN
    assert protocol_refusal.stderr_declares_no_data_touched(f"{t}: x\nmore")
    assert not protocol_refusal.stderr_declares_no_data_touched(f"warning\n{t}: x")
    assert not protocol_refusal.stderr_declares_no_data_touched(None)


# ---- the trial row under config-direct (G14, intended) ----------------------

def _sparse_summary(hypothesis_verdict, median_sharpe=0.3):
    return {"config_sha256": "x", "protocol_file": "p", "verdict": "refine",
            "results": [{"symbol": "BTCUSDT", "window": f"w{i}", "run_id": f"r{i}",
                         "core": {"trade_count": 2, "sharpe": None}} for i in range(4)],
            "per_symbol_summary": {"BTCUSDT": {"median_sharpe": median_sharpe}},
            "hypothesis_verdict": hypothesis_verdict}


@pytest.mark.parametrize("median_sharpe,before", [(0.3, "sharpe"), (None, "neither")])
def test_trial_row_statistic_valid_and_expectancy_under_diagnostics_only(tmp_path,
                                                                       median_sharpe, before):
    """G14: a sparse strategy (every window < 5 trades). With hypothesis_verdict
    null (what a config-direct row would read without the diagnostics; on master
    those runs recorded only a backtest_failed row): below_floor_pct 0,
    statistic_valid 'sharpe' -- or 'neither' when median_sharpe is None --,
    expectancy_bps None. Under --diagnostics-only: below_floor_pct 100 ->
    statistic_valid 'expectancy', expectancy_bps the per-trade mean."""
    cfg = tmp_path / "c.json"
    cfg.write_text("{}", encoding="utf-8")
    tds = {"per_trade_expectancy_bps": {"mean": -7.5, "se": 2.0, "t_stat": -3.7, "n": 8},
           "zero_trade_slot_pct": 0.0, "fee_reduction_metrics": None}
    rpr._record_backtest_trial("run_a", _sparse_summary(None, median_sharpe), cfg)
    s = _sparse_summary(None, median_sharpe)
    s["hypothesis_verdict"] = rp.diagnostics_only_hypothesis_verdict(s["results"], tds)
    rpr._record_backtest_trial("run_b", s, cfg)
    rows = {r["trial_id"]: r for r in rpr.load_campaign_state()["trial_sharpes"]}
    assert (rows["run_a"]["statistic_valid"], rows["run_a"]["expectancy_bps"],
            rows["run_a"]["below_floor_pct"]) == (before, None, 0.0)
    assert (rows["run_b"]["statistic_valid"], rows["run_b"]["expectancy_bps"],
            rows["run_b"]["below_floor_pct"]) == ("expectancy", -7.5, 100.0)
    assert rows["run_a"]["sharpe"] == rows["run_b"]["sharpe"] == median_sharpe


# ---------------------------------------------------------------------------
# C1.3 -- run_protocol.py
# ---------------------------------------------------------------------------

class _StubBacktest:
    """run_backtest stand-in: one metrics.json per window, counted."""

    def __init__(self, root: Path):
        self.root, self.calls = root, 0

    def __call__(self, cfg_path, symbol, start, end, results_root, **kwargs):
        self.calls += 1
        rd = self.root / f"stub_run_{self.calls}"
        rd.mkdir(parents=True, exist_ok=True)
        (rd / "metrics.json").write_text(json.dumps({"core": {
            "trade_count": 12, "net_pnl": 1.0, "sharpe": 0.4, "win_rate": 0.5,
            "max_drawdown_pct": -2.0, "forecast_return_corr": 0.03, "gross_pnl": 2.0,
            "cost_drag_pct": 40.0, "avg_trade_duration_bars": 6}}), encoding="utf-8")
        return rd


def _main(monkeypatch, tmp_path, *extra) -> tuple:
    stub = _StubBacktest(tmp_path / "sandbox_runs")
    monkeypatch.setattr(rp, "run_backtest", stub)
    monkeypatch.setattr(rp, "_RESULTS_ROOT", str(tmp_path / "results"))
    protocol = {"symbols": ["BTCUSDT"],
                "windows": [{"label": f"w{i}", "test": {"start": f"2022-0{i}-01",
                                                        "end": f"2022-0{i}-02"}}
                            for i in (1, 2)],
                "promotion": {"median_sharpe_gt": 0, "max_abs_drawdown_pct_lt": 25,
                              "min_trade_count_gte": 1, "kill_median_sharpe_lt": -1}}
    (tmp_path / "protocol.json").write_text(json.dumps(protocol), encoding="utf-8")
    (tmp_path / "config.json").write_text(json.dumps({"dummy": True}), encoding="utf-8")
    out = tmp_path / "out"
    monkeypatch.setattr(sys, "argv", ["run_protocol.py", str(tmp_path / "config.json"),
                                      str(tmp_path / "protocol.json"), "--out-dir", str(out),
                                      *extra])
    rp.main()
    return json.loads((out / "protocol_summary.json").read_text(encoding="utf-8")), stub


def test_run_protocol_without_flags_keeps_hypothesis_verdict_null(monkeypatch, tmp_path):
    """Review fix 2: a manual call or composite_cache (neither flag) is unchanged."""
    summary, _stub = _main(monkeypatch, tmp_path)
    assert summary["hypothesis_verdict"] is None


def test_composite_cache_runner_passes_neither_flag(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(cc.subprocess, "run",
                        lambda cmd, *a, **k: calls.append([str(c) for c in cmd]) or _Done())
    cc.subprocess_runner("py")(tmp_path / "c.json", tmp_path / "p.json", tmp_path / "o")
    (argv,) = calls
    assert "--diagnostics-only" not in argv and "--validation-protocol" not in argv


def test_run_protocol_diagnostics_only_writes_diagnostics(monkeypatch, tmp_path):
    summary, _stub = _main(monkeypatch, tmp_path, "--diagnostics-only")
    hv = summary["hypothesis_verdict"]
    assert hv["verdict"] is None
    assert hv["verdict_reason"] == rp.DIAGNOSTICS_ONLY_VERDICT_REASON
    assert hv["criteria_results"] == []
    diag = hv["diagnostics"]
    assert diag["median_gross_pnl"] == 2.0
    assert diag["median_cost_drag_pct"] == 40.0
    assert diag["median_forecast_return_corr"] == 0.03
    assert diag["below_floor_pct"] == 0.0
    assert diag["win_rate_vs_sharpe"] == rp.WIN_RATE_VS_SHARPE_NO_RULES


def _results_and_tds():
    results = [{"symbol": "BTCUSDT", "window": "w1", "run_id": "r1", "regime_validity": {},
                "core": {"trade_count": 3, "sharpe": None, "gross_pnl": -1.0,
                         "cost_drag_pct": 12.0, "forecast_return_corr": -0.01}}]
    per_symbol = {"BTCUSDT": {"median_sharpe": None, "max_abs_drawdown_pct": 1.0,
                              "min_trade_count": 3, "zero_trade_slot_pct": 0.0}}
    tds = {"per_trade_expectancy_bps": {"mean": -4.0, "se": 2.0, "t_stat": -2.0, "n": 3},
           "zero_trade_slot_pct": 0.0, "fee_reduction_metrics": None}
    return results, per_symbol, tds


def test_diagnostics_only_equals_the_evaluator_diagnostics_without_criteria(monkeypatch):
    """Review fixes 3/9: same block as the rule evaluator's, except the one
    criteria-derived field; and no second extended-summary build."""
    results, per_symbol, tds = _results_and_tds()
    full = rp.evaluate_against_decision_rules(per_symbol, results, {}, tds)
    calls = []
    monkeypatch.setattr(rp, "_build_extended_summary",
                        lambda *a, **k: calls.append(a) or {})
    only = rp.diagnostics_only_hypothesis_verdict(results, tds)
    assert calls == []
    assert full["diagnostics"]["win_rate_vs_sharpe"] == "both PASS or N/A"
    assert only["diagnostics"]["win_rate_vs_sharpe"] == rp.WIN_RATE_VS_SHARPE_NO_RULES
    strip = lambda d: {k: v for k, v in d.items() if k != "win_rate_vs_sharpe"}  # noqa: E731
    assert strip(only["diagnostics"]) == strip(full["diagnostics"])
    assert only["diagnostics"]["below_floor_pct"] == 100.0  # 3 < the sparse floor
    assert only["diagnostics"]["per_trade_expectancy_bps"]["mean"] == -4.0


def test_evaluator_diagnostics_unchanged_by_the_refactor():
    """The moved block still reads the criteria: a sharpe FAIL with a win-rate PASS."""
    results, per_symbol, tds = _results_and_tds()
    rows = [{"field": "median_win_rate", "result": "PASS"},
            {"field": "median_sharpe", "result": "FAIL"}]
    assert rp._build_diagnostics(results, rows, tds)["win_rate_vs_sharpe"] == \
        "win_rate PASS + sharpe FAIL"
    assert rp._build_diagnostics(results, [], tds)["win_rate_vs_sharpe"] == "both PASS or N/A"


def test_run_protocol_with_validation_protocol_is_the_rule_evaluator(monkeypatch, tmp_path):
    vp_doc = {"decision_rules": {"approve_if_all_met": ["median_sharpe > 0"],
                                 "reject_if_any_met": ["median_sharpe < -1"]},
              "required_evidence": []}
    vp = tmp_path / "validation_protocol.yaml"
    vp.write_text(yaml.safe_dump(vp_doc), encoding="utf-8")
    summary, _stub = _main(monkeypatch, tmp_path, "--validation-protocol", str(vp))
    hv = summary["hypothesis_verdict"]
    expected = rp.evaluate_against_decision_rules(
        summary["per_symbol_summary"], summary["results"], vp_doc,
        summary["trade_diagnostics_summary"] or None,
        runs_root=str((tmp_path / "out" / "results").resolve()), timeframe="1h")
    assert json.loads(json.dumps(expected, default=str)) == hv
    assert hv["verdict"] == "promote" and hv["criteria_results"]


_REAL_RUNS = _SR / "runs"


def _real_protocol_copy(run_id: str, tmp_path: Path) -> Path:
    """A byte copy of a real run's validation_protocol.yaml (the real file is
    only read, never modified)."""
    src = _REAL_RUNS / run_id / "artifacts" / "validation_protocol.yaml"
    if not src.exists():
        pytest.skip(f"{src} not in this checkout")
    dst = tmp_path / f"{run_id}_validation_protocol.yaml"
    dst.write_bytes(src.read_bytes())
    return dst


def _assert_refused_before_any_backtest(monkeypatch, tmp_path, capsys, vp: Path) -> None:
    with pytest.raises(SystemExit) as exc:
        _main(monkeypatch, tmp_path, "--validation-protocol", str(vp))
    assert exc.value.code == protocol_refusal.EXIT_NO_DATA_TOUCHED
    assert protocol_refusal.stderr_declares_no_data_touched(capsys.readouterr().err)
    assert rp.run_backtest.calls == 0
    assert not (tmp_path / "out" / "protocol_summary.json").exists()


@pytest.mark.parametrize("content", [
    None,                                              # file missing
    "",                                                # empty (None: .get crashes)
    "decision_rules: [unclosed\n",                     # unparseable
    "- a\n- b\n",                                      # a list, not a mapping
    "decision_rules:\n  approve_if_all_met: null\n",   # list(None) crashes
    b"decision_rules: [\x93median_sharpe > 0\x94]\n",  # cp1252 smart quotes, not UTF-8
], ids=["missing", "empty", "unparseable", "list", "approve_if_all_met_null", "cp1252"])
def test_bad_validation_protocol_refused_before_any_backtest(monkeypatch, tmp_path, capsys,
                                                             content):
    """Refused exactly when the rule evaluator (or reading the file) would fail."""
    vp = tmp_path / "validation_protocol.yaml"
    if isinstance(content, bytes):
        vp.write_bytes(content)
    elif content is not None:
        vp.write_text(content, encoding="utf-8")
    _assert_refused_before_any_backtest(monkeypatch, tmp_path, capsys, vp)


def test_real_run_003_shape_refused_before_any_backtest(monkeypatch, tmp_path, capsys):
    """run_003: `decision_rules: {approve: [...], reject: [...]}` -- the evaluator
    raises on a list where it splits a string; master spent every window first."""
    vp = _real_protocol_copy("run_003", tmp_path)
    assert isinstance(yaml.safe_load(vp.read_text(encoding="utf-8"))["decision_rules"]
                      ["approve"], list)
    _assert_refused_before_any_backtest(monkeypatch, tmp_path, capsys, vp)


def test_real_run_018_shape_proceeds_exactly_as_master(monkeypatch, tmp_path):
    """run_018: rules nested under `variants`, none at the top -- the evaluator
    returns (zero rules), so the run proceeds and hypothesis_verdict is exactly
    the evaluator's on that document, as on master."""
    vp = _real_protocol_copy("run_018", tmp_path)
    doc = yaml.safe_load(vp.read_text(encoding="utf-8"))
    assert "decision_rules" not in doc and doc.get("variants")
    summary, stub = _main(monkeypatch, tmp_path, "--validation-protocol", str(vp))
    assert stub.calls == 2
    expected = rp.evaluate_against_decision_rules(
        summary["per_symbol_summary"], summary["results"], doc,
        summary["trade_diagnostics_summary"] or None,
        runs_root=str((tmp_path / "out" / "results").resolve()), timeframe="1h")
    assert json.loads(json.dumps(expected, default=str)) == summary["hypothesis_verdict"]
    assert summary["hypothesis_verdict"]["criteria_results"] == []


@pytest.mark.parametrize("content", [
    "required_evidence: []\n",                         # no decision_rules: zero rules
    "decision_rules: []\nrequired_evidence: 'x'\n",    # a string of evidence: iterated
], ids=["no_rules", "evidence_str"])
def test_shapes_master_ran_still_run(monkeypatch, tmp_path, content):
    """Only an evaluator crash refuses; shapes master evaluated still run."""
    vp = tmp_path / "validation_protocol.yaml"
    vp.write_text(content, encoding="utf-8")
    summary, stub = _main(monkeypatch, tmp_path, "--validation-protocol", str(vp))
    assert stub.calls == 2 and summary["hypothesis_verdict"] is not None


def test_diagnostics_only_and_validation_protocol_are_exclusive(monkeypatch, tmp_path):
    vp = tmp_path / "validation_protocol.yaml"
    vp.write_text("decision_rules: []\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        _main(monkeypatch, tmp_path, "--diagnostics-only", "--validation-protocol", str(vp))
    assert exc.value.code == rp.EXIT_NO_DATA_TOUCHED
    assert rp.run_backtest.calls == 0
