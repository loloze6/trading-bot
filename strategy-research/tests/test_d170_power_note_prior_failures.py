"""D-170 (PR-10, run_098 defect): power_parameters.power_note and the prior_campaign_failures wording.

hypothesis-design/SKILL.md has asked the model to write `power_parameters.power_note` since
241548d2 (2026-07-06) while hypothesis_card.schema.json forbade it (power_parameters is
additionalProperties: false). The schema now gains an optional string `power_note`. The same skill's
"cite the run_ids" sentence for `library_lookup.prior_campaign_failures` now names the object form
{run_id, mechanism_tried} the schema's items already require. Declared prompt change, no flag.
"""
import json
import re
from pathlib import Path

import jsonschema

SR = Path(__file__).resolve().parent.parent
SKILL = SR / "workflow_artifacts" / "skills" / "hypothesis-design" / "SKILL.md"
SCHEMA = SR / "workflow_artifacts" / "schemas" / "hypothesis_card.schema.json"


def _validator():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    return jsonschema.validators.validator_for(schema)(schema)


def _card(power_extra=None, failures=None):
    power = {"activation_rate": 0.3, "plausible_ic_upper": 0.04}
    power.update(power_extra or {})
    lookup = {"indicator_id": None, "regime_affinity_for_target": None, "crowding_risk": None}
    if failures is not None:
        lookup["prior_campaign_failures"] = failures
    return {
        "hypothesis_id": "H_D170", "thesis": "t", "rationale": "r",
        "edge_source": {"category": "persistent_behavioral_bias", "evidence_type": "price_volume_only",
                        "specific_mechanism": "m", "why_not_arbitraged": "w", "measurable_proxy": "p"},
        "signal_concept": "s", "target_market": "m", "timeframe": "1d",
        "assumptions": ["a"], "expected_failure_modes": ["f1", "f2", "f3"],
        "library_lookup": lookup, "power_parameters": power,
    }


def _paths(card):
    return [e.json_path for e in _validator().iter_errors(card)]


def test_baseline_card_validates():
    assert _paths(_card()) == []


def test_power_note_string_validates():
    assert _paths(_card({"power_note": "dense OHLCV, low crowding: axis (c) drove the choice"})) == []


def test_power_note_must_be_a_string():
    assert _paths(_card({"power_note": ["dense"]})) == ["$.power_parameters.power_note"]
    assert _paths(_card({"power_note": 3})) == ["$.power_parameters.power_note"]


def test_power_note_is_optional_not_required():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    power = schema["properties"]["power_parameters"]
    assert "power_note" in power["properties"]
    assert "power_note" not in power["required"]
    assert _paths(_card()) == []  # a card without it still validates


def test_other_power_parameters_keys_are_still_refused():
    assert _paths(_card({"power_notes": "typo"})) == ["$.power_parameters"]


def test_prior_campaign_failures_objects_validate_and_bare_strings_fail():
    ok = [{"run_id": "run_040", "mechanism_tried": "ma crossover"}]
    assert _paths(_card(failures=ok)) == []
    assert _paths(_card(failures=["run_040"])) == ["$.library_lookup.prior_campaign_failures[0]"]


def _skill_flat():
    return re.sub(r"\s+", " ", SKILL.read_text(encoding="utf-8"))


def test_skill_asks_for_the_object_form_of_prior_campaign_failures():
    flat = _skill_flat()
    assert ("Record what you checked in `library_lookup.prior_campaign_failures` (cite each one you "
            "are redirecting from as `{run_id, mechanism_tried}`, the object form of that list's "
            "items) so the decision is auditable, not just asserted.") in flat
    assert "cite the `run_id`s you are redirecting from" not in flat


def test_skill_power_note_ask_matches_the_schema():
    flat = _skill_flat()
    assert "`power_parameters.power_note`" in flat
    assert "power_note" in json.loads(SCHEMA.read_text(encoding="utf-8"))["properties"][
        "power_parameters"]["properties"]
