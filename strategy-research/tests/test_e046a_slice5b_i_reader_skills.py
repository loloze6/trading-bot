"""
E-046a Slice 5b-i (specialist readers -- "readers + reports consumption" half of Slice 5b,
see engineering/roadmap/E-046a/S1_FINDINGS.md §8's split recommendation).

Covers:
  1. Each of the 5 workflow_artifacts/skills/readers/<category>-reader/SKILL.md files exists,
     is well-formed (frontmatter, non-empty, required sections present), and names both its
     own scoped input report and its own output proposals file.
  2. A hand-constructed, schema-VALID example proposals/<category>.yaml entry per category
     (grounded in build_reports.py's real report field shapes -- S1_FINDINGS.md §6) validates
     cleanly against workflow_artifacts/schemas/proposal.schema.json.
  3. Deliberately malformed examples (missing required field, out-of-range score, kind/patch-
     block mismatch) fail validation -- proving the schema actually constrains something.
  4. Rule-content-preservation for the 4 readers adapted from verdict-interpreter/SKILL.md
     (profitability, trade_efficiency, forecast_power, regime_power): asserts each reader's
     own SKILL.md still contains the SPECIFIC numeric thresholds / enum values its mapped
     rule used in verdict-interpreter/SKILL.md, with a positive control confirming those same
     tokens are genuinely present in the source file (not a self-referential tautology).
     component_attribution is explicitly exempted -- it has no existing rule-block analog
     (S1_FINDINGS.md §4), confirmed new content, not adapted content.
  5. Routing-authority guard: every reader's own Forbidden section explicitly forbids emitting
     hypothesis_verdict/lineage_routing, and no reader's Output requirements section defines
     either as a field it must populate -- an idea's status comes from the grid
     (idea_status.yaml); reader scores only rank candidates for decide-next (E-046a
     realignment, 2026-09-23).

WHY THIS FILE'S TEST STRATEGY IS MOCKED-CONTENT VALIDATION, NOT A REAL LLM CALL
--------------------------------------------------------------------------------
No ANTHROPIC_API_KEY exists in this build environment (S1_FINDINGS.md §9, confirmed directly,
value not echoed) -- the 5 skills this file tests cannot be invoked for real here. This file
therefore validates a hand-constructed, schema-shaped example of what a well-formed LLM
response WOULD look like (per category, grounded in build_reports.py's real report shapes)
against the schema a real response would need to satisfy -- proving the schema itself
constrains something, and that the skill files' own documented output shape is internally
consistent -- rather than asserting anything about a real model's actual output quality.

test_e056_config_direct_authoring.py was checked as the dispatch-named precedent for a
mocked-LLM-response pattern: its own mocking (`monkeypatch`-ing `subprocess.run`, its section
8) is orchestrator-level -- it mocks a deterministic TOOL-stage subprocess call
(`validate_config.py` via `run_tool_worker`), not an LLM invocation, and there is no LLM
response to mock in that file at all (config-direct-authoring's `strategy_config_authoring`
stage is itself Claude-Agent-SDK-invoked exactly like the readers here, but that file never
exercises the LLM call site). It is therefore NOT directly applicable to skill-CONTENT
validation the way the dispatch anticipated it might be -- this file's own strategy (schema
validation of hand-built example outputs) is designed independently, following the general
precedent named in S1_FINDINGS.md §9 (E-056 Slice 3b's and E-033.1 Slice 4a's commits: ship
unit-tested-but-not-proven-against-a-real-pass, `state: off_incomplete`) rather than reusing
test_e056_config_direct_authoring.py's specific mechanism.

That same file DOES supply a directly-applicable precedent for a different concern -- rule-
content preservation across a rewritten skill file
(`test_ungated_hypotheses_and_forbidden_sections_carried_over_byte_identical`, its own
docstring item 10). This file's own item 4 above adapts that precedent rather than reusing it
verbatim: Slice 3b's two carried-over sections were UNCHANGED prose (a literal byte-diff is
the right tool), whereas this build's rule content was rewritten to read from each category's
own narrow report shape instead of protocol_result.yaml/trade_diagnostics.json directly (S1_
FINDINGS.md §4's own build-list phrasing) -- a byte-diff would trivially fail on every prose
rewrite and prove nothing. Token-membership (the specific thresholds/enums survive the
rewrite) is the adapted check that actually answers "was a rule silently dropped," which is
what the precedent test is FOR, not just what it literally does.
"""
import copy
import json
from pathlib import Path

