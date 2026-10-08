"""
E-073 step 2 (P-CUL-81, D-083): value-checked citations and in-run dedup of
side findings, behind the epic's one flag orchestrator.observable_backtest
(off by default, requires reader_findings).

Sections:
  1. The value rule (reader_proposals.value_matches / check_citation_values):
     numbers within half a unit of the last written digit, `%`, text, bool,
     null exact; a missing path; a mapping is not a value; [*]; the file stem.
  2. The reader's one retry: a missing or mis-valued citation is sent back
     once with a code-written list (path, cited, actual) and the reader's own
     answer; still wrong, the reading is kept and the citation recorded
     (citation_checks/<category>.yaml). The retry is ONE: a shape retry
     spends it; a refused retry answer keeps the first answer; a spent budget
     or a check error never stops the reader.
  3. Under E-072 the check reads the readers' exploration copies, never the
     all-window files.
  4. In-run dedup: same spec_hashes + same config change = one finding, listed
     with every source; measured and counted once in the confirmation ledger;
     one decide-next candidate with the first source's scores (never the
     higher -- not agreement); a flagged citation is a warning only.
  5. Flag off (key absent or false): byte-identical.
  6. The final design after two reviews: the retry note shows paths and the
     cited value, never a file's value; the retry answer is kept only with
     fewer bad citations AND the same side findings; one number rule plus the
     zero exception; whole-text matching; hyphen keys; stem-rooted suggestions.

No LLM: _invoke_reader_llm is replaced wherever it is reached. No backtest, no
market data.
"""
import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import reader_proposals as rp  # noqa: E402
import reader_findings as rf  # noqa: E402
import decide_next as dn  # noqa: E402
import explore_confirm as ec  # noqa: E402

from test_e046a_slice5b_ii_b_readers_stage import RUN_ID, _set_orchestrator  # noqa: E402
from test_e068_5_readers_v3 import (  # noqa: E402
    V3_ON, _claim, _scores, _reading, _fenced, _run070_shaped, _memory_entry, _src, _inputs)
from test_e072_explore_confirm import (  # noqa: E402
    EC_ON, _ec_run, _protocol_execution_part, _pure_claim, _confirmation)
from test_e073_data_dictionary import _seed_dictionary  # noqa: E402

OB_ON = {**V3_ON, "observable_backtest": {"enabled": True}}
OB_OFF = {**V3_ON, "observable_backtest": {"enabled": False}}
EC_OB_ON = {**EC_ON, "observable_backtest": {"enabled": True}}
CAT = "trade_efficiency"
SIDE_ID = f"{CAT}-{RUN_ID}-1"
PERIOD = "strategies.regimes.unknown.components[0].params.period"  # 1 in the e068_5 config
REPORT = {"category": CAT, "variants": {"base": {"slices": {"overall": {
    "boundary_recross_rate": 0.9487, "exit_efficiency_median": 0.0576,
    "statistic_label": "rank IC (Spearman)",
    "fee_reduction_metrics": {"trade_less_often": {"boundary_recross_rate": 0.9487}}}}}}}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# 1. The value rule
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cited,actual,ok", [
    ("0.076977", 0.076977, True),          # as the file shows it
    ("0.077", 0.076977, True),             # rounded to 3 digits
    ("0.0770", 0.076977, True),
    ("0.07698", 0.076977, True),
    ("0.0769", 0.076977, False),           # truncated, not rounded
    ("0.077", 0.0765, True),               # exactly half a unit of the cited last digit
    ("0.077", 0.07649, False),             # just beyond it
    ("0.0765", 0.077, False),              # more digits than the file: they must hold
    ("2", 3, False),                       # run_073: "period 2" where the config has 3
    ("3", 3, True), ("2.0", 2, True), ("3 bars", 3, True),
    ("-0.0057", -0.00574, True), ("−0.5", -0.5, True), ("~0.08", 0.077, None),
    ("99.16%", 0.9916, True),              # a percent of a fraction
    ("99.16", 0.9916, False),              # without %: never rescaled
    ("99%", 99.16, True), ("12,830", 12830, True), ("1.2e-05", 0.0000123, True),
    ("0.0576 vs. mean: -0.8288", 0.0576, True),   # the first value after the path
    ("PASS", 0.5, None),                   # a word where the field holds a number: not checked
    ("FAIL", "FAIL", True), ("'FAIL'", "FAIL", True), ("fail", "FAIL", True),
    ("FAILED", "FAIL", False),
    ("rank IC (Spearman) as labelled", "rank IC (Spearman)", True),
    ("rank IC", "rank IC (Spearman)", False),
    ("true", True, True), ("false", True, False), ("1", True, False),
    ("null", None, True), ("0", None, False),
    ("0.5", "0.5", True), ("withheld", "withheld", True), ("0.5", "withheld", False),
])
def test_the_value_rule(cited, actual, ok):
    assert rp.value_matches(cited, actual) is ok


def _check(evidence, files=None):
    return rp.check_citation_values(files if files is not None else {"r.yaml": REPORT},
                                    evidence)


def test_a_mismatch_names_the_cited_and_the_actual_value_and_its_file():
    res = _check(["variants.base.slices.overall.boundary_recross_rate=0.96"])
    [bad] = res["bad"]
    assert bad == {"path": "variants.base.slices.overall.boundary_recross_rate", "cited": "0.96",
                   "status": rp.CITATION_MISMATCH, "actual": [0.9487], "files": ["r.yaml"]}


def test_a_missing_path_is_bad_and_a_matching_one_is_not():
    res = _check(["variants.base.slices.overall.signal_flip_pct: 99.16",
                  "variants.base.slices.overall.boundary_recross_rate: 0.9487",
                  "no path at all, 0.5"])
    assert [(c["path"], c["status"]) for c in res["citations"]] == [
        ("variants.base.slices.overall.signal_flip_pct", rp.CITATION_MISSING),
        ("variants.base.slices.overall.boundary_recross_rate", rp.CITATION_MATCH)]
    assert [b["status"] for b in res["bad"]] == [rp.CITATION_MISSING]
    assert res["no_path_items"] == 1


def test_a_path_without_a_value_or_to_a_mapping_is_not_value_checked():
    res = _check(["variants.base.slices.overall shows the base",
                  "variants.base.slices.overall: FAIL for base"])
    assert [c["status"] for c in res["citations"]] == [rp.CITATION_PATH_ONLY,
                                                       rp.CITATION_NOT_A_VALUE]
    assert res["bad"] == []


