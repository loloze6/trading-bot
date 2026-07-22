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

TOOLS_PATH = Path(__file__).parent.parent / "tools"
WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
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
        "citation": "docs/venue_survey_20260719.md 2026-07-20 supplement",
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
    """The link that let a research-path tool write `verdict_c7: refine`."""
    entry = {"id": "xs_momentum_cost_surviving_but_decaying", "verdict_c7": "refine"}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, entry_ref="KB finding 'xs'")
    assert "structurally ungated" in str(exc.value)


def test_g6_verdict_with_provenance_is_admissible():
    entry = {"id": "some_finding", "verdict_c7": "kill",
             "pass_rule_evaluation_ref": "runs/run_058/artifacts/pass_rule_evaluation.yaml"}
    assert vce.validate_verdict_provenance(entry) is entry


def test_g6_ungated_entry_may_keep_measurements_but_not_a_verdict():
    """A measurement is not a verdict — the entry keeps its numbers."""
    entry = {
        "id": "xs_momentum_cost_surviving_but_decaying",
        "verdict_status": "ungated",
        "signal_property": {"net_sharpe_full_sample": 1.325},
    }
    assert vce.validate_verdict_provenance(entry) is entry

    entry["verdict_c7"] = "refine"
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry)
    assert "contradictory" in str(exc.value)


def test_g6_live_kb_has_no_ungated_verdict_fields():
    """Guards the corrected record itself: every finding in the real KB must
    be admissible under G6."""
    import yaml
    kb_path = Path(__file__).parent.parent / "campaign_knowledge_base.yaml"
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
    kb_path = Path(__file__).parent.parent / "campaign_knowledge_base.yaml"
    kb = yaml.safe_load(kb_path.read_text(encoding="utf-8")) or {}
    entry = next(e for e in kb["findings"]
                 if e.get("id") == "xs_momentum_cost_surviving_but_decaying")

    assert "verdict_c7" not in entry
    assert entry["verdict_status"] == "ungated"
    # The measurement is real information and must survive the correction.
    assert entry["signal_property"]["net_sharpe_full_sample"] == 1.325
    assert entry["validation_gate"] == "PASS"


def test_campaign_honest_verdict_count():
    """After the correction, the hypotheses holding a verdict that passed
    through a pre-registered pass rule are H-041-C-v2 and FUNDING_MR_DAILY_RETEST
    — TWO, not one.

    The audit dispatch expected one. It is two: FUNDING_MR_DAILY_RETEST carries
    its own B11 total mapping in briefs/FUNDING_MR_DAILY_RETEST.md (every FAIL
    branch terminating both hypothesis and lineage, protocol pinned via
    machine_constraints), so it is as genuinely gated as H-041-C-v2. XS_momentum
    is the only entry whose verdict was withdrawn. If this list moves, something
    acquired or lost a verdict and it must be explained, not adjusted.
    """
    import yaml
    queue_path = Path(__file__).parent.parent / "config" / "campaign_queue.yaml"
    queue = yaml.safe_load(queue_path.read_text(encoding="utf-8")) or {}
    outcomes = {e["id"]: (e.get("outcome") or "") for e in queue.get("queue", [])}

    assert outcomes["XS_momentum"] == "ungated_measurement_no_admissible_verdict"
    assert "refine" not in outcomes["XS_momentum"]

    gated = sorted(hid for hid, out in outcomes.items() if out == "completed_rejected")
    assert gated == ["FUNDING_MR_DAILY_RETEST", "H-041-C-v2"], \
        f"gated-verdict set changed: {gated}"
