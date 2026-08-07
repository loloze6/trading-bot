"""
C7-EXT gate tests (2026-07-22) — the ungated-verdict defect chain.

Origin: XS_momentum was issued a "C7-style verdict REFINE" having never been
pre-registered under any pass_rule, off the orchestrator, with funding
unmodeled on a perp, no distribution stats, no deployable-today figure, and an
unexplained anomalous lag response. Nothing in the machinery objected.

One test per gate (G1-G7), plus a regression that walks the actual
XS_momentum shape end-to-end and asserts it can no longer produce a verdict.

The XS_momentum figures used below are quoted from
campaign_knowledge_base.yaml's xs_momentum_cost_surviving_but_decaying entry.
Nothing here re-runs or mutates panel_backtester.py's results or any archived
run artifact — the fixtures are constructed dicts in the shape those artifacts
take.
"""
import sys
from pathlib import Path

import pytest

_SR_ROOT = Path(__file__).parent.parent
TOOLS_PATH = _SR_ROOT / "tools"
WORKFLOW_PATH = _SR_ROOT / "workflow"
sys.path.insert(0, str(TOOLS_PATH))
sys.path.insert(0, str(WORKFLOW_PATH))

import verdict_criteria_evaluator as vce  # noqa: E402


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

def _complete_protocol_result(**overrides) -> dict:
    """A protocol_result.yaml that satisfies all four preconditions, so each
    gate test can knock out exactly one thing and attribute the block."""
    base = {
        "hypothesis_verdict": {"diagnostics": {
            "median_sharpe": 1.1,
            "skew": -0.4,
            "kurtosis": 6.2,
            "worst_period_return_pct": -12.0,
            "median_holding_hours": 4.0,
        }},
        "deployable_today": {
            "year": 2025, "net_sharpe": 0.07,
            "net_return_pct": -6.3, "cost_basis": "kraken_perp_2026_taker_5bps",
        },
        "robustness_checks": [
            {"id": "exec_lag", "anomalous": False},
        ],
    }
    base.update(overrides)
    return base


def _structured_pre_registration() -> dict:
    return {
        "pass_rule": {
            "statement": "PASS iff median_sharpe >= 0.5",
            "criteria": [{
                "id": "a", "metric": "median_sharpe", "comparator": ">=",
                "threshold": 0.5, "null_handling": "fails_threshold",
            }],
            "outcomes": [
                {"branch": "PASS", "hypothesis_verdict": "promote",
                 "lineage_routing": "terminate"},
                {"branch": "FAIL-a", "hypothesis_verdict": "kill",
                 "lineage_routing": "terminate"},
            ],
        }
    }


def _xs_momentum_brief() -> dict:
    """XS_momentum's real shape: Kraken perp, 1h bars, daily rebalance."""
    return {"product": "perp", "venue": "kraken", "timeframe": "1h",
            "rebalance_hours": 24}


def _blocked_ids(result: dict) -> list:
    return result.get("blocked_by", [])


# --------------------------------------------------------------------------
# G1 — cost-model completeness
# --------------------------------------------------------------------------

def _perp_held_past_funding() -> dict:
    """A perp run whose positions genuinely outlive the 8h funding interval —
    the default fixture holds 4h and so legitimately clears G1."""
    pr = _complete_protocol_result()
    pr["hypothesis_verdict"]["diagnostics"]["median_holding_hours"] = 24.0
    return pr


def test_g1_perp_holding_beyond_funding_interval_blocks_when_funding_unmodeled():
    """XS_momentum's link (a): daily rebalance on a perp = ~3 funding accruals
    per holding period, funding never modeled, verdict issued anyway."""
    result = vce.evaluate_pass_rule_criteria(
        _perp_held_past_funding(), _structured_pre_registration(), _xs_momentum_brief())

    assert result["result"] == "VERDICT_BLOCKED"
    assert "cost_model_completeness" in _blocked_ids(result)
    assert "neither modeled nor explicitly bounded" in result["reason"]


def test_g1_met_when_funding_bounded_with_citation():
    pre_reg = _structured_pre_registration()
    pre_reg["cost_model_completeness"] = {"funding": {
        "treatment": "bounded",
        "bound_bps_per_interval": 1.0,
        "citation": "docs/analysis-reports/venue_survey_20260719.md 2026-07-20 supplement",
    }}
    result = vce.evaluate_pass_rule_criteria(
        _perp_held_past_funding(), pre_reg, _xs_momentum_brief())
    assert result["result"] != "VERDICT_BLOCKED"