def test_the_same_path_with_two_values_is_checked_twice():
    res = _check(["variants.base.slices.overall.exit_efficiency_median=0.0576",
                  "variants.base.slices.overall.exit_efficiency_median=0.9"])
    assert [c["status"] for c in res["citations"]] == [rp.CITATION_MATCH, rp.CITATION_MISMATCH]


def test_any_list_element_may_match():
    files = {"g.yaml": {"blocks": [{"ic": 0.1}, {"ic": 0.2}]}}
    assert _check(["blocks[*].ic=0.2"], files)["bad"] == []
    assert _check(["blocks[0].ic=0.2"], files)["bad"][0]["status"] == rp.CITATION_MISMATCH
    assert _check(["blocks[*].ic=0.3"], files)["bad"][0]["actual"] == [0.1, 0.2]


def test_a_file_name_is_a_root_and_its_path_must_still_be_right():
    files = {"grid_evaluation.yaml": {"grid": {"residual_ic": {"base": {"value": 0.076977}}}}}
    ok = _check(["grid_evaluation.grid.residual_ic.base.value: 0.076977"], files)
    assert [c["status"] for c in ok["citations"]] == [rp.CITATION_MATCH]
    # run_073's readers dropped the `grid` level: a missing path
    bad = _check(["grid_evaluation.residual_ic.base.value: 0.076977"], files)
    assert bad["bad"][0]["status"] == rp.CITATION_MISSING


def test_the_record_only_resolver_is_unchanged():
    """D-048's resolve_evidence_paths still drops the value (record only)."""
    out = rp.resolve_evidence_paths({"r.yaml": REPORT},
                                    ["variants.base.slices.overall.boundary_recross_rate=999"])
    assert out == {"resolved": ["variants.base.slices.overall.boundary_recross_rate"],
                   "unresolved": [], "no_path_items": 0}


@pytest.mark.parametrize("bad", [None, "x", ["a"]])
def test_malformed_arguments_raise_type_error(bad):
    with pytest.raises(TypeError):
        rp.check_citation_values(bad, [])
    with pytest.raises(TypeError):
        rp.check_citation_values({}, "not a list")


# ---------------------------------------------------------------------------
# 2. The reader's one retry
# ---------------------------------------------------------------------------

def _cite_run(monkeypatch, flags=OB_ON) -> Path:
    run_dir = _run070_shaped(monkeypatch, flags=flags)
    _seed_dictionary()  # step 1's flag-on reader input
    rpr.save_yaml(run_dir / "artifacts" / "reports" / f"{CAT}.yaml", REPORT)
    return run_dir


def _cited_reading(period="1", ratio="0.9487") -> dict:
    side = {"proposal_id": SIDE_ID, "claim": _claim(),
            "evidence": [f"{PERIOD}={period}"], "scores": _scores()}
    return _reading(CAT, evidence=[f"variants.base.slices.overall.boundary_recross_rate={ratio}"],
                    sides=[side])


def _llm(answers: list, prompts: list):
    async def _fake(prompt):
        prompts.append(prompt)
        return answers[min(len(prompts), len(answers)) - 1], \
            {"usage": {}, "cost_usd": 0.0, "num_turns": 1}
    return _fake


def _checks(run_dir: Path) -> dict:
    return yaml.safe_load((run_dir / "artifacts" / rp.CITATION_CHECKS_DIR / f"{CAT}.yaml")
                          .read_text(encoding="utf-8"))


def _audit(run_dir: Path) -> dict:
    return rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]


def test_a_clean_reading_is_one_call_and_recorded_clean(monkeypatch):
    run_dir = _cite_run(monkeypatch)
    prompts = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm([_fenced(_cited_reading())], prompts))
    rpr.run_reader_worker(CAT, RUN_ID, run_dir)
    assert len(prompts) == 1
    doc = _checks(run_dir)
    assert doc["status"] == "clean" and doc["retried"] is False and doc["flagged"] == []
    assert doc["items"][SIDE_ID] == {"checked": 1, "bad": []}
    assert doc["files_read"] and "candidate_strategy_config.json" in doc["files_read"]


def test_a_wrong_setting_gets_one_retry_then_is_kept_and_flagged(monkeypatch):
    """run_073's case: a period the config does not have. Retried once with the
    list; still wrong: kept, flagged, recorded -- never dropped, never a stop."""
    run_dir = _cite_run(monkeypatch)
    prompts = []
    bad = _fenced(_cited_reading(period="2"))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm([bad, bad], prompts))
    dest = rpr.run_reader_worker(CAT, RUN_ID, run_dir)
    assert len(prompts) == 2
    note = prompts[1][len(prompts[0]):]
    assert "CITED FIELDS THAT DO NOT MATCH THE FILES YOU READ" in note
    assert f"- {SIDE_ID}: `{PERIOD}` cited '2': value does not match the file\n" in note
    assert "shows" not in note.split("The rule:")[0]       # no value from the files
    assert rp.CITATION_VALUE_RULE in note
    assert ("<<<PREVIOUS ANSWER\n" + yaml.safe_dump(_cited_reading(period="2"), sort_keys=False)
            + "PREVIOUS ANSWER>>>") in note
    kept = yaml.safe_load(dest.read_text(encoding="utf-8"))
    assert [s["proposal_id"] for s in kept["side_findings"]] == [SIDE_ID]   # kept
    doc = _checks(run_dir)
    assert doc["status"] == "flagged" and doc["retried"] is True
    assert doc["first_attempt_bad"] == 1 and doc["flagged"] == [SIDE_ID]
    assert doc["items"][SIDE_ID]["bad"] == [{"path": PERIOD, "cited": "2",
                                             "status": rp.CITATION_MISMATCH, "actual": [1],
                                             "files": ["candidate_strategy_config.json"]}]
    audit = _audit(run_dir)
    assert audit[f"specialist_readers_{CAT}_attempt_0"]["citation_check"]["status"] == "retry"
    final = audit[f"specialist_readers_{CAT}_attempt_0_retry1"]["citation_check"]
    assert final == {"status": "flagged", "retried": True, "flagged": [SIDE_ID], "n_bad": 1}


def test_a_retry_that_fixes_the_citation_is_recorded_clean(monkeypatch):
    run_dir = _cite_run(monkeypatch)
    prompts = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm(
        [_fenced(_cited_reading(period="2")), _fenced(_cited_reading(period="1"))], prompts))
    rpr.run_reader_worker(CAT, RUN_ID, run_dir)
    assert len(prompts) == 2
    doc = _checks(run_dir)
    assert doc["status"] == "clean" and doc["retried"] is True and doc["first_attempt_bad"] == 1


