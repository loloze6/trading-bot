"""D-199, D-203, D-204 (operator build window run_102, 2026-10-28).

D-199  the D-098 refusal of an all-bars rank IC is skipped for a test on a component's `signal`.
D-203  run_context gains "the run's book", built by code from the run's own artifacts
       (fixture: tests/fixtures/d203_run_102, a copy of run_102's files with window labels and
       dates replaced by placeholders); its figures join `settings`.
D-204  observations: no cap; `test` is any ok query; `variant`; floors_met true / false / null;
       code-written id, `measured`, fold_observed; unreported results join the same list;
       campaign_memory and the memory view carry the new keys; old records still load;
       OBSERVATION_ROWS_MAX is 100.
"""
from __future__ import annotations

import copy
import re
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import analyst_memory_view as amv  # noqa: E402
import analyst_session as asm  # noqa: E402
import campaign_memory as cm  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

import test_e075_pr4_queries as q4  # noqa: E402
from d178_legacy_fixture import d178_checks_off  # noqa: E402,F401
from test_e075_pr5_analyst import (  # noqa: E402,F401
    LONG, RUN_ID, _claim_answer, _entries_for_claim, _good_claim_with_rationale, _install, run)

FIXTURE = SR_ROOT / "tests" / "fixtures" / "d203_run_102"
ARTS = FIXTURE / "artifacts"


# ---------------------------------------------------------------------------
# D-199
# ---------------------------------------------------------------------------

class _Res:
    errors, tests_none, tests = [], False, [{"spec_hash": "h"}]


def _claim_check(text):
    return asm.check_answer(text, lens="trade_efficiency", run_id=RUN_ID,
                            entries=_entries_for_claim(), claim_check=lambda c: _Res(),
                            holdout_start=q4.HOLDOUT, fold="A", model_id="m")[2]


def _rank_ic_test(**extra):
    t = {"name": "t", "selector": {"kind": "all"},
         "outcome": {"kind": "fwd_return", "horizons": [1]}, "baseline": None,
         "statistic": "rank_ic", "direction": "greater", "floor": {"min_events": 5}}
    t.update(extra)
    return t


@pytest.mark.parametrize("extra,refused", [
    ({}, True),                                                    # the final forecast: refused
    ({"signal": "forecast"}, True),                                # the default, written out
    ({"signal": "debug_info.components.x.post_pipeline_value"}, False),
    ({"signal": "debug_info.components.x.weighted_contribution"}, False),
])
def test_d199_the_all_bars_rank_ic_refusal_skips_a_test_on_a_component_signal(extra, refused):
    errors = _claim_check(_claim_answer(claim={"tests": [_rank_ic_test(**extra)]}))
    assert any("rank IC over all bars" in e for e in errors) is refused, errors


def test_d199_only_the_signal_test_is_exempt():
    tests = [_rank_ic_test(signal="debug_info.components.x.post_pipeline_value"),
             _rank_ic_test(name="u")]
    errors = _claim_check(_claim_answer(claim={"tests": tests}))
    hits = [e for e in errors if "rank IC over all bars" in e]
    assert len(hits) == 1 and "'u'" in hits[0]


# ---------------------------------------------------------------------------
# D-203: the run's book
# ---------------------------------------------------------------------------

def _book():
    return asm.run_book(FIXTURE)


def test_d203_the_fixture_holds_no_window_label_or_date():
    for p in FIXTURE.rglob("*"):
        if p.is_file():
            text = p.read_text(encoding="utf-8")
            assert not re.search(r"\d{4}-\d{2}", text), p
            assert not re.search(r"\d{8}T\d{6}", text), p


