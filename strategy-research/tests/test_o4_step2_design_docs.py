"""
O-4 (D-053): Step 2 (innovation_expansion) receives the strategy design guide and the
component catalogue, under orchestrator.config_direct_authoring only.

Why: Step 2 writes patches against the base config and its SKILL.md points at both documents.
Before this change it received neither, so it had no list of components or parameters.

Pinned here:
  1. Flag ON: STRATEGY_DESIGN_GUIDE.md and COMPONENT_CATALOG.md are REQUIRED inputs of
     innovation_expansion's handoff, both resolve to real files, both reach the assembled
     prompt, and adding them twice adds them once.
  2. Flag OFF (or key absent): the handoff is untouched (no mutation at all) and the assembled
     prompt carries neither document -- the flags-off prompt is unchanged by this wiring.
  3. The docs are NOT in _CLOSED_BOOK_STAGE_INPUTS (that table runs with no flag) and NOT in any
     handoff template for innovation_expansion (the 1b block-manifest test keeps the guide out
     of every template except 1b's own).
  4. Only innovation_expansion is affected: the other stages the function knows are unchanged.
"""
import copy
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402

GUIDE = "../../docs/STRATEGY_DESIGN_GUIDE.md"
CATALOG = "../../docs/COMPONENT_CATALOG.md"
_DOCS = {GUIDE: SR_ROOT / "docs" / "STRATEGY_DESIGN_GUIDE.md",
         CATALOG: SR_ROOT / "docs" / "COMPONENT_CATALOG.md"}
_TEMPLATES = SR_ROOT / "workflow_artifacts" / "templates" / "handoffs"


def _set_flag(root: Path, enabled) -> None:
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    if enabled is None:  # section present, key absent
        (config_dir / "campaign_config.yaml").write_text("orchestrator: {}\n", encoding="utf-8")
        return
    (config_dir / "campaign_config.yaml").write_text(
        yaml.safe_dump({"orchestrator": {"config_direct_authoring": {"enabled": bool(enabled)}}}),
        encoding="utf-8")


def _sandbox(tmp_path: Path, monkeypatch, enabled, run_id: str = "run_o4") -> Path:
    """A root whose docs/ holds copies of the real guide and catalogue, the run dir under it,
    and the artifacts the stage's real template reads (empty placeholders)."""
    root = tmp_path / "root"
    for rel, src in _DOCS.items():
        dst = root / rel.replace("../../", "")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    monkeypatch.setattr(rpr, "ROOT", root)
    _set_flag(root, enabled)
    run_dir = root / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    return run_dir


def _real_step2_handoff(run_dir: Path) -> dict:
    """The real template's handoff, with every path it names created as an empty file so the
    prompt can be assembled without a pipeline run."""
    template = yaml.safe_load(
        (_TEMPLATES / "hypothesis_to_innovation_expansion.yaml").read_text(encoding="utf-8"))
    for key in ("required_inputs", "optional_inputs"):
        for req in template.get(key) or []:
            target = (run_dir / req["path"]).resolve()
            if not target.exists() and req["path"].startswith("artifacts/"):
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("{}\n", encoding="utf-8")
    return template


def _paths(handoff: dict) -> list[str]:
    return [r["path"] for r in handoff.get("required_inputs", [])]


def _prompt(handoff: dict, run_dir: Path, monkeypatch) -> str:
    monkeypatch.chdir(SR_ROOT)  # _build_stage_prompt reads the SKILL.md relative to the CWD
    # config/ and artifacts/ inputs the handoff names (the real template's, plus backtest_spec.yaml
    # under the flag) resolve against the sandbox: provide them as empty files
    for req in handoff.get("required_inputs", []) + handoff.get("optional_inputs", []):
        target = (run_dir / req["path"]).resolve()
        if not target.exists() and req["path"].startswith(("../../config/", "artifacts/")):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("{}\n", encoding="utf-8")
    return rpr._build_stage_prompt("innovation_expansion", handoff, run_dir)


# --- 1. flag on --------------------------------------------------------------

def test_flag_on_both_docs_are_required_inputs_of_innovation_expansion(tmp_path, monkeypatch):
    run_dir = _sandbox(tmp_path, monkeypatch, True)
    handoff = _real_step2_handoff(run_dir)
    before = _paths(handoff)
    rpr._apply_config_direct_authoring_context("innovation_expansion", handoff, run_dir)
    paths = _paths(handoff)
    assert GUIDE in paths and CATALOG in paths
    assert paths[:len(before)] == before, "existing inputs keep their order; the docs are appended"
    # required, not optional
    assert GUIDE not in [r["path"] for r in handoff.get("optional_inputs", [])]
    assert CATALOG not in [r["path"] for r in handoff.get("optional_inputs", [])]
    for p in (GUIDE, CATALOG):
        entry = next(r for r in handoff["required_inputs"] if r["path"] == p)
        assert entry["reason"].strip()
        assert (run_dir / p).resolve().is_file()