def test_a_missing_path_is_named_in_the_retry(monkeypatch):
    run_dir = _cite_run(monkeypatch)
    prompts = []
    doc = _cited_reading()
    doc["evidence"] = ["variants.base.slices.overall.trade_less_often.boundary_recross_rate=0.9487"]
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm([_fenced(doc)], prompts))
    rpr.run_reader_worker(CAT, RUN_ID, run_dir)
    assert len(prompts) == 2
    assert (f"- {CAT}-{RUN_ID}: `variants.base.slices.overall.trade_less_often."
            f"boundary_recross_rate` cited '0.9487': path not found") in prompts[1]
    assert _checks(run_dir)["flagged"] == [f"{CAT}-{RUN_ID}"]


def test_a_shape_retry_spends_the_one_retry(monkeypatch):
    """First answer refused on its shape, second valid but mis-cited: no third
    call; the reading is kept and flagged."""
    run_dir = _cite_run(monkeypatch)
    prompts = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm(
        ["no yaml at all", _fenced(_cited_reading(period="2"))], prompts))
    rpr.run_reader_worker(CAT, RUN_ID, run_dir)
    assert len(prompts) == 2 and "FAILED VALIDATION" in prompts[1]
    doc = _checks(run_dir)
    assert doc["status"] == "flagged" and doc["retried"] is True
    assert "first_attempt_bad" not in doc


def test_a_refused_retry_answer_keeps_the_first_answer(monkeypatch):
    run_dir = _cite_run(monkeypatch)
    prompts = []
    first = _cited_reading(period="2")
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm([_fenced(first), "no yaml"], prompts))
    dest = rpr.run_reader_worker(CAT, RUN_ID, run_dir)
    assert len(prompts) == 2
    kept = yaml.safe_load(dest.read_text(encoding="utf-8"))
    assert kept["side_findings"][0]["evidence"] == first["side_findings"][0]["evidence"]
    assert "skipped" not in kept
    doc = _checks(run_dir)
    assert doc["status"] == "flagged" and "fenced YAML block" in doc["retry_answer_refused"]


def test_a_spent_budget_skips_the_retry_and_never_stops(monkeypatch):
    run_dir = _cite_run(monkeypatch)
    prompts = []

    def _spent(run_dir, category):
        raise rpr._ReaderBudgetExceeded("spent")
    monkeypatch.setattr(rpr, "_check_reader_budget", _spent)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm([_fenced(_cited_reading(period="2"))],
                                                         prompts))
    rpr.run_reader_worker(CAT, RUN_ID, run_dir)
    assert len(prompts) == 1
    doc = _checks(run_dir)
    assert doc["status"] == "flagged" and doc["retried"] is False
    assert doc["retry_skipped"] == "no retry: spent"


def test_a_check_that_raises_never_stops_the_reader(monkeypatch):
    run_dir = _cite_run(monkeypatch)
    prompts = []

    def _boom(*a, **k):
        raise RuntimeError("bug")
    monkeypatch.setattr(rp, "check_citation_values", _boom)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm([_fenced(_cited_reading(period="2"))],
                                                         prompts))
    dest = rpr.run_reader_worker(CAT, RUN_ID, run_dir)
    assert len(prompts) == 1 and dest.exists()
    doc = _checks(run_dir)
    assert doc["status"] == "error" and "RuntimeError: bug" in doc["error"]


def test_the_handoff_line_names_the_check_flag_on_only(monkeypatch):
    run_dir = _cite_run(monkeypatch)
    on = rpr._reader_handoff(CAT, RUN_ID, 0, run_dir)
    assert "Code checks every `path=value` you cite" in on["objective"]
    _set_orchestrator(V3_ON)
    assert "Code checks every" not in rpr._reader_handoff(CAT, RUN_ID, 0, run_dir)["objective"]


# ---------------------------------------------------------------------------
# 3. Under E-072: the readers' exploration copies
# ---------------------------------------------------------------------------

def test_under_explore_confirm_the_check_reads_the_exploration_copies(monkeypatch):
    run_dir = _ec_run(monkeypatch, flags=EC_OB_ON)
    _protocol_execution_part(run_dir)
    files, _gone = rpr._reader_received_files(CAT, run_dir)
    config_rel = rpr._reader_base_config_rel(run_dir)[len("artifacts/"):]
    assert all(r.startswith("exploration/") or r == config_rel for r in files), sorted(files)
    arts = run_dir / "artifacts"
    seen = yaml.safe_load((arts / "exploration" / "grid_evaluation.yaml").read_text(
        encoding="utf-8"))["grid"]["c_win"]["base"]["value"]
    full = yaml.safe_load((arts / "grid_evaluation.yaml").read_text(
        encoding="utf-8"))["grid"]["c_win"]["base"]["value"]
    assert not rp.value_matches(str(full), seen)   # the two files differ here
    reading = _reading(CAT, evidence=[f"grid_evaluation.grid.c_win.base.value={seen}"], sides=[])
    check = rpr._citation_value_check(CAT, run_dir, yaml.safe_dump(reading))
    assert check["n_bad"] == 0
    reading["evidence"] = [f"grid_evaluation.grid.c_win.base.value={full}"]
    check = rpr._citation_value_check(CAT, run_dir, yaml.safe_dump(reading))
    [bad] = check["items"][f"{CAT}-{RUN_ID}"]["bad"]
    assert bad["files"] == ["exploration/grid_evaluation.yaml"] and bad["actual"] == [seen]
    # a withheld pooled criterion: its all-window value is never a match
    reading["evidence"] = ["grid_evaluation.grid.c_pool.base.result=FAIL"]
    check = rpr._citation_value_check(CAT, run_dir, yaml.safe_dump(reading))
    assert check["items"][f"{CAT}-{RUN_ID}"]["bad"][0]["actual"] == [ec.WITHHELD]


# ---------------------------------------------------------------------------
# 4. In-run dedup
# ---------------------------------------------------------------------------

def _side(cat, n=1, claim=None, change=None, scores=2, run_id=RUN_ID) -> dict:
    s = {"proposal_id": f"{cat}-{run_id}-{n}", "claim": claim or _pure_claim(),
         "evidence": ["exploration only"], "scores": _scores(scores)}
    if change is not None:
        s["config_change"] = change
    return s


def _readings(sides: dict, run_id=RUN_ID) -> dict:
    return {cat: _reading(cat, run_id=run_id, sides=s) for cat, s in sides.items()}


CHANGE = [{"component_id": "shock_reversal", "field": "params.period", "before": 1, "after": 2}]