def test_d203_the_book_has_one_block_per_variant_with_every_figure():
    text, _nums = _book()
    blocks = re.split(r"\n(?=- )", text.split("Variants:\n", 1)[1])
    assert [b.splitlines()[0] for b in blocks] == [
        "- base", "- asset_ltc_altcoin_l1", "- asset_xrp_payment", "- split_stretch_weight"]
    base = blocks[0]
    # the grid value and result
    assert "grid forecast_ic_median: FAIL, value -0.008353 (needs > 0.02), 6 windows, " \
           "2374 trades" in base
    # each bar: actual, threshold, result
    assert "sharpe_min -0.3371 (needs > 0) FAIL" in base
    assert "trade_frequency_min 0.1327 (needs >= 0.01) PASS" in base
    assert "max_drawdown_pct_max 21.7 (needs <= 20) FAIL [advisory]" in base
    # sharpe and max drawdown, named
    assert "sharpe -0.3371; max drawdown 21.7 percent" in base
    # window_economics totals
    assert "window economics, all windows: n_bars 17519, trades 2374, turnover 247.8" in base
    assert "net_pct -23.52" in base
    # the claim test: effect and windows agreeing per horizon
    assert "h6 effect 0.0006842 (oriented 0.0006842), 5 of 6 windows with the claimed sign" in base
    assert "h24 effect 0.0006223 (oriented 0.0006223), 3 of 6 windows with the claimed sign" in base
    xrp = blocks[2]
    assert "grid forecast_ic_median: PASS, value 0.0286" in xrp and "sharpe 0.2438" in xrp


def test_d203_the_book_has_the_card_statement_and_the_one_line_per_file():
    text, _ = _book()
    head = text.split("Variants:")[0]
    assert head.startswith("Card statement (artifacts/hypothesis_card.yaml):\n  predicts: ")
    assert "horizon_bars: 24" in head and "if_fail: " in head
    assert "Grid (artifacts/grid_evaluation.yaml): result GRID_EVALUATED; criteria " \
           "forecast_ic_median" in head
    assert "Idea status (artifacts/idea_status.yaml): idea_status refuted; result FAIL; " \
           "hypothesis_verdict kill" in head
    assert "Profit bars (artifacts/profit_bars_evaluation.yaml): result FAIL; passing none" in head
    (fold_line,) = [x for x in head.splitlines() if x.startswith("Fold confirmation")]
    assert "not_confirmed on fold B" in fold_line and "h24 3 of 6" in fold_line \
        and "h6 0.0006842" in fold_line


def test_d203_absent_files_are_said_absent(tmp_path):
    (tmp_path / "artifacts").mkdir()
    text, nums = asm.run_book(tmp_path)
    for name in ("hypothesis_card.yaml", "grid_evaluation.yaml", "idea_status.yaml",
                 "profit_bars_evaluation.yaml", "fold_confirmation.yaml"):
        assert f"(artifacts/{name}): absent" in text or \
            f"(artifacts/{name}): no statement" in text, name
    assert "Variants: none" in text and nums == set()


def test_d203_one_absent_file_leaves_the_others(tmp_path):
    shutil.copytree(FIXTURE, tmp_path / "r")
    (tmp_path / "r" / "artifacts" / "fold_confirmation.yaml").unlink()
    (tmp_path / "r" / "artifacts" / "variants" / "base" / "claim_test.yaml").unlink()
    text, _ = asm.run_book(tmp_path / "r")
    assert "Fold confirmation (artifacts/fold_confirmation.yaml): absent" in text
    assert "claim test (artifacts/variants/base/claim_test.yaml): absent" in text
    assert "- base\n  grid forecast_ic_median: FAIL" in text and "sharpe_min -0.3371" in text


def test_d203_an_unreadable_file_is_said_so_and_the_book_still_builds(tmp_path):
    shutil.copytree(FIXTURE, tmp_path / "r")
    (tmp_path / "r" / "artifacts" / "grid_evaluation.yaml").write_text("{ not: [yaml", "utf-8")
    (tmp_path / "r" / "artifacts" / "idea_status.yaml").write_text("- a list\n", "utf-8")
    text, _ = asm.run_book(tmp_path / "r")
    assert "Grid (artifacts/grid_evaluation.yaml): unreadable" in text
    assert "Idea status (artifacts/idea_status.yaml): unreadable" in text
    assert "sharpe_min -0.3371" in text                      # the other files still read
    assert "grid: unreadable" in text