import pytest
import yaml

jsonschema = pytest.importorskip("jsonschema")

_ROOT = Path(__file__).parent.parent
_SKILLS_DIR = _ROOT / "workflow_artifacts" / "skills" / "readers"
_SCHEMA_PATH = _ROOT / "workflow_artifacts" / "schemas" / "proposal.schema.json"
_VERDICT_INTERPRETER_PATH = _ROOT / "workflow_artifacts" / "skills" / "verdict-interpreter" / "SKILL.md"

CATEGORIES = [
    "profitability",
    "trade_efficiency",
    "forecast_power",
    "regime_power",
    "component_attribution",
]

REQUIRED_SECTIONS = [
    "## Mission",
    "## Required inputs",
    "## Required outputs",
    "## Output requirements",
    "## Scoring (0-3 anchors)",
    "## Checklist",
    "## Forbidden",
    "## Context rule",
]


def _schema() -> dict:
    return json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))


def _skill_text(category: str) -> str:
    return (_SKILLS_DIR / f"{category}-reader" / "SKILL.md").read_text(encoding="utf-8")


def _validate(instance: dict) -> None:
    jsonschema.validate(instance=instance, schema=_schema())


# ---------------------------------------------------------------------------
# 1. Existence + well-formedness
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("category", CATEGORIES)
def test_reader_skill_file_exists(category):
    path = _SKILLS_DIR / f"{category}-reader" / "SKILL.md"
    assert path.exists(), f"missing {path}"


@pytest.mark.parametrize("category", CATEGORIES)
def test_reader_skill_file_not_empty(category):
    text = _skill_text(category)
    assert len(text.strip()) > 500, f"{category}-reader/SKILL.md looks suspiciously short"


@pytest.mark.parametrize("category", CATEGORIES)
def test_reader_skill_has_valid_frontmatter(category):
    text = _skill_text(category)
    assert text.startswith("---\n"), f"{category}-reader/SKILL.md missing YAML frontmatter"
    end = text.index("\n---\n", 4)
    frontmatter = yaml.safe_load(text[4:end])
    assert frontmatter["name"] == f"{category}-reader"
    assert isinstance(frontmatter.get("description"), str) and len(frontmatter["description"]) > 20


@pytest.mark.parametrize("category", CATEGORIES)
def test_reader_skill_has_required_sections(category):
    text = _skill_text(category)
    missing = [s for s in REQUIRED_SECTIONS if s not in text]
    assert not missing, f"{category}-reader/SKILL.md missing required sections: {missing}"


@pytest.mark.parametrize("category", CATEGORIES)
def test_reader_skill_names_its_own_scoped_report_input(category):
    text = _skill_text(category)
    assert f"reports/{category}.yaml" in text


@pytest.mark.parametrize("category", CATEGORIES)
def test_reader_skill_names_its_own_proposals_output(category):
    text = _skill_text(category)
    assert f"proposals/{category}.yaml" in text


@pytest.mark.parametrize("category", CATEGORIES)
def test_reader_skill_scopes_grid_evaluation_as_optional(category):
    """Dispatch's own scoped-inputs requirement: ONLY the category's own report plus
    grid_evaluation.yaml (Slice 2), and grid_evaluation.yaml is off-by-default per E-046b
    -- so it must be documented as optional, not a hard requirement that would break a
    default (flag-off) run."""
    text = _skill_text(category)
    assert "grid_evaluation.yaml" in text
    assert "optional" in text.lower()


