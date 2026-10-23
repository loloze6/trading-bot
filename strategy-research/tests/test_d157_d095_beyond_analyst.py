"""D-157 (operator ruling 2026-10-20): D-095 extends beyond the analyst.

A claim test that selects lots by an exit-time field (holding_bars, exit_cause) and measures the
lot's own result (trade_net_return, trade_gross_return) is found by
analyst_session.exit_selector_own_outcome_hits (the one source of the facts and the core
sentence). D-095 refused it only at the analyst's check_answer
(exit_selector_own_outcome_errors); it is now also refused by reader_findings._check (the reader
side findings and decide-next, trade family on; d095_refusals) and by
run_phase1_research._check_1a_claim (step 1a and, D-157 (a), the keep of a pre-filled claim,
analyst flag on). It is NOT called from claim_card.check_claim, so fold_confirm's re-check of
recorded claims is unchanged. Each seam has its own text (operator ruling D-157): the analyst's
unchanged; step 1a's core + "Select on an entry-time field (...) or measure post_exit_return";
the side-finding check's one short line "D-095: <what>".

Pins:
  1. the refused shape, both outcomes, inside a full claim, through both new call sites;
  2. the reader side finding: the short line, no spec hash, trade family off gives no D-095 text;
  3. step 1a: core + step 1a's tail, tests dropped; flag off equals plain check_claim;
  4. what must still pass: entry-time selectors, post_exit_return;
  5. the three recorded confirmations, re-checked, are unchanged (spec hashes equal
     campaign_record/confirmations.yaml); fold_confirm.py references none of the new call sites;
  6. the analyst's refusal message appears once in a refused attempt (run_analyst_worker);
  7. the three texts, as literals;
  8. D-157 (a): a pre-filled claim of the refused shape is not kept (the retry's card stays).
No market data is read; no API key (the SDK query is stubbed as in test_e075_pr5_analyst).
"""
from __future__ import annotations

import asyncio  # noqa: F401  (the stub script is a coroutine)
import re
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import analyst_session as asm  # noqa: E402
import claim_card as cc  # noqa: E402
import reader_findings as rfi  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import test_e075_pr3_trade_tests as pr3  # noqa: E402
# the analyst harness of test_e075_pr5_analyst: `run` (a synthetic run directory), `_flags`
# (autouse there: analyst and folds on, imported here so it applies in this module too; every
# test below that cares about a flag sets it itself), `_install` (the stubbed SDK session)
from test_e075_pr5_analyst import RUN_ID, _cite, _flags, _install, _vehicle, run  # noqa: E402,F401
from d178_legacy_fixture import d178_checks_off  # noqa: E402,F401  (D-178; _flags uses it)

OWN_OUTCOMES = ("trade_net_return", "trade_gross_return")
D095_NEEDLE = "selects lots by an exit-time field"


def _where(*conds):
    return [{"field": f, "op": op, "value": v} for f, op, v in conds]


def _test(where, outcome="trade_net_return", name="t", direction="less", statistic="mean_diff",
          floor=None):
    out = {"kind": outcome}
    if outcome == "post_exit_return":
        out["horizons"] = [1, 6, 24]
    return {"name": name, "selector": {"kind": "trade", "where": where}, "outcome": out,
            "baseline": {"kind": "other_trades"}, "statistic": statistic,
            "direction": direction, "floor": floor or {"min_events": 5}}


def _claim(*tests):
    return pr3.claim(*tests, kind="execution_behaviour")


def _on(monkeypatch, analyst=True, folds=True):
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: analyst)
    monkeypatch.setattr(rpr, "_folds_enabled", lambda *a: folds)


