"""
D-112: orchestrator.exact_config_1b also covers step 2 (innovation_expansion).

With the flag on, an exact-config brief and the variant loop off, step 2 is
written by code: variant_patches.yaml holds exactly one variant, `base`, with an
empty patch and no `kind` / `symbol` key, and no model call is made. With the
loop on, or without an exact config, or with the flag off, step 2 is the model
call as before.
"""
import shutil
import sys
from pathlib import Path

import pytest

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import variant_coin as vc  # noqa: E402

from _reader_test_helpers import _set_orchestrator  # noqa: E402
from test_exact_config_1b import CDA, ON, _arts, _run  # noqa: E402

LOOP_ON = {**ON, "variant_loop": {"enabled": True}}
STEP2_HANDOFF = SR_ROOT / "workflow_artifacts" / "templates" / "handoffs" / \
    "hypothesis_to_innovation_expansion.yaml"


def _base_only(run_dir):
    doc = rpr.load_yaml(_arts(run_dir) / "variant_patches.yaml")
    return doc, doc["variants"]


# --- the mode ------------------------------------------------------------------

def test_mode_needs_flag_exact_config_and_loop_off(monkeypatch):
    run_dir = _run("run_950")
    _set_orchestrator(CDA)
    assert rpr._exact_config_step2_mode(run_dir) is False          # flag off
    _set_orchestrator(ON)
    assert rpr._exact_config_step2_mode(run_dir) is True           # flag on, loop off
    _set_orchestrator(LOOP_ON)
    assert rpr._exact_config_step2_mode(run_dir) is False          # loop on
    _set_orchestrator(ON)
    assert rpr._exact_config_step2_mode(_run("run_951", config=None, manifest=None)) is False


def test_flag_off_reads_nothing_but_the_flag(monkeypatch):
    _set_orchestrator(CDA)
    run_dir = _run("run_952")
    monkeypatch.setattr(rpr, "_brief_exact_config", lambda p: pytest.fail("flag off must read nothing"))
    monkeypatch.setattr(rpr, "_variant_loop_enabled", lambda *a, **k: pytest.fail("flag off: no loop read"))
    assert rpr._exact_config_step2_mode(run_dir) is False


# --- the code-written file -------------------------------------------------------

def test_writes_base_only_with_empty_patch_and_no_symbol():
    _set_orchestrator(ON)
    run_dir = _run("run_953")
    rpr._exact_config_variant_patches(run_dir, "run_953")
    doc, variants = _base_only(run_dir)
    assert len(variants) == 1
    base = variants[0]
    assert base["variant_id"] == "base" and base["patch"] == []
    assert "symbol" not in base and "kind" not in base
    assert doc["base_config_ref"] == "artifacts/backtest_spec.yaml"
    assert doc["hypothesis_id"] == "H-1"
    # step 5a reads it as a legacy (not per-coin) file: base on every coin of the protocol
    assert vc.per_coin_mode(variants) is False


# --- through run_loop -------------------------------------------------------------

def _loop_from_step2(monkeypatch, run_dir):
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["pending_stage"] = "innovation_expansion"
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    (run_dir / "handoffs").mkdir(exist_ok=True)
    for tpl in STEP2_HANDOFF.parent.glob("*.yaml"):  # every stage's handoff, as setup_run copies
        shutil.copy(tpl, run_dir / "handoffs" / tpl.name)
    if rpr._brief_exact_config(run_dir) is not None:  # 1b's output exists before step 2
        rpr._exact_config_1b(run_dir, run_dir.name)
    for name in ("available_feeds.yaml", "indicator_library.yaml"):  # step 2's required inputs
        stub = rpr.ROOT / "config" / name
        stub.parent.mkdir(parents=True, exist_ok=True)
        if not stub.exists():
            stub.write_text("{}\n", encoding="utf-8")
    seen = []

    async def _fake_invoke(stage_name, run_id, retry_context=None):
        seen.append(stage_name)
        if stage_name == "innovation_expansion":  # a model step 2 writes its file
            rpr.save_yaml(run_dir / "artifacts" / "variant_patches.yaml",
                          {"variants": [{"variant_id": "V1_model", "patch": []}]})
        raise RuntimeError("stop the loop here")  # end after the first call

    monkeypatch.setattr(rpr, "async_invoke_agent", _fake_invoke)
    rpr.run_loop(run_dir.name)
    return seen


def test_run_loop_flag_on_exact_loop_off_makes_no_step2_call(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _run("run_954")
    seen = _loop_from_step2(monkeypatch, run_dir)
    assert "innovation_expansion" not in seen
    assert seen == ["backtest_specification"]  # the route moved on to step 5a
    _, variants = _base_only(run_dir)
    assert [v["variant_id"] for v in variants] == ["base"]


def test_run_loop_flag_on_loop_on_calls_the_model(monkeypatch):
    _set_orchestrator(LOOP_ON)
    seen = _loop_from_step2(monkeypatch, _run("run_955"))
    assert seen == ["innovation_expansion"]


def test_run_loop_flag_on_without_exact_config_calls_the_model(monkeypatch):
    _set_orchestrator(ON)
    seen = _loop_from_step2(monkeypatch, _run("run_956", config=None, manifest=None))
    assert seen == ["innovation_expansion"]


def test_run_loop_flag_off_calls_the_model(monkeypatch):
    _set_orchestrator(CDA)
    seen = _loop_from_step2(monkeypatch, _run("run_957"))
    assert seen == ["innovation_expansion"]


def test_step_5a_accepts_the_code_written_files(monkeypatch):
    """The next stage's requirement (lesson 2026-10-12): the real backtest_specification
    tool stage builds and validates `base` from the code-written 1b and step 2."""
    import asyncio
    from test_d051_d053_forecast_rules import _ok_subprocess
    from test_exact_config_1b import LANE1_MANIFEST, _lane1
    _set_orchestrator(ON)
    run_dir = _run("run_958", config=_lane1(200), manifest=LANE1_MANIFEST)
    rpr._exact_config_1b(run_dir, "run_958")
    rpr._exact_config_variant_patches(run_dir, "run_958")
    monkeypatch.setattr(rpr.subprocess, "run", _ok_subprocess)
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))
    asyncio.run(rpr.run_tool_worker("backtest_specification", "run_958"))
    index = rpr.load_yaml(_arts(run_dir) / "variants" / "index.yaml")["variants"]
    assert list(index) == ["base"] and index["base"]["status"] == "validated"
    assert rpr.load_yaml(_arts(run_dir) / "candidate_strategy_config.json") == _lane1(200)


def test_config_direct_off_keeps_the_model_step2(monkeypatch):
    """Review of PR #400: without config-direct authoring, step 2 routes to stages that
    read the expanded card, so step 2 stays the model."""
    _set_orchestrator({"exact_config_1b": {"enabled": True}})
    run_dir = _run("run_959")
    assert rpr._exact_config_step2_mode(run_dir) is False