def test_component_attribution_states_it_is_new_territory():
    """S1_FINDINGS.md §4: component_attribution has no existing rule-block analog in
    verdict-interpreter/SKILL.md -- its own SKILL.md must say so, not silently present
    adapted-looking content."""
    text = _skill_text("component_attribution")
    assert "no existing rule-block analog" in text or "new territory" in text.lower()
    assert "new content" in text.lower() or "authored for this" in text.lower()


# ---------------------------------------------------------------------------
# 2 & 3. Schema validation -- hand-built, schema-shaped examples (mocked LLM output)
# ---------------------------------------------------------------------------

_VALID_EXAMPLES = {
    "profitability": {
        "proposal_id": "profitability-run_059-1",
        "kind": "patch",
        "patch": [
            {
                "component_id": "keltner",
                "field": "transforms[2].params.min_abs",
                "before": 15.0,
                "after": 20.0,
            }
        ],
        "evidence": [
            "slices.overall.diagnostics.median_cost_drag_pct=142.82, "
            "median_gross_pnl=+21.94 -- gross PnL positive but fees consume it (Rule 1 shape).",
            "slices.per_symbol.BTCUSDT[*].core.cost_drag_pct > 100% in 4/5 windows.",
        ],
        "scores": {"confidence_real": 2, "distance_to_profitable": 1, "mechanism_plausibility": 2},
        "model_id": "claude-sonnet-5",
        "rubric_version": "profitability-reader-v1",
    },
    "trade_efficiency": {
        "proposal_id": "trade_efficiency-run_059-1",
        "kind": "patch",
        "patch": [
            {"component_id": "keltner", "field": "stop_loss_pct", "before": 0.0, "after": 1.5}
        ],
        "evidence": [
            "slices.overall.pnl_concentration.pct_pnl_from_worst_decile_trades=123%, "
            "slices.overall.exit_reason_breakdown.signal_flip_pct=95% -- holding_sizing "
            "pattern, no stop mechanism (STEP 03 decision table).",
        ],
        "scores": {"confidence_real": 3, "distance_to_profitable": 2, "mechanism_plausibility": 3},
        "model_id": "claude-sonnet-5",
        "rubric_version": "trade_efficiency-reader-v1",
    },
    "forecast_power": {
        "proposal_id": "forecast_power-run_059-1",
        "kind": "new_block",
        "block": {
            "kind": "forecast",
            "config_paths": ["strategies.regimes.unknown.components"],
            "scaffolding": ["new signal component replacing rsi (Rule 2: no directional edge)"],
            "rationale": (
                "slices.overall.median_forecast_return_corr=0.012, below the 0.03 no-edge "
                "floor across 4/5 windows -- propose a structurally different signal."
            ),
        },
        "evidence": [
            "slices.overall.median_forecast_return_corr=0.012 (Rule 2 floor is 0.03); "
            "slices.per_window shows corr < 0.03 in 4/5 windows.",
        ],
        "scores": {"confidence_real": 2, "distance_to_profitable": 1, "mechanism_plausibility": 1},
        "model_id": "claude-sonnet-5",
        "rubric_version": "forecast_power-reader-v1",
    },
    "regime_power": {
        "proposal_id": "regime_power-run_059-1",
        "kind": "new_block",
        "block": {
            "kind": "regime",
            "config_paths": ["regime_detector"],
            "scaffolding": ["score_product mode instead of threshold_rules (Rule 4, n_bars >= 20)"],
            "rationale": (
                "trending regime's forward_return_mean is near zero with n_bars=340 "
                "(median across windows) -- reliable sample, regime label itself uninformative."
            ),
        },
        "evidence": [
            "slices.per_regime.trending[*].regime_validity.n_bars median=340 (>=20 floor); "
            "forward_return_mean near zero across those entries (Rule 4).",
        ],
        "scores": {"confidence_real": 2, "distance_to_profitable": 1, "mechanism_plausibility": 2},
        "model_id": "claude-sonnet-5",
        "rubric_version": "regime_power-reader-v1",
    },
    "component_attribution": {
        "proposal_id": "component_attribution-run_059-1",
        "kind": "patch",
        "patch": [
            {"component_id": "keltner", "field": "weight", "before": 1.0, "after": 0.3}
        ],
        "evidence": [
            "slices.overall.components_discovered=['rsi','keltner']; "
            "slices.per_regime.mean_reversion records for component='keltner' are constant "
            "0.0 across every bar listed, while slices.per_regime.trending records for the "
            "same component vary -- keltner appears inert outside trending (Rule CA-2).",
        ],
        "scores": {"confidence_real": 2, "distance_to_profitable": 1, "mechanism_plausibility": 2},
        "model_id": "claude-sonnet-5",
        "rubric_version": "component_attribution-reader-v1",
    },
}


