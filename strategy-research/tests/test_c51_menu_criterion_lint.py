"""
C5.1 (delivery_plan_v26_continuation.md, DELIVERY_REVIEW.md finding C4 /
A2_cards_A-G.md finding 5, D-013): registration-time enforcement for a
menu-shaped criterion, closing the gap slice 2 promised and never shipped
("Once slice 2 lands, extend the same lint to the menu's scale_free: true
rule") and the review found nowhere in code:

  1. A criterion identifying itself against `config/criterion_menu.yaml`
     (carries an `id`) must name a LIVE menu entry.
  2. It may only supply fields its menu entry lists under `card_overridable`
     (`_pass_rule_from_card`'s existing 1a-only check, unchanged in effect).
  3. A `scale_free: false` menu entry's `threshold` can never be set to a
     different value than the menu's own -- refused regardless of
     `card_overridable` (defense in depth).
  4. A criterion's `floor` override may only raise the menu's sample floor,
     never lower or drop any of its keys.

`verdict_criteria_evaluator.menu_criterion_overrides_violations` /
`lint_menu_shaped_pass_rule` are the ONE shared implementation behind THREE
call sites: `_pass_rule_from_card` (1a, unchanged raise-on-first-violation
style), and `run_campaign.py`'s `_materialize_run` / `_materialize_refinement_run`
(new -- an operator brief's own hand-written `evaluation.pass_rule` used to
reach pre_registration.yaml with NO menu check at all, DELIVERY_REVIEW.md C4).

`is_menu_referencing_criterion` (id present, no `metric_basis`) is also what
now makes `lint_pass_rule_structure` (CUL-267) and `_lint_pass_rule_total_mapping`'s
(B11) own per-criterion checks skip a menu-shaped criterion instead of
false-positiving on it (D-013: "the legacy B11/CUL-267 lints stay off for
menu-shaped criteria") -- reproduced directly against
`config/criterion_menu.yaml`'s real `sign_consistent_by_era` entry (it has no
`comparator`/`null_handling`, which both legacy lints require unconditionally)
before this fix, in this session.

Flag: NONE, matching CUL-267's own precedent (delivery_plan_v26.md slice 0.1:
"a lint that fires only on newly registered briefs cannot change any existing
artifact") -- this lint only ever REFUSES newly-registered content or leaves
it untouched; it never rewrites an existing pre_registration.yaml. The corpus
test below is this ticket's "flag-off byte-identity" proof: every real
committed run pre-dates the menu schema, so none of their criteria are
`is_menu_referencing_criterion` and the new lint is a universal no-op on them.
"""
from __future__ import annotations

import glob
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

_REAL_MENU_PATH = _SR / "config" / "criterion_menu.yaml"
_REAL_MENU = yaml.safe_load(_REAL_MENU_PATH.read_text(encoding="utf-8"))

# A synthetic menu entry the real menu deliberately never carries yet
# (scale_free: false with threshold listed as card_overridable, so the
# threshold-lock check is proven independent of the allowlist check).
_SYNTH_MENU = {
    "criteria": [
        {
            "id": "fake_nonscale_ratio",
            "metric": "some_metric",
            "source": "pooled",
            "comparator": ">",
            "threshold": 1.0,
            "card_overridable": ["threshold", "floor"],
            "scale_free": False,
            "floor": {"min_windows": 5, "min_trades": 15},
        },
    ],
}


# ---------------------------------------------------------------------------
# 1. is_menu_referencing_criterion: the legacy/menu-shape detector
# ---------------------------------------------------------------------------

def test_legacy_corpus_shaped_criterion_is_not_menu_referencing():
    """run_058-style: `id` used only as a human label, `source` is operator-
    judgment PROSE (not the menu schema's window|pooled|profit_bars enum),
    and `metric_basis` is present -- the real signal that distinguishes it."""
    legacy = {"id": "a", "metric": "median_sharpe", "metric_basis": "bar_level",
              "comparator": ">", "threshold": 0.5, "null_handling": "fails_threshold",
              "source": "Operator judgment (2026-07-15 registration ruling)."}
    assert vce.is_menu_referencing_criterion(legacy) is False


def test_resolved_menu_criterion_is_menu_referencing():
    resolved = vce.resolve_criteria_against_menu(
        [{"id": "sign_consistent_by_era"}], _REAL_MENU)[0]
    assert "metric_basis" not in resolved
    assert vce.is_menu_referencing_criterion(resolved) is True