def test_the_same_tests_from_two_readers_merge_into_one_listing_both():
    groups = rf.side_finding_merges(_readings({
        "trade_efficiency": [_side("trade_efficiency")],
        "forecast_power": [_side("forecast_power")]}))
    [g] = groups
    assert g["finding_id"] == f"forecast_power-{RUN_ID}-1"          # categories sorted
    assert g["finding_ids"] == [f"forecast_power-{RUN_ID}-1", f"trade_efficiency-{RUN_ID}-1"]
    assert g["sources"] == [{"category": "forecast_power", "finding_id": g["finding_ids"][0]},
                            {"category": "trade_efficiency", "finding_id": g["finding_ids"][1]}]
    assert len(g["spec_hashes"]) == 1 and g["config_change"] is None


def test_what_is_not_merged():
    other = copy.deepcopy(_pure_claim())
    other["tests"].append({**copy.deepcopy(other["tests"][0]), "name": "second",
                           "outcome": {"kind": "fwd_return", "horizons": [2]}})
    none = {**_pure_claim(), "tests": "none", "missing_block": "m"}
    assert rf.side_finding_merges(_readings({            # different config change
        "trade_efficiency": [_side("trade_efficiency", change=CHANGE)],
        "forecast_power": [_side("forecast_power")]})) == []
    assert rf.side_finding_merges(_readings({            # a partial overlap
        "trade_efficiency": [_side("trade_efficiency", claim=other)],
        "forecast_power": [_side("forecast_power")]})) == []
    assert rf.side_finding_merges(_readings({            # tests: none
        "trade_efficiency": [_side("trade_efficiency", claim=none)],
        "forecast_power": [_side("forecast_power", claim=none)]})) == []
    same_change = rf.side_finding_merges(_readings({     # the same change: merged
        "trade_efficiency": [_side("trade_efficiency", change=CHANGE)],
        "forecast_power": [_side("forecast_power", change=copy.deepcopy(CHANGE))]}))
    assert len(same_change) == 1 and same_change[0]["config_change"] == CHANGE


def test_a_statement_or_score_difference_does_not_prevent_a_merge():
    words = {**_pure_claim(), "statement": "Other words, same test.", "rationale": "x"}
    groups = rf.side_finding_merges(_readings({
        "trade_efficiency": [_side("trade_efficiency", claim=words, scores=3)],
        "forecast_power": [_side("forecast_power", scores=1)],
        "profitability": [_side("profitability", scores=0)]}))
    assert len(groups) == 1 and len(groups[0]["sources"]) == 3


def _two_readers_same_test():
    return {"trade_efficiency": [_side("trade_efficiency")],
            "forecast_power": [_side("forecast_power")]}


def _sides_llm(prompts: list, sides: dict):
    from build_reports import REPORT_CATEGORIES

    async def _fake(prompt):
        prompts.append(prompt)
        cat = next(c for c in REPORT_CATEGORIES if f"reader_category: {c}\n" in prompt)
        return (_fenced(_reading(cat, sides=sides.get(cat, []))),
                {"usage": {}, "cost_usd": 0.0, "num_turns": 1})
    return _fake