@pytest.mark.parametrize("category", CATEGORIES)
def test_valid_example_proposal_validates_clean(category):
    _validate(_VALID_EXAMPLES[category])


def test_valid_examples_cover_both_kinds():
    """Sanity check on the fixture set itself: both patch and new_block branches of the
    schema's if/then are actually exercised by the golden examples above."""
    kinds = {ex["kind"] for ex in _VALID_EXAMPLES.values()}
    assert kinds == {"patch", "new_block"}


def test_malformed_missing_evidence_fails():
    bad = copy.deepcopy(_VALID_EXAMPLES["profitability"])
    del bad["evidence"]
    with pytest.raises(jsonschema.ValidationError):
        _validate(bad)


def test_malformed_empty_evidence_list_fails():
    bad = copy.deepcopy(_VALID_EXAMPLES["trade_efficiency"])
    bad["evidence"] = []
    with pytest.raises(jsonschema.ValidationError):
        _validate(bad)


def test_malformed_out_of_range_score_fails():
    bad = copy.deepcopy(_VALID_EXAMPLES["forecast_power"])
    bad["scores"]["confidence_real"] = 5
    with pytest.raises(jsonschema.ValidationError):
        _validate(bad)


def test_malformed_negative_score_fails():
    bad = copy.deepcopy(_VALID_EXAMPLES["forecast_power"])
    bad["scores"]["mechanism_plausibility"] = -1
    with pytest.raises(jsonschema.ValidationError):
        _validate(bad)


def test_malformed_missing_score_dimension_fails():
    bad = copy.deepcopy(_VALID_EXAMPLES["component_attribution"])
    del bad["scores"]["distance_to_profitable"]
    with pytest.raises(jsonschema.ValidationError):
        _validate(bad)


def test_malformed_kind_patch_but_block_instead_of_patch_fails():
    bad = copy.deepcopy(_VALID_EXAMPLES["regime_power"])
    bad["kind"] = "patch"
    # block is still present, patch was never added -- kind=patch requires `patch`, forbids `block`.
    with pytest.raises(jsonschema.ValidationError):
        _validate(bad)


def test_malformed_kind_new_block_but_patch_present_fails():
    bad = copy.deepcopy(_VALID_EXAMPLES["profitability"])
    bad["kind"] = "new_block"
    # patch is still present, block was never added -- kind=new_block requires `block`, forbids `patch`.
    with pytest.raises(jsonschema.ValidationError):
        _validate(bad)


def test_malformed_missing_proposal_id_fails():
    bad = copy.deepcopy(_VALID_EXAMPLES["component_attribution"])
    del bad["proposal_id"]
    with pytest.raises(jsonschema.ValidationError):
        _validate(bad)


def test_malformed_invalid_kind_enum_value_fails():
    bad = copy.deepcopy(_VALID_EXAMPLES["profitability"])
    bad["kind"] = "rewrite_everything"
    with pytest.raises(jsonschema.ValidationError):
        _validate(bad)


def test_schema_file_is_valid_draft_2020_12_document():
    schema = _schema()
    assert schema["$schema"].startswith("https://json-schema.org/draft/2020-12")
    jsonschema.Draft202012Validator.check_schema(schema)