def test_d203_run_context_carries_the_book_after_the_variant_patches(tmp_path):
    run_dir = tmp_path / "run_x"
    shutil.copytree(FIXTURE, run_dir)
    ctx = asm.run_context(run_dir, "none.json", "B")
    assert asm.BOOK_TITLE in ctx
    assert ctx.index("## Variant patches") < ctx.index(asm.BOOK_TITLE) < ctx.index("## Cost model")
    assert "sharpe_min -0.3371" in ctx
    # a run with no artifacts: the section is there and says absent
    bare = tmp_path / "bare"
    bare.mkdir()
    assert "absent" in asm.run_context(bare, "none.json", None).split(asm.BOOK_TITLE)[1]


def test_d203_the_books_figures_join_settings_so_the_number_check_does_not_mask_them():
    nums = asm.book_settings(FIXTURE)
    assert -0.3371 in nums and 2374 in nums and 0.0286 in nums
    fields = {"claim.rationale": "The base Sharpe is -0.3371 over 2374 trades."}
    assert asm.number_hits(fields, [], {}, settings=None)             # masked without the book
    assert asm.number_hits(fields, [], {}, settings=nums) == []       # not masked with it
    assert asm.number_hits({"claim.rationale": "A Sharpe of -0.9999."}, [], {}, settings=nums)


def test_d203_the_formatter_is_fixed_notation_with_four_significant_digits():
    nums = set()
    assert asm._num(-7.943406474424542e-05, nums) == "-0.00007943"
    assert asm._num(247.78457, nums) == "247.8"
    assert asm._num(0.1, nums) == "0.1" and asm._num(3, nums) == "3" and asm._num(None, nums) == "None"
    assert asm._num(0.0, nums) == "0" and asm._num(21.7, nums) == "21.7"
    assert {-0.00007943, 247.8, 0.1, 3, 21.7} <= nums


def test_d203_book_figures_are_not_masked_in_a_real_analyst_run(run, monkeypatch):
    """Wiring (run_analyst_worker): the prompt carries the book, and a figure the book shows,
    written in the claim's prose, is not listed as unverified."""
    shutil.copytree(ARTS, run / "artifacts", dirs_exist_ok=True)
    monkeypatch.setattr(asm, "next_steps_errors", lambda *a, **k: [])
    monkeypatch.setattr(asm, "completeness_errors", lambda *a, **k: [])
    monkeypatch.setattr(asm, "_mechanism_errors", lambda *a, **k: [])
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_folds_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_score_provenance_enabled", lambda *a: False)

    async def script(call):
        return await _good_claim_with_rationale(call, "the base Sharpe of -0.3371 is not the point")
    stub = _install(monkeypatch, script)
    rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    assert asm.BOOK_TITLE in stub.prompt
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    assert record["unverified_numbers"] == []


# ---------------------------------------------------------------------------
# D-204: observations
# ---------------------------------------------------------------------------

ROW = {"effect": 0.0123, "n_events": 40, "n_windows_with_events": 5, "n_blocks": 5,
       "windows_claimed_sign": 5, "windows_with_value": 5}
VARIANTS = ["base", "split_stretch_weight"]


def _ce_entry(qid, *, selector=None, variant="base", row=None, floor=None):
    return {qid: {"id": qid, "function": "conditional_effect", "status": "ok",
                  "params": {"variant": variant, "statistic": "mean_diff"},
                  "result": {"spec_hash": f"h{qid}",
                             "test": {"selector": selector or LONG,
                                      "outcome": {"kind": "trade_net_return"},
                                      "baseline": {"kind": "other_trades"},
                                      "statistic": "mean_diff", "direction": "greater",
                                      "floor": floor or {"min_events": 5}},
                             "horizons": {"1": dict(ROW if row is None else row)}}}}


