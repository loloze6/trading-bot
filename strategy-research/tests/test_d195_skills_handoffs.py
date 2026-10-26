"""
D-195 (build window run_101, PR-3): skill and template text.

- the expansion skill adds a split `design` variant (modifier component at half weight);
- step 1b verifies a `not_expressible` entry against the engine before declaring it
  (supersedes D-190's copy sentence); step 1a limits its exclusions;
- the legacy A1.2 / A5.1 / TOKEN LIMIT / IMPROVEMENT clauses are gone from both handoff templates;
- the expansion stage's reverse_hypothesis, alternative_data_candidates and behavioral_features are
  no longer required (kept as optional legacy properties so earlier runs' artifacts still validate).
"""
import json
import sys
from pathlib import Path

import jsonschema
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "tools"))

SKILLS = SR_ROOT / "workflow_artifacts" / "skills"
HANDOFFS = SR_ROOT / "workflow_artifacts" / "templates" / "handoffs"
SCHEMA = SR_ROOT / "workflow_artifacts" / "schemas" / "expanded_hypothesis_card.schema.json"

LEGACY_FIELDS = ("reverse_hypothesis", "alternative_data_candidates", "behavioral_features",
                 "feed_wishlist_routes", "evidence_type_constraint")


def _flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def _raw(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---- (a) the split variant ------------------------------------------------------------

def test_the_split_variant_rule_is_in_the_expansion_skill():
    text = _flat(SKILLS / "innovation-expansion" / "SKILL.md")
    assert "The split variant (D-195)" in text
    assert "halves the weight of the modifier component" in text
    assert "negated or subtracted term of step 1a's formula" in text
    assert "the second listed component" in text
    assert "`/strategies/regimes/<regime>/components/<index>/weight`" in text
    assert "is a `design` variant" in text
    assert "not a component swap" in text
    assert "`tools/structure_key.py`" in text
    assert "stays the same structure as the base" in text
    assert "never on top of them" in text


def test_the_split_variant_claim_about_the_structure_key_is_true():
    import structure_key as sk
    base = {"regime_detector": {"mode": "threshold_rules", "rules": [], "default_regime": "unknown"},
            "strategies": {"regimes": {"unknown": {"components": [
                {"id": "a", "class": "x.A", "weight": 2.0, "transforms": [{"op": "standardise"}]},
                {"id": "b", "class": "x.B", "weight": -1.0, "transforms": [{"op": "standardise"}]}]}}}}
    half = json.loads(json.dumps(base))
    half["strategies"]["regimes"]["unknown"]["components"][1]["weight"] = -0.5
    flipped = json.loads(json.dumps(base))
    flipped["strategies"]["regimes"]["unknown"]["components"][1]["weight"] = 1.0
    assert sk.compute_structure_hash(base) == sk.compute_structure_hash(half)
    assert sk.compute_structure_hash(base) != sk.compute_structure_hash(flipped)


# ---- (b) step 1b verifies, step 1a limits ---------------------------------------------

def test_step_1b_verifies_a_not_expressible_entry_before_copying_it():
    text = _flat(SKILLS / "strategy-config-authoring" / "SKILL.md")
    assert "Verify it before you copy it (D-195, supersedes D-190's copy sentence)" in text
    assert 'the "Transform ops" section of `STRATEGY_DESIGN_GUIDE.md`' in text
    assert "`ema`" in text and "`threshold_filter`" in text
    assert "`COMPONENT_CATALOG.md`" in text
    assert "both are in your context" in text
    assert "that file is where the ops live, not a file to open" in text
    assert "An entry that can be expressed there is expressed" in text
    assert "Only an entry that survives the check becomes a declared deviation" in text
    assert "`DEVIATION: declared by step 1a`" in text


def test_the_old_d190_copy_sentence_is_gone():
    text = _flat(SKILLS / "strategy-config-authoring" / "SKILL.md")
    assert "is a part step 1a already declared a forecast cannot express: copy it into the deviation record" not in text
    assert "copy it into the deviation record as step 1a declared it" not in text


def test_step_1a_limits_not_expressible_to_exits_position_state_and_order_placement():
    text = _flat(SKILLS / "hypothesis-design" / "SKILL.md")
    assert "and only three kinds: exits, position state and order placement" in text
    assert "exits, holds, position state" not in text
    assert "The config-authoring stage (1b) checks each entry" in text


# ---- (c) the legacy clauses are gone from both handoffs --------------------------------

def test_the_templates_still_parse_as_yaml():
    for name in ("research_brief_to_hypothesis.yaml", "hypothesis_to_innovation_expansion.yaml"):
        doc = yaml.safe_load(_raw(HANDOFFS / name))
        assert doc["deliverables"] and doc["required_inputs"], name
        assert all(r.get("reason") for r in doc["required_inputs"] + doc.get("optional_inputs", [])), name


def test_research_brief_handoff_carries_none_of_the_legacy_clauses():
    text = _raw(HANDOFFS / "research_brief_to_hypothesis.yaml")
    for old in ("single, testable", "A1.2", "available_feeds", "feed_wishlist", "TOKEN LIMIT", "KB BAN-CHECK",
                "campaign_knowledge_base", "exhausted_mechanisms", "A5.1", "D-055"):
        assert old not in text, old
    doc = yaml.safe_load(text)
    paths = [r["path"] for r in doc["required_inputs"]]
    assert paths == ["artifacts/research_brief.yaml", "../../config/indicator_library.yaml"]
    assert [r["path"] for r in doc["optional_inputs"]] == ["artifacts/run_context.yaml"]


def test_expansion_handoff_carries_none_of_the_legacy_clauses():
    text = _raw(HANDOFFS / "hypothesis_to_innovation_expansion.yaml")
    for old in ("A1.2", "available_feeds", "funding", "IMPROVEMENT 01", "IMPROVEMENT 04", "conservative variant",
                "TOKEN LIMIT", "DIVERSITY CHECK", "price_volume_only"):
        assert old not in text, old
    doc = yaml.safe_load(text)
    assert [r["path"] for r in doc["required_inputs"]] == [
        "artifacts/research_brief.yaml", "artifacts/hypothesis_card.yaml", "../../config/indicator_library.yaml"]
    assert [r["path"] for r in doc["optional_inputs"]] == ["artifacts/refinement_notes.yaml"]
    assert len(doc["constraints"]) == 1 and "refinement notes" in doc["constraints"][0]


# ---- the five orphaned fields ----------------------------------------------------------

def test_the_expansion_skill_no_longer_asks_for_the_legacy_fields():
    text = _raw(SKILLS / "innovation-expansion" / "SKILL.md")
    for field in LEGACY_FIELDS:
        assert field not in text, field
    assert "available_feeds" not in text


def test_the_schema_no_longer_requires_the_legacy_fields_and_keeps_them_optional():
    schema = json.loads(_raw(SCHEMA))
    for field in LEGACY_FIELDS:
        assert field not in schema["required"], field
    assert schema["required"] == ["base_hypothesis_id", "expanded_variants", "regime_specific_variants"]
    assert set(schema["properties"]) == {"base_hypothesis_id", "expanded_variants", "regime_specific_variants",
                                         "alternative_data_candidates", "reverse_hypothesis",
                                         "behavioral_features"}


def test_a_new_card_without_the_fields_validates_and_an_old_one_with_them_still_does():
    validator = jsonschema.Draft7Validator(json.loads(_raw(SCHEMA)))
    new = {"base_hypothesis_id": "H-1", "expanded_variants": ["base", "split"],
           "regime_specific_variants": []}
    validator.validate(new)
    old = dict(new, alternative_data_candidates=["funding rate"], reverse_hypothesis="short it",
               behavioral_features=["capitulation"])
    validator.validate(old)
    assert not validator.is_valid({"base_hypothesis_id": "H-1", "expanded_variants": []})