# the exit-time shapes that are refused, with the exit-time fields the message names
REFUSED = [
    pytest.param(_where(("holding_bars", ">", 5)), "trade_net_return", "holding_bars",
                 id="holding_bars-net"),
    pytest.param(_where(("holding_bars", ">", 5)), "trade_gross_return", "holding_bars",
                 id="holding_bars-gross"),
    pytest.param(_where(("exit_cause", "==", "flip")), "trade_net_return", "exit_cause",
                 id="exit_cause-net"),
    pytest.param(_where(("exit_cause", "==", "flip")), "trade_gross_return", "exit_cause",
                 id="exit_cause-gross"),
    pytest.param(_where(("holding_bars", ">=", 3), ("exit_cause", "==", "flip")),
                 "trade_gross_return", "exit_cause, holding_bars", id="both-gross"),
    # an exit-time field next to an entry-time one is still an exit-time selector
    pytest.param(_where(("side", "==", "long"), ("holding_bars", ">", 5)), "trade_net_return",
                 "holding_bars", id="entry-plus-exit-net"),
]

# what must pass through every call site: (name, test)
ACCEPTED = [
    pytest.param(_test(_where(("entry_forecast", ">=", 10))), id="entry_forecast-net"),
    pytest.param(_test(_where(("side", "==", "short"))), id="side-short-net"),
    pytest.param(_test(_where(("entry_forecast", ">", -10), ("entry_forecast", "<", 10)),
                       outcome="trade_gross_return"), id="entry_forecast-band-gross"),
    pytest.param(_test(_where(("exit_cause", "==", "flip")), outcome="post_exit_return",
                       statistic="hit_rate", direction="greater",
                       floor={"min_events": 100, "min_windows": 4}), id="post_exit_return-flip"),
    pytest.param(_test(_where(("holding_bars", ">", 5)), outcome="post_exit_return",
                       direction="greater"), id="post_exit_return-holding"),
]


def _msg(where, outcome, named, name="t"):
    """The analyst's own message, as pinned verbatim in test_e075_pr5_analyst (first part)."""
    return (f"claim test {name!r} selects lots by an exit-time field ({named}) and measures "
            f"their own {outcome}: it cannot tell 'the exit comes too late' from 'a losing lot "
            f"stays open longer' (a lot closes only when the allocation changes, so long-held "
            f"lots are the ones the price kept going against). Select on an entry-time field "
            f"(side, entry_hour, entry_weekday, regime_at_entry, entry_forecast), or measure "
            f"post_exit_return. 'The exit comes too late' has no claim test yet (it needs the "
            f"return from bar N to the exit): explore it with event_study (trade_filter on "
            f"{named.split(', ')[0]}) and, if it is your best idea, end with no_claim and give "
            f"it as best_rejected")


def _1a(named, outcome, name="t"):
    """Step 1a's message (operator ruling D-157): the core, then step 1a's own tail."""
    return (f"claim test {name!r} selects lots by an exit-time field ({named}) and measures "
            f"their own {outcome}: it cannot tell 'the exit comes too late' from 'a losing lot "
            f"stays open longer' (a lot closes only when the allocation changes, so long-held "
            f"lots are the ones the price kept going against). Select on an entry-time field "
            f"(side, entry_hour, entry_weekday, regime_at_entry, entry_forecast) or measure "
            f"post_exit_return")


def _short(named, outcome, name="t"):
    """The side-finding check's one short line (decide-next's INFEASIBLE reason)."""
    return (f"D-095: claim test {name!r} selects lots by an exit-time field ({named}) and "
            f"measures their own {outcome}")


# ---------------------------------------------------------------------------
# 1. the shape, as the claim card sees it: check_claim alone still accepts it
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("where, outcome, named", REFUSED)
def test_check_claim_alone_still_accepts_the_shape_and_the_analyst_string_is_the_message(
        where, outcome, named):
    """The refusal is not in check_claim (fold_confirm re-checks recorded claims through it)."""
    t = _test(where, outcome)
    res = cc.check_claim(_claim(t), folds=True, trade_tests=True)
    assert res.errors == [] and len(res.tests) == 1
    assert asm.exit_selector_own_outcome_errors(_claim(t)) == [_msg(where, outcome, named)]