def test_id_less_self_contained_criterion_is_not_menu_referencing():
    """Documented shape: a fully self-contained criterion with no `id` at all
    -- 'the menu is not consulted for that criterion at all'."""
    self_contained = {"metric": "x", "source": "pooled", "reducer": "median",
                       "comparator": ">", "threshold": 1.0}
    assert vce.is_menu_referencing_criterion(self_contained) is False


# ---------------------------------------------------------------------------
# 2. menu_criterion_overrides_violations / lint_menu_shaped_pass_rule
# ---------------------------------------------------------------------------

def test_clean_menu_reference_with_allowed_override_passes():
    resolved = vce.resolve_criteria_against_menu(
        [{"id": "sign_consistent_by_era", "metric": "forecast_return_corr"}], _REAL_MENU)
    assert vce.lint_menu_shaped_pass_rule({"criteria": resolved}, _REAL_MENU) == []


def test_unauthorized_override_is_refused():
    resolved = vce.resolve_criteria_against_menu(
        [{"id": "sign_consistent_by_era"}], _REAL_MENU)
    bad = dict(resolved[0])
    bad["threshold"] = 999  # not in card_overridable: [metric]
    v = vce.lint_menu_shaped_pass_rule({"criteria": [bad]}, _REAL_MENU)
    assert v and "threshold" in v[0]


def test_restating_the_menus_own_value_is_not_an_override():
    """A criterion may carry every backfilled field verbatim (e.g. copied from
    a 1a-resolved criterion into a new operator brief) without tripping the
    allowlist -- only a DIFFERING value counts as an override."""
    resolved = vce.resolve_criteria_against_menu(
        [{"id": "realized_edge_to_cost_ratio"}], _REAL_MENU)
    assert vce.lint_menu_shaped_pass_rule({"criteria": resolved}, _REAL_MENU) == []


def test_unknown_menu_id_is_refused():
    v = vce.lint_menu_shaped_pass_rule(
        {"criteria": [{"id": "not_a_real_menu_id", "metric": "x", "source": "pooled"}]},
        _REAL_MENU)
    assert v and "not a live entry" in v[0]


def test_scale_free_false_threshold_override_refused():
    crit = {"id": "fake_nonscale_ratio", "threshold": 2.0}
    v = vce.lint_menu_shaped_pass_rule({"criteria": [crit]}, _SYNTH_MENU)
    assert v and any("scale_free: false" in x for x in v)


def test_scale_free_false_threshold_restated_identically_is_allowed():
    crit = {"id": "fake_nonscale_ratio", "threshold": 1.0}  # same as the menu's own
    v = vce.lint_menu_shaped_pass_rule({"criteria": [crit]}, _SYNTH_MENU)
    assert v == []


def test_floor_lowered_is_refused():
    crit = {"id": "fake_nonscale_ratio", "floor": {"min_windows": 2, "min_trades": 15}}
    v = vce.lint_menu_shaped_pass_rule({"criteria": [crit]}, _SYNTH_MENU)
    assert v and any("below the menu's" in x for x in v)


def test_floor_dropping_a_key_is_refused():
    crit = {"id": "fake_nonscale_ratio", "floor": {"min_windows": 5}}  # drops min_trades
    v = vce.lint_menu_shaped_pass_rule({"criteria": [crit]}, _SYNTH_MENU)
    assert v and any("min_trades" in x for x in v)


def test_floor_raised_is_allowed():
    crit = {"id": "fake_nonscale_ratio", "floor": {"min_windows": 10, "min_trades": 20}}
    v = vce.lint_menu_shaped_pass_rule({"criteria": [crit]}, _SYNTH_MENU)
    assert v == []


@pytest.mark.parametrize("pass_rule", [None, "some legacy prose pass rule", {}, {"criteria": []}])
def test_legacy_and_empty_shapes_are_untouched(pass_rule):
    assert vce.lint_menu_shaped_pass_rule(pass_rule, _REAL_MENU) == []


# ---------------------------------------------------------------------------
# 3. B11 / CUL-267 no longer false-positive on a menu-shaped criterion
# ---------------------------------------------------------------------------