def test_a_merged_finding_is_measured_and_counted_once(monkeypatch):
    run_dir = _ec_run(monkeypatch, flags=EC_OB_ON, conf_sign=1.0)
    _seed_dictionary()
    _protocol_execution_part(run_dir)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _sides_llm([], _two_readers_same_test()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    merges = yaml.safe_load((run_dir / "artifacts" / rf.MERGES_ARTIFACT).read_text(
        encoding="utf-8"))
    assert merges["note"] == rf.MERGE_NOT_AGREEMENT and len(merges["merged"]) == 1
    primary, dup = merges["merged"][0]["finding_ids"]
    [rec] = _confirmation(run_dir)["side_findings"]
    assert rec["finding_id"] == primary and rec["merged_finding_ids"] == [dup]
    assert [s["finding_id"] for s in rec["sources"]] == [primary, dup]
    assert rec["merge_note"] == rf.MERGE_NOT_AGREEMENT
    assert rec["confirmation_sign_retained"] is True
    ledger = ec.load_ledger(rpr.ROOT)
    assert set(ledger["findings"]) == {primary}
    key = ec.set_key(ec.load_split(run_dir / "artifacts")["confirmation"])
    assert ledger["by_set"] == {key: {"n_looks": 1, "n_comparisons": 1}}
    assert [ln for ln in ec.summary_lines(rpr.ROOT) if "Side findings:" in ln][0].startswith(
        "- Side findings: 1 (held 1,")
    # a resumed stage measures and counts nothing again
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert ec.load_ledger(rpr.ROOT)["by_set"] == {key: {"n_looks": 1, "n_comparisons": 1}}


def test_flag_off_the_two_proposals_stay_two_records_as_before(monkeypatch):
    """explore_confirm alone (observable_backtest off): unchanged -- two records,
    two looks, no merges file (what step 2 corrects, under its flag only)."""
    run_dir = _ec_run(monkeypatch, flags=EC_ON, conf_sign=1.0)
    _protocol_execution_part(run_dir)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _sides_llm([], _two_readers_same_test()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert not (run_dir / "artifacts" / rf.MERGES_ARTIFACT).exists()
    assert not (run_dir / "artifacts" / rp.CITATION_CHECKS_DIR).exists()
    recs = _confirmation(run_dir)["side_findings"]
    assert len(recs) == 2 and not any("sources" in r for r in recs)
    key = ec.set_key(ec.load_split(run_dir / "artifacts")["confirmation"])
    assert ec.load_ledger(rpr.ROOT)["by_set"] == {key: {"n_looks": 2, "n_comparisons": 2}}


def test_a_run_built_from_the_duplicate_resolves_the_primary():
    findings = {"forecast_power-run_990-1": {
        "finding_id": "forecast_power-run_990-1", "confirmation_sign_retained": ec.PENDING,
        "merged_finding_ids": ["trade_efficiency-run_990-1"]}}
    assert ec.pending_for(findings, "trade_efficiency-run_990-1", "run_991") \
        is findings["forecast_power-run_990-1"]
    assert ec.pending_for(findings, "profitability-run_990-1", "run_991") is None
    assert ec.pending_for(findings, "forecast_power-run_990-1", "run_991") \
        is findings["forecast_power-run_990-1"]


# decide-next ---------------------------------------------------------------

def _dn_side(cat, scores=2) -> dict:
    return {"proposal_id": f"{cat}-run_070-1", "kind": rp.SIDE_FINDING, "claim": _claim(),
            "evidence": ["e"], "scores": _scores(scores), "model_id": "m",
            "rubric_version": f"{cat}-reading-v1"}


def _merged_src(a, b, flags=None, primary_first=True) -> dict:
    src = _src([{"category": "forecast_power", "proposal": a},
                {"category": "trade_efficiency", "proposal": b}])
    ids = [a["proposal_id"], b["proposal_id"]]
    doc = rf.merges_doc("run_070", [{"finding_id": ids[0], "finding_ids": ids,
                                     "sources": [{"category": "forecast_power",
                                                  "finding_id": ids[0]},
                                                 {"category": "trade_efficiency",
                                                  "finding_id": ids[1]}],
                                     "spec_hashes": ["h"], "config_change": None}])
    src["side_finding_merges"] = rf.merge_index(doc)
    if flags:
        src["citation_flags"] = flags
    return src


def _decide(src) -> dict:
    inputs = _inputs(memory={"runs": {"run_070": _memory_entry()}}, runs={"run_070": src})
    return dn.decide(inputs, now="2026-10-08T00:00:00Z",
                     trigger={"after_run": "run_070", "after_entry": "E", "idea_status": "refuted"})


def test_a_merged_pair_is_one_candidate_with_the_primarys_scores():
    a, b = _dn_side("forecast_power", scores=1), _dn_side("trade_efficiency", scores=3)
    rec = _decide(_merged_src(a, b))
    [cand] = rec["candidates"]
    assert cand["candidate_id"] == "forecast_power-run_070-1" and cand["rank"] == 1
    assert cand["scores"]["confidence_real"] == 1          # never the higher of the two
    assert cand["merged_sources"] == [
        "runs/run_070/artifacts/proposals/forecast_power.yaml#forecast_power-run_070-1",
        "runs/run_070/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_070-1"]
    assert cand["merge_note"] == dn.MERGE_NOTE and cand["collapsed_sources"] == []
    assert "_merge" not in cand
    # without the merge file the existing collapse keeps the higher score (unchanged)
    src = _merged_src(a, b)
    del src["side_finding_merges"]
    [plain] = _decide(src)["candidates"]
    assert plain["candidate_id"] == "trade_efficiency-run_070-1" and "merged_sources" not in plain


def test_a_duplicate_whose_primary_is_ineligible_stays_its_own_candidate():
    a = {**_dn_side("forecast_power"), "claim": {**_claim(), "tests": "none",
                                                 "missing_block": "m"}}
    b = _dn_side("trade_efficiency")
    rec = _decide(_merged_src(a, b))
    elig = [c for c in rec["candidates"] if c["eligible"]]
    assert [c["candidate_id"] for c in elig] == ["trade_efficiency-run_070-1"]
    assert "merged_sources" not in elig[0]


def test_a_flagged_citation_is_a_warning_and_never_changes_eligibility_or_rank():
    jsonschema = pytest.importorskip("jsonschema")
    a, b = _dn_side("forecast_power"), _dn_side("trade_efficiency")
    bad = [{"path": PERIOD, "cited": "2", "status": rp.CITATION_MISMATCH, "actual": [3],
            "files": ["c.json"]}]
    rec = _decide(_merged_src(a, b, flags={"forecast_power-run_070-1": bad}))
    [cand] = rec["candidates"]
    assert cand["eligible"] is True and cand["rank"] == 1
    assert cand["warnings"] == [{"kind": dn.CITATION_WARNING, "bad": bad}]
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas"
                         / "decision_record.schema.json").read_text(encoding="utf-8"))
    errors = [e.message for e in jsonschema.Draft202012Validator(schema).iter_errors(
        yaml.safe_load(yaml.safe_dump(rec)))]
    assert errors == []
    lines = camp._candidate_warning_lines(rec, "d.yaml")
    assert lines == ["WARNING forecast_power-run_070-1: 1 cited value(s) do not match the file "
                     "the reader read, after its one retry (kept, flagged) -- warning only, "
                     "see d.yaml"]


def test_every_warning_kind_gets_a_log_line_and_the_class_line_is_unchanged():
    rec = {"candidates": [{"candidate_id": "c", "warnings": [
        {"kind": "unknown_component_class", "name": "XComponent", "suggestion": "YComponent"},
        {"kind": rf.WARN_REPEAT, "spec_hash": "h", "own_claim": False, "runs": []}]}]}
    assert camp._candidate_warning_lines(rec, "d") == [
        "WARNING c: reader names unknown component class XComponent (nearest real class: "
        "YComponent) -- warning only, see d",
        f"WARNING c: {rf.WARN_REPEAT} -- warning only, see d"]


def test_load_inputs_reads_the_two_files_only_when_they_exist(tmp_path):
    arts = tmp_path / "artifacts"
    arts.mkdir()
    assert dn._observable_inputs(arts) == {}
    rpr.save_yaml(arts / rf.MERGES_ARTIFACT, rf.merges_doc("run_070", []))
    (arts / rp.CITATION_CHECKS_DIR).mkdir()
    rpr.save_yaml(arts / rp.CITATION_CHECKS_DIR / "trade_efficiency.yaml",
                  {"items": {"trade_efficiency-run_070-1": {"bad": [{"path": "p"}]},
                             "trade_efficiency-run_070": {"bad": []}}})
    (arts / rp.CITATION_CHECKS_DIR / "profitability.yaml").write_text(": : not yaml [",
                                                                      encoding="utf-8")
    assert dn._observable_inputs(arts) == {
        "side_finding_merges": {}, "citation_flags": {"trade_efficiency-run_070-1": [{"path": "p"}]}}


# ---------------------------------------------------------------------------
# 5. Flag off: byte-identical
# ---------------------------------------------------------------------------

def _worker_outputs(monkeypatch, flags) -> tuple:
    run_dir = _cite_run(monkeypatch, flags=flags)
    prompts = []
    bad = _fenced(_cited_reading(period="2"))       # a mis-cited reading
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm([bad, bad], prompts))
    dest = rpr.run_reader_worker(CAT, RUN_ID, run_dir)
    audit = {k: {f: v for f, v in e.items() if f not in ("timestamp", "execution_time_seconds")}
             for k, e in _audit(run_dir).items()}
    return prompts, dest.read_bytes(), audit, (run_dir / "artifacts" / rp.CITATION_CHECKS_DIR)