def test_g1_uncited_bound_is_not_a_bound():
    pre_reg = _structured_pre_registration()
    pre_reg["cost_model_completeness"] = {"funding": {
        "treatment": "bounded", "bound_bps_per_interval": 1.0, "citation": None,
    }}
    result = vce.evaluate_pass_rule_criteria(
        _perp_held_past_funding(), pre_reg, _xs_momentum_brief())
    assert result["result"] == "VERDICT_BLOCKED"
    assert "cost_model_completeness" in _blocked_ids(result)


def test_g1_perp_closing_inside_funding_interval_is_met():
    """Not every perp owes a funding model — only one that holds through an
    accrual. The 4h default fixture is exactly that case."""
    result = vce.evaluate_pass_rule_criteria(
        _complete_protocol_result(), _structured_pre_registration(),
        {"product": "perp", "timeframe": "1h"})
    assert "cost_model_completeness" not in _blocked_ids(result)


def test_g1_unmeasured_holding_period_blocks_rather_than_assuming_short():
    """An unmeasured holding period cannot demonstrate it sits inside the
    funding interval — silence is not evidence of brevity."""
    pr = _complete_protocol_result()
    pr["hypothesis_verdict"]["diagnostics"].pop("median_holding_hours")
    brief = {"product": "perp", "venue": "kraken", "timeframe": "1h"}
    result = vce.evaluate_pass_rule_criteria(pr, _structured_pre_registration(), brief)
    assert result["result"] == "VERDICT_BLOCKED"
    assert "cost_model_completeness" in _blocked_ids(result)


def test_g1_spot_product_needs_no_funding_treatment():
    result = vce.evaluate_pass_rule_criteria(
        _complete_protocol_result(), _structured_pre_registration(),
        {"product": "spot", "timeframe": "1h", "rebalance_hours": 24})
    assert result["result"] != "VERDICT_BLOCKED"


# --------------------------------------------------------------------------
# G2 — distribution stats mandatory alongside Sharpe
# --------------------------------------------------------------------------

@pytest.mark.parametrize("dropped", ["skew", "kurtosis", "worst_period_return_pct"])
def test_g2_sharpe_without_distribution_stats_blocks(dropped):
    pr = _complete_protocol_result()
    pr["hypothesis_verdict"]["diagnostics"].pop(dropped)
    result = vce.evaluate_pass_rule_criteria(
        pr, _structured_pre_registration(), {"product": "spot"})
    assert result["result"] == "VERDICT_BLOCKED"
    assert "distribution_stats" in _blocked_ids(result)


def test_g2_no_sharpe_means_no_requirement():
    """The gate attaches to the Sharpe, not to every run."""
    pr = {"hypothesis_verdict": {"diagnostics": {"win_rate": 0.51}},
          "deployable_today": {"year": 2025, "net_sharpe": 0.07, "cost_basis": "x"},
          "robustness_checks": []}
    result = vce.evaluate_pass_rule_criteria(
        pr, _structured_pre_registration(), {"product": "spot"})
    assert "distribution_stats" not in _blocked_ids(result)


# --------------------------------------------------------------------------
# G3 — deployable-today mandatory
# --------------------------------------------------------------------------

def test_g3_missing_deployable_today_blocks():
    """XS_momentum's link (c): headline 1.325 (2017/2020-dominated) carried the
    verdict; the most recent full year was 0.07 and never surfaced."""
    pr = _complete_protocol_result()
    pr.pop("deployable_today")
    result = vce.evaluate_pass_rule_criteria(
        pr, _structured_pre_registration(), {"product": "spot"})
    assert result["result"] == "VERDICT_BLOCKED"
    assert "deployable_today" in _blocked_ids(result)


def test_g3_partial_deployable_today_blocks():
    pr = _complete_protocol_result(
        deployable_today={"year": 2025, "net_sharpe": 0.07})  # no cost_basis
    result = vce.evaluate_pass_rule_criteria(
        pr, _structured_pre_registration(), {"product": "spot"})
    assert result["result"] == "VERDICT_BLOCKED"
    assert "deployable_today" in _blocked_ids(result)


# --------------------------------------------------------------------------
# G4 — anomalous robustness result needs a written mechanism
# --------------------------------------------------------------------------

def test_g4_unexplained_anomaly_blocks():
    """XS_momentum's link (d): net Sharpe RISING with execution lag
    (1.33/1.42/1.51) was recorded as reassurance, never explained."""
    pr = _complete_protocol_result(robustness_checks=[
        {"id": "exec_lag", "anomalous": True, "detail": "sharpe rises 1.33->1.42->1.51"},
    ])
    result = vce.evaluate_pass_rule_criteria(
        pr, _structured_pre_registration(), {"product": "spot"})
    assert result["result"] == "VERDICT_BLOCKED"
    assert "robustness_mechanism" in _blocked_ids(result)
    assert "exec_lag" in result["reason"]