# ---------------------------------------------------------------------------
# 2. the reader side finding (reader_findings._check, under the trade family)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("where, outcome, named", REFUSED)
def test_a_reader_side_finding_of_that_shape_is_refused_with_the_short_line(
        where, outcome, named):
    claim = _claim(_test(where, outcome))
    out = rfi.side_finding_review({"claim": claim}, prior={}, own=set(), run_id="r",
                                  folds=True, trade_tests=True)
    assert out["errors"] == [_short(named, outcome)] == rfi.d095_refusals(claim)
    assert out["spec_hashes"] == []                   # the tests are dropped as for any refusal
    assert out["warnings"] == []


@pytest.mark.parametrize("where, outcome, named", REFUSED[:2])
def test_the_reader_check_without_the_trade_family_gives_no_d095_text(where, outcome, named):
    """Trade family off: check_claim's own refusal (an unknown selector), never D-095's."""
    claim = _claim(_test(where, outcome))
    out = rfi.side_finding_review({"claim": claim}, prior={}, own=set(), run_id="r", folds=True)
    assert out["errors"] and not any(D095_NEEDLE in e for e in out["errors"])
    res = rfi._check(claim, True, False)
    assert res.errors == out["errors"] == cc.check_claim(claim, folds=True).errors


def test_the_reader_check_keeps_check_claims_errors_first_then_the_d095_ones():
    good = _test(_where(("holding_bars", ">", 5)), name="bad_shape")
    broken = _test(_where(("side", "==", "long")), name="broken", direction="sideways")
    claim = _claim(good, broken)
    plain = cc.check_claim(claim, folds=True, trade_tests=True)
    assert plain.errors                                       # the second test is refused
    res = rfi._check(claim, True, True)
    own = rfi.d095_refusals(claim)
    assert len(own) == 1 and "'bad_shape'" in own[0]
    assert res.errors == plain.errors + own and res.tests == []


@pytest.mark.parametrize("t", ACCEPTED)
def test_a_reader_side_finding_of_an_accepted_shape_passes(t):
    claim = _claim(t)
    out = rfi.side_finding_review({"claim": claim}, prior={}, own=set(), run_id="r",
                                  folds=True, trade_tests=True)
    assert out["errors"] == [] and len(out["spec_hashes"]) == 1
    # the same hash as check_claim alone gives: the extension changes nothing for these
    assert out["spec_hashes"] == [x["spec_hash"] for x in
                                  cc.check_claim(claim, folds=True, trade_tests=True).tests]


def test_one_refused_test_refuses_the_whole_reader_claim():
    ok = _test(_where(("entry_forecast", ">=", 10)), name="ok")
    bad = _test(_where(("exit_cause", "==", "flip")), "trade_gross_return", name="bad")
    out = rfi.side_finding_review({"claim": _claim(ok, bad)}, prior={}, own=set(), run_id="r",
                                  folds=True, trade_tests=True)
    assert len(out["errors"]) == 1 and "'bad'" in out["errors"][0] and out["spec_hashes"] == []


# ---------------------------------------------------------------------------
# 3. step 1a (run_phase1_research._check_1a_claim, under the analyst flag)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("where, outcome, named", REFUSED)
def test_a_step_1a_claim_of_that_shape_is_refused_with_step_1as_message(
        monkeypatch, where, outcome, named):
    _on(monkeypatch)
    claim = _claim(_test(where, outcome))
    res = rpr._check_1a_claim(cc, claim, [])
    assert res.errors == [_1a(named, outcome)]
    assert res.tests == []


@pytest.mark.parametrize("where, outcome, named", REFUSED[:3])
def test_step_1a_with_the_flag_off_is_exactly_check_claim(monkeypatch, where, outcome, named):
    _on(monkeypatch, analyst=False)
    claim = _claim(_test(where, outcome))
    got = rpr._check_1a_claim(cc, claim, ["c1"])
    want = cc.check_claim(claim, ["c1"], folds=True)          # what _claim_check_kw gives
    assert (got.errors, got.tests, got.tests_none) == (want.errors, want.tests, want.tests_none)
    assert not any(D095_NEEDLE in e for e in got.errors)