def _other_entry(qid, function="describe", variant="base"):
    return {qid: {"id": qid, "function": function, "status": "ok",
                  "params": {"column": "forecast", "variant": variant},
                  "result": {"column": "forecast", "n": 100}}}


def _obs(qid="q7", **over):
    o = {"statement": "Long lots lose more after a large move.", "test": qid,
         "evidence": [f"{qid}:horizons.1.effect=0.0123"], "floors_met": True,
         "mechanism_query": "q1"}
    o.update(over)
    return o


def _answer(observations):
    nc = {"reason": "every mechanism failed on another coin",
          "best_rejected": {"statement": "longs lead", "killed_by": "q3"},
          "next_steps": {k: "not run: the budget" for k in asm.NEXT_STEPS_KEYS}}
    if observations is not None:
        nc["observations"] = observations
    return "```yaml\n" + yaml.safe_dump({
        "outcome": "no_claim", "evidence": ["q1:horizons.1.effect=0.0123"],
        "no_claim": nc}, sort_keys=False) + "```"


def _entries(*extra):
    out = dict(_entries_for_claim())
    for e in extra:
        out.update(e)
    return out


def _check(observations, entries, variants=VARIANTS, fold="B"):
    return asm.check_answer(_answer(observations), lens="trade_efficiency", run_id="run_102",
                            entries=entries, claim_check=lambda c: None,
                            holdout_start=q4.HOLDOUT, fold=fold, model_id="m", variants=variants)


def test_d204_there_is_no_observation_cap():
    assert not hasattr(asm, "OBSERVATIONS_MAX")
    n = 12
    entries = _entries(*[_ce_entry(f"q{10 + i}") for i in range(n)])
    # the 12 tests have distinct spec_hashes; each is its own observation
    obs = [_obs(f"q{10 + i}", statement=f"Behaviour {i}.") for i in range(n)]
    _r, rec, errors = _check(obs, entries)
    assert errors == [], errors
    assert [o["id"] for o in rec["no_claim"]["observations"]] == [
        f"O-run_102-trade_efficiency-{i + 1}" for i in range(n)]


def test_d204_the_recorded_observation_is_written_by_code():
    entries = _entries(_ce_entry("q7"))
    _r, rec, errors = _check([_obs()], entries)
    assert errors == []
    (o,) = rec["no_claim"]["observations"]
    assert o["id"] == "O-run_102-trade_efficiency-1"
    assert o["fold_observed"] == "B" and o["variant"] == "base"
    m = o["measured"]
    assert m["function"] == "conditional_effect" and m["statistic"] == "mean_diff"
    assert m["params"]["variant"] == "base" and m["spec_hash"] == "hq7"
    assert m["selector"] == LONG and m["floor"] == {"min_events": 5}
    assert "horizons" not in m and "spec" not in o
    assert "mechanism_query" in o and "variant" in o


def test_d204_test_is_any_ok_query_and_floors_met_is_null_for_a_tool_without_floors():
    entries = _entries(_other_entry("q8", "describe"), _other_entry("q9", "trade_slice"))
    obs = [_obs("q8", floors_met=None, evidence=["q8:n=100"], mechanism_query=None),
           _obs("q9", floors_met=None, evidence=["q9:n=100"], statement="Other.")]
    for o in obs:
        o.pop("mechanism_query")
    _r, rec, errors = _check(obs, entries)
    assert errors == [], errors
    first, second = rec["no_claim"]["observations"]
    assert first["measured"] == {"function": "describe",
                                 "params": {"column": "forecast", "variant": "base"},
                                 "statistic": None}
    assert first["floors_met"] is None and second["measured"]["function"] == "trade_slice"


