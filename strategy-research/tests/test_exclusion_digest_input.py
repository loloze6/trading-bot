"""
E-032 S2a -- off-by-default proof for the exclusion-digest required_input.

Sandboxing: relies on tests/conftest.py's autouse _sandbox_by_default fixture
for rpr.ROOT (already redirected to a per-test tmp_path sandbox before any
test body runs), same precedent test_k3_protocol_pinning.py's B7 tests and
test_halt_quarantine_policy.py established for this exact shape of flag.

The acceptance bar (per the dispatching session's brief, not merely "the
code path is skipped"): flag-off must produce a BYTE-IDENTICAL fully-
assembled prompt to a baseline that never calls
_apply_exclusion_digest_input at all -- because adding an optional_input
changes what run_claude_worker reads into context_blocks, which changes the
prompt text an LLM stage receives. Comparing prompt TEXT, not just asserting
the handoff dict/code path, is the actual proof.
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
        "asset: BTCUSDT\n", encoding="utf-8")
    return run_dir


def _base_handoff() -> dict:
    return {
        "required_inputs": [{"path": "artifacts/research_brief.yaml", "reason": "base"}],
        "optional_inputs": [],
    }


def _set_flag(root: Path, enabled) -> None:
    """enabled: True, False, or None (key/section absent entirely)."""
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    if enabled is None:
        (config_dir / "campaign_config.yaml").write_text("orchestrator: {}\n", encoding="utf-8")
        return
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"orchestrator": {"exclusion_digest_input": {"enabled": bool(enabled)}}}, f)


def _write_digest(root: Path) -> None:
    digest_path = root / "campaign_record" / "exclusion_digest.yaml"
    digest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(digest_path, "w", encoding="utf-8") as f:
        yaml.safe_dump({
            "schema_version": 1,
            "families": {"funding_rate_extreme": {"confidence": "structural_indicator_id",
                                                    "triples": [{"instrument": "BTCUSDT",
                                                                  "timeframe": "1h",
                                                                  "run_ids": ["run_044"]}]}},
        }, f)


# ---------------------------------------------------------------------------
# _exclusion_digest_input_enabled
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("enabled,expected", [(True, True), (False, False), (None, False)])
def test_exclusion_digest_input_enabled_reads_flag(enabled, expected):
    root = rpr.ROOT
    _set_flag(root, enabled)
    assert rpr._exclusion_digest_input_enabled() is expected


def test_exclusion_digest_input_enabled_false_when_config_file_absent():
    # deliberately do not create config/campaign_config.yaml
    assert rpr._exclusion_digest_input_enabled() is False


# ---------------------------------------------------------------------------
# _apply_exclusion_digest_input -- handoff mutation
# ---------------------------------------------------------------------------

def test_apply_exclusion_digest_input_noop_when_flag_off():
    root = rpr.ROOT
    _set_flag(root, False)
    _write_digest(root)
    run_dir = _minimal_run(root, "run_900")
    handoff = _base_handoff()
    rpr._apply_exclusion_digest_input("hypothesis_generation", handoff, run_dir)
    assert handoff["optional_inputs"] == []


def test_apply_exclusion_digest_input_noop_for_non_generating_stage():
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root)
    run_dir = _minimal_run(root, "run_901")
    handoff = _base_handoff()
    rpr._apply_exclusion_digest_input("validation", handoff, run_dir)
    assert handoff["optional_inputs"] == []


def test_apply_exclusion_digest_input_skips_missing_digest_file_even_when_flag_on():
    root = rpr.ROOT
    _set_flag(root, True)
    # deliberately do not write campaign_record/exclusion_digest.yaml
    run_dir = _minimal_run(root, "run_902")
    handoff = _base_handoff()
    rpr._apply_exclusion_digest_input("hypothesis_generation", handoff, run_dir)  # must not raise
    assert handoff["optional_inputs"] == []


def test_apply_exclusion_digest_input_adds_when_flag_on_and_file_exists():
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root)
    run_dir = _minimal_run(root, "run_903")
    handoff = _base_handoff()
    rpr._apply_exclusion_digest_input("hypothesis_generation", handoff, run_dir)
    paths = {req["path"] for req in handoff["optional_inputs"]}
    assert paths == {"../../campaign_record/exclusion_digest.yaml"}


def test_apply_exclusion_digest_input_deduplicates_already_listed_path():
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root)
    run_dir = _minimal_run(root, "run_904")
    handoff = _base_handoff()
    handoff["optional_inputs"].append({"path": "../../campaign_record/exclusion_digest.yaml",
                                        "reason": "already listed"})
    rpr._apply_exclusion_digest_input("hypothesis_generation", handoff, run_dir)
    matching = [r for r in handoff["optional_inputs"]
                if r["path"] == "../../campaign_record/exclusion_digest.yaml"]
    assert len(matching) == 1


def test_apply_exclusion_digest_input_covers_both_generating_stages():
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root)
    for stage in ("hypothesis_generation", "innovation_expansion"):
        run_dir = _minimal_run(root, f"run_905_{stage}")
        handoff = _base_handoff()
        rpr._apply_exclusion_digest_input(stage, handoff, run_dir)
        paths = {req["path"] for req in handoff["optional_inputs"]}
        assert paths == {"../../campaign_record/exclusion_digest.yaml"}, f"stage {stage} must receive it"


# ---------------------------------------------------------------------------
# Off-by-default acceptance bar: fully-assembled PROMPT TEXT, flag off vs.
# a baseline that never calls _apply_exclusion_digest_input at all.
# ---------------------------------------------------------------------------

def test_flag_off_prompt_is_byte_identical_to_never_calling_the_union_at_all():
    root = rpr.ROOT
    _set_flag(root, False)
    _write_digest(root)  # present on disk but must not matter -- flag is off
    run_dir = _minimal_run(root, "run_906")

    baseline_handoff = _base_handoff()
    baseline_prompt = rpr._build_stage_prompt("hypothesis_generation", baseline_handoff, run_dir)

    flag_off_handoff = _base_handoff()
    rpr._apply_exclusion_digest_input("hypothesis_generation", flag_off_handoff, run_dir)
    flag_off_prompt = rpr._build_stage_prompt("hypothesis_generation", flag_off_handoff, run_dir)

    assert flag_off_prompt == baseline_prompt, (
        "flag-off must be byte-identical to the code path that never calls "
        "_apply_exclusion_digest_input at all -- a divergence here means the "
        "input gate leaked even while nominally off"
    )


def test_flag_off_prompt_identical_even_when_key_and_section_are_absent():
    """None (absent key/section), not just False, must be indistinguishable
    from off -- same discipline as _quarantine_enabled()."""
    root = rpr.ROOT
    _set_flag(root, None)
    _write_digest(root)
    run_dir = _minimal_run(root, "run_907")

    baseline_handoff = _base_handoff()
    baseline_prompt = rpr._build_stage_prompt("hypothesis_generation", baseline_handoff, run_dir)

    handoff = _base_handoff()
    rpr._apply_exclusion_digest_input("hypothesis_generation", handoff, run_dir)
    prompt = rpr._build_stage_prompt("hypothesis_generation", handoff, run_dir)

    assert prompt == baseline_prompt


def test_flag_on_prompt_differs_and_carries_digest_content():
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root)
    run_dir = _minimal_run(root, "run_908")

    baseline_handoff = _base_handoff()
    baseline_prompt = rpr._build_stage_prompt("hypothesis_generation", baseline_handoff, run_dir)

    on_handoff = _base_handoff()
    rpr._apply_exclusion_digest_input("hypothesis_generation", on_handoff, run_dir)
    on_prompt = rpr._build_stage_prompt("hypothesis_generation", on_handoff, run_dir)

    assert on_prompt != baseline_prompt
    assert "funding_rate_extreme" in on_prompt
    assert "exclusion_digest.yaml" in on_prompt


def test_flag_on_innovation_expansion_prompt_also_carries_digest_content():
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root)
    run_dir = _minimal_run(root, "run_909")
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(
        "hypothesis_id: X\n", encoding="utf-8")

    handoff = {
        "required_inputs": [
            {"path": "artifacts/research_brief.yaml", "reason": "base"},
            {"path": "artifacts/hypothesis_card.yaml", "reason": "base"},
        ],
        "optional_inputs": [],
    }
    rpr._apply_exclusion_digest_input("innovation_expansion", handoff, run_dir)
    prompt = rpr._build_stage_prompt("innovation_expansion", handoff, run_dir)
    assert "funding_rate_extreme" in prompt


# ---------------------------------------------------------------------------
# E-036 S2a (2026-09-27, S1_FINDINGS_SLICE8.md operator decision 3 + code
# review). Every test above is master's, unchanged: with no
# campaign_record/campaign_memory.yaml (regroup_record off, today's default)
# the input is still exclusion_digest.yaml, byte-identical. When the memory
# exists the input is artifacts/tried_ideas.yaml INSTEAD (never both).
# ---------------------------------------------------------------------------

from test_e036_s2a_exact_match_gate import _config, _prior_run_in_memory  # noqa: E402

_TRIED = "artifacts/tried_ideas.yaml"
_DIGEST = "../../campaign_record/exclusion_digest.yaml"
# VERBATIM the reason string origin/master (ed8b406e) hard-coded -- the pin.
_MASTER_DIGEST_REASON = (
    "E-032 S2a: family-scoped (family, instrument, timeframe) triples "
    "already tried, freshly derived from run artifacts -- NOT "
    "campaign_state.yaml's stale, family-blind instruments_tried/"
    "timeframes_tried lists. Prefer a candidate whose family is absent "
    "here, or whose (instrument, timeframe) triple is absent under its "
    "family, over a same-family tweak when both are viable. This is "
    "raw material, not a binding gate -- the anti_adjacency_gate tool "
    "stage makes the mechanical refusal decision downstream."
)


def test_default_without_memory_is_byte_identical_to_master():
    """The pin: flag on (the committed default), digest on disk, no memory
    file -> exactly master's handoff entry and assembled prompt, and nothing
    written into the run."""
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root)
    run_dir = _minimal_run(root, "run_920")
    handoff = _base_handoff()
    rpr._apply_exclusion_digest_input("hypothesis_generation", handoff, run_dir)
    assert handoff["optional_inputs"] == [{"path": _DIGEST, "reason": _MASTER_DIGEST_REASON}]
    master_handoff = _base_handoff()
    master_handoff["optional_inputs"].append({"path": _DIGEST, "reason": _MASTER_DIGEST_REASON})
    assert (rpr._build_stage_prompt("hypothesis_generation", handoff, run_dir)
            == rpr._build_stage_prompt("hypothesis_generation", master_handoff, run_dir))
    assert not (run_dir / _TRIED).exists()


def test_with_memory_the_input_is_tried_ideas_instead_of_the_digest():
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root)  # still on disk -- must NOT also be fed
    _prior_run_in_memory("run_044", _config(), protocol_name="run_044_generated.json")
    run_dir = _minimal_run(root, "run_921")
    handoff = _base_handoff()
    rpr._apply_exclusion_digest_input("hypothesis_generation", handoff, run_dir)
    assert [r["path"] for r in handoff["optional_inputs"]] == [_TRIED]
    view = rpr.load_yaml(run_dir / _TRIED)
    assert view["runs"] == [{"run_id": "run_044", "hypothesis_id": "H-PRIOR",
                             "symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1h",
                             "idea_status": "refuted", "variants_tested": 1}]
    prompt = rpr._build_stage_prompt("hypothesis_generation", handoff, run_dir)
    assert "H-PRIOR" in prompt and f"CONTENT OF {_DIGEST}" not in prompt


def test_with_memory_flag_off_writes_nothing_and_prompt_is_unchanged():
    root = rpr.ROOT
    _set_flag(root, False)
    _prior_run_in_memory("run_044", _config(), protocol_name="run_044_generated.json")
    run_dir = _minimal_run(root, "run_922")
    baseline = rpr._build_stage_prompt("hypothesis_generation", _base_handoff(), run_dir)
    handoff = _base_handoff()
    rpr._apply_exclusion_digest_input("hypothesis_generation", handoff, run_dir)
    assert handoff["optional_inputs"] == []
    assert rpr._build_stage_prompt("hypothesis_generation", handoff, run_dir) == baseline
    assert not (run_dir / _TRIED).exists()


def test_tried_ideas_reason_names_the_campaign_record_and_no_family_grouping():
    root = rpr.ROOT
    _set_flag(root, True)
    _prior_run_in_memory("run_044", _config(), protocol_name="run_044_generated.json")
    run_dir = _minimal_run(root, "run_923")
    handoff = _base_handoff()
    rpr._apply_exclusion_digest_input("innovation_expansion", handoff, run_dir)
    reason = handoff["optional_inputs"][0]["reason"]
    assert "campaign_memory.yaml" in reason and "No family grouping" in reason
    assert "family-scoped" not in reason


def test_tried_ideas_view_is_bounded_most_recent_kept():
    import campaign_memory as cm
    runs = {f"run_{i:03d}": {"run_id": f"run_{i:03d}", "hypothesis_id": f"H{i}",
                             "recorded_at": f"2021-01-{i + 1:02d}T00:00:00+00:00",
                             "idea_status": "refuted", "timeframe": "1h", "variants": {}}
            for i in range(5)}
    view = cm.tried_ideas({"runs": runs}, root=rpr.ROOT, max_rows=3)
    assert [r["run_id"] for r in view["runs"]] == ["run_002", "run_003", "run_004"]
    assert view["omitted_older_runs"] == 2 and view["runs_in_memory"] == 5
    assert "family" not in yaml.safe_dump(view["runs"])