@pytest.mark.parametrize("t", ACCEPTED)
def test_a_step_1a_claim_of_an_accepted_shape_passes_and_equals_check_claim(monkeypatch, t):
    _on(monkeypatch)
    claim = _claim(t)
    got = rpr._check_1a_claim(cc, claim, [])
    want = cc.check_claim(claim, [], **rpr._claim_check_kw())
    assert got.errors == [] and len(got.tests) == 1
    assert (got.errors, got.tests, got.tests_none) == (want.errors, want.tests, want.tests_none)


def test_step_1a_with_a_missing_claim_is_check_claims_answer(monkeypatch):
    _on(monkeypatch)
    for bad in (None, "x", {"tests": "x"}):
        got = rpr._check_1a_claim(cc, bad, [])
        want = cc.check_claim(bad, [], **rpr._claim_check_kw())
        assert (got.errors, got.tests, got.tests_none) == (want.errors, want.tests, want.tests_none)


# ---------------------------------------------------------------------------
# 4/5. the three recorded confirmations are unchanged
# ---------------------------------------------------------------------------
# Copied from strategy-research/campaign_record/campaign_memory.yaml (fold_confirmations ->
# finding -> tests -> spec: run_078 ~:2626, run_079 ~:3003, run_096 ~:6116), as literals, so the
# test does not parse the 237 kB memory file. The hashes are those of
# strategy-research/campaign_record/confirmations.yaml (`looks`), which this test also reads.

def _floor():
    return {"min_events": 100, "min_windows": 4}


RECORDED = {
    "strong_long_entries_earn_more": {
        "hash": "70837262630bcfce9f4373dd633c9ab654e12dc62b69ed280f137805a7d6be5e",
        "spec": {"selector": {"kind": "trade", "where": [
                     {"field": "entry_forecast", "op": ">=", "value": 10}]},
                 "outcome": {"kind": "trade_net_return"}, "baseline": {"kind": "other_trades"},
                 "statistic": "mean_diff", "direction": "greater", "floor": _floor()}},
    "flip_closed_lots_continue": {
        "hash": "c609a010c712c29acad11eeee063bf8d0a5b5c05a0b801ce83df3f52acb4aeb7",
        "spec": {"selector": {"kind": "trade", "where": [
                     {"field": "exit_cause", "op": "==", "value": "flip"}]},
                 "outcome": {"kind": "post_exit_return", "horizons": [1, 6, 24]},
                 "baseline": {"kind": "other_trades"}, "statistic": "hit_rate",
                 "direction": "greater", "floor": _floor()}},
    "shorts_earn_less_than_other_lots": {
        "hash": "05508ac0c6df321b1ff06d30f20ad42e37e052a8924a700e79fa77f8931c2951",
        "spec": {"selector": {"kind": "trade", "where": [
                     {"field": "side", "op": "==", "value": "short"}]},
                 "outcome": {"kind": "trade_net_return"}, "baseline": {"kind": "other_trades"},
                 "statistic": "mean_diff", "direction": "less", "floor": _floor()}},
}


def _recorded_claim(name):
    return _claim({"name": name, **RECORDED[name]["spec"]})


def test_the_recorded_hashes_are_those_of_confirmations_yaml():
    doc = yaml.safe_load((SR_ROOT / "campaign_record" / "confirmations.yaml")
                         .read_text(encoding="utf-8"))
    by_test = {look["test"]: look["spec_hash"] for look in doc["looks"]}
    for name, rec in RECORDED.items():
        assert by_test[name] == rec["hash"], name


@pytest.mark.parametrize("name", sorted(RECORDED))
def test_a_recorded_confirmation_rechecked_as_fold_confirm_does_is_unchanged(name):
    """fold_confirm.py:543 re-checks the recorded claim with check_claim(claim, folds=True,
    trade_tests=True): no errors, and the spec hash the confirmation was recorded under."""
    res = cc.check_claim(_recorded_claim(name), folds=True, trade_tests=True)
    assert res.errors == []
    assert [t["spec_hash"] for t in res.tests] == [RECORDED[name]["hash"]]


