"""
D-189 (operator direction 2026-10-24, PR-6) -- per-stage model mapping.

`orchestrator.stage_models` in config/campaign_config.yaml maps a stage name to a
model id; run_phase1_research._stage_model(stage_name) returns it, else
_CLAUDE_WORKER_MODEL. run_claude_worker uses that one value for the CLI/SDK model,
the provenance `requested` and the drift check (`mismatch`). Steps 1a
(hypothesis_generation) and 1b (strategy_config_authoring) are Sonnet 5.5; every
other stage, the readers and the analyst are unchanged. Not a flag: no `enabled`.

Proven with stubs only (no paid call, no CLI, no backtest, no trial row, nothing
under the real runs/ or campaign_record/): tests/conftest.py's autouse sandbox
redirects rpr.ROOT, and the real config file is read directly by path.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock  # noqa: E402

from _reader_test_helpers import ALL_ON, _set_orchestrator  # noqa: E402

SONNET = "claude-sonnet-5-5"
DEFAULT = rpr._CLAUDE_WORKER_MODEL
REAL_CONFIG = SR_ROOT / "config" / "campaign_config.yaml"
ON = {**ALL_ON, "score_provenance": {"enabled": True}}


def _real_cfg() -> dict:
    return yaml.safe_load(REAL_CONFIG.read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# 1. the reader
# ---------------------------------------------------------------------------

def test_the_default_is_the_haiku_constant():
    assert DEFAULT == "claude-haiku-5-5"


def test_a_listed_stage_gets_its_mapped_model():
    cfg = {"orchestrator": {"stage_models": {"hypothesis_generation": "m-a",
                                             "strategy_config_authoring": "m-b"}}}
    assert rpr._stage_model("hypothesis_generation", cfg) == "m-a"
    assert rpr._stage_model("strategy_config_authoring", cfg) == "m-b"


def test_an_unlisted_stage_gets_the_default():
    cfg = {"orchestrator": {"stage_models": {"hypothesis_generation": "m-a"}}}
    for stage in ("innovation_expansion", "validation", "verdict_interpreter", "no_such_stage"):
        assert rpr._stage_model(stage, cfg) == DEFAULT


@pytest.mark.parametrize("cfg", [
    {}, {"orchestrator": {}}, {"orchestrator": None},
    {"orchestrator": {"stage_models": None}}, {"orchestrator": {"stage_models": {}}},
])
def test_an_absent_mapping_falls_back_to_the_default(cfg):
    assert rpr._stage_model("hypothesis_generation", cfg) == DEFAULT


def test_the_value_is_stripped():
    cfg = {"orchestrator": {"stage_models": {"validation": f"  {SONNET}  "}}}
    assert rpr._stage_model("validation", cfg) == SONNET


@pytest.mark.parametrize("bad", ["", "   ", None, 5, 1.5, True, ["claude-sonnet-5-5"], {"model": "x"}])
def test_a_malformed_value_raises_not_falls_back(bad):
    cfg = {"orchestrator": {"stage_models": {"hypothesis_generation": bad}}}
    with pytest.raises(ValueError, match=r"orchestrator\.stage_models\.hypothesis_generation"):
        rpr._stage_model("hypothesis_generation", cfg)


def test_a_bad_value_only_raises_for_its_own_stage():
    cfg = {"orchestrator": {"stage_models": {"hypothesis_generation": ""}}}
    assert rpr._stage_model("validation", cfg) == DEFAULT


@pytest.mark.parametrize("bad", [["hypothesis_generation"], "claude-sonnet-5-5", 7])
def test_a_mapping_that_is_not_a_mapping_raises(bad):
    cfg = {"orchestrator": {"stage_models": bad}}
    with pytest.raises(ValueError, match=r"orchestrator\.stage_models"):
        rpr._stage_model("hypothesis_generation", cfg)


def test_the_reader_reads_the_config_file_when_no_cfg_is_passed():
    _set_orchestrator(None)  # no config file in the sandbox
    assert rpr._stage_model("hypothesis_generation") == DEFAULT
    _set_orchestrator({"stage_models": {"hypothesis_generation": "m-file"}})
    assert rpr._stage_model("hypothesis_generation") == "m-file"
    assert rpr._stage_model("validation") == DEFAULT


# ---------------------------------------------------------------------------
# 2. the real config file
# ---------------------------------------------------------------------------

def test_the_real_config_maps_exactly_steps_1a_and_1b_to_sonnet():
    mapping = _real_cfg()["orchestrator"]["stage_models"]
    assert mapping == {"hypothesis_generation": SONNET, "strategy_config_authoring": SONNET}


def test_the_real_config_resolves_every_stage():
    cfg = _real_cfg()
    for stage in rpr.STAGE_CONFIGS:
        want = SONNET if stage in ("hypothesis_generation", "strategy_config_authoring") else DEFAULT
        assert rpr._stage_model(stage, cfg) == want, stage
    assert rpr._stage_model("innovation_expansion", cfg) == DEFAULT


def test_every_mapped_name_is_a_real_stage_spelled_as_in_stage_configs():
    for name in _real_cfg()["orchestrator"]["stage_models"]:
        assert name in rpr.STAGE_CONFIGS, name


def test_stage_models_is_not_a_flag():
    mapping = _real_cfg()["orchestrator"]["stage_models"]
    assert "enabled" not in mapping
    register = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml")
                              .read_text(encoding="utf-8"))
    text = yaml.safe_dump(register)
    assert "stage_models" not in text


def test_the_analyst_and_its_default_do_not_read_stage_models():
    cfg = {"orchestrator": {"stage_models": {"hypothesis_generation": "m-a"},
                            "analyst": {"enabled": True}}}
    assert rpr._analyst_caps(cfg)["model"] == DEFAULT
    cfg["orchestrator"]["analyst"]["model"] = "m-analyst"
    assert rpr._analyst_caps(cfg)["model"] == "m-analyst"


# ---------------------------------------------------------------------------
# 3. the options helper
# ---------------------------------------------------------------------------

def test_options_default_and_explicit_model():
    assert rpr._stage_agent_options().model == DEFAULT
    assert rpr._stage_agent_options(model=SONNET).model == SONNET


def test_options_default_is_read_at_call_time(monkeypatch):
    monkeypatch.setattr(rpr, "_CLAUDE_WORKER_MODEL", "sentinel-model")
    assert rpr._stage_agent_options().model == "sentinel-model"


def test_the_analyst_model_still_overrides_the_stage_model():
    spec = {"server": rpr.create_sdk_mcp_server("t", tools=[]), "hook": rpr._analyst_deny_hook([]),
            "model": "m-analyst", "max_turns": 3, "max_budget_usd": 1.0, "timeout_s": 5.0}
    assert rpr._stage_agent_options(analyst=spec, model=SONNET).model == "m-analyst"


# ---------------------------------------------------------------------------
# 4. the helpers' `requested`
# ---------------------------------------------------------------------------

def test_provenance_helpers_use_the_given_requested_model():
    assert rpr._base_provenance([SONNET], None, SONNET)["requested"] == SONNET
    assert rpr._base_provenance([SONNET], None)["requested"] == DEFAULT
    assert rpr._observed_model_facts([SONNET], SONNET) == (SONNET, False)
    assert rpr._observed_model_facts([f"{SONNET}-20260101"], SONNET) == (f"{SONNET}-20260101", False)
    assert rpr._observed_model_facts([DEFAULT], SONNET) == (DEFAULT, True)
    assert rpr._observed_model_facts([SONNET], DEFAULT) == (SONNET, True)
    assert rpr._observed_model_facts([SONNET]) == (SONNET, True)  # no requested: the default
    assert rpr._provenance_record(SONNET, False, {}, True, requested=SONNET)["requested"] == SONNET
    assert rpr._provenance_record(SONNET, True, {}, True)["requested"] == DEFAULT


# ---------------------------------------------------------------------------
# 5. run_claude_worker (stubbed query: no paid call)
# ---------------------------------------------------------------------------

def _card_scores():
    def item(card):
        return {"card": card, "model_id": "self-reported-model", "rubric_version": "brief-card-v1",
                "scores": {"confidence_real": 2, "distance_to_profitable": 1,
                           "mechanism_plausibility": 3}}
    return {"cards": [item("hypothesis_card_2.yaml")]}


def _stage_text() -> str:
    return ("Done.\n```yaml\n# hypothesis_card.yaml\nhypothesis_id: H-1\n```\n"
            f"```yaml\n# extra_card_scores.yaml\n{yaml.safe_dump(_card_scores())}```\n")


def _run_stage(monkeypatch, tmp_path, stage, stage_models, answered_by, orchestrator=ON):
    """Run run_claude_worker for `stage` on a stub stream answered by `answered_by`;
    returns (options the stub saw, the stage's audit entry, run_dir)."""
    _set_orchestrator({**orchestrator, **({"stage_models": stage_models} if stage_models is not None else {})})
    monkeypatch.chdir(SR_ROOT)  # _build_stage_prompt opens the skill relative to cwd
    run_dir = tmp_path / "runs" / "run_d189"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"status": "active", "audit_log": {}}), encoding="utf-8")
    seen = []

    async def _query(*, prompt, options=None):
        seen.append(options)
        yield AssistantMessage(content=[TextBlock(text=_stage_text())], model=answered_by)
        yield ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1, is_error=False,
                            num_turns=1, session_id="s", total_cost_usd=0.0,
                            usage={"input_tokens": 1, "output_tokens": 1},
                            model_usage={answered_by: {}})
    monkeypatch.setattr(rpr, "query", _query)
    handoff = {"required_inputs": [], "optional_inputs": [], "injected_context": {"stage_attempt": "0"}}
    asyncio.run(rpr.run_claude_worker(stage, handoff, run_dir))
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    assert len(seen) == 1
    return seen[0], audit[f"{stage}_attempt_0"], run_dir