def test_d204_floors_met_true_or_false_on_a_tool_without_floors_is_refused():
    entries = _entries(_other_entry("q8"))
    for fm in (True, False):
        _r, _rec, errors = _check([_obs("q8", floors_met=fm, evidence=["q8:n=100"])], entries)
        assert any("floors_met must be null" in e for e in errors), errors


def test_d204_floors_met_must_be_true_false_or_null():
    entries = _entries(_ce_entry("q7"))
    _r, _rec, errors = _check([_obs(floors_met="yes")], entries)
    assert any("must be true, false or null" in e for e in errors), errors


def test_d204_a_conditional_effect_with_a_known_floor_state_cannot_be_null():
    clears = _entries(_ce_entry("q7"))
    assert any("floors_met is null" in e for e in _check([_obs(floors_met=None)], clears)[2])
    misses = _entries(_ce_entry("q7", row=dict(ROW, n_events=2)))
    assert any("floors_met is true" in e for e in _check([_obs(floors_met=True)], misses)[2])
    assert _check([_obs(floors_met=False)], misses)[2] == []


def test_d204_mechanism_query_or_stopped_by_is_required_only_when_floors_met_is_true():
    clears = _entries(_ce_entry("q7"))
    bare = _obs()
    bare.pop("mechanism_query")
    assert any("needs `mechanism_query" in e for e in _check([bare], clears)[2])
    assert _check([dict(bare, stopped_by="the comparison budget")], clears)[2] == []
    # false and null: not required
    misses = _entries(_ce_entry("q7", row=dict(ROW, n_events=2)))
    assert _check([dict(bare, floors_met=False)], misses)[2] == []
    other = _entries(_other_entry("q8"))
    assert _check([dict(bare, test="q8", floors_met=None, evidence=["q8:n=100"])], other)[2] == []


def test_d204_one_query_per_observation_and_the_same_spec_hash_is_the_same_test():
    entries = _entries(_ce_entry("q7"), _ce_entry("q8"))
    entries["q8"]["result"]["spec_hash"] = "hq7"
    obs = [_obs(), _obs("q8", statement="Same test again.")]
    errors = _check(obs, entries)[2]
    assert any("observations[1].test='q8'" in e and "different test" in e for e in errors)
    same_q = _check([_obs(), _obs(statement="Same query.")], _entries(_ce_entry("q7")))[2]
    assert any("observations[1].test='q7'" in e for e in same_q)


def test_d204_variant_must_be_a_variant_of_the_run_and_defaults_to_the_tests_own():
    entries = _entries(_ce_entry("q7", variant="split_stretch_weight"))
    errors = _check([_obs(variant="no_such_variant")], entries)[2]
    assert any("variant='no_such_variant' must be a variant of this run" in e for e in errors)
    assert any("variant=''" in e for e in _check([_obs(variant="")], entries)[2])
    _r, rec, errors = _check([_obs(variant="split_stretch_weight")], entries)
    assert errors == [] and rec["no_claim"]["observations"][0]["variant"] == "split_stretch_weight"
    _r, rec, errors = _check([_obs()], entries)
    assert errors == [] and rec["no_claim"]["observations"][0]["variant"] == "split_stretch_weight"
    # the run's variants are not known: not checked
    assert _check([_obs(variant="split_stretch_weight")], entries, variants=None)[2] == []


def test_d204_a_test_that_is_not_an_ok_query_is_refused():
    entries = _entries(_ce_entry("q7"))
    entries["q9"] = {"id": "q9", "function": "describe", "status": "refused", "params": {}}
    for bad in ("q99", "q9"):
        errors = _check([_obs(bad)], entries)[2]
        assert any("must be the id of an ok query" in e for e in errors), errors


