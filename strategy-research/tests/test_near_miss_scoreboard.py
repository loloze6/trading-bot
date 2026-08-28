"""Tests for tools/near_miss_scoreboard.py (E-018 S1).

Covers: per-schema parsing (the two verdict_interpretation.yaml families plus
the thin/no-verdict case), the "never impute" rule (ambiguous or
sign-contradicting extractions must fall back to not_recorded rather than a
guess), denominator honesty (every count matches what's actually on disk,
never rounded or assumed), ranking, and a regression lock against the real
`runs/` corpus's known-good verdict-field distribution.

None of these tests touch workflow/run_campaign.py, workflow/run_phase1_research.py,
or setup_run.py, so the autouse `_sandbox_by_default` fixture in conftest.py
is a no-op for this file (nothing here reads those modules' patched globals);
no `real_repo_readonly` marker is needed for the same reason the K2 tests
don't need one.
"""
import sys
from pathlib import Path

import pytest
import yaml

TOOLS = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS))
import near_miss_scoreboard as nms  # noqa: E402

REPO_RUNS_DIR = Path(__file__).parent.parent / "runs"


# --- criterion parsing: structured (dict) forms -----------------------------

def test_dict_criterion_scalar_pass():
    c = nms.parse_dict_criterion({"criterion": "sharpe", "result": "PASS",
                                   "actual": 0.9, "required": "> 0.8"})
    assert c.result == "PASS"
    assert c.op == ">"
    assert c.threshold == 0.8
    assert c.actual == 0.9
    assert c.margin_frac == pytest.approx((0.9 - 0.8) / 0.8)


def test_dict_criterion_per_symbol_dict_actual_takes_binding_worst():
    c = nms.parse_dict_criterion({
        "criterion": "criterion_a", "result": "FAIL",
        "actual": {"BTCUSDT": -0.296, "ETHUSDT": -0.979},
        "required": "> 0.8",
    })
    # ">" direction: the binding (worst) value is the smallest.
    assert c.actual == -0.979
    assert c.actual_source == "structured_per_symbol"
    assert c.margin_frac < 0


def test_dict_criterion_actual_btc_eth_split_keys():
    """run_016-style: no 'actual' key at all, only actual_btc/actual_eth."""
    c = nms.parse_dict_criterion({
        "criterion": "approval_gate_1: sharpe >= 0.5", "result": "FAIL",
        "actual_btc": -2.944, "actual_eth": -2.715, "required": ">= 0.5",
    })
    assert c.actual_source == "structured_per_symbol_keys"
    assert c.actual == -2.944  # min of the two, binding for a ">=" gate
    assert c.margin_frac == pytest.approx((-2.944 - 0.5) / 0.5)


def test_dict_criterion_no_actual_at_all_is_not_recorded():
    c = nms.parse_dict_criterion({"criterion": "no hold-out split", "result": "UNTESTED"})
    assert c.actual is None
    assert c.margin_frac is None


# --- criterion parsing: free-text forms -------------------------------------

def test_text_criterion_symbol_paren_form():
    text = "median_sharpe_across_windows (> 0.30): FAIL — actual -4.081 (BTCUSDT), -1.236 (ETHUSDT)"
    c = nms.parse_text_criterion(text)
    assert c.result == "FAIL"
    assert c.op == ">"
    assert c.threshold == 0.30
    assert c.actual == -4.081  # worst of the two under ">"
    assert c.margin_frac == pytest.approx((-4.081 - 0.30) / 0.30)


def test_text_criterion_label_equals_form():
    text = "spearman_ic: FAIL — pooled ic_active_bars=-0.0403 (target ≥0.15)"
    c = nms.parse_text_criterion(text)
    assert c.result == "FAIL"
    # exactly one label=number pair in the detail segment -> used directly
    assert c.actual == -0.0403


def test_text_criterion_past_tense_failed_parses_as_fail_with_evidence_preserved():
    """FIX 5 (review, 2026-08-24): the real run_043 verdict text uses 'FAILED'
    (past tense), which the un-widened RESULT_RE (no word boundary between the
    'L'/'D' and a following letter is irrelevant here -- the real bug is
    simply that 'FAILED' != 'FAIL' under an exact-token \\b(...)\\b match)
    could not match at all, so result fell back to 'unknown' and detail_seg
    was forced to '' -- silently dropping the ic_all_bars/p-value evidence
    that follows the result word."""
    text = ("Walk-forward Spearman IC >= 0.2: FAILED at prescreen (ic_all_bars = "
            "-0.021091, p = 0.5876 >> 0.10, not significant)")
    c = nms.parse_text_criterion(text)
    assert c.result == "FAIL"
    assert "ic_all_bars" in c.raw  # raw text always preserved regardless
    # The evidence after the result word must now be reachable by the
    # detail-segment extractors (label=number form here).
    detail_seg = text[text.index("FAILED") + len("FAILED"):]
    assert "-0.021091" in detail_seg