def test_flag_off_the_reader_is_byte_identical(monkeypatch):
    import shutil
    absent = _worker_outputs(monkeypatch, V3_ON)
    shutil.rmtree(rpr.ROOT / "runs" / RUN_ID)
    off = _worker_outputs(monkeypatch, OB_OFF)
    assert absent[0] == off[0] and len(absent[0]) == 1      # no retry for a citation
    assert absent[1] == off[1] and absent[2] == off[2]
    assert not any("citation_check" in e for e in absent[2].values())
    assert not absent[3].exists() and not off[3].exists()


def test_flag_off_the_stage_writes_no_merges_and_no_checks(monkeypatch):
    run_dir = _cite_run(monkeypatch, flags=V3_ON)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _sides_llm([], {
        "trade_efficiency": [_side("trade_efficiency")],
        "profitability": [_side("profitability")]}))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert not (run_dir / "artifacts" / rf.MERGES_ARTIFACT).exists()
    assert not (run_dir / "artifacts" / rp.CITATION_CHECKS_DIR).exists()


def test_flag_off_confirm_findings_is_unchanged_without_merges(monkeypatch):
    run_dir = _ec_run(monkeypatch, flags=EC_ON, conf_sign=1.0)
    _protocol_execution_part(run_dir)
    readings = _readings(_two_readers_same_test())
    split = ec.load_split(run_dir / "artifacts")
    from test_e072_explore_confirm import _eras_holdout
    eras, holdout = _eras_holdout()
    kw = dict(base_variant="base", eras=eras, holdout_start=holdout)
    assert ec.confirm_findings(run_dir, RUN_ID, readings, split, **kw) \
        == ec.confirm_findings(run_dir, RUN_ID, readings, split, merges=None, **kw) \
        == ec.confirm_findings(run_dir, RUN_ID, readings, split, merges={}, **kw)


def test_the_run_scoped_files_include_the_new_ones():
    assert rf.MERGES_ARTIFACT in rpr._SPECIALIST_READERS_RUN_SCOPED_FILES
    assert rp.CITATION_CHECKS_DIR in rpr._SPECIALIST_READERS_RUN_SCOPED_DIRS


# ---------------------------------------------------------------------------
# 6. Final design after two reviews (PR #346): suggestions, keys, keep rule, kind
# ---------------------------------------------------------------------------

GRID = {"grid": {"residual_ic": {"base": {"value": 0.076977, "p_value_one_sided": 0.01937},
                                 "design_period_3": {"value": 0.075277}},
                 "realized_edge_to_cost_ratio": {"base": {"value": -1.2805}}}}


def test_a_shortened_path_stays_missing_and_names_the_real_one():
    """run_073: `grid_evaluation.residual_ic...` for `grid.residual_ic...`:
    suggested, never accepted -- the citation counts as missing."""
    [bad] = _check(["grid_evaluation.residual_ic.base.value: 0.076977"],
                   {"grid_evaluation.yaml": GRID})["bad"]
    assert bad["status"] == rp.CITATION_MISSING
    assert bad["suggestions"][0] == {"path": "grid_evaluation.grid.residual_ic.base.value",
                                     "file": "grid_evaluation.yaml", "value_matches": True}
    assert [s["path"] for s in bad["suggestions"]] == [
        "grid_evaluation.grid.residual_ic.base.value",
        "grid_evaluation.grid.realized_edge_to_cost_ratio.base.value",
        "grid_evaluation.grid.residual_ic.design_period_3.value"]
    # the suggested path itself is a valid citation, as written
    assert _check(["grid_evaluation.grid.residual_ic.base.value: 0.076977"],
                  {"grid_evaluation.yaml": GRID})["bad"] == []


def test_at_most_three_suggestions_the_cited_value_first_none_for_an_invented_key():
    files = {"g.yaml": {"a": {"value": 1}, "b": {"value": 2}, "c": {"value": 3},
                        "d": {"value": 4}}}
    [bad] = _check(["a.x.value=4"], files)["bad"]
    assert rp.CITATION_MAX_SUGGESTIONS == 3
    assert [s["path"] for s in bad["suggestions"]] == ["g.d.value", "g.a.value", "g.b.value"]
    assert [s["value_matches"] for s in bad["suggestions"]] == [True, False, False]
    [bad] = _check(["a.invented_key=4"], files)["bad"]
    assert bad["status"] == rp.CITATION_MISSING and bad["suggestions"] == []


def test_list_elements_are_suggested_as_any_element():
    files = {"r.yaml": {"variants": {"base": {"per_window": [{"core": {"corr": -0.0112}},
                                                            {"core": {"corr": 0.0196}}]}}}}
    [bad] = _check(["variants.base.per_window[1,2].core.corr = -0.0112"], files)["bad"]
    assert bad["suggestions"] == [{"path": "r.variants.base.per_window[*].core.corr",
                                   "file": "r.yaml", "value_matches": True}]


def test_every_suggestable_path_resolves_as_written_in_its_own_file():
    """A suggestion is always citable as written: every received key's path is
    rooted at its file's stem (a top-level scalar too, and a top-level key two
    files share), and re-resolves in that file."""
    files = {"reports/trade_efficiency.yaml": {"idea_status": "refuted", "variants": {"base": {
                 "per_window": {"2022-09": {"n": 3}}, "risks": {"a key": 1}}}},
             "grid_evaluation.yaml": {"idea_status": "supported", "variants": {"base": {"n": 7}},
                                      "blocks": [{"ic": 0.1}, {"ic": 0.2}]}}
    index = rp._cite_index(files)
    assert {e["path"] for e in index} >= {
        "trade_efficiency.idea_status", "grid_evaluation.idea_status",
        "trade_efficiency.variants.base.per_window.2022-09.n",
        'trade_efficiency.variants.base.risks["a key"]', "grid_evaluation.blocks[*].ic"}
    for e in index:
        value = f" = {e['values'][0]}" if e["values"] else ""
        [c] = rp.check_citation_values(files, [e["path"] + value])["citations"]
        assert c["path"] == e["path"], e
        assert c["status"] == (rp.CITATION_MATCH if value else rp.CITATION_PATH_ONLY), (e, c)
    [c] = _check(["grid_evaluation.idea_status: supported"], files)["citations"]
    assert c["status"] == rp.CITATION_MATCH       # the grid's, not the report's


