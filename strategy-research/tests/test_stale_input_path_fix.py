"""
E-032 S2b -- off-by-default proof for the stale optional_input path fix.

hypothesis_generation's own handoff template
(workflow_artifacts/templates/handoffs/research_brief_to_hypothesis.yaml)
declares two optional_inputs whose paths have never resolved:
"../../campaign_knowledge_base.yaml" and "../../feed_wishlist.yaml" -- both
predate the E-002 restructure (8f162fa6, 2026-08-06) that moved the real
files under campaign_record/. Because both are optional, a missing one has
always been silent (no error, no log) -- see EPIC.md's S2a review entry and
this story's Log entry.

Sandboxing: relies on tests/conftest.py's autouse _sandbox_by_default fixture
for rpr.ROOT, same precedent as test_exclusion_digest_input.py.

Acceptance bar (same as test_exclusion_digest_input.py, not merely "the code
path is skipped"): flag-off must produce a BYTE-IDENTICAL fully-assembled
prompt to a baseline that never calls _apply_stale_input_path_fix at all.
"""

import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402


def _minimal_run(root: Path, run_id: str) -> Path:
    run_dir = root / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (run_dir / "artifacts" / "research_brief.yaml").write_text(
        "asset: BTCUSDT\n", encoding="utf-8"
    )
    return run_dir


def _base_handoff() -> dict:
    return {
        "required_inputs": [
            {"path": "artifacts/research_brief.yaml", "reason": "base"}
        ],
        "optional_inputs": [
            {
                "path": "../../campaign_knowledge_base.yaml",
                "reason": "A5.1: coverage_matrix + exhausted_mechanisms.",
            },
            {
                "path": "../../feed_wishlist.yaml",
                "reason": "A1.2: append new feed requests here if needed.",
            },
        ],
    }


def _set_flag(root: Path, enabled) -> None:
    """enabled: True, False, or None (key/section absent entirely)."""
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    if enabled is None:
        (config_dir / "campaign_config.yaml").write_text(
            "orchestrator: {}\n", encoding="utf-8"
        )
        return
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(
            {"orchestrator": {"stale_input_path_fix": {"enabled": bool(enabled)}}}, f
        )


def _write_real_kb_and_wishlist(root: Path) -> None:
    record_dir = root / "campaign_record"
    record_dir.mkdir(parents=True, exist_ok=True)
    (record_dir / "campaign_knowledge_base.yaml").write_text(
        "exhausted_mechanisms: []\ncoverage_matrix: {}\n", encoding="utf-8"
    )
    (record_dir / "feed_wishlist.yaml").write_text(
        "- liquidation_data\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# _stale_input_path_fix_enabled
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "enabled,expected", [(True, True), (False, False), (None, False)]
)
def test_stale_input_path_fix_enabled_reads_flag(enabled, expected):
    root = rpr.ROOT
    _set_flag(root, enabled)
    assert rpr._stale_input_path_fix_enabled() is expected


def test_stale_input_path_fix_enabled_false_when_config_file_absent():
    # deliberately do not create config/campaign_config.yaml
    assert rpr._stale_input_path_fix_enabled() is False


# ---------------------------------------------------------------------------
# _apply_stale_input_path_fix -- handoff mutation
# ---------------------------------------------------------------------------


def test_apply_stale_input_path_fix_noop_when_flag_off():
    root = rpr.ROOT
    _set_flag(root, False)
    handoff = _base_handoff()
    before = [dict(r) for r in handoff["optional_inputs"]]
    rpr._apply_stale_input_path_fix("hypothesis_generation", handoff)
    assert handoff["optional_inputs"] == before


def test_apply_stale_input_path_fix_noop_for_non_target_stage():
    root = rpr.ROOT
    _set_flag(root, True)
    handoff = _base_handoff()
    before = [dict(r) for r in handoff["optional_inputs"]]
    rpr._apply_stale_input_path_fix("innovation_expansion", handoff)
    assert handoff["optional_inputs"] == before, (
        "innovation_expansion's own template never declares these paths -- "
        "the fix must not touch a stage it was not measured against"
    )


def test_apply_stale_input_path_fix_corrects_both_paths_when_flag_on():
    root = rpr.ROOT
    _set_flag(root, True)
    handoff = _base_handoff()
    rpr._apply_stale_input_path_fix("hypothesis_generation", handoff)
    paths = {req["path"] for req in handoff["optional_inputs"]}
    assert paths == {
        "../../campaign_record/campaign_knowledge_base.yaml",
        "../../campaign_record/feed_wishlist.yaml",
    }