@pytest.mark.parametrize("name", sorted(RECORDED))
def test_the_recorded_confirmations_are_also_accepted_by_both_new_call_sites(monkeypatch, name):
    claim = _recorded_claim(name)
    assert asm.exit_selector_own_outcome_errors(claim) == []
    out = rfi.side_finding_review({"claim": claim}, prior={}, own=set(), run_id="r",
                                  folds=True, trade_tests=True)
    assert out["errors"] == [] and out["spec_hashes"] == [RECORDED[name]["hash"]]
    _on(monkeypatch)
    res = rpr._check_1a_claim(cc, claim, [])
    assert res.errors == [] and [t["spec_hash"] for t in res.tests] == [RECORDED[name]["hash"]]


def test_fold_confirm_reaches_none_of_the_new_call_sites():
    """Static: an accepted claim must not become 'claim refused' at fold time, so fold_confirm
    must not reference the checkers that carry D-095."""
    text = (SR_ROOT / "tools" / "fold_confirm.py").read_text(encoding="utf-8")
    for name in ("reader_findings", "analyst_session", "_check_1a_claim", "d095_refusals",
                 "exit_selector_own_outcome"):
        assert name not in text, name
    # and claim_card.check_claim itself does not call it
    card = (SR_ROOT / "tools" / "claim_card.py").read_text(encoding="utf-8")
    assert "exit_selector_own_outcome" not in card and "analyst_session" not in card


# ---------------------------------------------------------------------------
# 6. the analyst's message appears once (run_analyst_worker's duplicate filter)
# ---------------------------------------------------------------------------

EXIT_SELECTOR = {"kind": "trade", "where": [{"field": "holding_bars", "op": ">", "value": 5}]}


async def _exit_selector_claim(call):
    ce = await call("conditional_effect", {"condition": EXIT_SELECTOR, "direction": "less"})
    ts = await call("trade_slice", {"filter": [], "agg": [{"field": "trade_net_return",
                                                            "stat": "mean"}],
                                    "by": "direction"})
    test = ce["result"]["test"]
    answer = {"outcome": "claim",
              "claim": {"statement": "Lots held more than 5 bars earn less than the other lots.",
                        "kind": "execution_behaviour", "tests": [test],
                        "pass_if": "held lots below the others on the unseen fold",
                        "fail_if": "not below", "rationale": "the exit comes too late"},
              "why_query": ts["query_id"],
              "evidence": [_cite(ce["query_id"], ce["result"], "horizons.trade.effect")],
              "vehicle": _vehicle(), "combines_as": "execution_rule"}
    return "Here is my claim.\n```yaml\n" + yaml.safe_dump(answer, sort_keys=False) + "```\n"


def test_a_d095_refused_analyst_answer_lists_the_message_once(run, monkeypatch):
    """The analyst's claim is also its one side finding, so the content check's side finding
    review repeats check_answer's D-095 refusal, in its short line ('side_findings[0]: D-095:
    ...'). The filter in run_analyst_worker drops that repeat; the analyst's text appears once,
    unprefixed, as before. Full run_analyst_worker call on the stubbed session of
    test_e075_pr5_analyst; the content check's own return is captured to show the repeat exists
    before the filter."""
    content = []
    real = rpr._reading_content_errors

    def spy(*a, **k):
        out = real(*a, **k)
        content.append(list(out))
        return out
    monkeypatch.setattr(rpr, "_reading_content_errors", spy)
    _install(monkeypatch, _exit_selector_claim)
    rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    first = record["attempts"][0]
    assert first["status"] == "refused"
    msgs = [e for e in first["errors"] if D095_NEEDLE in e]
    assert len(msgs) == 1, first["errors"]
    assert msgs[0].startswith("claim test ") and "holding_bars" in msgs[0]
    assert not any(e.startswith("side_findings[") and D095_NEEDLE in e for e in first["errors"])
    # the repeat existed before the filter (so the filter, not luck, produced the single copy)
    claim = yaml.safe_load(first["answer"].split("```yaml\n")[1].split("```")[0])["claim"]
    assert content and [f"side_findings[0]: {s}" for s in rfi.d095_refusals(claim)] == \
        [e for e in content[0] if D095_NEEDLE in e]
    # the analyst's string is unchanged: it is exactly what the module function gives
    assert msgs == asm.exit_selector_own_outcome_errors(claim)
    assert msgs[0] == _msg(None, claim["tests"][0]["outcome"]["kind"], "holding_bars",
                           name=claim["tests"][0].get("name", 0))