def test_d204_unreported_results_join_the_same_list_tagged_by_code():
    other_sel = {"kind": "calendar", "hours": [0, 1]}
    entries = _entries(_ce_entry("q7"), _ce_entry("q9", selector=other_sel,
                                                  variant="split_stretch_weight"))
    _r, rec, errors = _check([_obs()], entries)
    assert errors == []
    first, second = rec["no_claim"]["observations"]
    assert "unreported_by_model" not in first
    assert second["id"] == "O-run_102-trade_efficiency-2"
    assert second["unreported_by_model"] is True and second["test"] == "q9"
    assert second["variant"] == "split_stretch_weight" and second["floors_met"] is True
    assert second["fold_observed"] == "B" and second["measured"]["selector"] == other_sel
    assert second["evidence"] == ["q9:horizons.1.effect=0.0123"]
    assert second["effect"] == {"1": 0.0123}
    assert asm.check_citations(second["evidence"], entries) == []      # real citations
    # the D-184 record stays
    assert [u["query"] for u in rec[asm.UNREPORTED_KEY]] == ["q9"]


def test_d204_unreported_results_alone_make_the_list_when_the_model_wrote_none():
    entries = _entries(_ce_entry("q9", selector={"kind": "calendar", "hours": [3]}))
    _r, rec, errors = _check(None, entries)
    assert errors == []
    (o,) = rec["no_claim"]["observations"]
    assert o["id"] == "O-run_102-trade_efficiency-1" and o["unreported_by_model"] is True


def test_d204_the_angle_tag_is_still_written_by_code():
    regime = {"kind": "bar_field", "field": "volatility_rank", "op": ">", "value": 0.5}
    entries = _entries(_ce_entry("q7", selector=regime))
    entries["q7"]["params"]["statistic"] = "mean_diff"
    _r, rec, errors = _check([_obs()], entries)
    assert errors == []
    assert rec["no_claim"]["observations"][0].get("angle") == "regime"


# --- campaign_memory --------------------------------------------------------

def _write_record(run_dir, observations, lens="trade_efficiency"):
    doc = {"lens": lens, "outcome": "no_claim",
           "attempts": [{"status": "accepted", "outcome": "no_claim"}],
           "no_claim": {"reason": "r", "best_rejected": {"statement": "s", "killed_by": "q3"},
                        "observations": observations}}
    path = Path(run_dir) / asm.record_rel(lens)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


SPEC = {"spec_hash": "hq7", "selector": LONG, "outcome": {"kind": "trade_net_return"},
        "baseline": {"kind": "other_trades"}, "statistic": "mean_diff", "direction": "greater",
        "floor": {"min_events": 5}}
OLD = {"statement": "Long lots lose more.", "test": "q7", "evidence": ["q7:horizons.1.effect=1"],
       "floors_met": True, "spec": SPEC}
NEW = {"id": "O-run_102-trade_efficiency-1", "statement": "Long lots lose more.", "test": "q7",
       "evidence": ["q7:horizons.1.effect=1"], "floors_met": True, "variant": "base",
       "measured": {"function": "conditional_effect", "params": {"variant": "base"},
                    "statistic": "mean_diff", **{k: v for k, v in SPEC.items()
                                                 if k != "statistic"}},
       "fold_observed": "B"}


def test_d204_campaign_memory_fields_carry_the_new_keys():
    assert {"id", "variant", "measured", "fold_observed"} <= set(cm.OBSERVATION_FIELDS)
    assert "spec" not in cm.OBSERVATION_FIELDS and "spec" in cm.LEGACY_OBSERVATION_FIELDS
    assert {"unreported_by_model", "vehicle", "angle"} <= set(cm.OBSERVATION_OPTIONAL_FIELDS)


def test_d204_an_old_shape_record_still_loads_beside_a_new_one(tmp_path):
    _write_record(tmp_path, [OLD, NEW])
    old, new = cm.analyst_observations(tmp_path, "run_102")
    assert old["spec"] == SPEC and "id" not in old and "measured" not in old
    assert new["id"] == NEW["id"] and new["measured"] == NEW["measured"]
    assert new["variant"] == "base" and new["fold_observed"] == "B" and "spec" not in new
    assert old["lens"] == new["lens"] == "trade_efficiency" and old["ref"] == new["ref"]