def test_apply_stale_input_path_fix_does_not_add_entries_that_are_not_declared():
    root = rpr.ROOT
    _set_flag(root, True)
    handoff = {
        "required_inputs": [
            {"path": "artifacts/research_brief.yaml", "reason": "base"}
        ],
        "optional_inputs": [],
    }
    rpr._apply_stale_input_path_fix("hypothesis_generation", handoff)
    assert handoff["optional_inputs"] == [], (
        "the fix must only correct paths already present in the handoff, "
        "never add a new optional_input entry"
    )


def test_apply_stale_input_path_fix_leaves_unrelated_optional_inputs_alone():
    root = rpr.ROOT
    _set_flag(root, True)
    handoff = _base_handoff()
    handoff["optional_inputs"].append(
        {
            "path": "artifacts/run_context.yaml",
            "reason": "instrument escalation override",
        }
    )
    rpr._apply_stale_input_path_fix("hypothesis_generation", handoff)
    paths = {req["path"] for req in handoff["optional_inputs"]}
    assert "artifacts/run_context.yaml" in paths


# ---------------------------------------------------------------------------
# Off-by-default acceptance bar: fully-assembled PROMPT TEXT, flag off vs.
# a baseline that never calls _apply_stale_input_path_fix at all.
# ---------------------------------------------------------------------------


def test_flag_off_prompt_is_byte_identical_to_never_calling_the_fix_at_all():
    root = rpr.ROOT
    _set_flag(root, False)
    _write_real_kb_and_wishlist(
        root
    )  # present on disk but must not matter -- flag is off
    run_dir = _minimal_run(root, "run_910")

    baseline_handoff = _base_handoff()
    baseline_prompt = rpr._build_stage_prompt(
        "hypothesis_generation", baseline_handoff, run_dir
    )

    flag_off_handoff = _base_handoff()
    rpr._apply_stale_input_path_fix("hypothesis_generation", flag_off_handoff)
    flag_off_prompt = rpr._build_stage_prompt(
        "hypothesis_generation", flag_off_handoff, run_dir
    )

    assert flag_off_prompt == baseline_prompt, (
        "flag-off must be byte-identical to the code path that never calls "
        "_apply_stale_input_path_fix at all -- a divergence here means the "
        "path fix leaked even while nominally off"
    )


def test_flag_on_prompt_actually_carries_kb_and_wishlist_content():
    root = rpr.ROOT
    _set_flag(root, True)
    _write_real_kb_and_wishlist(root)
    run_dir = _minimal_run(root, "run_911")

    handoff = _base_handoff()
    rpr._apply_stale_input_path_fix("hypothesis_generation", handoff)
    prompt = rpr._build_stage_prompt("hypothesis_generation", handoff, run_dir)

    assert "exhausted_mechanisms" in prompt, (
        "corrected KB path must actually resolve into the prompt"
    )
    assert "liquidation_data" in prompt, (
        "corrected feed_wishlist path must actually resolve into the prompt"
    )


# ---------------------------------------------------------------------------
# The general "silent optional input" defect: a WARNING now fires instead of
# vanishing with zero trace. Unconditional (no flag) -- diagnostic only, does
# not change context_blocks/full_prompt (proven by the byte-identity test
# above, which still passes with the warning wired in).
# ---------------------------------------------------------------------------


def test_missing_optional_input_warns_instead_of_vanishing_silently(capsys):
    root = rpr.ROOT
    run_dir = _minimal_run(root, "run_912")
    # deliberately do not write campaign_record/campaign_knowledge_base.yaml
    # or campaign_record/feed_wishlist.yaml -- both optional_inputs miss.
    handoff = _base_handoff()

    rpr._build_stage_prompt("hypothesis_generation", handoff, run_dir)

    captured = capsys.readouterr()
    assert "campaign_knowledge_base.yaml" in captured.out
    assert "feed_wishlist.yaml" in captured.out
    assert captured.out.count("WARNING: optional_input never resolved") == 2


def test_present_optional_input_suppresses_its_own_warning(capsys):
    root = rpr.ROOT
    _write_real_kb_and_wishlist(root)
    run_dir = _minimal_run(root, "run_913")
    # Use the CORRECT paths directly (flag-independent: this test exercises
    # the warning, not the path-fix union).
    handoff = {
        "required_inputs": [
            {"path": "artifacts/research_brief.yaml", "reason": "base"}
        ],
        "optional_inputs": [
            {
                "path": "../../campaign_record/campaign_knowledge_base.yaml",
                "reason": "kb",
            },
        ],
    }

    rpr._build_stage_prompt("hypothesis_generation", handoff, run_dir)

    captured = capsys.readouterr()
    assert "WARNING: optional_input never resolved" not in captured.out