def test_g4_written_mechanism_clears_the_gate():
    pr = _complete_protocol_result(robustness_checks=[
        {"id": "exec_lag", "anomalous": True,
         "mechanism_explanation": "7d-momentum ranks are stale relative to a 1h bar; "
                                  "delaying execution skips the first-bar reversal."},
    ])
    result = vce.evaluate_pass_rule_criteria(
        pr, _structured_pre_registration(), {"product": "spot"})
    assert result["result"] != "VERDICT_BLOCKED"


def test_g4_accepts_mapping_shaped_robustness_block():
    pr = _complete_protocol_result(robustness_checks={
        "exec_lag": {"anomalous": True},
    })
    result = vce.evaluate_pass_rule_criteria(
        pr, _structured_pre_registration(), {"product": "spot"})
    assert "robustness_mechanism" in _blocked_ids(result)


# --------------------------------------------------------------------------
# G5 — preconditions are pass_rule-independent and dominate
# --------------------------------------------------------------------------

def test_g5_preconditions_block_even_with_no_pass_rule_at_all():
    """The hole that let XS_momentum through: with no pass_rule, K2 returned
    `legacy_not_evaluable`, which hands the run to stage discretion — and
    stage discretion has never heard of these four checks."""
    pr = _complete_protocol_result()
    pr.pop("deployable_today")
    result = vce.evaluate_pass_rule_criteria(pr, {}, {"product": "spot"})

    assert result["result"] == "VERDICT_BLOCKED"
    assert result["result"] != "legacy_not_evaluable"
    assert "deployable_today" in _blocked_ids(result)


def test_g5_preconditions_block_a_rule_that_would_otherwise_pass():
    """Domination: a cleanly-PASSing pass_rule does not rescue a blocked run."""
    pr = _complete_protocol_result()
    pr.pop("deployable_today")
    result = vce.evaluate_pass_rule_criteria(
        pr, _structured_pre_registration(), {"product": "spot"})
    assert result["result"] == "VERDICT_BLOCKED"
    assert result.get("hypothesis_verdict") is None
    assert result.get("lineage_routing") is None


def test_g5_met_preconditions_are_stamped_onto_a_passing_result():
    """A later reader must be able to see the gates were checked, not assume it."""
    result = vce.evaluate_pass_rule_criteria(
        _complete_protocol_result(), _structured_pre_registration(), {"product": "spot"})
    assert result["result"] == "PASS"
    assert [g["id"] for g in result["preconditions"]] == list(vce.VERDICT_PRECONDITION_IDS)
    assert all(g["result"] == "MET" for g in result["preconditions"])


def test_g5_k2_legacy_behaviour_survives_when_preconditions_are_met():
    """C7-EXT must not break R3: a legacy string pass_rule with clean
    preconditions still routes to stage judgment, exactly as before."""
    result = vce.evaluate_pass_rule_criteria(
        _complete_protocol_result(),
        {"pass_rule": "prose rule from a pre-K2 brief"},
        {"product": "spot"})
    assert result["result"] == "legacy_not_evaluable"


# --------------------------------------------------------------------------
# G6 — no verdict enters the KB/queue without evaluator provenance
# --------------------------------------------------------------------------

def test_g6_verdict_without_provenance_is_rejected():
    """The link that let a research-path tool write `verdict_c7: refine`.

    Two refusals now, for two different reasons, and both matter:
      - the ORIGINAL XS_momentum shape (`verdict_c7`) is refused by the closed
        schema as an unknown field -- C7-EXT-R2 removed that legacy name rather
        than keeping it on a list, and the record type no longer admits it;
      - the same claim written in the DESIGNATED field is refused for the reason
        this test was originally about: no provenance.
    """
    legacy = {"id": "xs_momentum_cost_surviving_but_decaying", "verdict_c7": "refine"}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(legacy, entry_ref="KB finding 'xs'")
    assert "unknown field" in str(exc.value)

    designated = {"id": "xs_momentum_cost_surviving_but_decaying",
                  "outcome": "refine_research_path_edge_real",
                  "evidence_runs": ["research_path_panel_backtester"]}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(designated, entry_ref="KB finding 'xs'",
                                        root=_SR_ROOT)
    assert "structurally ungated" in str(exc.value)


