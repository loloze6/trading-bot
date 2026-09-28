"""
E-061 C1.2 + C1.3 (delivery_plan_v26_continuation.md C1; review findings A1, A2;
C2_S1_FINDINGS.md G14) -- targeted unit tests. The joined-up proof is
tests/test_e061_end_to_end_wiring.py (A1, A2, A5 and the two joined-up tests).

C1.2 -- the handoff contract under config-direct authoring:
  * 5a / data gate / protocol_execution load their own code-written handoff,
    whose required inputs never name validation_protocol.yaml and whose checked
    deliverables are files the config-direct tool branches always write;
  * step 2 (innovation_expansion) gets variant_patches.yaml as a checked
    deliverable;
  * hypothesis_to_innovation_expansion.yaml has one required_inputs key.
C1.3 -- the validation protocol is optional under config-direct:
  * run_tool_worker passes --validation-protocol only when the file exists;
  * run_protocol.py opens a passed file before any backtest, and without one
    writes the diagnostics block with an empty rule set and no verdict.
Flag off: the legacy handoffs are loaded, nothing new is written, the argv
still carries --validation-protocol, and run_protocol.py's output with a
validation protocol is what the rule evaluator returns for that file.

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
@pytest.mark.parametrize("stage", _CD_STAGES)
def test_config_direct_handoff_never_requires_validation_protocol(stage, variant_loop):
    doc = rpr._config_direct_handoff_doc(stage, "run_001", variant_loop)
    paths = [x["path"] for x in doc["required_inputs"]]
    assert "artifacts/validation_protocol.yaml" not in paths
    assert doc["to_stage"] == stage and doc["assigned_engine"] == "tool"
    assert doc["run_id"] == "run_001" and doc["config_direct_authoring"] is True


@pytest.mark.parametrize("variant_loop,inputs,deliverables", [
    (True, ["artifacts/variants/index.yaml"], ["variants/index.yaml"]),
    (False, ["artifacts/candidate_strategy_config.json"], ["data_availability_gate.yaml"]),
])
def test_config_direct_gate_handoff_matches_what_the_gate_writes(variant_loop, inputs,
                                                                 deliverables):
    """The variant loop writes per-variant gate files and rewrites the index -- never
    artifacts/data_availability_gate.yaml (the singular file the legacy handoff lists)."""
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


def test_ensure_config_direct_handoff_writes_once():
    _set_flags(**_CD_VL)
    run_dir = _minimal_run(rpr.ROOT, "run_001")
    (run_dir / "handoffs").mkdir()
    path = rpr._ensure_config_direct_handoff("protocol_execution", "run_001", run_dir)
    assert path == run_dir / "handoffs" / "config_direct_protocol_execution.yaml"
    assert rpr.load_yaml(path) == rpr._config_direct_handoff_doc("protocol_execution",
                                                                  "run_001", True)
    rpr.save_yaml(path, {"edited": True})  # an existing handoff is never overwritten
    rpr._ensure_config_direct_handoff("protocol_execution", "run_001", run_dir)
    assert rpr.load_yaml(path) == {"edited": True}


def test_apply_config_direct_deliverables():
    handoff = {"deliverables": ["expanded_hypothesis_card.yaml", "innovation_notes.yaml"]}
    rpr._apply_config_direct_deliverables("innovation_expansion", handoff)  # flag off
    assert handoff == {"deliverables": ["expanded_hypothesis_card.yaml",
                                        "innovation_notes.yaml"]}
    _set_flags(config_direct_authoring=True)
    rpr._apply_config_direct_deliverables("validation", handoff)  # another stage
    assert "variant_patches.yaml" not in handoff["deliverables"]
    rpr._apply_config_direct_deliverables("innovation_expansion", handoff)
    rpr._apply_config_direct_deliverables("innovation_expansion", handoff)  # idempotent
    assert handoff["deliverables"] == ["expanded_hypothesis_card.yaml", "innovation_notes.yaml",
                                       "variant_patches.yaml"]


# ---- run_loop: which handoff each stage loads ------------------------------

class _Stop(RuntimeError):
    pass


def _run_at(run_id: str, pending_stage: str) -> Path:
    sr.setup_run(run_id)
    run_dir = rpr.ROOT / "runs" / run_id
    rpr.update_state(path=run_dir, pending_stage=pending_stage, status="active")
    return run_dir


def _drive_one_stage(monkeypatch, run_id: str) -> list:
    """run_loop for one stage: the stage body is stubbed to stop the run, so only
    the handoff it loaded (recorded) and the input check are exercised."""
    loaded = []
    real_load = rpr.load_yaml

    def _spy(path):
        if Path(path).parent.name == "handoffs":
            loaded.append(Path(path).name)
        return real_load(path)

    async def _stop(stage_name, rid, retry_context=None):
        raise _Stop(f"stopped at {stage_name}")

    monkeypatch.setattr(rpr, "load_yaml", _spy)
    monkeypatch.setattr(rpr, "async_invoke_agent", _stop)
    rpr.run_loop(run_id)
    return loaded


_LEGACY = {"backtest_specification": "validation_to_backtest_specification.yaml",
           "data_availability_gate": "backtest_spec_to_data_availability_gate.yaml",
           "protocol_execution": "backtest_spec_to_protocol_execution.yaml"}


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
    loaded = _drive_one_stage(monkeypatch, "run_001")
    assert loaded[0] == _LEGACY[stage]
    assert f"stopped at {stage}" in rpr.load_yaml(run_dir / "pipeline_state.yaml")["last_error"]
    assert sorted(p.name for p in (run_dir / "handoffs").iterdir()) == before
    assert not list((run_dir / "handoffs").glob("config_direct_*"))


@pytest.mark.parametrize("stage", _CD_STAGES)
def test_run_loop_config_direct_loads_its_own_handoff(monkeypatch, stage):
    """Flag on: the config-direct handoff, its inputs present without any
    validation_protocol.yaml, and the stage body is reached."""
    _set_flags(**_CD_VL)
    run_dir = _run_at("run_001", stage)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "backtest_spec.yaml", {"status": "spec_ready", "config": {}})
    rpr.save_yaml(arts / "variant_patches.yaml", {"variants": []})
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {}})
    assert not (arts / "validation_protocol.yaml").exists()
    loaded = _drive_one_stage(monkeypatch, "run_001")
    assert loaded[0] == rpr._CONFIG_DIRECT_HANDOFFS[stage]
    assert f"stopped at {stage}" in rpr.load_yaml(run_dir / "pipeline_state.yaml")["last_error"]


def test_run_loop_innovation_expansion_checks_variant_patches(monkeypatch):
    """Under config-direct, a step 2 that writes no variant_patches.yaml fails the
    stage's deliverable check (not 5a later)."""
    _set_flags(config_direct_authoring=True)
    run_dir = _run_at("run_001", "innovation_expansion")
    arts = run_dir / "artifacts"
    for rel in ("research_brief.yaml", "hypothesis_card.yaml", "backtest_spec.yaml"):
        (arts / rel).write_text("{}\n", encoding="utf-8")
    for rel in ("available_feeds.yaml", "indicator_library.yaml"):
        (rpr.ROOT / "config" / rel).write_text("{}\n", encoding="utf-8")

    async def _writes_two_of_three(stage_name, rid, retry_context=None):
        for rel in ("expanded_hypothesis_card.yaml", "innovation_notes.yaml"):
            (arts / rel).write_text("{}\n", encoding="utf-8")

    monkeypatch.setattr(rpr, "async_invoke_agent", _writes_two_of_three)
    rpr.run_loop("run_001")
    st = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert st["status"] == "failed"
    assert "variant_patches.yaml" in st["last_error"]
    assert "variant_patches.yaml" in rpr.load_yaml(
        run_dir / "handoffs" / "hypothesis_to_innovation_expansion.yaml")["deliverables"]