MAPPING = {"hypothesis_generation": SONNET, "strategy_config_authoring": SONNET}


@pytest.mark.parametrize("stage", ["hypothesis_generation", "strategy_config_authoring"])
def test_a_mapped_stage_sends_sonnet_and_records_it_as_requested(monkeypatch, tmp_path, stage):
    opts, entry, _ = _run_stage(monkeypatch, tmp_path, stage, MAPPING, SONNET)
    assert opts.model == SONNET
    prov = entry["provenance"]
    assert prov["requested"] == SONNET and prov["observed_models"] == [SONNET]
    assert prov["cards"]["requested"] == SONNET
    assert prov["cards"]["mismatch"] is False


def test_an_unmapped_stage_sends_the_default_and_records_it(monkeypatch, tmp_path):
    opts, entry, _ = _run_stage(monkeypatch, tmp_path, "validation", MAPPING, DEFAULT)
    assert opts.model == DEFAULT
    assert entry["provenance"]["requested"] == DEFAULT
    assert entry["provenance"]["cards"]["mismatch"] is False


def test_innovation_expansion_stays_on_the_default(monkeypatch, tmp_path):
    opts, entry, _ = _run_stage(monkeypatch, tmp_path, "innovation_expansion", MAPPING, DEFAULT)
    assert opts.model == DEFAULT and entry["provenance"]["requested"] == DEFAULT