def test_schema_documents_it_is_not_loaded_by_code():
    """This repo's own convention (strategy-research/CLAUDE.md: 'Schemas are declared but
    not enforced' / backtest_spec.schema.json's own $comment) -- this new schema must not
    silently imply it's an enforced contract when nothing loads it at runtime."""
    schema = _schema()
    comment = schema.get("$comment", "")
    assert "not load" in comment.lower() or "documentation" in comment.lower()


# ---------------------------------------------------------------------------
# 4. Rule-content preservation (adapted check -- see module docstring for why a literal
#    byte-diff, Slice 3b's own precedent, does not apply here)
# ---------------------------------------------------------------------------

_RULE_CONTENT_PRESERVATION = {
    # Rule 1 (cost drag) + Rule 5 (regime too rare) thresholds/field names.
    "profitability": [
        "80%", "median_cost_drag_pct", "median_gross_pnl",
        "win_rate_vs_sharpe", "0.03", "threshold_filter",
    ],
    # STEP 03 trade-attribution decision table + IMPROVEMENT 10 fee-reduction candidates.
    "trade_efficiency": [
        # NOTE: verdict-interpreter/SKILL.md's own STEP 03 table uses a Unicode minus sign
        # (U+2212, "< −0.10") for entry_efficiency_median's threshold, not an ASCII
        # hyphen -- "0.10" alone is the glyph-independent token both files genuinely share.
        "0.30", "0.10", "80%", "0.50",
        "combine_nearby_trades", "exit_later", "enter_earlier", "trade_less_often",
    ],
    # Rule 2 (no edge), Rule 3 (inverted), Rule 6 (null) thresholds.
    "forecast_power": ["0.03", "-0.03", "0.10", "20"],
    # Rule 4 (regime uninformative) n_bars floor + IMPROVEMENT 02's 4 conclusion enum values.
    "regime_power": [
        "20", "signal_bad_everywhere", "signal_good_wrong_regime_gate",
        "signal_good_regime_gate_correct", "inconclusive_low_detector_confidence",
    ],
}


@pytest.mark.parametrize("category,tokens", _RULE_CONTENT_PRESERVATION.items())
def test_rule_thresholds_and_enums_carried_forward_into_reader(category, tokens):
    text = _skill_text(category)
    missing = [t for t in tokens if t not in text]
    assert not missing, (
        f"{category}-reader/SKILL.md is missing carried-forward verdict-interpreter "
        f"tokens: {missing}"
    )


@pytest.mark.parametrize("category,tokens", _RULE_CONTENT_PRESERVATION.items())
def test_rule_thresholds_positive_control_against_source_skill(category, tokens):
    """Positive control: confirms these tokens are genuinely present in
    verdict-interpreter/SKILL.md itself. Without this, the test above could pass on a
    fixture that drifted from the real source (e.g. a typo'd threshold both files happen
    to share) without ever proving anything was actually carried FORWARD from somewhere
    real."""
    source_text = _VERDICT_INTERPRETER_PATH.read_text(encoding="utf-8")
    missing = [t for t in tokens if t not in source_text]
    assert not missing, (
        f"verdict-interpreter/SKILL.md itself doesn't contain {missing} -- "
        "this test's own fixture has drifted from the real source file"
    )


# ---------------------------------------------------------------------------
# 5. Routing-authority guard (self-adversarial review's central question: does any reader
#    quietly make a routing decision that belongs to 5b-ii's mechanical synthesis step?)
# ---------------------------------------------------------------------------

_ROUTING_FIELDS = ("hypothesis_verdict", "lineage_routing")


@pytest.mark.parametrize("category", CATEGORIES)
def test_reader_skill_forbidden_section_bans_routing_fields(category):
    text = _skill_text(category)
    forbidden_section = text[text.index("## Forbidden"):]
    missing = [f for f in _ROUTING_FIELDS if f not in forbidden_section]
    assert not missing, (
        f"{category}-reader/SKILL.md's Forbidden section does not explicitly ban {missing}"
    )