# ---------------------------------------------------------------------------
# C1.3 -- run_tool_worker's argv
# ---------------------------------------------------------------------------

def test_validation_protocol_args(tmp_path):
    vp = tmp_path / "validation_protocol.yaml"
    assert rpr._validation_protocol_args(vp) == ["--validation-protocol", str(vp)]  # flag off
    _set_flags(config_direct_authoring=True)
    assert rpr._validation_protocol_args(vp) == []
    vp.write_text("{}", encoding="utf-8")
    assert rpr._validation_protocol_args(vp) == ["--validation-protocol", str(vp)]


def _fake_protocol_run(calls: list):
    def _run(cmd, *a, **k):
        calls.append([str(c) for c in cmd])
        out = Path(cmd[cmd.index("--out-dir") + 1])
        out.mkdir(parents=True, exist_ok=True)
        (out / "protocol_summary.json").write_text(json.dumps({
            "config_sha256": "x", "protocol_file": "p", "results": [],
            "per_symbol_summary": {"BTCUSDT": {"median_sharpe": 0.1}}, "verdict": "refine",
            "hypothesis_verdict": {"verdict": None, "diagnostics": {}}}), encoding="utf-8")

        class _Ok:
            returncode, stdout, stderr = 0, "", ""
        return _Ok()
    return _run


def _pinned_run(run_id: str) -> Path:
    _write_protocol(rpr.ROOT, "p.json")
    run_dir = _minimal_run(rpr.ROOT, run_id)
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": "protocols/p.json"})
    return run_dir