def test_flag_on_adding_twice_adds_once(tmp_path, monkeypatch):
    run_dir = _sandbox(tmp_path, monkeypatch, True)
    handoff = {"required_inputs": []}
    rpr._apply_config_direct_authoring_context("innovation_expansion", handoff, run_dir)
    rpr._apply_config_direct_authoring_context("innovation_expansion", handoff, run_dir)
    assert _paths(handoff).count(GUIDE) == 1
    assert _paths(handoff).count(CATALOG) == 1


def test_flag_on_both_documents_reach_the_assembled_prompt(tmp_path, monkeypatch):
    run_dir = _sandbox(tmp_path, monkeypatch, True)
    handoff = _real_step2_handoff(run_dir)
    rpr._apply_config_direct_authoring_context("innovation_expansion", handoff, run_dir)
    prompt = _prompt(handoff, run_dir, monkeypatch)
    for p, src in _DOCS.items():
        assert f"--- CONTENT OF {p} ---" in prompt
        assert src.read_text(encoding="utf-8") in prompt


def test_flag_on_a_missing_doc_fails_loud(tmp_path, monkeypatch):
    """Required means required: a checkout without the catalogue must stop the stage, not run it
    blind (the same rule _build_stage_prompt applies to every required input)."""
    run_dir = _sandbox(tmp_path, monkeypatch, True)
    (rpr.ROOT / "docs" / "COMPONENT_CATALOG.md").unlink()
    handoff = _real_step2_handoff(run_dir)
    rpr._apply_config_direct_authoring_context("innovation_expansion", handoff, run_dir)
    with pytest.raises(FileNotFoundError):
        _prompt(handoff, run_dir, monkeypatch)


# --- 2. flag off -------------------------------------------------------------

@pytest.mark.parametrize("enabled", [False, None])
def test_flag_off_handoff_and_prompt_are_unchanged(enabled, tmp_path, monkeypatch):
    run_dir = _sandbox(tmp_path, monkeypatch, enabled)
    handoff = _real_step2_handoff(run_dir)
    before = copy.deepcopy(handoff)
    rpr._apply_config_direct_authoring_context("innovation_expansion", handoff, run_dir)
    assert handoff == before, "flag off must never mutate the handoff"
    assert GUIDE not in _paths(handoff) and CATALOG not in _paths(handoff)
    assert GUIDE not in [r["path"] for r in handoff.get("optional_inputs", [])]
    assert _prompt(handoff, run_dir, monkeypatch) == _prompt(before, run_dir, monkeypatch)
    prompt = _prompt(handoff, run_dir, monkeypatch)
    assert f"--- CONTENT OF {GUIDE} ---" not in prompt
    assert f"--- CONTENT OF {CATALOG} ---" not in prompt


# --- 3. where the docs must NOT be wired --------------------------------------

def test_docs_are_not_in_the_no_flag_closed_book_table():
    for stage, entries in rpr._CLOSED_BOOK_STAGE_INPUTS.items():
        for path, _kind, _reason in entries:
            if stage == "strategy_config_authoring":
                continue  # that stage has its own template entries; the table holds only QF
            assert "STRATEGY_DESIGN_GUIDE" not in path, (stage, path)
            assert "COMPONENT_CATALOG" not in path, (stage, path)


@pytest.mark.parametrize("name", ["hypothesis_to_innovation_expansion.yaml",
                                  "innovation_expansion_to_validation.yaml"])
def test_docs_are_not_in_the_innovation_expansion_templates(name):
    text = (_TEMPLATES / name).read_text(encoding="utf-8")
    assert "STRATEGY_DESIGN_GUIDE" not in text
    assert "COMPONENT_CATALOG" not in text


def test_closed_book_inputs_do_not_add_the_docs_to_innovation_expansion(tmp_path, monkeypatch):
    run_dir = _sandbox(tmp_path, monkeypatch, True)
    coin = rpr.ROOT / "config" / "coin_universe.yaml"
    coin.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SR_ROOT / "config" / "coin_universe.yaml", coin)
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs("innovation_expansion", handoff, run_dir)
    assert GUIDE not in _paths(handoff) and CATALOG not in _paths(handoff)


# --- 4. other stages -----------------------------------------------------------

@pytest.mark.parametrize("stage", ["hypothesis_generation", "strategy_config_authoring",
                                   "validation", "backtest_specification", "verdict_interpreter"])
def test_other_stages_do_not_get_the_docs_from_this_function(stage, tmp_path, monkeypatch):
    run_dir = _sandbox(tmp_path, monkeypatch, True)
    handoff = {"required_inputs": []}
    rpr._apply_config_direct_authoring_context(stage, handoff, run_dir)
    assert GUIDE not in _paths(handoff) and CATALOG not in _paths(handoff)
