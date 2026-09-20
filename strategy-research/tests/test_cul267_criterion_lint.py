"""
CUL-267: registration-time structural lint over a pass_rule's `criteria`.

Before this ticket, `verdict_criteria_evaluator.py::_evaluate_one_criterion`
returned SPEC_ERROR at EVALUATION time -- after a real backtest already
ran -- when a criterion's `metric` was missing/empty, its `comparator`
wasn't in `_VALID_COMPARATORS`, or (for a non-per-symbol criterion)
`null_handling` wasn't `"fails_threshold"`. `lint_pass_rule_structure`
(same module) moves the structural half of that check to registration
time, wired into `run_campaign.py`'s `_materialize_run` /
`_materialize_refinement_run` right next to the existing B11
total-mapping lint.

These tests exercise `lint_pass_rule_structure` directly rather than via
`_materialize_run`/`_materialize_refinement_run` -- those two call sites
are mechanical wiring (same raise-on-violation pattern as the adjacent B11
lint) and are covered by the corpus-compatibility test below, which is the
behavior that actually matters: the lint must not reject anything that
registered cleanly under the old rules.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

import yaml  # noqa: E402

import verdict_criteria_evaluator as vce  # noqa: E402

_SR_ROOT = Path(__file__).parent.parent


def _valid_criterion(**overrides) -> dict:
    """A single structurally-clean, non-per-symbol criterion."""
    base = {
        "id": "a",
        "metric": "median_sharpe",
        "metric_basis": "bar_level",
        "comparator": ">=",
        "threshold": 0.5,
        "null_handling": "fails_threshold",
    }
    base.update(overrides)
    return base


def _valid_pass_rule(criteria: list) -> dict:
    return {
        "statement": "test fixture",
        "criteria": criteria,
        "outcomes": [
            {"branch": "PASS", "hypothesis_verdict": "promote", "lineage_routing": None},
            {"branch": "FAIL-a", "hypothesis_verdict": "kill", "lineage_routing": "terminate"},
        ],
    }


def test_unmatchable_empty_metric_refused():
    """A criterion with an empty/absent `metric` can never resolve via
    _lookup_metric_value regardless of data -- refused at registration."""
    pass_rule = _valid_pass_rule([_valid_criterion(metric="")])
    violations = vce.lint_pass_rule_structure(pass_rule)
    assert violations, "empty metric should be refused"
    assert any("metric" in v for v in violations)

    pass_rule_missing = _valid_pass_rule([{k: v for k, v in _valid_criterion().items()
                                            if k != "metric"}])
    violations_missing = vce.lint_pass_rule_structure(pass_rule_missing)
    assert violations_missing, "absent metric should be refused"
    assert any("metric" in v for v in violations_missing)


def test_bad_comparator_refused():
    """A comparator outside _VALID_COMPARATORS is a guaranteed SPEC_ERROR at
    evaluation time -- refused at registration instead."""
    pass_rule = _valid_pass_rule([_valid_criterion(comparator="~=")])
    violations = vce.lint_pass_rule_structure(pass_rule)
    assert violations, "invalid comparator should be refused"
    assert any("comparator" in v for v in violations)


def test_missing_null_handling_refused_when_not_per_symbol():
    """A non-per-symbol criterion with no (or wrong) null_handling hits
    _evaluate_one_criterion's SPEC_ERROR path the instant the metric
    resolves null -- refused at registration."""
    pass_rule = _valid_pass_rule([{k: v for k, v in _valid_criterion().items()
                                    if k != "null_handling"}])
    violations = vce.lint_pass_rule_structure(pass_rule)
    assert violations, "missing null_handling should be refused"
    assert any("null_handling" in v for v in violations)

    pass_rule_wrong = _valid_pass_rule([_valid_criterion(null_handling="ignore")])
    violations_wrong = vce.lint_pass_rule_structure(pass_rule_wrong)
    assert violations_wrong, "null_handling not equal to fails_threshold should be refused"
    assert any("null_handling" in v for v in violations_wrong)


def test_per_symbol_threshold_criterion_exempt_from_null_handling_check():
    """A per_symbol_threshold criterion is exempted from this lint's
    null_handling check (data-dependent per symbol; the existing B11
    total-mapping lint already requires null_handling be PRESENT for this
    shape) -- a clean per-symbol criterion with null_handling set should not
    be flagged."""
    criterion = _valid_criterion(per_symbol_threshold={"BTCUSDT": 0.8, "ETHUSDT": 0.8})
    del criterion["threshold"]
    pass_rule = _valid_pass_rule([criterion])
    violations = vce.lint_pass_rule_structure(pass_rule)
    assert violations == []


def test_legacy_shapes_not_linted():
    """A None or plain-string pass_rule is the pre-K2 legacy schema and must
    not be linted here -- same tolerance as _lint_pass_rule_total_mapping."""
    assert vce.lint_pass_rule_structure(None) == []
    assert vce.lint_pass_rule_structure("some legacy prose pass rule") == []


def test_clean_pass_rule_yields_no_violations():
    pass_rule = _valid_pass_rule([_valid_criterion()])
    assert vce.lint_pass_rule_structure(pass_rule) == []


def test_corpus_every_real_dict_shaped_pass_rule_registers_cleanly():
    """Every real runs/run_*/artifacts/pre_registration.yaml with a
    dict-shaped pass_rule was registered under the OLD rules (no structural
    lint) and must still register cleanly under the new one -- this lint
    only ADDS a refusal for a criterion that would previously have silently
    gone to SPEC_ERROR later; it must not change behavior for anything that
    already validated."""
    files = sorted((_SR_ROOT / "runs").glob("run_*/artifacts/pre_registration.yaml"))
    assert files, "expected at least one real pre_registration.yaml in the corpus"

    checked_dict_shaped = 0
    for path in files:
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        pass_rule = data.get("pass_rule")
        if not isinstance(pass_rule, dict):
            continue  # legacy (string) or absent -- not this lint's concern
        checked_dict_shaped += 1
        violations = vce.lint_pass_rule_structure(pass_rule)
        assert violations == [], (
            f"{path} regressed against the new CUL-267 structural lint "
            f"(registered cleanly under the old rules): {violations}"
        )

    # As of this ticket's authoring, three real runs (run_058/059/060) carry
    # a dict-shaped pass_rule. Asserting >= 1 rather than a hardcoded count
    # so a future added run doesn't spuriously fail this test.
    assert checked_dict_shaped >= 1