def test_g6_verdict_with_provenance_is_admissible():
    """C7-EXT-R/D-4: this fixture used to cite
    runs/run_058/artifacts/pass_rule_evaluation.yaml -- a file that DOES NOT
    EXIST. It passed anyway, which is precisely the bypass the audit found: the
    ref was never resolved, so any truthy string conferred provenance. It now
    cites run_059's real evaluation, the only one in the campaign."""
    entry = {"id": "funding_mr_daily_retest_killed",
             "hypothesis_id": "FUNDING_MR_DAILY_RETEST",
             "evidence_runs": ["run_059"],
             "outcome": "completed_rejected",
             "pass_rule_evaluation_ref": "runs/run_059/artifacts/pass_rule_evaluation.yaml"}
    assert vce.validate_verdict_provenance(entry, root=_SR_ROOT) is entry


def test_g6_ungated_entry_may_keep_measurements_but_not_a_verdict():
    """A measurement is not a verdict — the entry keeps its numbers."""
    entry = {
        "id": "xs_momentum_cost_surviving_but_decaying",
        "verdict_status": "ungated",
        "signal_property": {"net_sharpe_full_sample": 1.325},
    }
    assert vce.validate_verdict_provenance(entry) is entry

    # C7-EXT-R2: the legacy `verdict_c7` route into this entry no longer exists
    # at all -- the closed schema refuses the field before any contradiction
    # check is reached. Refused earlier and more absolutely than before.
    entry["verdict_c7"] = "refine"
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry)
    assert "unknown field" in str(exc.value)


def test_g6_live_kb_has_no_ungated_verdict_fields():
    """Guards the corrected record itself: every finding in the real KB must
    be admissible under G6."""
    import yaml
    kb_path = Path(__file__).parent.parent / "campaign_record" / "campaign_knowledge_base.yaml"
    kb = yaml.safe_load(kb_path.read_text(encoding="utf-8")) or {}
    for entry in kb.get("findings", []):
        if isinstance(entry, dict):
            vce.validate_verdict_provenance(
                entry, entry_ref=f"KB finding {entry.get('id')!r}")


# --------------------------------------------------------------------------
# G7 — the generic promotion fallback must fail loudly
# --------------------------------------------------------------------------

def test_g7_missing_promotion_block_raises_instead_of_defaulting():
    """The direct C7 recurrence: a brief with no pre-registered thresholds
    used to silently acquire median_sharpe_gt=0 / max_abs_drawdown_pct_lt=30 /
    min_trade_count_gte=20 — and that 30% DD bar is the very number
    XS_momentum's post-hoc verdict was argued against."""
    import run_phase1_research as rpr

    with pytest.raises(rpr.UngatedProtocolError) as exc:
        rpr._require_pre_registered_promotion(
            {"symbols": ["BTCUSDT"], "start": "2018-01-01", "end": "2025-12-31"},
            "run_099")
    msg = str(exc.value)
    assert "structurally ungated" in msg
    assert "Refusing to substitute generic thresholds" in msg


def test_g7_pre_registered_promotion_is_returned_verbatim():
    import run_phase1_research as rpr

    promotion = {"median_sharpe_gt": 0.5, "max_abs_drawdown_pct_lt": 25}
    assert rpr._require_pre_registered_promotion(
        {"promotion": promotion}, "run_099") is promotion


def test_g7_protocol_materialization_routes_through_the_guard():
    """Belt-and-braces: the materializer must call the guard, not read
    `promotion` directly. (The old fallback dict still appears once in the
    tree — quoted inside _require_pre_registered_promotion's own docstring as
    the record of what was removed — so a bare source-scan for the literal is
    not a valid check here.)"""
    src = (WORKFLOW_PATH / "run_phase1_research.py").read_text(encoding="utf-8")
    assert '"promotion": _require_pre_registered_promotion(proto_constraint, run_id)' in src
    # The removed default must survive only as documentation, never as code.
    assert src.count('proto_constraint.get("promotion", {') == 1
    docstring_start = src.index("def _require_pre_registered_promotion")
    docstring_end = src.index("promotion = proto_constraint.get(\"promotion\")")
    assert docstring_start < src.index('proto_constraint.get("promotion", {') < docstring_end


# --------------------------------------------------------------------------
# REGRESSION — the XS_momentum path, end to end
# --------------------------------------------------------------------------

def test_xs_momentum_path_can_no_longer_produce_a_verdict():
    """Reproduces the run as it was actually produced: Kraken perp, 1h bars,
    daily rebalance, no pass_rule, funding unmodeled, no distribution stats,
    no deployable-today figure, anomalous lag response left unexplained.

    Before C7-EXT this returned `legacy_not_evaluable` and a human wrote
    "REFINE" on top of it. It must now be structurally unable to yield any
    verdict, and must trip all four preconditions rather than just the first.
    """
    as_produced = {
        "hypothesis_verdict": {"diagnostics": {
            "median_sharpe": 1.325,        # net, full sample
            "gross_sharpe": 1.665,
            # no skew, no kurtosis, no tail statistic
        }},
        # no deployable_today block
        "robustness_checks": [
            {"id": "exec_lag_1_2_4_bars", "anomalous": True,
             "detail": "net Sharpe RISES 1.33 -> 1.42 -> 1.51 with execution delay"},
        ],
    }
    result = vce.evaluate_pass_rule_criteria(
        as_produced,
        {},                       # no pre_registration.yaml ever existed
        _xs_momentum_brief())

    assert result["result"] == "VERDICT_BLOCKED"
    assert result.get("hypothesis_verdict") is None
    assert result.get("lineage_routing") is None
    assert set(_blocked_ids(result)) == set(vce.VERDICT_PRECONDITION_IDS)


