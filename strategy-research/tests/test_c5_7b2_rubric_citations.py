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

from _reader_test_helpers import (  # noqa: E402
    ALL_ON, BASELINE_ENTRY_KEYS, ON, RUN_ID, _bytes, _loaded, _one_proposal, _reader_text,
    _seed_run, _set_orchestrator,
)

CAT = "profitability"
REQUESTED = rpr._CLAUDE_WORKER_MODEL
SKILL_DIR = SR_ROOT / "workflow_artifacts" / "skills" / "readers"
CATEGORIES = ["profitability", "forecast_power", "regime_power", "component_attribution",
              "trade_efficiency"]
# Independent pin of each SKILL's rubric literal. regime_power is -v3 since CUL-381
# removed detector_health from its report and its scoring rows.
EXPECTED_RUBRIC = {c: f"{c}-reader-v2" for c in CATEGORIES}
EXPECTED_RUBRIC["regime_power"] = "regime_power-reader-v3"


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


def _seq_llm(texts: list, calls: list | None = None, models=("claude-haiku-5-5",)):
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
    assert sorted(rpr.READER_CATEGORIES) == sorted(CATEGORIES)


@pytest.mark.parametrize("cat", CATEGORIES)
def test_the_rubric_constants_are_the_pinned_literals(cat):
    """D-198: the reader SKILL files this was pinned to are deleted; the literal is pinned
    here (an old run's proposals carry it, so the constant must not drift)."""
    assert rp.READER_RUBRIC_VERSIONS[cat] == EXPECTED_RUBRIC[cat]


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
    assert rp.load_proposals(d, [cat], strict_provenance=True)[cat][0]["rubric_version"] == EXPECTED_RUBRIC[cat]


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



# D-198: the audit-log citation block, the reader stage's retry/stamp wiring and their flag-off
# identity tests went with the readers; the resolver and the rubric constants above stay.