def test_the_retry_line_shows_paths_and_never_a_value_from_the_files(monkeypatch):
    run_dir = _cite_run(monkeypatch)
    prompts = []
    doc = _cited_reading()
    doc["evidence"] = ["variants.base.slices.overall.trade_less_often.boundary_recross_rate=0.5"]
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm([_fenced(doc)], prompts))
    rpr.run_reader_worker(CAT, RUN_ID, run_dir)
    line = (f"- {CAT}-{RUN_ID}: `variants.base.slices.overall.trade_less_often."
            f"boundary_recross_rate` cited '0.5': path not found; nearest real paths: "
            f"`trade_efficiency.variants.base.slices.overall.fee_reduction_metrics."
            f"trade_less_often.boundary_recross_rate`, "
            f"`trade_efficiency.variants.base.slices.overall.boundary_recross_rate`\n")
    assert line in prompts[1]
    listed = prompts[1][len(prompts[0]):].split("The rule:")[0]
    assert "0.9487" not in listed                       # the file's value is never shown
    [bad] = _checks(run_dir)["items"][f"{CAT}-{RUN_ID}"]["bad"]
    assert bad["status"] == rp.CITATION_MISSING and len(bad["suggestions"]) == 2


@pytest.mark.parametrize("bad,line", [
    ({"path": "a.b", "cited": "2", "status": "mismatch", "actual": [3], "files": ["f.yaml"]},
     "- X: `a.b` cited '2': value does not match the file"),
    ({"path": "a.b", "cited": None, "status": "missing", "suggestions": []},
     "- X: `a.b` cited None: path not found"),
    ({"path": "a.b", "cited": "2", "status": "missing",
      "suggestions": [{"path": "f.a.c.b", "file": "f.yaml", "value_matches": True}]},
     "- X: `a.b` cited '2': path not found; nearest real paths: `f.a.c.b`"),
])
def test_a_retry_line_is_path_cited_value_and_problem(bad, line):
    assert rpr._citation_line("X", bad) == line


TE = {"variants": {"base": {"slices": {"per_window": {
    "2022-09": {"exit_efficiency": {"mean": -0.7213}}}}}}}
TE_PATH = "variants.base.slices.per_window.2022-09.exit_efficiency.mean"


def test_hyphenated_keys_resolve_and_an_unknown_one_is_cut_at_its_hyphen():
    """trade_efficiency's YYYY-MM per_window keys resolve; a hyphenated key the
    file does not have is cut at its first hyphen (the rest is prose)."""
    files = {"reports/trade_efficiency.yaml": TE}
    for ev in (f"{TE_PATH} = -0.72", f"{TE_PATH}=-0.72", f"{TE_PATH}: -0.7213 (worst window)"):
        assert [(c["path"], c["status"]) for c in _check([ev], files)["citations"]] == [
            (TE_PATH, rp.CITATION_MATCH)], ev
    assert _check([f"{TE_PATH} = -0.5"], files)["bad"][0]["status"] == rp.CITATION_MISMATCH
    # the key exists, a later one does not: missing as written (no cut)
    typo = "variants.base.slices.per_window.2022-09.exit_eff.mean"
    assert _check([f"{typo} = -0.72"], files)["bad"][0]["path"] == typo
    # n_trades-adjusted is not a key: `metrics.n_trades` followed by prose
    m = {"r.yaml": {"metrics": {"n_trades": 3012}}}
    assert _check(["metrics.n_trades-adjusted: 3012"], m)["citations"] == [
        {"path": "metrics.n_trades", "cited": None, "status": rp.CITATION_PATH_ONLY}]
    # the record-only D-048 resolver is unchanged (recorded under another flag)
    assert rp.resolve_evidence_paths(files, [TE_PATH])["unresolved"] == [
        "variants.base.slices.per_window.2022"]


def test_a_key_with_spaces_is_cited_in_quoted_brackets():
    card = {"risks": {"Cost drag spikes >80% at 0.15": {"severity": "high"}}}
    files = {"hypothesis_card.yaml": card}
    for ev in ('risks["Cost drag spikes >80% at 0.15"].severity = high',
               "risks['Cost drag spikes >80% at 0.15'].severity = high"):
        assert [c["status"] for c in _check([ev], files)["citations"]] == [rp.CITATION_MATCH]
    [bad] = _check(["risks.severity = high"], files)["bad"]
    assert bad["suggestions"][0]["path"] == (
        'hypothesis_card.risks["Cost drag spikes >80% at 0.15"].severity')


def test_dictionary_style_paths_are_not_checked():
    """`summary.` / `trades[]` (trade_diagnostics.json, never received) and
    `slices.` are no root of a received file: not a citation (no_path_items),
    unless a received file has that top-level key."""
    files = {"reports/trade_efficiency.yaml": {"variants": {"base": {"slices": {"overall": {
        "exit_reason_breakdown": {"signal_flip_pct": 99.16}}}}}}}
    res = _check(["summary.exit_reason_breakdown.signal_flip_pct = 1",
                  "slices.overall.exit_reason_breakdown.signal_flip_pct = 1",
                  "trades[*].mae = 0.5"], files)
    assert res["citations"] == [] and res["no_path_items"] == 3
    assert _check(["summary.n = 3"], {"d.yaml": {"summary": {"n": 3}}})["bad"] == []


def _retry_pair(monkeypatch, first, second):
    run_dir = _cite_run(monkeypatch)
    prompts = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm",
                        _llm([_fenced(first), _fenced(second)], prompts))
    dest = rpr.run_reader_worker(CAT, RUN_ID, run_dir)
    assert len(prompts) == 2
    return yaml.safe_load(dest.read_text(encoding="utf-8")), _checks(run_dir)


@pytest.mark.parametrize("period,ratio,n_retry", [
    ("2", "0.5", 2),     # more bad citations
    ("1", "0.5", 1),     # as many (a different one)
])
def test_a_retry_without_fewer_bad_citations_keeps_the_first_answer(monkeypatch, period, ratio,
                                                                   n_retry):
    """The retry answer replaces the first only with STRICTLY fewer bad
    citations; both counts are recorded."""
    first = _cited_reading(period="2")
    kept, doc = _retry_pair(monkeypatch, first, _cited_reading(period=period, ratio=ratio))
    assert kept["evidence"] == first["evidence"]
    assert kept["side_findings"][0]["evidence"] == first["side_findings"][0]["evidence"]
    assert doc["first_attempt_bad"] == 1 and doc["retry_attempt_bad"] == n_retry
    assert doc["kept_answer"] == "first" and doc["n_bad"] == 1 and doc["status"] == "flagged"


def test_a_retry_with_fewer_bad_citations_and_the_same_findings_is_kept(monkeypatch):
    second = _cited_reading(period="1")
    second["side_findings"][0]["claim"]["statement"] = "Reworded: wording is not structure."
    kept, doc = _retry_pair(monkeypatch, _cited_reading(period="2", ratio="0.5"), second)
    assert kept["side_findings"][0]["evidence"] == second["side_findings"][0]["evidence"]
    assert doc["first_attempt_bad"] == 2 and doc["retry_attempt_bad"] == 0
    assert doc["kept_answer"] == "retry" and doc["status"] == "clean"