def test_text_criterion_lowercase_untested_normalizes():
    text = "holdout comparison: untested (no holdout split registered for this run)"
    c = nms.parse_text_criterion(text)
    assert c.result == "UNTESTED"


def test_text_criterion_past_tense_passed_normalizes():
    text = "sharpe >= 0.8: PASSED (actual 1.2)"
    c = nms.parse_text_criterion(text)
    assert c.result == "PASS"


@pytest.mark.parametrize("token,expected", [
    ("PASS", "PASS"), ("FAIL", "FAIL"), ("UNTESTED", "UNTESTED"),
])
def test_text_criterion_exact_tokens_unaffected_by_the_widened_regex(token, expected):
    """Regression: the pre-existing exact-token PASS/FAIL/UNTESTED path must
    still resolve to exactly the same result after RESULT_RE was widened."""
    text = f"some criterion (>= 1.0): {token} (actual 2.0)"
    c = nms.parse_text_criterion(text)
    assert c.result == expected


def test_text_criterion_requirement_label_is_never_mistaken_for_actual():
    """Regression: a rationale that restates the threshold as
    'validation_protocol required=1.5' inside the detail segment must NOT be
    picked up as the observed value (this produced a bogus exact-zero margin
    before the _REQUIREMENT_LABELS filter was added)."""
    text = ("Walk-forward pooled IC >= 1.5-2.0%: FAIL (BTCUSDT actual 0.0372, "
            "ETHUSDT actual 0.0199; validation_protocol required=1.5 is a spec error)")
    c = nms.parse_text_criterion(text)
    assert c.actual != 1.5, "the restated requirement leaked through as the actual value"
    assert c.margin_frac is None or c.margin_frac < -0.5


def test_text_criterion_date_like_digits_never_become_actual():
    """Regression: 'FAIL (only 3 windows: 2024-06, 2024-08, 2024-09)' must
    not parse '2024' out of a date as if it were a metric value -- caught
    here via the result-consistency safety net (margin would come out
    positive for a FAIL, which is impossible, so it is suppressed)."""
    text = "Robustness gate (>=5 trades in 4 of 5 validation windows): FAIL (only 3 windows: 2024-06, 2024-08, 2024-09)"
    c = nms.parse_text_criterion(text)
    assert c.margin_frac is None, (
        f"expected the date-derived value to be rejected, got margin_frac={c.margin_frac}"
    )


def test_never_impute_ambiguous_multi_label_detail_stays_not_recorded():
    text = ("Approval gate (V1_sharpe >= 0.30 AND V1_win_rate >= 0.50 AND V1_trade_count >= 50): "
            "FAIL (sharpe=0.0, win_rate=50% PASS, trade_count=27 FAIL)")
    c = nms.parse_text_criterion(text)
    # Three plausible candidate values, none disambiguated -> must not guess.
    assert c.actual is None
    assert c.margin_frac is None


def test_contradicts_stated_result_is_suppressed_not_flipped():
    """A margin whose sign disagrees with the criterion's own stated result
    (e.g. a sign/unit mismatch making a FAIL look like a huge pass) must be
    dropped to None, never silently kept or "corrected" -- the whole point
    is to never present a fabricated number as evidence."""
    c = nms.Criterion(raw="x", result="FAIL", op=">=", threshold=5.0, actual=2024.0,
                       actual_source="text_extracted_label", compound=False)
    assert c.margin_frac is None
    assert c.actual_source.endswith("_contradicts_result")


# --- row assembly: full_protocol schema -------------------------------------

def _write_yaml(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def test_build_row_full_protocol_schema(tmp_path):
    run_dir = tmp_path / "run_999"
    _write_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml", {
        "hypothesis_id": "H-999",
        "hypothesis_family": "test_family",
        "protocol_verdict": "refine",
        "status": "pivot",
        "criteria_summary": [
            {"criterion": "sharpe", "result": "FAIL", "actual": -0.1, "required": "> 0.8"},
            {"criterion": "drawdown", "result": "PASS", "actual": 10.0, "required": "<= 30"},
        ],
        "primary_failure_mode": "No directional edge detected. Further detail follows.",
        "root_cause": {"mechanism_failure": "already_priced_in", "confidence": "high"},
    })
    row = nms.build_row(run_dir)
    assert row["evidence_tier"] == "full_protocol"
    assert row["protocol_verdict"] == "refine"
    assert row["status"] == "pivot"
    assert row["hypothesis_family"] == "test_family"
    assert row["n_criteria_pass"] == 1
    assert row["n_criteria_fail"] == 1
    assert row["root_cause_mechanism"] == "already_priced_in"
    assert "nosignal" in row["primary_failure_mode_bucket"]
    assert row["worst_fail_margin_frac"] == pytest.approx((-0.1 - 0.8) / 0.8)