def test_d204_the_unreported_tag_and_the_optional_keys_are_copied(tmp_path):
    row = dict(NEW, unreported_by_model=True, effect={"1": 0.0123}, windows={"1": {}},
               vehicle=[{"component_id": "a", "field": "weight", "before": 1, "after": 0}],
               angle="sizing")
    _write_record(tmp_path, [row])
    (out,) = cm.analyst_observations(tmp_path, "run_102")
    for k in ("unreported_by_model", "effect", "windows", "vehicle", "angle"):
        assert out[k] == row[k]


@pytest.mark.parametrize("bad", [
    dict(NEW, surprise=1),                                          # an unknown key
    {k: v for k, v in NEW.items() if k != "measured"},              # neither shape complete
    {k: v for k, v in OLD.items() if k != "test"},
    "text",
])
def test_d204_an_observation_of_neither_shape_raises(tmp_path, bad):
    _write_record(tmp_path, [bad])
    with pytest.raises(cm.CampaignMemoryError):
        cm.analyst_observations(tmp_path, "run_102")


# --- the memory view --------------------------------------------------------

def _memory(rows, rid="run_102"):
    return {"runs": {rid: {"fold": "B", "recorded_at": "t", "observations": rows}}}


def _mem_row(base, **over):
    return {"lens": "trade_efficiency", "ref": "r", **copy.deepcopy(base), **over}


def test_d204_the_view_row_limit_is_100():
    assert amv.OBSERVATION_ROWS_MAX == 100
    rows = [_mem_row(NEW, id=f"O-run_102-trade_efficiency-{i}") for i in range(120)]
    view = amv.build_memory_view(_memory(rows))
    assert len(view["observations"]) == 100 and view["omitted_older_observations"] == 20
    assert view["observations_max_rows"] == 100 and view["observations_in_memory"] == 120
    assert view["observations"][-1]["id"] == "O-run_102-trade_efficiency-119"   # newest kept


def test_d204_the_view_shows_id_variant_vehicle_and_the_measured_test():
    vehicle = [{"component_id": "a", "field": "weight", "before": 1.0, "after": 0.25}]
    view = amv.build_memory_view(_memory([_mem_row(NEW, vehicle=vehicle)]))
    (row,) = view["observations"]
    assert row["id"] == NEW["id"] and row["variant"] == "base" and row["vehicle"] == vehicle
    assert row["test"]["spec_hash"] == "hq7" and row["test"]["floor"] == {"min_events": 5}
    assert row["fold_observed"] == "B" and row["floors_met"] is True
    assert row["vehicle"] is not vehicle                                      # a copy


def test_d204_the_view_shows_a_tool_without_a_test_block_by_function_and_params():
    row = dict(NEW, floors_met=None, measured={"function": "describe", "statistic": None,
                                              "params": {"column": "forecast", "variant": "base"}})
    (out,) = amv.build_memory_view(_memory([_mem_row(row)]))["observations"]
    assert out["test"] == {"function": "describe",
                           "params": {"column": "forecast", "variant": "base"}}
    assert out["floors_met"] is None


def test_d204_an_old_shape_row_is_shown_as_it_was():
    (out,) = amv.build_memory_view(_memory([_mem_row(OLD)]))["observations"]
    assert out["test"]["spec_hash"] == "hq7" and out["test"]["floor"] == {"min_events": 5}
    assert "id" not in out and "variant" not in out and "vehicle" not in out
    assert out["status"] == amv.OBSERVED and out["fold_observed"] == "B"


def test_d204_the_unreported_tag_is_shown():
    (out,) = amv.build_memory_view(_memory([_mem_row(NEW, unreported_by_model=True)]))[
        "observations"]
    assert out["unreported_by_model"] is True