def test_xs_momentum_kb_entry_is_labelled_ungated_not_refine():
    """The corrected record: measurements retained, verdict withdrawn."""
    import yaml
    kb_path = Path(__file__).parent.parent / "campaign_record" / "campaign_knowledge_base.yaml"
    kb = yaml.safe_load(kb_path.read_text(encoding="utf-8")) or {}
    entry = next(e for e in kb["findings"]
                 if e.get("id") == "xs_momentum_cost_surviving_but_decaying")

    assert "verdict_c7" not in entry
    assert entry["verdict_status"] == "ungated"
    # The measurement is real information and must survive the correction.
    assert entry["signal_property"]["net_sharpe_full_sample"] == 1.325
    assert entry["validation_gate"] == "PASS"


def test_campaign_honest_verdict_count():
    """C7-EXT-R/D-5. The count is ONE, and it is now asserted from EVIDENCE.

    The superseded version of this test counted queue entries whose `outcome`
    string equalled "completed_rejected" and concluded TWO. That tests nothing
    about gatedness -- it is a string match on a label anyone can type.
    H-041-C-v2 was counted by it despite having been rejected by an LLM
    validation stage before its pass_rule ever ran; runs/run_058/artifacts/
    contains no pass_rule_evaluation.yaml at all, and the KB entry's own
    exhausted_basis says the registered evaluation "was NEVER EXECUTED".

    A verdict is gated iff the evaluator ran and resolved it. That is an
    artifact on disk, so that is what this asserts.
    """
    import yaml
    kb = yaml.safe_load(
        (_SR_ROOT / "campaign_record" / "campaign_knowledge_base.yaml").read_text(encoding="utf-8")) or {}
    queue = yaml.safe_load(
        (_SR_ROOT / "config" / "campaign_queue.yaml").read_text(encoding="utf-8")) or {}

    gated = vce.honest_verdict_count(kb, queue, root=_SR_ROOT)
    assert gated == ["FUNDING_MR_DAILY_RETEST"], \
        f"gated-verdict set changed: {gated} -- something acquired or lost a " \
        f"verdict and it must be explained, not adjusted"

    # And the artifact that makes it the one: it exists, and it RESOLVED.
    evaluation = _SR_ROOT / "runs" / "run_059" / "artifacts" / "pass_rule_evaluation.yaml"
    assert evaluation.exists()
    assert (yaml.safe_load(evaluation.read_text(encoding="utf-8")) or {})["result"] == "FAIL"

    # H-041-C-v2 is NOT among them, and the reason is checkable rather than asserted.
    assert not (_SR_ROOT / "runs" / "run_058" / "artifacts"
                / "pass_rule_evaluation.yaml").exists()

    outcomes = {e["id"]: (e.get("outcome") or "") for e in queue.get("queue", [])}
    # Relabelled 2026-07-23 (commit 6b27d56) through the G6 closed-schema
    # validator: `ungated_measurement_no_admissible_verdict` ->
    # `ungated_decayed_measurement_no_admissible_verdict`, so the outcome string
    # itself carries the edge-decay fact. The relabel is a naming change with no
    # verdict-count effect -- this entry was never gated -- which is why the
    # assertion below moves and the gated set above does not.
    assert outcomes["XS_momentum"] == "ungated_decayed_measurement_no_admissible_verdict"
    assert "refine" not in outcomes["XS_momentum"]


# --------------------------------------------------------------------------
# C7-EXT-R (2026-07-22) — remediation of the independent audit.
#
# Each test below is named for the audit finding it closes and re-runs the
# audit's OWN bypass input. See engineering/sessions/session_reports/20260722_c7ext_audit.md.
# --------------------------------------------------------------------------

def test_d4_bypass_a_outcome_field_kill_is_now_refused():
    """Audit bypass A, verbatim. `outcome` is the field the KB, the queue and
    _write_kb_findings_entry all actually use; it was not gated, so a
    hand-written kill with nothing behind it was ACCEPTED."""
    entry = {"id": "x", "outcome": "kill_mechanism_falsified",
             "evidence_runs": ["run_999"]}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, root=_SR_ROOT)
    assert "verdict-bearing `outcome: kill_mechanism_falsified`" in str(exc.value)