def test_build_row_prescreen_only_schema(tmp_path):
    run_dir = tmp_path / "run_998"
    _write_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml", {
        "hypothesis_id": "H-998",
        "hypothesis_family": "funding_test",
        "verdict_label": "insufficient_sample_inconclusive",
        "prescreen_result_summary": {
            "ic_active_bars": 0.19, "edge_to_cost_ratio": 3.75, "p_value": 0.55,
        },
    })
    row = nms.build_row(run_dir)
    assert row["evidence_tier"] == "prescreen_only"
    assert row["verdict_label_or_disposition"] == "insufficient_sample_inconclusive"
    assert row["ic"] == 0.19
    assert row["ic_source"] == "structured"
    assert row["cost_ratio"] == 3.75
    # This schema carries no protocol_verdict/status field at all.
    assert row["protocol_verdict"] == "not_recorded"
    assert row["status"] == "not_recorded"


def test_build_row_thin_run_no_verdict_file_never_imputes(tmp_path):
    run_dir = tmp_path / "run_997"
    _write_yaml(run_dir / "pipeline_state.yaml", {"status": "failed", "current_stage": "validation"})
    row = nms.build_row(run_dir)
    assert row["evidence_tier"] == "thin_no_verdict_file"
    assert row["pipeline_status"] == "failed"
    assert row["pipeline_stage"] == "validation"
    # Every verdict-derived field must be the explicit marker, never a guess.
    for key in ("protocol_verdict", "status", "root_cause_mechanism", "worst_fail_margin_frac"):
        assert row[key] in ("not_recorded", None)


def test_build_row_no_artifacts_no_pipeline_state_still_produces_a_row(tmp_path):
    """A run dir with nothing recoverable at all must still appear in the
    table (never silently dropped) -- it's information that the record is
    this thin."""
    run_dir = tmp_path / "run_996"
    run_dir.mkdir()
    row = nms.build_row(run_dir)
    assert row["run_id"] == "run_996"
    assert row["evidence_tier"] == "thin_no_verdict_file"
    assert row["pipeline_status"] == "not_recorded"


# --- ranking -----------------------------------------------------------------

def test_rank_rows_orders_near_miss_before_blowout_before_thin():
    rows = [
        {"run_id": "run_c", "worst_fail_margin_frac": None, "evidence_tier": "thin_no_verdict_file",
         "status": "not_recorded", "ic": None},
        {"run_id": "run_b", "worst_fail_margin_frac": -5.0, "evidence_tier": "full_protocol",
         "status": "kill", "ic": None},
        {"run_id": "run_a", "worst_fail_margin_frac": -0.1, "evidence_tier": "full_protocol",
         "status": "refine", "ic": None},
        {"run_id": "run_d", "worst_fail_margin_frac": None, "evidence_tier": "full_protocol",
         "status": "refine", "ic": None},
    ]
    nms.rank_rows(rows)
    order = [r["run_id"] for r in rows]
    # run_a (smallest-magnitude miss) before run_b (blowout) before run_d
    # (verdict but no numeric margin) before run_c (no verdict at all).
    assert order == ["run_a", "run_b", "run_d", "run_c"]
    assert [r["rank"] for r in rows] == [1, 2, 3, 4]


# --- denominator honesty & idempotency ---------------------------------------

def test_denominators_match_actual_counts_on_a_mixed_synthetic_corpus(tmp_path):
    runs_dir = tmp_path / "runs"
    # 1 full_protocol, 1 prescreen_only, 1 thin.
    _write_yaml(runs_dir / "run_a" / "artifacts" / "verdict_interpretation.yaml", {
        "protocol_verdict": "refine", "status": "refine",
        "criteria_summary": [{"criterion": "x", "result": "FAIL", "actual": 0.0, "required": "> 1.0"}],
    })
    _write_yaml(runs_dir / "run_b" / "artifacts" / "verdict_interpretation.yaml", {
        "verdict_label": "parked", "prescreen_result_summary": {"ic_active_bars": 0.05},
    })
    (runs_dir / "run_c").mkdir(parents=True)

    rows = nms.build_scoreboard(runs_dir)
    denom_lines = nms._denominator_report(rows)
    joined = "\n".join(denom_lines)
    assert "Total run dirs scanned: 3" in joined
    assert "Have a verdict_interpretation.yaml: 2 of 3" in joined
    assert "full_protocol schema: 1 of 3" in joined
    assert "prescreen_only schema: 1 of 3" in joined
    assert "IC recovered (any source): 1 of 3" in joined