def test_cul267_skips_a_menu_shaped_criterion():
    resolved = vce.resolve_criteria_against_menu(
        [{"id": "sign_consistent_by_era"}], _REAL_MENU)  # no comparator/null_handling
    assert vce.lint_pass_rule_structure({"criteria": resolved}) == []


def test_cul267_still_catches_a_genuinely_malformed_legacy_criterion():
    bad_legacy = {"id": "z", "metric_basis": "bar_level", "comparator": "~="}
    v = vce.lint_pass_rule_structure({"criteria": [bad_legacy]})
    assert v  # unaffected: not menu-referencing (carries metric_basis)


def test_b11_skips_a_menu_shaped_criterion():
    resolved = vce.resolve_criteria_against_menu(
        [{"id": "sign_consistent_by_era"}], _REAL_MENU)
    pre_reg = {"pass_rule": {
        "criteria": resolved,
        "outcomes": [
            {"branch": "PASS", "hypothesis_verdict": "promote", "lineage_routing": None},
            {"branch": "FAIL-sign_consistent_by_era", "hypothesis_verdict": "kill",
             "lineage_routing": "terminate"},
        ],
    }}
    violations, _warnings = rpr._lint_pass_rule_total_mapping(pre_reg)
    assert violations == []


def test_b11_still_catches_a_genuinely_malformed_legacy_criterion():
    pre_reg = {"pass_rule": {
        "criteria": [{"id": "z", "metric_basis": "bar_level"}],  # missing metric/comparator
        "outcomes": [
            {"branch": "PASS", "hypothesis_verdict": "promote", "lineage_routing": None},
            {"branch": "FAIL-z", "hypothesis_verdict": "kill", "lineage_routing": "terminate"},
        ],
    }}
    violations, _warnings = rpr._lint_pass_rule_total_mapping(pre_reg)
    assert violations  # unaffected: not menu-referencing


# ---------------------------------------------------------------------------
# 4. Real-corpus check (this ticket's flag-off byte-identity proof)
# ---------------------------------------------------------------------------

def test_corpus_no_real_run_is_newly_refused():
    """Every real runs/run_*/artifacts/pre_registration.yaml pre-dates the
    menu schema -- none of their criteria are is_menu_referencing_criterion,
    so the new C5.1 lint must be a universal no-op on the whole corpus. Reads
    the real repo directly (module-level Path, not camp.ROOT/rpr.ROOT), same
    convention as test_cul267_criterion_lint.py's own corpus test -- no
    real_repo_readonly marker needed (nothing here touches the sandboxed
    globals)."""
    files = sorted((_SR / "runs").glob("run_*/artifacts/pre_registration.yaml"))
    assert files, "expected at least one real pre_registration.yaml in the corpus"

    checked = 0
    for path in files:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        pass_rule = data.get("pass_rule")
        if not isinstance(pass_rule, dict):
            continue
        checked += 1
        violations = vce.lint_menu_shaped_pass_rule(pass_rule, _REAL_MENU)
        assert violations == [], f"{path} newly refused by the C5.1 menu lint: {violations}"

    assert checked >= 1


# ---------------------------------------------------------------------------
# 5. Wired end to end: an operator brief's OWN pass_rule is now checked
#    (DELIVERY_REVIEW.md C4: "operator briefs keep their own pass rule with
#    no menu check" -- confirmed by reading _materialize_run/
#    _materialize_refinement_run before this fix: neither called any menu
#    check at all, only B11's total-mapping lint and CUL-267's structural one).
# ---------------------------------------------------------------------------

def _seed_real_menu(sandbox: Path):
    (sandbox / "config").mkdir(parents=True, exist_ok=True)
    (sandbox / "config" / "criterion_menu.yaml").write_text(
        _REAL_MENU_PATH.read_text(encoding="utf-8"), encoding="utf-8")


def _fresh_launch_brief(pass_rule):
    return {
        "brief_id": "OPERATOR_BRIEF_TEST",
        "venue": None,
        "product": None,
        "machine_constraints": {
            "significance_methodology": "block_bootstrap_all_bars_v1",  # non-empty, no protocol pinned
        },
        "evaluation": {"pass_rule": pass_rule},
    }