def test_d4_bypass_b_forged_ref_is_now_refused():
    """Audit bypass B. The ref was never resolved, so any truthy string was
    provenance.

    Written through the DESIGNATED field: the original fixture used
    `verdict_c7`, which C7-EXT-R2's closed schema now refuses as an unknown
    field before ref resolution is ever reached -- so that shape would no longer
    exercise the ref check this test exists to pin."""
    entry = {"id": "y", "outcome": "promote_to_holdout",
             "evidence_runs": ["run_059"],
             "pass_rule_evaluation_ref": "does/not/exist.yaml"}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, root=_SR_ROOT)
    assert "does not exist" in str(exc.value)


def test_d4_bypass_c_a_renamed_verdict_field_is_now_refused():
    """Audit bypass C, verbatim. Under C7-EXT-R2 these are refused as UNKNOWN
    FIELDS by the closed schema, not by any judgement about their names."""
    entry = {"id": "z", "final_verdict": "refine", "c7_verdict": "refine"}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, root=_SR_ROOT)
    assert "c7_verdict" in str(exc.value) and "final_verdict" in str(exc.value)
    assert "unknown field" in str(exc.value)


def test_d4_provenance_describing_fields_are_not_themselves_verdicts():
    """The name-shape rule must not eat the vocabulary the fix introduced:
    verdict_status and verdict_void_reason DESCRIBE provenance, they do not
    assert a verdict."""
    entry = {"id": "w", "verdict_status": "ungated",
             "verdict_void_reason": "no pass_rule_evaluation.yaml exists"}
    assert vce.validate_verdict_provenance(entry, root=_SR_ROOT) is entry


def test_d4_a_ref_belonging_to_another_run_is_refused():
    """Beyond the audit: run_058 may not borrow run_059's evaluation. Without
    this, the D-5 correction could be undone by citing the one real artifact in
    the campaign from any entry at all."""
    entry = {"id": "u", "evidence_runs": ["run_058"], "outcome": "completed_rejected",
             "pass_rule_evaluation_ref": "runs/run_059/artifacts/pass_rule_evaluation.yaml"}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, root=_SR_ROOT)
    assert "does not lie under any of this entry's own runs" in str(exc.value)


def test_d4_a_non_binding_evaluation_is_not_provenance(tmp_path):
    """A VERDICT_BLOCKED evaluation is the evaluator declining to decide.
    Citing it as provenance cites a non-decision."""
    import yaml
    run_artifacts = tmp_path / "runs" / "run_777" / "artifacts"
    run_artifacts.mkdir(parents=True)
    (run_artifacts / "pass_rule_evaluation.yaml").write_text(
        yaml.safe_dump({"result": "VERDICT_BLOCKED", "blocked_by": ["deployable_today"]}),
        encoding="utf-8")
    entry = {"id": "v", "evidence_runs": ["run_777"], "outcome": "kill_something",
             "pass_rule_evaluation_ref": "runs/run_777/artifacts/pass_rule_evaluation.yaml"}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, root=tmp_path)
    assert "not a resolved verdict" in str(exc.value)


def test_d4_honest_ungated_declaration_is_admissible():
    """The escape hatch is honesty, and it is the point of the whole fix: an
    entry may keep a verdict-shaped outcome IF it states that nothing gated it."""
    entry = {"id": "z", "outcome": "kill_mechanism_falsified",
             "verdict_status": "ungated"}
    assert vce.validate_verdict_provenance(entry, root=_SR_ROOT) is entry


def test_d4_engineering_states_need_no_gate():
    """`invalidated_artifact` and friends assert nothing about the hypothesis."""
    for outcome in ("invalidated_artifact", "blocked_feed_unavailable",
                    "inconclusive", "hypothesis_generation"):
        assert not vce.outcome_is_verdict_bearing(outcome), outcome
    for outcome in ("kill_er_gate_mechanism_falsified", "no_edge_observed",
                    "completed_rejected", "promote_to_holdout", "refine_x"):
        assert vce.outcome_is_verdict_bearing(outcome), outcome


def test_d4_unrecognised_outcome_defaults_to_requiring_provenance():
    """An outcome nobody classified is exactly the shape the XS_momentum
    incident arrived in. Default-deny."""
    assert vce.outcome_is_verdict_bearing("some_brand_new_conclusion_nobody_listed")


def test_d4_bypass_c_the_live_record_passes_the_standalone_lint():
    """Audit bypass C: the KB was validated only as a side effect of an
    orchestrator write, and the queue not at all. This runs the standalone lint
    over both live files with no write involved."""
    import lint_verdict_provenance as lint
    violations = lint.lint_verdict_provenance(root=_SR_ROOT)
    assert violations == [], "\n".join(violations)