# ---------------------------------------------------------------------------
# 7. the three texts (operator ruling D-157), as literals
# ---------------------------------------------------------------------------

CORE = ("claim test 'x' selects lots by an exit-time field (exit_cause, holding_bars) and "
        "measures their own trade_gross_return: it cannot tell 'the exit comes too late' from "
        "'a losing lot stays open longer' (a lot closes only when the allocation changes, so "
        "long-held lots are the ones the price kept going against).")


def test_the_three_texts(monkeypatch):
    claim = _claim(_test(_where(("holding_bars", ">=", 3), ("exit_cause", "==", "flip")),
                         "trade_gross_return", name="x"))
    hits = asm.exit_selector_own_outcome_hits(claim)
    assert [h["core"] for h in hits] == [CORE]
    # the analyst: byte-identical to the message before D-157 (pinned again in
    # test_e075_pr5_analyst)
    assert asm.exit_selector_own_outcome_errors(claim) == [
        CORE + " Select on an entry-time field (side, entry_hour, entry_weekday, regime_at_entry, "
        "entry_forecast), or measure post_exit_return. 'The exit comes too late' has no claim "
        "test yet (it needs the return from bar N to the exit): explore it with event_study "
        "(trade_filter on exit_cause) and, if it is your best idea, end with no_claim and give "
        "it as best_rejected"]
    # step 1a
    _on(monkeypatch)
    assert rpr._check_1a_claim(cc, claim).errors == [
        CORE + " Select on an entry-time field (side, entry_hour, entry_weekday, regime_at_entry, "
        "entry_forecast) or measure post_exit_return"]
    # the side-finding check, and decide-next's INFEASIBLE reason built from it
    assert rfi.d095_refusals(claim) == [
        "D-095: claim test 'x' selects lots by an exit-time field (exit_cause, holding_bars) and "
        "measures their own trade_gross_return"]
    assert rfi.side_finding_review({"claim": claim}, prior={}, own=set(), run_id="r",
                                   folds=True, trade_tests=True)["errors"] == \
        rfi.d095_refusals(claim)


# ---------------------------------------------------------------------------
# 8. D-157 (a): the keep of a pre-filled claim applies decide-next's test, D-095 included
# ---------------------------------------------------------------------------

