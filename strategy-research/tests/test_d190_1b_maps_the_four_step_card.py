"""
D-190 (review round, direction answers 2026-10-24): the four-step card has no
`signal_concept`, so step 1b's fidelity rule maps `idea_quantities` and the
`statement`; each `not_expressible` entry reaches artifacts/deviations.yaml as a
`DEVIATION:` entry declared by step 1a; the old step-1a instructions (power
pre-registration, library lookup, cost_feasibility, dead IMPROVEMENT pointers)
are gone from the skills, the handoff template and the card template.
"""
import re
import sys
from pathlib import Path

import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "tools"))

import nearest_build as nb  # noqa: E402

SKILLS = SR_ROOT / "workflow_artifacts" / "skills"
HD = SKILLS / "hypothesis-design"
SCA = SKILLS / "strategy-config-authoring"


def _flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def _fidelity() -> str:
    text = (SCA / "SKILL.md").read_text(encoding="utf-8")
    start = text.index("**Fidelity (O-7)")
    end = text.index("**`component_gap` only after compositions are ruled out.**")
    return " ".join(text[start:end].split())


def test_the_fidelity_paragraph_maps_idea_quantities_and_the_statement():
    para = _fidelity()
    assert "signal_concept" not in para
    assert "EACH `idea_quantities` entry of the card, and the `statement`" in para
    for part in ("`predicts`", "`horizon_bars`", "`condition`"):
        assert part in para
    # the rest of the paragraph is intact: the deviation rule, fill timing, sizing (D-187)
    assert "`config_choice` starts with `DEVIATION:`" in para
    assert "A fill-timing clause in a card" in para
    assert "A sizing clause in a card" in para


def test_each_not_expressible_entry_is_copied_as_declared_by_step_1a_without_tried():
    para = _fidelity()
    assert "Each entry of the card's `not_expressible`" in para
    assert "`DEVIATION: declared by step 1a`" in para
    assert "no new argument and no `tried` list" in para
    assert "into the run's deviation record" in para


def test_a_declared_not_expressible_entry_reaches_deviations_yaml_with_no_code_change():
    """The skill's wording (one config_rationale DEVIATION: entry per item, the card's
    text as hypothesis_claim) is what nearest_build.build_record already derives
    artifacts/deviations.yaml from."""
    spec = {"config_rationale": [
        {"hypothesis_claim": "exit after 12 bars",
         "config_choice": "DEVIATION: declared by step 1a, nothing built"},
        {"hypothesis_claim": "the 1-bar return", "config_choice": "PriceEvolutionComponent(period=1)"}]}
    rec = nb.build_record("run_x", {"status": "spec_ready"}, spec)
    assert rec["status"] == nb.STATUS_APPROXIMATION
    assert rec["config_rationale_lines"] == [
        {"clause": "exit after 12 bars", "text": "declared by step 1a, nothing built"}]
    assert "exit after 12 bars" in nb.approximation_block(rec)["line"]


def test_the_old_numbered_section_pointers_are_gone_from_the_two_skills():
    for path in list(HD.glob("*.md")) + list(SCA.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(r"IMPROVEMENT 0\d", text):
            # the one that stays: strategy-config-authoring's note on backtest-engineering's
            # own IMPROVEMENT 01 (a different skill's section), never a pointer into hypothesis-design
            assert path.name == "SKILL.md" and path.parent == SCA and m.group(0) == "IMPROVEMENT 01", \
                (path.name, m.group(0))


def test_the_dead_pointers_name_step_0_pass_through():
    assert "(hypothesis-design step 0, pass-through)" in (SCA / "SKILL.md").read_text(encoding="utf-8")
    assert "step 0 (pass-through)" in _flat(HD / "DECIDE_NEXT_CANDIDATES.md") \
        or "step 0 stands unchanged" in _flat(HD / "DECIDE_NEXT_CANDIDATES.md")
    assert "step 0, pass-through" in _flat(HD / "CLAIM_TESTS.md")


def test_the_addenda_name_idea_quantities_and_the_statement_not_signal_concept():
    for name in ("PREFILLED_CLAIM.md", "DECIDE_NEXT_CANDIDATES.md", "BRIEF_HYPOTHESES.md"):
        text = _flat(HD / name)
        assert "signal_concept" not in text, name
        assert "cost_feasibility" not in text and "expected_failure_modes" not in text, name
    assert "`idea_quantities`" in _flat(HD / "PREFILLED_CLAIM.md")
    # D-194: BRIEF_HYPOTHESES.md named idea_quantities only to place a card against the block
    # registry (the distance score); that score is gone, so the addendum no longer names it.


def test_decide_next_no_longer_tells_1a_to_name_residual_ic_or_pick_a_live_entry():
    text = _flat(HD / "DECIDE_NEXT_CANDIDATES.md")
    assert "residual_ic" not in text and "at least one live entry" not in text


def test_the_handoff_and_card_templates_carry_none_of_the_old_instructions():
    handoff = (SR_ROOT / "workflow_artifacts" / "templates" / "handoffs"
               / "research_brief_to_hypothesis.yaml").read_text(encoding="utf-8")
    for old in ("signal_concept", "POWER PRE-REGISTRATION", "power_parameters", "Improvement 04",
                "IMPROVEMENT 01"):
        assert old not in handoff, old
    assert all(r.get("reason") for r in yaml.safe_load(handoff)["required_inputs"])   # schema: reason required
    card = yaml.safe_load((SR_ROOT / "workflow_artifacts" / "templates" / "hypothesis_card.yaml")
                          .read_text(encoding="utf-8"))
    for old in ("signal_concept", "rationale", "assumptions", "expected_failure_modes",
                "power_parameters"):
        assert old not in card, old
    for new in ("idea_quantities", "not_expressible", "statement", "criteria_rationale"):
        assert new in card, new