# ---------------------------------------------------------------------------
# review round 1 (same PR)
# ---------------------------------------------------------------------------

def test_review1_a_refused_attempts_observations_do_not_survive_into_the_final_record(
        run, monkeypatch, d178_checks_off):
    """The record merges each attempt's `rec`; `observations` is set on a refused attempt that
    has unreported rows, so the next attempt (which has none) must not inherit them."""
    calls = {"n": 0}
    stale = [{"id": "O-run_102-trade_efficiency-1", "unreported_by_model": True}]

    def fake_check(text, **kw):
        calls["n"] += 1
        rec = {"lens": kw["lens"], "category": "trade_efficiency", "outcome": "claim"}
        if calls["n"] == 1:
            rec["observations"] = stale
        return None, rec, [f"refused {calls['n']}"]
    monkeypatch.setattr(asm, "check_answer", fake_check)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_folds_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_score_provenance_enabled", lambda *a: False)
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))

    async def script(call):
        return "no answer"
    _install(monkeypatch, script)
    rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    assert calls["n"] == 2 and "observations" not in record


def test_review1_an_observations_variant_must_be_the_variant_its_test_ran_on():
    entries = _entries(_ce_entry("q7", variant="base"))
    errors = _check([_obs(variant="split_stretch_weight")], entries)[2]
    assert any("variant='split_stretch_weight' differs from the variant q7 ran on ('base')" in e
               for e in errors), errors
    assert _check([_obs(variant="base")], entries)[2] == []
    # a variant given on a test that ran on another one, in the other direction
    entries = _entries(_ce_entry("q7", variant="split_stretch_weight"))
    assert any("differs from the variant q7 ran on" in e
               for e in _check([_obs(variant="base")], entries)[2])
    assert _check([_obs(variant="split_stretch_weight")], entries)[2] == []


def test_review1_agreement_counts_and_the_card_horizon_join_settings_without_a_claim_test(tmp_path):
    arts = tmp_path / "artifacts"
    arts.mkdir()
    (arts / "fold_confirmation.yaml").write_text(
        "status: not_confirmed\nfold: B\nreason: x\nagreement:\n  t:\n    '6': 5 of 7\n"
        "    '24': 3 of 7\n", encoding="utf-8")
    (arts / "hypothesis_card.yaml").write_text(
        "statement:\n  predicts: p\n  horizon_bars: 24\n", encoding="utf-8")
    assert not (arts / "variants").exists()                      # no claim test anywhere
    text, nums = asm.run_book(tmp_path)
    assert "h6 5 of 7" in text and "h24 3 of 7" in text
    assert {5, 7, 3, 24} <= nums
    assert asm.book_settings(tmp_path) == nums
    fields = {"claim.rationale": "5 of 7 windows held at the 24-bar horizon."}
    assert asm.number_hits(fields, [], {}, settings=nums) == []


def test_review1_floors_met_null_is_refused_on_a_conditional_effect_even_with_an_unknown_floor():
    # the log cannot tell: min_eras is not in the result, so floors_met_in_log is None
    unknown = _entries(_ce_entry("q7", floor={"min_events": 5, "min_eras": 3}))
    assert asm.floors_met_in_log(unknown["q7"]) is None
    errors = _check([_obs(floors_met=None)], unknown)[2]
    assert any("floors_met must be true or false" in e and "q7" in e for e in errors), errors
    # true or false as the model wrote it is accepted
    assert _check([_obs(floors_met=True)], unknown)[2] == []
    assert _check([_obs(floors_met=False)], unknown)[2] == []
    # null stays right for a tool without floors
    other = _entries(_other_entry("q8"))
    bare = _obs("q8", floors_met=None, evidence=["q8:n=100"])
    bare.pop("mechanism_query")
    assert _check([bare], other)[2] == []
