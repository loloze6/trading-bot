"""
C5.7b-2 -- score provenance, slices S2 + S4 (D-048;
engineering/review_2026-09-27/C5_7B_PROVENANCE_S1.md). Review finding C12.

Behind orchestrator.score_provenance.enabled (added by C5.7b-1):
  S2  `rubric_version` on a reader proposal is a closed per-category set
      (tools/reader_proposals.READER_RUBRIC_VERSIONS), pinned here to the literals
      in the five reader SKILL.md files. `load_proposals(..., strict_provenance=)`
      defaults False, so every existing `-v1` fixture stays valid; under the flag
      the reader stage passes True and an unknown / other-category / `-v1` value
      goes through the EXISTING reader retry path (one retry with the message
      appended, then the stage raises).
  S4  `resolve_evidence_paths(received_files, evidence)` (pure) measures which
      cited field paths exist in the files the reader received; the stage records
      it in the audit-log `provenance.citations` block. Record only (option A):
      nothing is rejected, retried or raised for a citation.

Proven with stubs only: no LLM, no API call, no backtest, no trial row, no holdout,
nothing under the real campaign_record/ or runs/ (tests/conftest.py's autouse
sandbox redirects rpr.ROOT).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import reader_proposals as rp  # noqa: E402

from test_e046a_slice5b_ii_b_readers_stage import (  # noqa: E402
    ALL_ON, RUN_ID, _seed_run, _set_orchestrator,
)
from test_c5_7b1_model_id_stamp import (  # noqa: E402
    BASELINE_ENTRY_KEYS, ON, _bytes, _loaded, _one_proposal, _reader_text,
)

CAT = "profitability"
REQUESTED = rpr._CLAUDE_WORKER_MODEL
SKILL_DIR = SR_ROOT / "workflow_artifacts" / "skills" / "readers"
CATEGORIES = ["profitability", "forecast_power", "regime_power", "component_attribution",
              "trade_efficiency"]


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _skill_text(cat: str) -> str:
    return (SKILL_DIR / f"{cat}-reader" / "SKILL.md").read_text(encoding="utf-8")


def _write(tmp_path: Path, cat: str, proposals: list) -> Path:
    d = tmp_path / "proposals"
    d.mkdir(exist_ok=True)
    (d / f"{cat}.yaml").write_text(yaml.safe_dump(proposals, sort_keys=False), encoding="utf-8")
    return d


def _proposal(cat=CAT, rubric=None, evidence=None, pid=None, n=1) -> dict:
    p = _one_proposal(pid=pid or f"{cat}-run_990-{n}")
    p["rubric_version"] = rubric if rubric is not None else rp.READER_RUBRIC_VERSIONS[cat]
    if evidence is not None:
        p["evidence"] = evidence
    return p


def _seq_llm(texts: list, calls: list | None = None, models=("claude-haiku-4-5",)):
    """An async stand-in for _invoke_reader_llm returning `texts` in order."""
    it = iter(texts)

    async def _fake(prompt: str):
        if calls is not None:
            calls.append(prompt)
        meta = {"usage": {"input_tokens": 10, "output_tokens": 5}, "cost_usd": 0.0, "num_turns": 1}
        if models is not None:
            meta["models"] = list(models)
        return next(it), meta
    return _fake


def _run_reader(monkeypatch, llm, orchestrator=ON, report=None, registry="keep", grid="keep"):
    """Seed a run (optionally with a realistic report / registry / grid) and run
    ONE reader (profitability) through run_reader_worker."""
    _set_orchestrator(orchestrator)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    arts = run_dir / "artifacts"
    if report is not None:
        rpr.save_yaml(arts / "reports" / f"{CAT}.yaml", report)
    if registry != "keep":
        rpr.save_yaml(arts / "registry_summary.yaml", registry)
    if grid != "keep":
        rpr.save_yaml(arts / "grid_evaluation.yaml", grid)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", llm)
    dest = rpr.run_reader_worker(CAT, RUN_ID, run_dir, stage_attempt=0)
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    return run_dir, dest, audit


def _entry(audit, retry=None):
    suffix = f"_retry{retry}" if retry else ""
    return audit[f"specialist_readers_{CAT}_attempt_0{suffix}"]


REPORT = {
    "category": CAT,
    "variants": {"base": {"slices": {
        "overall": {"diagnostics": {"median_cost_drag_pct": 142.82, "median_gross_pnl": 21.94}},
        "per_window": [{"core": {"sharpe": 0.1, "cost_drag_pct": 120.0}},
                       {"core": {"sharpe": -0.2, "cost_drag_pct": 90.0}}],
        "per_regime": {"trending": {"core": {"sharpe": 0.3}}},
        "per_symbol": {"BTCUSDT": [{"core": {"cost_drag_pct": 120.0}}, {"core": {"cost_drag_pct": 90.0}}]},
    }}},
}
REGISTRY = {
    "schema_version": 1, "run_id": RUN_ID,
    "registry": {"n_blocks": 1, "revision": 3, "n_forecast_blocks": 1, "grouping": "none"},
    "this_run": {"idea_status": "refuted", "block_type": None, "reason": "no_block_manifest",
                 "type_already_registered": None, "neighbour_block_ids": [],
                 "correlation_to_composite": {"status": "no_composite", "max_abs": None}},
    "blocks": [{"block_id": "b1", "relation_to_this_run": None, "residual_ic": 0.02}],
}
GRID = {"result": "REFUTED", "criteria": [{"id": "c1", "value": 0.4}], "evaluated_at": "t"}
FILES = {"reports/profitability.yaml": REPORT, "grid_evaluation.yaml": GRID,
         "registry_summary.yaml": REGISTRY}


def _resolve(evidence, files=FILES):
    return rp.resolve_evidence_paths(files, evidence)


# ---------------------------------------------------------------------------
# S2a. the closed set is pinned to the SKILL files
# ---------------------------------------------------------------------------

def test_the_closed_set_covers_exactly_the_reader_categories():
    assert sorted(rp.READER_RUBRIC_VERSIONS) == sorted(CATEGORIES)
    assert sorted(rpr._reader_categories()) == sorted(CATEGORIES)


@pytest.mark.parametrize("cat", CATEGORIES)
def test_the_rubric_literal_in_each_skill_file_is_the_constant(cat):
    """Each SKILL carries exactly one rubric_version literal; the constant is it."""
    literals = re.findall(r'rubric_version:\s*"([^"]+)"', _skill_text(cat))
    assert literals == [f"{cat}-reader-v2"], literals
    assert rp.READER_RUBRIC_VERSIONS[cat] == literals[0]


# ---------------------------------------------------------------------------
# S2b. strict_provenance in load_proposals
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad", [
    "made-up-v2",                      # unknown
    "forecast_power-reader-v2",        # another category's rubric
    "profitability-reader-v1",         # the old value
    "profitability-reader-v3",         # a future value the constant does not know
    "profitability-reader-v2 ",        # not an exact match
])
def test_strict_rejects_unknown_other_category_and_v1(tmp_path, bad):
    d = _write(tmp_path, CAT, [_proposal(rubric=bad)])
    with pytest.raises(rp.ProposalError, match=r"rubric_version=.* write exactly 'profitability-reader-v2'"):
        rp.load_proposals(d, [CAT], strict_provenance=True)


@pytest.mark.parametrize("value", ["made-up-v2", "forecast_power-reader-v2",
                                   "profitability-reader-v1", "profitability-reader-v3"])
def test_default_accepts_what_strict_rejects(tmp_path, value):
    d = _write(tmp_path, CAT, [_proposal(rubric=value)])
    assert rp.load_proposals(d, [CAT])[CAT][0]["rubric_version"] == value
    assert rp.load_proposals(d, [CAT], strict_provenance=False)[CAT][0]["rubric_version"] == value


@pytest.mark.parametrize("cat", CATEGORIES)
def test_strict_accepts_each_categorys_own_v2(tmp_path, cat):
    d = _write(tmp_path, cat, [_proposal(cat=cat)])
    assert rp.load_proposals(d, [cat], strict_provenance=True)[cat][0]["rubric_version"] == f"{cat}-reader-v2"


def test_strict_rejects_an_unlisted_category(tmp_path):
    d = _write(tmp_path, "zzz", [{**_proposal(), "proposal_id": "zzz-run_990-1"}])
    with pytest.raises(rp.ProposalError, match="no closed rubric_version is defined for category 'zzz'"):
        rp.load_proposals(d, ["zzz"], strict_provenance=True)


def test_an_empty_or_absent_file_is_still_fine_under_strict(tmp_path):
    d = tmp_path / "proposals"
    d.mkdir()
    (d / f"{CAT}.yaml").write_text("[]\n", encoding="utf-8")
    assert rp.load_proposals(d, [CAT, "regime_power"], strict_provenance=True) == \
        {CAT: [], "regime_power": []}


def test_brief_cards_are_untouched_brief_card_v1_is_still_the_card_rubric():
    import decide_next as dn
    assert dn.BRIEF_CARD_RUBRIC == "brief-card-v1"
    assert "brief-card-v1" not in rp.READER_RUBRIC_VERSIONS.values()


# ---------------------------------------------------------------------------
# S2c. wired into the reader stage under the flag (existing retry path)
# ---------------------------------------------------------------------------

def test_reader_strictness_is_empty_flag_off_and_strict_flag_on():
    _set_orchestrator(ALL_ON)
    assert rpr._reader_strictness() == {}
    _set_orchestrator({**ALL_ON, "score_provenance": {"enabled": False}})
    assert rpr._reader_strictness() == {}
    _set_orchestrator(ON)
    assert rpr._reader_strictness() == {"strict_provenance": True}


def test_flag_on_a_v1_reader_output_is_retried_and_the_message_reaches_the_reader(monkeypatch):
    calls = []
    bad = _reader_text([_proposal(rubric="profitability-reader-v1")])
    good = _reader_text([_proposal()])
    run_dir, dest, audit = _run_reader(monkeypatch, _seq_llm([bad, good], calls))
    assert len(calls) == 2
    assert "YOUR PREVIOUS OUTPUT FAILED VALIDATION" in calls[1]
    assert "rubric_version='profitability-reader-v1'" in calls[1]
    assert "write exactly 'profitability-reader-v2'" in calls[1]
    assert "YOUR PREVIOUS OUTPUT FAILED" not in calls[0]
    assert _loaded(dest)[0]["rubric_version"] == "profitability-reader-v2"
    assert f"specialist_readers_{CAT}_attempt_0" in audit and \
        f"specialist_readers_{CAT}_attempt_0_retry1" in audit


@pytest.mark.parametrize("bad", ["made-up-v2", "forecast_power-reader-v2", "profitability-reader-v1"])
def test_flag_on_a_second_rubric_failure_drops_the_proposal_and_records_it(monkeypatch, bad):
    """CUL-380: the wrong-rubric proposal never reaches the proposals file and
    the refusal is recorded; the run is no longer stopped."""
    calls = []
    text = _reader_text([_proposal(rubric=bad)])
    _, dest, audit = _run_reader(monkeypatch, _seq_llm([text, text], calls))
    assert len(calls) == 2                                   # exactly one retry
    assert _loaded(dest) == []
    run_dir = rpr.ROOT / "runs" / RUN_ID
    assert (run_dir / "artifacts" / f"debug_specialist_readers_{CAT}_raw_output.txt").exists()
    [drop] = audit[f"specialist_readers_{CAT}_attempt_0_retry1"]["dropped_proposals"]
    assert "rubric_version" in drop["error"]


def test_flag_off_the_same_v1_output_is_accepted_first_time(monkeypatch):
    calls = []
    text = _reader_text([_proposal(rubric="profitability-reader-v1")])
    _, dest, audit = _run_reader(monkeypatch, _seq_llm([text], calls), ALL_ON)
    assert len(calls) == 1
    assert _loaded(dest)[0]["rubric_version"] == "profitability-reader-v1"


def test_the_resume_revalidation_is_strict_too_under_the_flag(monkeypatch):
    """A proposals file left by a pre-flag attempt (`-v1`) stops a flag-on resume."""
    _set_orchestrator(ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    proposals_dir = run_dir / "artifacts" / "proposals"
    proposals_dir.mkdir(parents=True, exist_ok=True)
    (proposals_dir / f"{CAT}.yaml").write_text(
        yaml.safe_dump([_proposal(rubric="profitability-reader-v1")]), encoding="utf-8")
    with pytest.raises(rp.ProposalError, match="rubric_version"):
        rpr._run_specialist_readers(RUN_ID, run_dir, 0)


def test_flag_off_load_proposals_is_called_exactly_as_before(monkeypatch):
    """Byte-for-byte the pre-change call: no new keyword when the flag is off."""
    seen = []
    real = rp.load_proposals

    def spy(*args, **kwargs):
        seen.append((len(args), dict(kwargs)))
        return real(*args, **kwargs)
    monkeypatch.setattr(rp, "load_proposals", spy)
    text = _reader_text([_proposal(rubric="profitability-reader-v1")])
    _run_reader(monkeypatch, _seq_llm([text]), ALL_ON)
    assert seen and all(kw == {} for _, kw in seen)


# ---------------------------------------------------------------------------
# S4a. the resolver, table-driven from the SKILL files' own examples
# ---------------------------------------------------------------------------

def _skill_examples(cat: str) -> tuple:
    """(GOOD evidence list, BAD evidence list) from the SKILL's `evidence` format rule."""
    text = _skill_text(cat)
    m = re.search(r"# GOOD[^\n]*\n(?P<good>.*?)# BAD[^\n]*\n(?P<bad>.*?)```", text, re.S)
    assert m, f"{cat}: no GOOD/BAD example found"
    good = yaml.safe_load(m.group("good"))["evidence"]
    bad = yaml.safe_load(m.group("bad"))["evidence"]
    assert isinstance(good, list) and isinstance(bad, list) and good and bad
    return good, bad


