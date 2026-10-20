"""D-157 (operator ruling 2026-10-20): D-095 extends beyond the analyst.

A claim test that selects lots by an exit-time field (holding_bars, exit_cause) and measures the
lot's own result (trade_net_return, trade_gross_return) is refused by
analyst_session.exit_selector_own_outcome_errors. D-095 called it only from the analyst's
check_answer; it is now also called from reader_findings._check (the reader side findings, trade
family on) and from run_phase1_research._check_1a_claim (step 1a, analyst flag on). It is NOT
called from claim_card.check_claim, so fold_confirm's re-check of recorded claims is unchanged.

Pins:
  1. the refused shape, both outcomes, inside a full claim, through both new call sites;
  2. the reader side finding: errors are the analyst's strings, no spec hash, trade family off
     gives no D-095 text;
  3. step 1a: the same strings, tests dropped; flag off equals plain check_claim;
  4. what must still pass: entry-time selectors, post_exit_return;
  5. the three recorded confirmations, re-checked, are unchanged (spec hashes equal
     campaign_record/confirmations.yaml); fold_confirm.py references none of the new call sites;
  6. the analyst's refusal message appears once in a refused attempt (run_analyst_worker).
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
def test_a_reader_side_finding_of_that_shape_is_refused_with_the_analysts_message(
        where, outcome, named):
    claim = _claim(_test(where, outcome))
    own = asm.exit_selector_own_outcome_errors(claim)
    assert len(own) == 1
    out = rfi.side_finding_review({"claim": claim}, prior={}, own=set(), run_id="r",
                                  folds=True, trade_tests=True)
    assert out["errors"] == own                       # exactly the analyst's strings
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
    own = asm.exit_selector_own_outcome_errors(claim)
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
def test_a_step_1a_claim_of_that_shape_is_refused_with_the_analysts_message(
        monkeypatch, where, outcome, named):
    _on(monkeypatch)
    claim = _claim(_test(where, outcome))
    res = rpr._check_1a_claim(cc, claim, [])
    assert res.errors == asm.exit_selector_own_outcome_errors(claim)
    assert len(res.errors) == 1 and res.tests == []


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
    for name in ("reader_findings", "analyst_session", "_check_1a_claim",
                 "exit_selector_own_outcome_errors"):
        assert name not in text, name
    # and claim_card.check_claim itself does not call it
    card = (SR_ROOT / "tools" / "claim_card.py").read_text(encoding="utf-8")
    assert "exit_selector_own_outcome_errors" not in card and "analyst_session" not in card


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
    review now repeats check_answer's D-095 string ('side_findings[0]: <string>'). The filter in
    run_analyst_worker drops that repeat; the analyst's text appears once, unprefixed, as
    before. Full run_analyst_worker call on the stubbed session of test_e075_pr5_analyst; the
    content check's own return is captured to show the repeat exists before the filter."""
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
    assert content and f"side_findings[0]: {msgs[0]}" in content[0]
    # the analyst's string is unchanged: it is exactly what the module function gives
    assert msgs[0] in asm.exit_selector_own_outcome_errors(
        yaml.safe_load(first["answer"].split("```yaml\n")[1].split("```")[0])["claim"])