def test_d4_queue_writer_refuses_an_ungated_verdict(tmp_path, monkeypatch):
    """run_campaign._save_queue bypassed validation entirely. Now it cannot."""
    import run_campaign
    queue_dir = tmp_path / "config"
    queue_dir.mkdir(parents=True)
    monkeypatch.setattr(run_campaign, "QUEUE_PATH", queue_dir / "campaign_queue.yaml")
    monkeypatch.setattr(run_campaign, "ROOT", tmp_path)

    run_campaign._save_queue({"queue": [{"id": "OK", "outcome": "done"}]})
    assert (queue_dir / "campaign_queue.yaml").exists()

    with pytest.raises(vce.UngatedVerdictError):
        run_campaign._save_queue({"queue": [
            {"id": "SNEAKY", "outcome": "kill_mechanism_falsified"}]})


def test_d6_nested_machine_constraints_pass_rule_is_found():
    """D-6: run_057's real pre_registration.yaml nests its pass_rule under
    machine_constraints, where the top-level-only lookup could not see it."""
    import yaml
    pre_reg = yaml.safe_load(
        (_SR_ROOT / "runs" / "run_057" / "artifacts" / "pre_registration.yaml")
        .read_text(encoding="utf-8")) or {}
    assert pre_reg.get("pass_rule") is None, "fixture drifted: rule is no longer nested"
    found = vce._find_pass_rule(pre_reg)
    assert found is not None
    assert "median Sharpe" in str(found)

    # Honest limit: finding it does not make it machine-evaluable. run_057's rule
    # is a legacy PROSE STRING, so it still resolves to legacy_not_evaluable --
    # which is the accurate diagnosis, and the basis for the relabelling.
    assert isinstance(found, str)
    assert vce._resolve_pass_rule({}, pre_reg)["result"] == "legacy_not_evaluable"


def test_d6_a_nested_structured_rule_is_actually_evaluated():
    """The forward-looking half of D-6: a future brief nesting a STRUCTURED rule
    is now evaluated rather than silently dropped to stage discretion."""
    pre_reg = {"machine_constraints": _structured_pre_registration()}
    result = vce._resolve_pass_rule(
        {"per_symbol_summary": {"BTCUSDT": {"median_sharpe": 0.9}}}, pre_reg)
    assert result["result"] != "legacy_not_evaluable"


def test_d6_run_057_record_no_longer_claims_a_kill():
    """The relabelling itself, and the measurements it must not have deleted."""
    import yaml
    kb = yaml.safe_load(
        (_SR_ROOT / "campaign_record" / "campaign_knowledge_base.yaml").read_text(encoding="utf-8")) or {}
    entry = next(e for e in kb["findings"]
                 if e.get("id") == "p4_sma_trend_longonly_daily_auto")

    assert entry["outcome"] == "ungated_er_gate_variant_too_sparse_to_evaluate"
    assert entry["verdict_status"] == "ungated"
    assert "readjudication_20260722" in entry
    # The superseded label is retained, not erased.
    assert any(h.get("outcome") == "kill_er_gate_mechanism_falsified"
               for h in entry.get("outcome_history_superseded_20260722", []))
    # The S2 evidence that survives the relabelling is still recorded verbatim.
    assert "1395.9" in entry["outcome_reason"]


def test_d6_run_057_sparsity_is_what_the_artifacts_say():
    """The relabelling is a claim about the data; this recomputes it from the
    archived artifact rather than trusting the prose. 29/30 window-symbols below
    the five-trade floor, exactly ONE non-null per-window Sharpe in the run."""
    import yaml
    protocol_result = yaml.safe_load(
        (_SR_ROOT / "runs" / "run_057" / "artifacts" / "protocol_result.yaml")
        .read_text(encoding="utf-8")) or {}
    rows = protocol_result["results"]
    assert len(rows) == 30
    assert sum(1 for r in rows if r["core"]["trade_count"] < 5) == 29
    non_null = [r for r in rows if r["core"]["sharpe"] is not None]
    assert len(non_null) == 1
    assert non_null[0]["symbol"] == "ETHUSDT"
    assert non_null[0]["core"]["sharpe"] == -0.686