def _doc_for(token: str):
    """Build a nested doc for one token, honouring `[*]`, `[]`, `[n]`, `[name]`."""
    def build(steps):
        if not steps:
            return True
        key, brackets = steps[0]
        inner = build(steps[1:])
        for b in reversed(brackets):
            if b.isdigit():
                inner = [{} for _ in range(int(b))] + [inner]
            elif b in ("*", ""):
                inner = [inner]
            else:
                inner = {b: inner}
        return {key: inner}
    return build(rp._cite_steps(token))


def _merge(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        for k, v in b.items():
            a[k] = _merge(a[k], v) if k in a else v
        return a
    return b if a is True else a


@pytest.mark.parametrize("cat", CATEGORIES)
def test_each_skills_good_example_has_paths_and_bad_example_has_none(cat):
    good, bad = _skill_examples(cat)
    res = rp.resolve_evidence_paths({}, good)
    assert res["no_path_items"] == 0                     # every GOOD item cites a path
    assert res["resolved"] == [] and res["unresolved"]   # ... none exists in an empty report
    res_bad = rp.resolve_evidence_paths({}, bad)
    assert res_bad == {"resolved": [], "unresolved": [], "no_path_items": len(bad)}


@pytest.mark.parametrize("cat", CATEGORIES)
def test_each_skills_good_example_resolves_against_a_report_that_holds_the_paths(cat):
    good, _ = _skill_examples(cat)
    tokens = rp.resolve_evidence_paths({}, good)["unresolved"]
    assert tokens and all(t.startswith("variants.") for t in tokens)
    doc: dict = {}
    for t in tokens:
        doc = _merge(doc, _doc_for(t))
    res = rp.resolve_evidence_paths({"report": doc}, good)
    assert res["resolved"] == tokens and res["unresolved"] == [] and res["no_path_items"] == 0


def test_the_profitability_good_example_by_hand():
    good, bad = _skill_examples("profitability")
    res = _resolve(good)
    assert res["resolved"] == [
        "variants.base.slices.overall.diagnostics.median_cost_drag_pct",
        "variants.base.slices.per_window[*].core.cost_drag_pct",  # CUL-370: core in per_window only
    ]
    assert res["unresolved"] == [] and res["no_path_items"] == 0
    assert _resolve(bad) == {"resolved": [], "unresolved": [], "no_path_items": 1}


def test_regime_power_good_example_index_and_trailing_value():
    good, _ = _skill_examples("regime_power")
    report = {"variants": {"base": {"slices": {"per_window": [
        {}, {}, {"hindsight_lag": {"median_lag_bars": 14}}]}}}}
    res = rp.resolve_evidence_paths({"r": report}, good)
    assert res["resolved"] == ["variants.base.slices.per_window[2].hindsight_lag.median_lag_bars"]
    assert res["unresolved"] == [] and res["no_path_items"] == 0
    # the same example against a report with only two windows: index 2 is out of range
    short = {"variants": {"base": {"slices": {"per_window": [{}, {}]}}}}
    assert rp.resolve_evidence_paths({"r": short}, good)["unresolved"] == \
        ["variants.base.slices.per_window[2].hindsight_lag.median_lag_bars"]


# ---------------------------------------------------------------------------
# S4b. normalisation
# ---------------------------------------------------------------------------

def test_star_and_empty_brackets_match_any_element():
    ev = ["variants.base.slices.per_symbol.BTCUSDT[*].core.cost_drag_pct all > 100%",
          "variants.base.slices.per_symbol.BTCUSDT[].core.cost_drag_pct",
          "variants.base.slices.per_window[*].core.sharpe",
          "variants.base.slices.per_symbol.BTCUSDT[*]"]
    res = _resolve(ev)
    assert len(res["resolved"]) == 4 and res["unresolved"] == []


def test_star_needs_a_list_and_a_matching_element():
    res = _resolve([
        "variants.base.slices.per_regime.trending[*].core",            # a mapping, not a list
        "variants.base.slices.per_symbol.BTCUSDT[*].core.nope",       # no element has it
        "variants.base.slices.per_window[*].core.sharpe",             # ok
    ])
    assert res["resolved"] == ["variants.base.slices.per_window[*].core.sharpe"]
    assert len(res["unresolved"]) == 2


def test_empty_list_resolves_a_bare_star_but_not_a_path_below_it():
    files = {"r": {"variants": {"base": {"slices": {"per_window": []}}}}}
    assert _resolve(["variants.base.slices.per_window[*]"], files)["resolved"]
    assert _resolve(["variants.base.slices.per_window[*].core"], files)["unresolved"]


def test_numeric_index_in_and_out_of_range():
    res = _resolve(["variants.base.slices.per_window[1].core.sharpe=-0.2",
                    "variants.base.slices.per_window[7].core.sharpe",
                    "variants.base.slices.overall[0].x"])
    assert res["resolved"] == ["variants.base.slices.per_window[1].core.sharpe"]
    assert res["unresolved"] == ["variants.base.slices.per_window[7].core.sharpe",
                                 "variants.base.slices.overall[0].x"]


def test_trailing_value_and_prose_are_dropped_and_the_value_is_not_compared():
    res = _resolve(["variants.base.slices.overall.diagnostics.median_cost_drag_pct=999999 -- wrong number",
                    "variants.base.slices.overall.diagnostics.median_gross_pnl=+21.94, positive;"])
    assert res["resolved"] == ["variants.base.slices.overall.diagnostics.median_cost_drag_pct",
                               "variants.base.slices.overall.diagnostics.median_gross_pnl"]
    assert res["unresolved"] == []


def test_a_path_can_end_a_sentence_and_be_wrapped_in_punctuation():
    res = _resolve(["(see variants.base.slices.overall.diagnostics.median_gross_pnl).",
                    "the field `variants.base.slices.per_regime.trending.core.sharpe`, above 0.03."])
    assert len(res["resolved"]) == 2 and res["unresolved"] == []


def test_named_bracket_indexes_a_mapping():
    res = _resolve(["variants.base.slices.per_regime[trending].core.sharpe",
                    "variants.base.slices.per_regime[range].core.sharpe"])
    assert len(res["resolved"]) == 1 and len(res["unresolved"]) == 1


def test_an_unknown_key_is_unresolved_and_numbers_and_prose_are_not_paths():
    res = _resolve(["variants.base.slices.overall.diagnostics.not_a_field=1",
                    "corr fell below 0.03 in 4/5 windows, i.e. no edge (e.g. Rule 2)."])
    assert res["unresolved"] == ["variants.base.slices.overall.diagnostics.not_a_field"]
    assert res["resolved"] == [] and res["no_path_items"] == 1


def test_duplicates_are_reported_once_in_first_seen_order():
    p = "variants.base.slices.overall.diagnostics.median_gross_pnl"
    res = _resolve([f"{p}=1", "variants.base.slices.per_window[0].core.sharpe", f"{p}=2"])
    assert res["resolved"] == [p, "variants.base.slices.per_window[0].core.sharpe"]


def test_a_path_broken_across_lines_resolves_its_prefix():
    """The SKILL example folds `...per_regime.mean_reversion.` / `keltner={...}`
    over two lines; the prefix is a path, the rest is prose."""
    files = {"r": {"variants": {"base": {"slices": {"per_regime": {"mean_reversion": {"keltner": 1}}}}}}}
    res = rp.resolve_evidence_paths(
        files, ["variants.base.slices.per_regime.mean_reversion.\n     keltner={n: 38}"])
    assert res["resolved"] == ["variants.base.slices.per_regime.mean_reversion"]


# ---------------------------------------------------------------------------
# S4c. slices that are unavailable, and the other received files
# ---------------------------------------------------------------------------

def test_an_unavailable_slice_resolves_its_flag_but_not_the_fields_it_lacks():
    files = {"r": {"variants": {"base": {"slices": {
        "overall": {"unavailable": True, "reason": "no debug_info.components.* columns"},
        "per_window": [{"core": {"sharpe": 0.1}}]}}}}}
    res = rp.resolve_evidence_paths(files, [
        "variants.base.slices.overall.unavailable=true (no components columns)",
        "variants.base.slices.overall.diagnostics.median_cost_drag_pct=1.0",
        "variants.base.slices.per_window[0].core.sharpe=0.1"])
    assert res["resolved"] == ["variants.base.slices.overall.unavailable",
                               "variants.base.slices.per_window[0].core.sharpe"]
    assert res["unresolved"] == ["variants.base.slices.overall.diagnostics.median_cost_drag_pct"]


def test_registry_summary_root_resolves():
    res = _resolve([
        "registry_summary.yaml this_run.idea_status=refuted decided the distance score",
        "registry.n_forecast_blocks=1 > 0 so correlation is not measurable",
        "this_run.correlation_to_composite.max_abs=null",
        "blocks[*].relation_to_this_run is null for every row",
        "this_run.patches_registered_block=None",                     # not in this summary
    ])
    assert res["resolved"] == ["this_run.idea_status", "registry.n_forecast_blocks",
                               "this_run.correlation_to_composite.max_abs",
                               "blocks[*].relation_to_this_run"]
    assert res["unresolved"] == ["this_run.patches_registered_block"]


def test_grid_evaluation_top_level_keys_are_roots():
    res = _resolve(["criteria[0].value=0.4 misses the floor", "criteria[3].value", "result=REFUTED"])
    assert res["resolved"] == ["criteria[0].value"]
    assert res["unresolved"] == ["criteria[3].value"]
    assert res["no_path_items"] == 1                    # `result=REFUTED` has no dotted path


def test_a_missing_file_makes_its_rooted_paths_unresolved_not_ignored():
    files = {"reports/profitability.yaml": REPORT, "grid_evaluation.yaml": None,
             "registry_summary.yaml": None}
    res = _resolve(["this_run.idea_status=refuted", "registry.n_blocks=1",
                    "variants.base.slices.overall.diagnostics.median_gross_pnl"], files)
    assert res["unresolved"] == ["this_run.idea_status", "registry.n_blocks"]
    assert res["resolved"] == ["variants.base.slices.overall.diagnostics.median_gross_pnl"]
    res = rp.resolve_evidence_paths({}, ["variants.base.slices.overall.x"])
    assert res["unresolved"] == ["variants.base.slices.overall.x"]


def test_no_path_items_counts_items_without_a_rooted_path():
    res = _resolve(["The strategy loses too much to fees.", "slices.overall.x=1",
                    "variants.base.slices.per_window[0].core.sharpe", ""])
    assert res["no_path_items"] == 3 and len(res["resolved"]) == 1


def test_the_resolver_is_pure_and_never_raises_on_odd_items():
    files = {"r": {"variants": {"base": {}}}}
    assert rp.resolve_evidence_paths(files, [None, 3, ["x"], {"a": 1}, "variants.base.x"]) == \
        {"resolved": [], "unresolved": ["variants.base.x"], "no_path_items": 4}
    with pytest.raises(TypeError):
        rp.resolve_evidence_paths(files, "not a list")
    with pytest.raises(TypeError):
        rp.resolve_evidence_paths([], ["variants.a.b"])


# ---------------------------------------------------------------------------
# S4d. recorded in the audit log under the flag; never rejects, never raises
# ---------------------------------------------------------------------------

EVIDENCE = ["variants.base.slices.overall.diagnostics.median_cost_drag_pct=142.82 -- fees dominate",
            "variants.base.slices.per_symbol.BTCUSDT[*].core.cost_drag_pct all > 100%",
            "variants.base.slices.overall.diagnostics.invented_field=3",
            "this_run.idea_status=refuted",
            "The strategy loses too much to fees."]


def test_the_citation_block_is_recorded_under_the_flag(monkeypatch):
    text = _reader_text([_proposal(evidence=EVIDENCE)])
    _, dest, audit = _run_reader(monkeypatch, _seq_llm([text]), report=REPORT,
                                 registry=REGISTRY, grid=GRID)
    cit = _entry(audit)["provenance"]["citations"]
    assert cit["files_read"] == ["grid_evaluation.yaml", "registry_summary.yaml",
                                 f"reports/{CAT}.yaml"]
    assert cit["files_unavailable"] == []
    assert cit["proposals"] == {f"{CAT}-run_990-1": {
        "resolved": ["variants.base.slices.overall.diagnostics.median_cost_drag_pct",
                     "variants.base.slices.per_symbol.BTCUSDT[*].core.cost_drag_pct",
                     "this_run.idea_status"],
        "unresolved": ["variants.base.slices.overall.diagnostics.invented_field"],
        "no_path_items": 1}}
    # record only: the proposal was accepted as written
    assert _loaded(dest)[0]["evidence"] == EVIDENCE
    # the block already sits beside the S0/S1 keys
    assert {"requested", "observed_models", "mismatch"} <= set(_entry(audit)["provenance"])


def test_an_all_unresolved_citation_set_is_still_accepted_and_never_retried(monkeypatch):
    calls = []
    text = _reader_text([_proposal(evidence=["variants.nope.x.y=1", "registry.nope=2"])])
    _, dest, audit = _run_reader(monkeypatch, _seq_llm([text], calls), report=REPORT,
                                 registry=REGISTRY, grid=GRID)
    assert len(calls) == 1 and dest.exists()
    (rec,) = _entry(audit)["provenance"]["citations"]["proposals"].values()
    assert rec["resolved"] == [] and len(rec["unresolved"]) == 2


def test_an_absent_grid_and_an_unparseable_registry_are_listed_not_fatal(tmp_path):
    """(The reader's prompt builder requires all three files, so this is the
    defensive path: a file that vanished or is unreadable after the prompt.)"""
    arts = tmp_path / "artifacts"
    rpr.save_yaml(arts / "reports" / f"{CAT}.yaml", {"marker": {"x": 1}})
    (arts / "registry_summary.yaml").write_text("a: [unclosed\n", encoding="utf-8")
    body = yaml.safe_dump([_proposal(evidence=["this_run.idea_status", "marker.x"])])
    cit = rpr._citation_provenance(CAT, tmp_path, body)
    assert cit["files_unavailable"] == ["grid_evaluation.yaml", "registry_summary.yaml"]
    assert cit["files_read"] == [f"reports/{CAT}.yaml"]
    (rec,) = cit["proposals"].values()
    assert rec == {"resolved": ["marker.x"], "unresolved": ["this_run.idea_status"],
                   "no_path_items": 0}


def test_a_resolver_error_is_recorded_per_proposal_and_never_raised(monkeypatch):
    def boom(files, evidence):
        raise RuntimeError("walker exploded")
    monkeypatch.setattr(rp, "resolve_evidence_paths", boom)
    text = _reader_text([_proposal(evidence=EVIDENCE)])
    _, dest, audit = _run_reader(monkeypatch, _seq_llm([text]), report=REPORT)
    cit = _entry(audit)["provenance"]["citations"]
    assert cit["proposals"] == {f"{CAT}-run_990-1": {"error": "RuntimeError: walker exploded"}}
    assert dest.exists() and _loaded(dest)[0]["evidence"] == EVIDENCE   # the reader still completed


def test_a_failure_outside_the_resolver_is_recorded_as_one_error(monkeypatch):
    def boom():
        raise RuntimeError("module gone")
    monkeypatch.setattr(rpr, "_reader_proposals_module", boom)
    block = rpr._citation_provenance(CAT, Path("does-not-matter"), "[]\n")
    assert block == {"error": "RuntimeError: module gone"}


def test_a_body_that_is_not_a_list_records_no_proposals(tmp_path):
    (tmp_path / "artifacts").mkdir()
    block = rpr._citation_provenance(CAT, tmp_path, "just: a mapping\n")
    assert block["proposals"] == {} and block["files_read"] == []
    assert block["files_unavailable"] == ["grid_evaluation.yaml", "registry_summary.yaml",
                                          f"reports/{CAT}.yaml"]


# ---------------------------------------------------------------------------
# flag-off byte identity
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("orchestrator", [ALL_ON, {**ALL_ON, "score_provenance": {"enabled": False}}])
def test_flag_off_reader_file_and_audit_entry_are_unchanged(monkeypatch, orchestrator):
    # a `-v1` proposal that cites real paths: flag off it is written verbatim, and
    # the audit entry carries neither a provenance nor a citations key
    text = _reader_text([_proposal(rubric="profitability-reader-v1", evidence=EVIDENCE)])
    calls = []
    _, dest, audit = _run_reader(monkeypatch, _seq_llm([text], calls, models=["claude-sonnet-4-5"]),
                                 orchestrator, report=REPORT, registry=REGISTRY, grid=GRID)
    assert len(calls) == 1
    assert _bytes(dest) == (rpr._READER_OUTPUT_BLOCK_RE.findall(text)[0].strip() + "\n").encode("utf-8")
    entry = _entry(audit)
    assert set(entry) == BASELINE_ENTRY_KEYS and "provenance" not in entry
    assert set(audit) == {f"specialist_readers_{CAT}_attempt_0"}


def test_the_flag_on_stamp_and_flag_off_file_differ_only_in_the_stamped_field(monkeypatch):
    """Sanity: with a valid v2 proposal the flag adds provenance and stamps model_id,
    and changes nothing else in the proposal (C5.7b-1 behaviour, unchanged here)."""
    text = _reader_text([_proposal(evidence=EVIDENCE)])
    _, dest_off, _ = _run_reader(monkeypatch, _seq_llm([text]), ALL_ON, report=REPORT)
    off = _loaded(dest_off)
    _, dest_on, _ = _run_reader(monkeypatch, _seq_llm([text]), ON, report=REPORT)
    on = _loaded(dest_on)
    assert [{k: v for k, v in p.items() if k != "model_id"} for p in on] == \
        [{k: v for k, v in p.items() if k != "model_id"} for p in off]