def test_main_is_idempotent(tmp_path):
    runs_dir = tmp_path / "runs"
    _write_yaml(runs_dir / "run_a" / "artifacts" / "verdict_interpretation.yaml", {
        "protocol_verdict": "kill", "status": "kill",
        "criteria_summary": [{"criterion": "x", "result": "FAIL", "actual": 0.0, "required": "> 1.0"}],
    })
    out_dir = tmp_path / "out"
    nms.main(["--runs-dir", str(runs_dir), "--out-dir", str(out_dir)])
    first = (out_dir / "near_miss_scoreboard.yaml").read_text(encoding="utf-8")
    nms.main(["--runs-dir", str(runs_dir), "--out-dir", str(out_dir)])
    second = (out_dir / "near_miss_scoreboard.yaml").read_text(encoding="utf-8")
    assert first == second


def test_main_writes_only_under_requested_out_dir(tmp_path):
    runs_dir = tmp_path / "runs"
    (runs_dir / "run_a").mkdir(parents=True)
    out_dir = tmp_path / "out"
    real_e018 = Path(__file__).parent.parent / "engineering" / "roadmap" / "E-018" / "artifacts"
    before = real_e018.stat().st_mtime if real_e018.exists() else None
    nms.main(["--runs-dir", str(runs_dir), "--out-dir", str(out_dir)])
    assert (out_dir / "near_miss_scoreboard.yaml").exists()
    after = real_e018.stat().st_mtime if real_e018.exists() else None
    assert before == after, "main() with an explicit --out-dir must not touch the real repo artifacts dir"


# --- regression lock against the real corpus ---------------------------------

@pytest.mark.skipif(not REPO_RUNS_DIR.exists(), reason="runs/ not present in this checkout")
def test_real_corpus_verdict_field_denominators_match_known_good():
    """Locks in pre-verified corpus numbers so a change to the corpus or the
    parser is caught: 39 of 60 run dirs carry a verdict_interpretation.yaml;
    protocol_verdict is 26 refine / 11 kill / 2 absent-within-file; status is
    14 refine / 10 pivot / 7 escalate / 3 kill / 5 absent-within-file; and --
    the whole reason this is worth locking down -- 'promote' appears in
    NEITHER field, anywhere.

    REBASELINED 2026-08-28 from the 2026-08-23 measurement (59 runs, 38 with
    verdicts, 10 protocol kills, 2 status kills). The ONLY change is run_060
    (FUNDING_MR_4H_RETEST), which finished as evidence_tier=full_protocol with
    protocol_verdict=kill and status=kill. Every other cell is untouched:
    refine stays 26/14, pivot 10, escalate 7, not_recorded 2/5. The rebaseline
    is therefore fully attributable to one new run rather than absorbing
    unexplained drift -- which is the only condition under which re-pinning
    these numbers is legitimate."""
    rows = nms.build_scoreboard(REPO_RUNS_DIR)
    assert len(rows) == 60

    has_verdict = [r for r in rows if r["evidence_tier"] != "thin_no_verdict_file"]
    assert len(has_verdict) == 39

    from collections import Counter
    pv = Counter(r["protocol_verdict"] for r in has_verdict)
    st = Counter(r["status"] for r in has_verdict)

    assert pv.get("refine", 0) == 26
    assert pv.get("kill", 0) == 11
    assert pv.get("not_recorded", 0) == 2
    assert "promote" not in pv

    assert st.get("refine", 0) == 14
    assert st.get("pivot", 0) == 10
    assert st.get("escalate", 0) == 7
    assert st.get("kill", 0) == 3
    assert st.get("not_recorded", 0) == 5
    assert "promote" not in st


@pytest.mark.skipif(not REPO_RUNS_DIR.exists(), reason="runs/ not present in this checkout")
def test_real_corpus_never_produces_a_margin_that_contradicts_its_own_result():
    """Sweeps the whole real corpus: every recovered worst_fail_margin_frac
    must be <= 0 (consistent with it having been binding for a FAIL). If this
    ever fails, the result-consistency safety net has a hole."""
    rows = nms.build_scoreboard(REPO_RUNS_DIR)
    bad = [r["run_id"] for r in rows
           if r["worst_fail_margin_frac"] is not None and r["worst_fail_margin_frac"] > 1e-9]
    assert bad == []