def test_a_prefilled_claim_of_the_refused_shape_is_not_kept(monkeypatch):
    """Analyst on: the brief's pre-filled claim is D-095's shape (check_claim alone accepts
    it). _keep_prefilled_claim refuses it as decide-next would, so it never overwrites 1a's card,
    nor the card of the claim retry that step 1a's own D-095 refusal triggers: the retry's
    claim is the run's claim."""
    import test_d139_prefilled_claim_kept as d139
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))
    d139._set_orchestrator(d139.ON)
    _on(monkeypatch)
    bad = _claim(_test(_where(("holding_bars", ">", 5)), floor={"min_events": 100,
                                                               "min_windows": 4}))
    assert cc.check_claim(bad, **rpr._claim_check_kw()).errors == []    # only D-095 refuses it
    good = _claim(_test(_where(("entry_forecast", ">=", 10)), name="g",
                        floor={"min_events": 100, "min_windows": 4}))
    run_dir = d139._run("run_957", bad, bad)                 # 1a copied it unchanged
    before = d139._card_bytes(run_dir)
    assert rpr._keep_prefilled_claim(run_dir, "run_957") is rpr._NOT_KEPT
    assert d139._card_bytes(run_dir) == before
    seen = []

    def _invoke(stage, run_id, rdir, expected, state):
        st = rpr.load_yaml(rdir / "pipeline_state.yaml")[rpr.CLAIM_RETRY_STATE_KEY]
        seen.append(st["last_error"])
        card = dict(d139.CARD, claim=good)          # 1a's outputs were set aside: a new card
        rpr.save_yaml(rdir / "artifacts" / "hypothesis_card.yaml", card)

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    monkeypatch.setattr(rpr, "_claim_power_check", lambda *a, **k: [])
    rpr._check_claim_after_1a("run_957", run_dir, [], {})
    assert len(seen) == 1 and f"hypothesis_card.yaml: {_1a('holding_bars', 'trade_net_return')}" \
        in seen[0]
    assert d139._card_claim(run_dir) == good                 # the retry's own claim stays
    assert d139._prefill_record(run_dir)["status"] == "changed"


def test_a_prefilled_claim_of_an_accepted_trade_shape_is_still_kept(monkeypatch):
    import test_d139_prefilled_claim_kept as d139
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))
    d139._set_orchestrator(d139.ON)
    _on(monkeypatch)
    pre = _claim(_test(_where(("exit_cause", "==", "flip")), outcome="post_exit_return",
                       statistic="hit_rate", direction="greater",
                       floor={"min_events": 100, "min_windows": 4}))
    run_dir = d139._run("run_958", None, pre)
    assert rpr._keep_prefilled_claim(run_dir, "run_958") is None   # 1a wrote no claim
    assert d139._card_claim(run_dir) == pre


# ---------------------------------------------------------------------------
# 9. added after the wiring: one core, decide-next end to end, the keep unchanged elsewhere
# ---------------------------------------------------------------------------

def test_the_three_texts_derive_from_one_core(monkeypatch):
    """Changes nothing: proves the structure. The core is a prefix of the analyst's and of step
    1a's text, and the short line is "D-095: " and the core's first clause (the part before
    ': it cannot tell')."""
    claim = _claim(_test(_where(("holding_bars", ">=", 3), ("exit_cause", "==", "flip")),
                         "trade_gross_return", name="x"))
    (hit,) = asm.exit_selector_own_outcome_hits(claim)
    core = hit["core"]
    assert core == CORE
    (analyst,) = asm.exit_selector_own_outcome_errors(claim)
    _on(monkeypatch)
    (step_1a,) = rpr._check_1a_claim(cc, claim).errors
    (short,) = rfi.d095_refusals(claim)
    assert analyst.startswith(core + " ") and step_1a.startswith(core + " ")
    first_clause = core.split(": it cannot tell", 1)[0]
    assert first_clause == hit["what"]
    assert short == "D-095: " + first_clause
    # the tails differ, the core does not
    assert analyst != step_1a and core not in short


@pytest.mark.parametrize("where, outcome, named", REFUSED)
def test_decide_nexts_infeasible_reason_is_the_prefix_and_the_short_line(where, outcome, named):
    """decide-next end to end (decide_next._side_finding_review -> decide): trade family on, the
    candidate of a side finding of the refused shape is INFEASIBLE with the reason
    'next_test_refused: ' + the short line, and with the family off it carries no D-095 text."""
    import test_d091_trade_tests_pipeline as d091
    import test_e077_folds as tf
    claim = _claim(_test(where, outcome))
    for on in (True, False):
        inputs, pid = tf._scenario("run_074", "ROOT", {"run_074": tf.FOLD_A})
        inputs["runs"]["run_074"]["proposals"] = [{"category": "profitability",
                                                   "proposal": d091._side_item(pid, claim)}]
        if on:
            inputs["trade_tests"] = True
        cand = tf._cand(tf._decide(inputs, "run_074"), pid)
        reasons = cand["gates"]["feasibility"]["reasons"]
        if on:
            assert "next_test_refused: " + _short(named, outcome) in reasons
            assert cand["eligible"] is False
            assert not any(_msg(where, outcome, named) in r or _1a(named, outcome) in r
                           for r in reasons)             # neither longer text reaches decide-next
        else:
            assert not any(D095_NEEDLE in r for r in reasons)