def test_flag_off_protocol_execution_argv_unchanged(monkeypatch):
    """Flag off: the argv is exactly the pre-C1.3 one -- --validation-protocol
    passed, in the same position -- even when the file is absent."""
    run_dir = _pinned_run("run_910")
    arts = run_dir / "artifacts"
    (arts / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    calls = []
    monkeypatch.setattr(rpr.subprocess, "run", _fake_protocol_run(calls))
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_910"))
    assert calls == [[
        "stub-python", str(rpr.ROOT / "tools" / "run_protocol.py"),
        str(arts / "candidate_strategy_config.json"), str(rpr._resolve_protocol_path(run_dir,
                                                                                     "run_910")),
        "--validation-protocol", str(arts / "validation_protocol.yaml"),
        "--out-dir", str(run_dir)]]


@pytest.mark.parametrize("with_file", [False, True])
def test_variant_loop_argv_passes_validation_protocol_only_when_it_exists(monkeypatch,
                                                                          with_file):
    _set_flags(**_CD_VL)
    run_dir = _pinned_run("run_911")
    arts = run_dir / "artifacts"
    (arts / "variants" / "base").mkdir(parents=True)
    (arts / "variants" / "base" / "strategy_config.json").write_text("{}", encoding="utf-8")
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {"base": {
        "status": "validated", "config_path": "artifacts/variants/base/strategy_config.json"}}})
    if with_file:
        (arts / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    calls = []
    monkeypatch.setattr(rpr.subprocess, "run", _fake_protocol_run(calls))
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_911"))
    (argv,) = calls
    vp_pair = ["--validation-protocol", str(arts / "validation_protocol.yaml")]
    expected = [
        "stub-python", str(rpr.ROOT / "tools" / "run_protocol.py"),
        str(arts / "variants" / "base" / "strategy_config.json"),
        str(rpr._resolve_protocol_path(run_dir, "run_911")),
        *(vp_pair if with_file else []),
        "--out-dir", str(run_dir / "variants" / "base")]
    assert argv == expected


def test_config_direct_without_variant_loop_argv(monkeypatch):
    """Config-direct without the variant loop runs the single-candidate branch:
    no validation_protocol.yaml -> no --validation-protocol either."""
    _set_flags(config_direct_authoring=True)
    run_dir = _pinned_run("run_912")
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    calls = []
    monkeypatch.setattr(rpr.subprocess, "run", _fake_protocol_run(calls))
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_912"))
    (argv,) = calls
    assert "--validation-protocol" not in argv


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


def test_run_protocol_without_validation_protocol_writes_diagnostics(monkeypatch, tmp_path):
    summary, _stub = _main(monkeypatch, tmp_path)
    hv = summary["hypothesis_verdict"]
    assert hv["verdict"] is None
    assert hv["verdict_reason"] == rp.DIAGNOSTICS_ONLY_VERDICT_REASON
    assert hv["criteria_results"] == []
    diag = hv["diagnostics"]
    assert diag["median_gross_pnl"] == 2.0
    assert diag["median_cost_drag_pct"] == 40.0
    assert diag["median_forecast_return_corr"] == 0.03
    assert diag["below_floor_pct"] == 0.0
    # The stub writes no trade files, so there is no trade-diagnostics summary to
    # enrich from (its enrichment is pinned in the unit test below).


def test_diagnostics_only_equals_the_rule_evaluator_with_an_empty_rule_set():
    results = [{"symbol": "BTCUSDT", "window": "w1", "run_id": "r1", "regime_validity": {},
                "core": {"trade_count": 3, "sharpe": None, "gross_pnl": -1.0,
                         "cost_drag_pct": 12.0, "forecast_return_corr": -0.01}}]
    per_symbol = {"BTCUSDT": {"median_sharpe": None, "max_abs_drawdown_pct": 1.0,
                              "min_trade_count": 3, "zero_trade_slot_pct": 0.0}}
    tds = {"per_trade_expectancy_bps": {"mean": -4.0, "se": 2.0, "t_stat": -2.0, "n": 3},
           "zero_trade_slot_pct": 0.0, "fee_reduction_metrics": None}
    full = rp.evaluate_against_decision_rules(per_symbol, results, {}, tds)
    only = rp.diagnostics_only_hypothesis_verdict(per_symbol, results, tds)
    assert only["diagnostics"] == full["diagnostics"]
    assert only["diagnostics"]["below_floor_pct"] == 100.0  # 3 < the sparse floor
    assert only["diagnostics"]["per_trade_expectancy_bps"]["mean"] == -4.0
    assert full["verdict"] == "refine" and only["verdict"] is None


def test_run_protocol_with_validation_protocol_is_the_rule_evaluator(monkeypatch, tmp_path):
    """Flag-off output: with a validation protocol, hypothesis_verdict is exactly
    evaluate_against_decision_rules on the parsed file (a real verdict label, the
    file's criteria), not the diagnostics-only block."""
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


def test_run_protocol_missing_validation_protocol_fails_before_any_backtest(monkeypatch,
                                                                          tmp_path):
    with pytest.raises(SystemExit) as exc:
        _main(monkeypatch, tmp_path, "--validation-protocol", str(tmp_path / "absent.yaml"))
    assert exc.value.code == 1
    assert rp.run_backtest.calls == 0
    assert not (tmp_path / "out" / "protocol_summary.json").exists()


def test_run_protocol_unparseable_validation_protocol_fails_before_any_backtest(monkeypatch,
                                                                              tmp_path):
    bad = tmp_path / "validation_protocol.yaml"
    bad.write_text("decision_rules: [unclosed\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        _main(monkeypatch, tmp_path, "--validation-protocol", str(bad))
    assert exc.value.code == 1
    assert rp.run_backtest.calls == 0