def test_d5_h041c_v2_is_recorded_as_stage_discretion_not_a_gated_verdict():
    import yaml
    kb = yaml.safe_load(
        (_SR_ROOT / "campaign_record" / "campaign_knowledge_base.yaml").read_text(encoding="utf-8")) or {}
    entry = next(e for e in kb["findings"]
                 if e.get("id") == "fear_greed_contrarian_v2_validation_rejected")
    assert entry["verdict_status"] == "stage_discretion"
    assert entry["outcome"] == "stage_discretion_rejection_no_gated_verdict"
    assert entry["outcome_reason"] == "validation_gate_rejection_pre_pass_rule"
    # The rejection's own reasoning is not withdrawn.
    assert any(h.get("outcome") == "completed_rejected"
               for h in entry.get("outcome_history_superseded", []))


def test_d3_generic_promotion_block_is_refused_at_selection(tmp_path, monkeypatch):
    """D-3: G7 guarded protocol GENERATION only. A run that simply loads a
    committed protocol carrying the abolished block was untouched."""
    import json
    import run_phase1_research as rpr
    monkeypatch.setattr(rpr, "ROOT", tmp_path)
    protocols = tmp_path / "protocols"
    protocols.mkdir()
    generic = protocols / "baseline_v1.json"
    generic.write_text(json.dumps({
        "symbols": ["BTCUSDT"], "windows": [],
        "promotion": dict(rpr._GENERIC_PROMOTION)}), encoding="utf-8")

    with pytest.raises(rpr.UngatedProtocolError) as exc:
        rpr._assert_promotion_ratified(generic)
    assert "abolished generic promotion block" in str(exc.value)

    # Explicit ratification is the documented way through -- and it is a claim a
    # human makes on the record, not something the code can supply for itself.
    ratified = json.loads(generic.read_text(encoding="utf-8"))
    ratified["promotion_provenance"] = {"ratified_by": "operator ruling 2026-07-22",
                                        "ratified_at": "2026-07-22"}
    generic.write_text(json.dumps(ratified), encoding="utf-8")
    rpr._assert_promotion_ratified(generic)


def test_d3_every_committed_generic_protocol_is_marked_unratified():
    """The nine committed protocol files carrying the abolished block are
    recorded as unratified, so selecting one fails loudly instead of silently
    supplying thresholds no brief ever froze.

    (The audit report said seven; recounting from the tree gives nine --
    baseline_v1/v2, four escalation_*, and three run_0NN_generated.)"""
    import json
    import run_phase1_research as rpr
    generic_files = []
    for path in sorted((_SR_ROOT / "protocols").glob("*.json")):
        obj = json.loads(path.read_text(encoding="utf-8"))
        if rpr.promotion_is_generic(obj.get("promotion")):
            generic_files.append(path.name)
            provenance = obj.get("promotion_provenance") or {}
            assert provenance.get("status") == "generic_unratified", path.name
            assert provenance.get("ratified_by") is None, \
                f"{path.name} was ratified without a human saying so"
    assert len(generic_files) == 9, generic_files


def test_d3_forced_diagnostic_without_a_named_protocol_no_longer_defaults(tmp_path, monkeypatch):
    """The second half of D-3: the implicit baseline_v1.json default is gone."""
    import run_phase1_research as rpr
    monkeypatch.setattr(rpr, "ROOT", tmp_path)
    run_dir = tmp_path / "runs" / "run_900"
    (run_dir / "artifacts").mkdir(parents=True)
    rpr.save_yaml(run_dir / "artifacts" / "run_context.yaml",
                  {"run_type": "forced_diagnostic"})  # no `protocol` key

    with pytest.raises(rpr.UngatedProtocolError) as exc:
        rpr._resolve_protocol_path(run_dir, "run_900")
    assert "names no `protocol`" in str(exc.value)


def test_d1_fail_routes_to_kill_terminate_through_the_public_entry():
    """D-1. Before this, every public-entry assertion in the suite was
    VERDICT_BLOCKED, PASS, or legacy_not_evaluable -- the kill-routing path, the
    most consequential one the evaluator has, was pinned only through the
    _resolve_pass_rule kernel. Mutating the public entry to stop calling that
    kernel was caught by a single PASS-path test.

    This pins FAIL -> hypothesis_verdict: kill / lineage_routing: terminate
    end-to-end through evaluate_pass_rule_criteria, with the preconditions MET so
    the kernel is genuinely reached."""
    protocol_result = _complete_protocol_result()
    protocol_result["hypothesis_verdict"]["diagnostics"]["median_sharpe"] = 0.1

    result = vce.evaluate_pass_rule_criteria(
        protocol_result, _structured_pre_registration(), {"product": "spot"})

    assert result["result"] == "FAIL"
    assert result["hypothesis_verdict"] == "kill"
    assert result["lineage_routing"] == "terminate"
    assert result["statement_branch_matched"] == "FAIL-a"
    # The preconditions were genuinely evaluated, not skipped on the way past.
    assert all(g["result"] == "MET" for g in result["preconditions"])