@pytest.mark.parametrize("category", CATEGORIES)
def test_reader_skill_output_requirements_never_defines_a_routing_field(category):
    """The Output requirements section (what the reader MUST populate) must never define
    hypothesis_verdict/lineage_routing/status as a field of its own output -- distinct from
    the Forbidden section's explicit ban (which legitimately NAMES these fields in order to
    prohibit them)."""
    text = _skill_text(category)
    start = text.index("## Output requirements")
    end = text.index("## Rules", start) if "## Rules" in text[start:] else start + 3000
    section = text[start:end]
    for bad_key in ("hypothesis_verdict:", "lineage_routing:", "status:"):
        assert bad_key not in section, (
            f"{category}-reader/SKILL.md's Output requirements section defines {bad_key!r} "
            "as an output field -- that authority belongs to 5b-ii's synthesis step"
        )


@pytest.mark.parametrize("category", CATEGORIES)
def test_valid_example_proposal_has_no_routing_fields(category):
    """The schema-valid example fixtures themselves (standing in for a real reader's output)
    must not carry a routing decision either -- proves the schema's own required/properties
    set doesn't quietly make room for one."""
    example = _VALID_EXAMPLES[category]
    for f in _ROUTING_FIELDS:
        assert f not in example
    assert "status" not in example


@pytest.mark.parametrize("category", CATEGORIES)
def test_schema_rejects_a_proposal_that_smuggles_in_routing_fields(category):
    """CODE-REVIEW REGRESSION: the shipped schema had no additionalProperties: false
    anywhere, so an otherwise-valid proposal carrying hypothesis_verdict/lineage_routing/
    status alongside it validated cleanly -- silently defeating the one mechanical
    backstop this slice has for the routing-authority boundary (schemas here are
    documentation-only, never loaded by code, per strategy-research/CLAUDE.md -- this
    JSON Schema plus this test suite IS the enforcement). The prior test above only
    checked the hand-built fixtures never contain these fields; it never exercised
    whether the SCHEMA ITSELF would reject them if a real reader emitted one. This test
    does exactly that: takes a genuinely schema-valid example and adds the forbidden
    fields, and asserts validation now fails."""
    smuggled = copy.deepcopy(_VALID_EXAMPLES[category])
    smuggled["hypothesis_verdict"] = "promote"
    smuggled["lineage_routing"] = "next_stage"
    smuggled["status"] = "approved"
    with pytest.raises(jsonschema.ValidationError):
        _validate(smuggled)


def test_schema_rejects_any_undeclared_top_level_field():
    """Same gap, generalized: additionalProperties: false must reject ANY field the
    schema doesn't declare, not just the three routing fields this slice specifically
    cares about -- otherwise a future field added elsewhere in this project's YAML
    conventions could slip through unnoticed too."""
    smuggled = copy.deepcopy(_VALID_EXAMPLES["profitability"])
    smuggled["totally_undeclared_field"] = "should never validate"
    with pytest.raises(jsonschema.ValidationError):
        _validate(smuggled)


def test_schema_requires_patch_items_to_name_their_field():
    """5b-ii-A REVIEW REGRESSION: patch items were bare {type: object}, so a
    reader could write {component, param, ...} and pass the schema while the
    loader (tools/reader_proposals.py) rejected it. The contract and the
    consumer now agree."""
    bad = copy.deepcopy(_VALID_EXAMPLES["profitability"])
    assert bad["kind"] == "patch"
    bad["patch"] = [{"component": "keltner", "param": "atr_multiplier", "before": 2.0, "after": 2.5}]
    with pytest.raises(jsonschema.ValidationError):
        _validate(bad)


def test_schema_requires_a_non_empty_config_paths_for_new_block():
    new_block = next(e for e in _VALID_EXAMPLES.values() if e["kind"] == "new_block")
    bad = copy.deepcopy(new_block)
    bad["block"]["config_paths"] = []
    with pytest.raises(jsonschema.ValidationError):
        _validate(bad)