def test_no_mapping_in_the_config_is_the_old_behaviour(monkeypatch, tmp_path):
    opts, entry, _ = _run_stage(monkeypatch, tmp_path, "hypothesis_generation", None, DEFAULT)
    assert opts.model == DEFAULT and entry["provenance"]["requested"] == DEFAULT
    assert entry["provenance"]["cards"]["mismatch"] is False


def test_the_drift_check_compares_against_the_stage_model(monkeypatch, tmp_path):
    # a mapped Sonnet stage answered by Haiku IS a mismatch (it would not be against the default)
    _, entry, run_dir = _run_stage(monkeypatch, tmp_path, "hypothesis_generation", MAPPING, DEFAULT)
    cards = entry["provenance"]["cards"]
    assert cards["requested"] == SONNET and cards["observed"] == DEFAULT
    assert cards["mismatch"] is True
    # recorded, not stopped: the deliverables are still written
    assert (run_dir / "artifacts" / "extra_card_scores.yaml").exists()


def test_a_dated_snapshot_of_the_stage_model_is_not_a_mismatch(monkeypatch, tmp_path):
    _, entry, _ = _run_stage(monkeypatch, tmp_path, "hypothesis_generation", MAPPING,
                             f"{SONNET}-20260101")
    assert entry["provenance"]["cards"]["mismatch"] is False


def test_the_stage_models_reach_the_flag_off_options_too(monkeypatch, tmp_path):
    # score_provenance off: no provenance block, but the model is still the stage's
    opts, entry, _ = _run_stage(monkeypatch, tmp_path, "hypothesis_generation", MAPPING, SONNET,
                                orchestrator=ALL_ON)
    assert opts.model == SONNET and "provenance" not in entry


def test_a_malformed_mapping_raises_before_any_call(monkeypatch, tmp_path):
    _set_orchestrator({**ON, "stage_models": {"hypothesis_generation": ""}})
    monkeypatch.chdir(SR_ROOT)
    run_dir = tmp_path / "runs" / "run_d189"
    (run_dir / "artifacts").mkdir(parents=True)
    called = []

    async def _query(*, prompt, options=None):
        called.append(1)
        yield  # pragma: no cover
    monkeypatch.setattr(rpr, "query", _query)
    handoff = {"required_inputs": [], "optional_inputs": [], "injected_context": {"stage_attempt": "0"}}
    with pytest.raises(ValueError, match=r"orchestrator\.stage_models\.hypothesis_generation"):
        asyncio.run(rpr.run_claude_worker("hypothesis_generation", handoff, run_dir))
    assert called == []