def test_decide_nexts_infeasible_reason_literal():
    """Operator ruling D-157 (4th): decide-next's INFEASIBLE reason, pinned as one literal next to
    the analyst's and step 1a's (test_the_three_texts), through decide-next end to end."""
    import test_d091_trade_tests_pipeline as d091
    import test_e077_folds as tf
    claim = _claim(_test(_where(("holding_bars", ">=", 3), ("exit_cause", "==", "flip")),
                         "trade_gross_return", name="x"))
    inputs, pid = tf._scenario("run_074", "ROOT", {"run_074": tf.FOLD_A})
    inputs["runs"]["run_074"]["proposals"] = [{"category": "profitability",
                                               "proposal": d091._side_item(pid, claim)}]
    inputs["trade_tests"] = True
    reasons = tf._cand(tf._decide(inputs, "run_074"), pid)["gates"]["feasibility"]["reasons"]
    assert ("next_test_refused: D-095: claim test 'x' selects lots by an exit-time field "
            "(exit_cause, holding_bars) and measures their own trade_gross_return") in reasons


@pytest.mark.parametrize("i", range(len(ACCEPTED)))
def test_an_accepted_prefilled_claim_is_kept_as_before(monkeypatch, i):
    """Entry-time + trade_net_return, exit_cause + post_exit_return and the rest of ACCEPTED:
    analyst on, 1a's own (different) claim is replaced by the pre-filled one, unchanged, and
    _keep_prefilled_claim returns 1a's own claim -- exactly as D-139 has it."""
    import test_d139_prefilled_claim_kept as d139
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))
    d139._set_orchestrator(d139.ON)
    _on(monkeypatch)
    pre = _claim(ACCEPTED[i].values[0])
    own = dict(d139.BAR_CLAIM, statement="1a's own idea")
    run_dir = d139._run(f"run_98{i}", own, pre)
    assert rpr._keep_prefilled_claim(run_dir, f"run_98{i}") == own
    assert d139._card_claim(run_dir) == pre


@pytest.mark.parametrize("pre_name", ["bar", "exit_selector", "run_095", "entry_trade"])
def test_the_keep_with_the_analyst_flag_off_is_check_claims_decision(monkeypatch, pre_name):
    """Flag off: _keep_prefilled_claim keeps exactly the claims claim_card.check_claim (with the
    pipeline's keywords) accepts -- no D-095 anywhere. The refused shape is refused anyway
    (the trade family is off), and the card is untouched when not kept."""
    import test_d139_prefilled_claim_kept as d139
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))
    d139._set_orchestrator(d139.ON)
    _on(monkeypatch, analyst=False)
    pre = {"bar": d139.BAR_CLAIM,
           "exit_selector": _claim(_test(_where(("holding_bars", ">", 5)))),
           "run_095": d139.RUN_095_PREFILLED,
           "entry_trade": _claim(_test(_where(("entry_forecast", ">=", 10))))}[pre_name]
    want = cc.check_claim(pre, **rpr._claim_check_kw())
    own = dict(d139.BAR_CLAIM, statement="1a's own idea")
    run_dir = d139._run("run_990", own, pre)
    before = d139._card_bytes(run_dir)
    got = rpr._keep_prefilled_claim(run_dir, "run_990")
    if want.errors or want.tests_none:
        assert got is rpr._NOT_KEPT and d139._card_bytes(run_dir) == before
        assert not any(D095_NEEDLE in e for e in want.errors)
    else:
        assert got == own and d139._card_claim(run_dir) == pre