def test_operator_brief_fresh_launch_illegal_override_is_refused(_sandbox_by_default):
    _seed_real_menu(_sandbox_by_default)
    resolved = vce.resolve_criteria_against_menu(
        [{"id": "sign_consistent_by_era"}], _REAL_MENU)
    resolved[0]["threshold"] = 123  # unauthorized: not in card_overridable
    pass_rule = {
        "criteria": resolved,
        "outcomes": [
            {"branch": "PASS", "hypothesis_verdict": "promote", "lineage_routing": None},
            {"branch": "FAIL-sign_consistent_by_era", "hypothesis_verdict": "kill",
             "lineage_routing": "terminate"},
        ],
    }
    with pytest.raises(ValueError, match="C5.1 menu lint"):
        camp._materialize_run("run_test_001", _fresh_launch_brief(pass_rule))


def test_operator_brief_fresh_launch_clean_menu_pass_rule_registers(_sandbox_by_default):
    _seed_real_menu(_sandbox_by_default)
    resolved = vce.resolve_criteria_against_menu(
        [{"id": "sign_consistent_by_era", "metric": "forecast_return_corr"}], _REAL_MENU)
    pass_rule = {
        "criteria": resolved,
        "outcomes": [
            {"branch": "PASS", "hypothesis_verdict": "promote", "lineage_routing": None},
            {"branch": "FAIL-sign_consistent_by_era", "hypothesis_verdict": "kill",
             "lineage_routing": "terminate"},
        ],
    }
    run_id = "run_test_002"
    camp._materialize_run(run_id, _fresh_launch_brief(pass_rule))
    written = yaml.safe_load(
        (camp.ROOT / "runs" / run_id / "artifacts" / "pre_registration.yaml")
        .read_text(encoding="utf-8"))
    assert written["pass_rule"]["criteria"][0]["metric"] == "forecast_return_corr"


def test_operator_brief_refinement_illegal_floor_is_refused(_sandbox_by_default, tmp_path):
    _seed_real_menu(_sandbox_by_default)
    resolved = vce.resolve_criteria_against_menu(
        [{"id": "sign_consistent_by_era"}], _REAL_MENU)
    resolved[0]["floor"] = {"min_windows": 1, "min_trades": 1}  # lowered below the menu's
    brief = {
        "brief_id": "OPERATOR_REFINEMENT_TEST",
        "evaluation": {"pass_rule": {
            "criteria": resolved,
            "outcomes": [
                {"branch": "PASS", "hypothesis_verdict": "promote", "lineage_routing": None},
                {"branch": "FAIL-sign_consistent_by_era", "hypothesis_verdict": "kill",
                 "lineage_routing": "terminate"},
            ],
        }},
    }
    brief_path = tmp_path / "refinement_brief.yaml"
    brief_path.write_text(yaml.safe_dump(brief), encoding="utf-8")
    with pytest.raises(ValueError, match="C5.1 menu lint"):
        camp._materialize_refinement_run("run_test_003", brief, brief_path)


def test_operator_brief_menu_check_not_bypassed_when_only_legacy_lints_would_pass(_sandbox_by_default):
    """The exact DELIVERY_REVIEW.md C4 scenario: a brief names a real menu id
    but overrides a field the menu forbids AND, being menu-shaped, would have
    slipped past B11/CUL-267 entirely (no metric_basis/comparator required for
    sign_consistent_by_era) -- only the new C5.1 lint catches it."""
    _seed_real_menu(_sandbox_by_default)
    resolved = vce.resolve_criteria_against_menu(
        [{"id": "sign_consistent_by_era"}], _REAL_MENU)
    resolved[0]["symbol_reducer"] = "pooled"  # not in card_overridable: [metric]
    pass_rule = {"criteria": resolved, "outcomes": [
        {"branch": "PASS", "hypothesis_verdict": "promote", "lineage_routing": None},
        {"branch": "FAIL-sign_consistent_by_era", "hypothesis_verdict": "kill",
         "lineage_routing": "terminate"},
    ]}
    # Confirm the premise: B11 and CUL-267 alone see nothing wrong here.
    assert vce.lint_pass_rule_structure(pass_rule) == []
    b11_violations, _ = rpr._lint_pass_rule_total_mapping({"pass_rule": pass_rule})
    assert b11_violations == []
    # The new lint is the one that catches it.
    with pytest.raises(ValueError, match="C5.1 menu lint"):
        camp._materialize_run("run_test_004", _fresh_launch_brief(pass_rule))