def _another_test(doc):
    doc["side_findings"][0]["claim"]["tests"][0]["selector"]["q"] = 0.2


def _another_kind(doc):
    doc["side_findings"][0]["claim"]["kind"] = "direction_forecast"


def _one_more_finding(doc):
    extra = copy.deepcopy(doc["side_findings"][0])
    extra["proposal_id"] = f"{CAT}-{RUN_ID}-2"
    doc["side_findings"].append(extra)


def _one_finding_less(doc):
    doc["side_findings"] = []


@pytest.mark.parametrize("change", [_another_test, _another_kind, _one_more_finding,
                                    _one_finding_less])
def test_a_retry_that_changes_the_side_findings_keeps_the_first_answer(monkeypatch, change):
    """Fewer bad citations is not enough: the retry must propose the same side
    findings (count, claim kind, spec_hash set, item kind) as the first."""
    first = _cited_reading(period="2")
    second = _cited_reading(period="1")
    change(second)
    assert rf.reading_structure(first) != rf.reading_structure(second)
    kept, doc = _retry_pair(monkeypatch, first, second)
    assert "retry_answer_refused" not in doc            # a valid answer, refused by the guard
    assert kept["side_findings"] == first["side_findings"]
    assert doc["retry_attempt_bad"] < doc["first_attempt_bad"] == 1
    assert doc["kept_answer"] == "first" and doc["status"] == "flagged"


def test_a_retry_whose_check_errors_keeps_the_first_answer(monkeypatch):
    first = _cited_reading(period="2")
    real = rp.check_citation_values
    calls = []

    def _third_call_raises(*a, **k):
        calls.append(1)
        if len(calls) == 3:   # the first answer's check is 2 calls (one per item)
            raise RuntimeError("bug")
        return real(*a, **k)
    monkeypatch.setattr(rp, "check_citation_values", _third_call_raises)
    kept, doc = _retry_pair(monkeypatch, first, _cited_reading(period="1"))
    assert kept["side_findings"][0]["evidence"] == first["side_findings"][0]["evidence"]
    assert doc["kept_answer"] == "first" and doc["retry_attempt_bad"] is None


def test_the_same_tests_under_two_claim_kinds_are_not_merged():
    """finding_route routes by kind (a block kind PENDING, a pure kind
    IN_RUN), so the kind is part of the merge key."""
    import claim_card as cc
    block_kind = {**_pure_claim(), "kind": "direction_forecast"}
    assert not cc.check_claim(block_kind).errors
    assert ec.finding_route({"claim": block_kind})[0] != ec.finding_route(
        {"claim": _pure_claim()})[0]
    assert rf.side_finding_merges(_readings({
        "trade_efficiency": [_side("trade_efficiency", claim=block_kind)],
        "forecast_power": [_side("forecast_power")]})) == []
    assert len(rf.side_finding_merges(_readings({
        "trade_efficiency": [_side("trade_efficiency", claim=copy.deepcopy(block_kind))],
        "forecast_power": [_side("forecast_power", claim=block_kind)]}))) == 1


@pytest.mark.parametrize("cited,actual,ok", [
    # one number rule: rounded to the decimals written (half a unit of the last digit)
    ("8%", 0.083, True), ("-8%", -0.0791, True), ("5%", 0.054, True), ("2", 2.3, True),
    ("9", 9.3, True), ("10", 9.6, True), ("5", 5.4, True), ("-1", -0.8288, True),
    ("0.05", 0.054, True), ("0.5", 0.52, True), ("0.05", 0.056, False), ("2", 2.6, False),
    ("120 trades over 2022-09", 120, True), ("0.83.", 0.8288, True), ("5%.", 0.05, True),
    # the one exception: a 0 written with fewer than 2 decimals means |x| < 0.005
    ("0", 0.3, False), ("0", 0.004, True), ("-0", -0.004, True), ("0", 0.006, False),
    ("0.0", 0.006, False), ("0.00", 0.004, True), ("0.0", 0.004, True),
    # not a plain number: not checked (None), never a mismatch
    ("3k", 3012, None), ("3.3k", 3312, None), ("~3k trades", 2950, None),
    ("about 120", 120, None), ("approx 0.83", 0.8288, None), ("1M", 1000000, None),
    ("3.3kg", 3.3, None),
    # text: the file's whole text, ignoring case and surrounding spaces
    ("Trending_Up", "TRENDING_UP", True), ("  fail ", "FAIL", True),
    ("trending", "trending_up", False),
    ("robust across all windows", "not robust across all windows", False),
    ("the edge survives costs in every era",
     "it is false that the edge survives costs in every era", False),
    ("'directional accuracy above chance'",
     "Directional accuracy above chance on 4 of 6 windows", False),
])
def test_the_value_rule_final_design(cited, actual, ok):
    assert rp.value_matches(cited, actual) is ok


def test_a_number_written_another_way_is_not_checked_never_a_mismatch():
    files = {"r.yaml": {"metrics": {"n_trades": 3012, "sharpe": 0.8288}}}
    res = _check(["metrics.n_trades = 3k", "metrics.sharpe = approx 0.83"], files)
    assert [c["status"] for c in res["citations"]] == [rp.CITATION_PATH_ONLY] * 2
    assert res["bad"] == []


def test_a_path_is_read_from_the_file_named_else_the_first_file_that_has_it():
    """`variants` is a top-level key of several received files; the reader's
    own report (first in the received order) wins."""
    own = {"variants": {"base": {"n": 5}}}
    other = {"variants": {"base": {"n": 7, "m": 1}}}
    files = {"reports/trade_efficiency.yaml": own, "registry_summary.yaml": other}
    [bad] = _check(["variants.base.n = 7"], files)["bad"]
    assert bad["status"] == rp.CITATION_MISMATCH
    assert bad["files"] == ["reports/trade_efficiency.yaml"] and bad["actual"] == [5]
    assert _check(["variants.base.m = 1"], files)["bad"] == []          # only the other has it
    assert _check(["registry_summary.variants.base.n = 7"], files)["bad"] == []   # named


def test_the_received_files_start_with_the_readers_own_report(monkeypatch):
    run_dir = _cite_run(monkeypatch)
    files, _gone = rpr._reader_received_files(CAT, run_dir)
    assert list(files)[0] == f"reports/{CAT}.yaml"
