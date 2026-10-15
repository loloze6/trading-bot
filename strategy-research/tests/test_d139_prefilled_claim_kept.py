"""D-139: a pre-registered claim is not re-authored by a model.

(a) After step 1a writes its card, when the brief carries a pre-filled `candidate.claim`
    (a decide-next brief from a reader's side finding) and that claim validates with
    decide-next's own test (claim_card.check_claim with the pipeline's keywords, no errors,
    not `tests: none`), code writes it into the card's `claim` unchanged, before the claim
    check reads the card. _check_prefilled_claim still records 1a's OWN claim's difference.
    Invalid pre-filled claim, no pre-filled claim, or claim_tests off: exactly as before.

run_095 (operator's checkout, 2026-10-15): the brief carried two trade-level tests; step 1a
read only CLAIM_TESTS.md, wrote `tests: none` with a missing_block, and the child's claim was
never measured (fold confirmation not_comparable). Its claim_prefill.yaml content is copied
below as fixture data (never read from runs/).
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import run_phase1_research as rpr  # noqa: E402
import claim_card as cc  # noqa: E402

from test_k3_protocol_pinning import _minimal_run  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402

ON = {"config_direct_authoring": {"enabled": True}, "claim_tests": {"enabled": True}}
CARD = {"hypothesis_id": "H-1", "thesis": "t", "rationale": "r",
        "edge_source": {"category": "persistent_behavioral_bias", "specific_mechanism": "m",
                        "why_not_arbitraged": "w", "evidence_type": "price_volume_only",
                        "measurable_proxy": "p"},
        "signal_concept": "s", "target_market": "BTC", "timeframe": "1d",
        "assumptions": ["a"], "expected_failure_modes": ["1", "2", "3"],
        "criteria": [{"id": "sign_consistent_by_era"}]}

UPPER = {"name": "upper_breakout",
         "selector": {"kind": "event", "field": "forecast", "op": ">=", "value": 12},
         "outcome": {"kind": "fwd_return", "horizons": [1, 2, 3, 4, 5]},
         "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "greater",
         "floor": {"min_events": 100, "min_windows": 4},
         "consistency": {"unit": "window", "min_same_sign": 4}}
BAR_CLAIM = {"statement": "Breakouts continue for 1-5 days.", "kind": "conditional_behaviour",
             "tests": [UPPER], "pass_if": "beats other days at every horizon",
             "fail_if": "significantly worse at any horizon", "rationale": "herding after breakouts"}

# run_095's artifacts/claim_prefill.yaml `prefilled` (= research_brief.yaml candidate.claim)
RUN_095_PREFILLED = yaml.safe_load("""
statement: 'In this strategy, lots opened at a forecast of 10 or more, or of -10
  or less (a full-size entry on either side), earn a lower mean net return than
  the other lots, in most windows.

  '
kind: execution_behaviour
tests:
- name: long_strong_entries_earn_less
  selector:
    kind: trade
    where:
    - field: entry_forecast
      op: '>='
      value: 10
  outcome:
    kind: trade_net_return
  baseline:
    kind: other_trades
  statistic: mean_diff
  direction: less
  floor:
    min_events: 100
    min_windows: 4
- name: short_strong_entries_earn_less
  selector:
    kind: trade
    where:
    - field: entry_forecast
      op: <=
      value: -10
  outcome:
    kind: trade_net_return
  baseline:
    kind: other_trades
  statistic: mean_diff
  direction: less
  floor:
    min_events: 100
    min_windows: 4
pass_if: 'On the unseen fold, both tests show a negative effect (the selected lots
  earn less than the other lots), with at least 100 selected lots each and the sign
  in most windows.

  '
fail_if: 'Either test shows a zero or positive effect (the selected lots earn at
  least as much as the other lots), or the effect points the other way in most windows.

  '
rationale: 'Overnight gaps in this market continue rather than refill: after a large
  gap, the next bar moves further in the gap''s direction, not back. The strategy''s
  negated forecast bets on the refill, so the lots it opens at large size are on
  the wrong side. The loss appears on both legs, so it is not a side effect of one
  direction.

  '
""")

# run_095's hypothesis_card.yaml `claim`, as step 1a wrote it
RUN_095_1A = {
    "statement": RUN_095_PREFILLED["statement"],
    "kind": "conditional_behaviour",
    "tests": "none",
    "missing_block": ("Lot-level realized net return (trade_net_return) by entry_forecast "
                      "selector (>= 10 or <= -10) against an other_trades baseline. No outcome, "
                      "selector or baseline slot in CLAIM_TESTS.md expresses it."),
    "pass_if": "On the unseen fold, both legs show a negative effect.",
    "fail_if": "Either leg shows a zero or positive effect.",
    "rationale": RUN_095_PREFILLED["rationale"],
}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _flags(monkeypatch, *, folds=False, analyst=False):
    monkeypatch.setattr(rpr, "_folds_enabled", lambda *a, **k: folds)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a, **k: analyst)


def _run(run_id: str, card_claim, prefilled) -> Path:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    cand = {"criteria_from": "hypothesis_generation", "source": {"hypothesis_id": "H-1"}}
    if prefilled is not None:
        cand["claim"] = copy.deepcopy(prefilled)
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", {"candidate": cand})
    card = copy.deepcopy(CARD)
    if card_claim is not None:
        card["claim"] = copy.deepcopy(card_claim)
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", card)
    return run_dir


def _card_bytes(run_dir: Path) -> bytes:
    return (run_dir / "artifacts" / "hypothesis_card.yaml").read_bytes()


def _card_claim(run_dir: Path):
    return rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml").get("claim")


def _prefill_record(run_dir: Path) -> dict:
    return rpr.load_yaml(run_dir / "artifacts" / rpr._CLAIM_PREFILL_FILE)


def _status(run_dir: Path) -> dict:
    return rpr.load_yaml(run_dir / "artifacts" / "claim_test_status.yaml")


def _requests_for(run_id: str) -> list:
    path = rpr.ROOT / cc.TEST_REQUESTS_REL
    rows = (rpr.load_yaml(path) or {}).get("requests", []) if path.exists() else []
    return [r for r in rows if r.get("run_id") == run_id]


def _no_1a_call(monkeypatch):
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry",
                        lambda *a, **k: pytest.fail("no 1a retry expected"))


# ---------------------------------------------------------------------------
# flags off / no pre-filled claim / invalid pre-filled claim: exactly as before
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("orch", [None, {"config_direct_authoring": {"enabled": True}},
                                  {"config_direct_authoring": {"enabled": True},
                                   "claim_tests": {"enabled": False}}],
                         ids=["no_config", "cda_only", "claim_tests_off"])
def test_claim_tests_off_leaves_the_card_byte_identical(monkeypatch, orch):
    _set_orchestrator(orch)
    _flags(monkeypatch, folds=True, analyst=True)
    _no_1a_call(monkeypatch)
    run_dir = _run("run_960", RUN_095_1A, RUN_095_PREFILLED)
    before = _card_bytes(run_dir)
    names = sorted(p.name for p in (run_dir / "artifacts").iterdir())
    assert rpr._check_claim_after_1a("run_960", run_dir, [], {}) is None
    assert _card_bytes(run_dir) == before
    assert sorted(p.name for p in (run_dir / "artifacts").iterdir()) == names


def test_no_prefilled_claim_leaves_the_card_byte_identical(monkeypatch):
    _set_orchestrator(ON)
    _flags(monkeypatch)
    _no_1a_call(monkeypatch)
    run_dir = _run("run_961", dict(BAR_CLAIM, statement="1a's own idea"), None)
    before = _card_bytes(run_dir)
    assert rpr._keep_prefilled_claim(run_dir, "run_961") is rpr._NOT_KEPT
    rpr._check_claim_after_1a("run_961", run_dir, [], {})
    assert _card_bytes(run_dir) == before
    assert not (run_dir / "artifacts" / rpr._CLAIM_PREFILL_FILE).exists()


@pytest.mark.parametrize("bad", [
    dict(BAR_CLAIM, kind="vibes"),                                   # refused by check_claim
    {k: v for k, v in BAR_CLAIM.items() if k != "tests"} | {"tests": "none",
                                                             "missing_block": "x"},  # tests: none
], ids=["refused", "tests_none"])
def test_an_invalid_prefilled_claim_is_todays_behaviour(monkeypatch, bad):
    _set_orchestrator(ON)
    _flags(monkeypatch)
    _no_1a_call(monkeypatch)
    own = dict(BAR_CLAIM, statement="1a's own idea")
    run_dir = _run("run_962", own, bad)
    before = _card_bytes(run_dir)
    assert rpr._keep_prefilled_claim(run_dir, "run_962") is rpr._NOT_KEPT
    rpr._check_claim_after_1a("run_962", run_dir, [], {})
    assert _card_bytes(run_dir) == before                    # 1a's claim stays, as today
    assert _status(run_dir)["usable"] is True                # 1a's own claim is the one checked
    assert _prefill_record(run_dir)["status"] == "changed"   # the existing record, as today


# ---------------------------------------------------------------------------
# a valid pre-filled claim is kept; the record still shows 1a's difference
# ---------------------------------------------------------------------------

def test_a_valid_prefilled_claim_replaces_1as_tests_none(monkeypatch, capsys):
    _set_orchestrator(ON)
    _flags(monkeypatch)
    _no_1a_call(monkeypatch)
    own = {"statement": "a rewritten statement", "kind": "lead_lag", "tests": "none",
           "missing_block": "no slot expresses it", "pass_if": "p", "fail_if": "f",
           "rationale": "r"}
    run_dir = _run("run_963", own, BAR_CLAIM)
    rpr._check_claim_after_1a("run_963", run_dir, [], {})
    assert _card_claim(run_dir) == BAR_CLAIM                 # the whole claim, unchanged
    card = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")
    assert {k: v for k, v in card.items() if k != "claim"} == CARD   # nothing else touched
    rec = _prefill_record(run_dir)
    assert rec["status"] == "changed"
    assert rec["changed"] == ["statement", "kind", "tests (spec_hash)"]   # 1a's difference
    assert rec["prefilled"] == BAR_CLAIM
    st = _status(run_dir)
    assert st["usable"] is True and [t["name"] for t in st["tests"]] == ["upper_breakout"]
    assert _requests_for("run_963") == []                    # no tests_none request row
    out = capsys.readouterr().out
    assert "[D-139]" in out and "step 1a changed the pre-filled claim" in out
    check = rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"]
    assert len(check) == 1 and check[0]["cards"]["hypothesis_card.yaml"]["tests_none"] is False


def test_a_broken_1a_claim_needs_no_retry_when_the_prefill_is_kept(monkeypatch):
    """Before D-139 a broken claim on a pre-filled run cost a 1a retry; the kept claim is
    the one checked, so there is nothing to retry."""
    _set_orchestrator(ON)
    _flags(monkeypatch)
    _no_1a_call(monkeypatch)
    run_dir = _run("run_964", {"broken": True}, BAR_CLAIM)
    rpr._check_claim_after_1a("run_964", run_dir, [], {})
    assert _card_claim(run_dir) == BAR_CLAIM
    assert _status(run_dir)["usable"] is True
    rec = _prefill_record(run_dir)
    assert rec["status"] == "changed" and "tests (spec_hash)" in rec["changed"]


def test_a_card_without_a_claim_gets_the_prefilled_one(monkeypatch):
    _set_orchestrator(ON)
    _flags(monkeypatch)
    _no_1a_call(monkeypatch)
    run_dir = _run("run_965", None, BAR_CLAIM)
    rpr._check_claim_after_1a("run_965", run_dir, [], {})
    assert _card_claim(run_dir) == BAR_CLAIM
    assert _prefill_record(run_dir)["changed"] == ["the card has no claim"]


def test_an_exact_copy_is_not_rewritten(monkeypatch, capsys):
    _set_orchestrator(ON)
    _flags(monkeypatch)
    _no_1a_call(monkeypatch)
    run_dir = _run("run_966", BAR_CLAIM, BAR_CLAIM)
    before = _card_bytes(run_dir)
    rpr._check_claim_after_1a("run_966", run_dir, [], {})
    assert _card_bytes(run_dir) == before
    assert _prefill_record(run_dir)["status"] == "unchanged"
    assert "[D-139]" not in capsys.readouterr().out


def test_after_a_retry_the_retrys_card_gets_the_prefill_and_its_own_claim_is_recorded(
        monkeypatch):
    """A retry (here forced by a power warning on the first check) re-writes the card; the
    pre-filled claim is written into the retry's card too, and the record compares the
    retry's own claim -- the card the run keeps."""
    _set_orchestrator(ON)
    _flags(monkeypatch)
    run_dir = _run("run_967", dict(BAR_CLAIM, statement="first 1a statement"), BAR_CLAIM)
    retry_claim = dict(BAR_CLAIM, kind="lead_lag")
    calls = []

    def _invoke(stage, run_id, rdir, expected, state):
        calls.append(stage)
        card = copy.deepcopy(CARD)
        card["claim"] = copy.deepcopy(retry_claim)
        rpr.save_yaml(rdir / "artifacts" / "hypothesis_card.yaml", card)

    power_calls = []

    def _power(run_dir_, run_id, attempt, stage, card, name):
        power_calls.append(attempt)
        return [{"message": "floor unreachable"}] if attempt == 0 else []

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    monkeypatch.setattr(rpr, "_claim_power_check", _power)
    rpr._check_claim_after_1a("run_967", run_dir, [], {})
    assert calls == ["hypothesis_generation"]
    assert _card_claim(run_dir) == BAR_CLAIM
    rec = _prefill_record(run_dir)
    assert rec["status"] == "changed" and rec["changed"] == ["kind"]   # the retry's own claim


def test_an_undone_retry_restores_the_first_answers_record(monkeypatch):
    """A retry whose card the keep cannot touch (not a mapping) leaves the run's card worse;
    the first answer (already carrying the kept claim) comes back, and the record compares
    the FIRST 1a claim again, not the retry's."""
    _set_orchestrator(ON)
    _flags(monkeypatch)
    run_dir = _run("run_974", dict(BAR_CLAIM, statement="first 1a statement"), BAR_CLAIM)

    def _invoke(stage, run_id, rdir, expected, state):
        (rdir / "artifacts" / "hypothesis_card.yaml").write_text("- not a card\n",
                                                                 encoding="utf-8")

    def _power(run_dir_, run_id, attempt, stage, card, name):
        return [{"message": "floor unreachable"}] if attempt == 0 else []

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    monkeypatch.setattr(rpr, "_claim_power_check", _power)
    rpr._check_claim_after_1a("run_974", run_dir, [], {})
    check = rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"]
    assert any(a.get("retry_undone") == "worse than the first answer" for a in check)
    assert _card_claim(run_dir) == BAR_CLAIM
    rec = _prefill_record(run_dir)
    assert rec["status"] == "changed" and rec["changed"] == ["statement"]


# ---------------------------------------------------------------------------
# run_095's shape: trade-level tests, kept only with the analyst flag on
# ---------------------------------------------------------------------------

def test_run_095_shape_analyst_on_keeps_the_trade_claim(monkeypatch):
    _set_orchestrator(ON)
    _flags(monkeypatch, folds=True, analyst=True)
    _no_1a_call(monkeypatch)
    run_dir = _run("run_968", RUN_095_1A, RUN_095_PREFILLED)
    rpr._check_claim_after_1a("run_968", run_dir, [], {})
    assert _card_claim(run_dir) == RUN_095_PREFILLED
    rec = _prefill_record(run_dir)
    # exactly run_095's record: 1a's own difference is still recorded
    assert (rec["status"], rec["changed"]) == ("changed", ["kind", "tests (spec_hash)"])
    st = _status(run_dir)
    assert st["usable"] is True
    assert [t["name"] for t in st["tests"]] == ["long_strong_entries_earn_less",
                                               "short_strong_entries_earn_less"]
    assert all(t["verdict_possible"] is False for t in st["tests"])   # trade tests: effect size
    assert _requests_for("run_968") == []


def test_run_095_shape_analyst_off_is_todays_behaviour(monkeypatch):
    _set_orchestrator(ON)
    _flags(monkeypatch, folds=True, analyst=False)
    _no_1a_call(monkeypatch)
    run_dir = _run("run_969", RUN_095_1A, RUN_095_PREFILLED)
    before = _card_bytes(run_dir)
    assert cc.check_claim(RUN_095_PREFILLED, **rpr._claim_check_kw()).errors   # not valid here
    rpr._check_claim_after_1a("run_969", run_dir, [], {})
    assert _card_bytes(run_dir) == before
    st = _status(run_dir)
    assert (st["usable"], st["reason"]) == (False, "tests_none")       # run_095's status
    rec = _prefill_record(run_dir)
    # the existing record, unchanged: with the family refused both claims hash to [] (so
    # run_095's own record, which lists the tests, shows its analyst flag was on)
    assert (rec["status"], rec["changed"]) == ("changed", ["kind"])
    assert [r["missing_block"] for r in _requests_for("run_969")] == [RUN_095_1A["missing_block"]]


def test_the_validator_is_decide_nexts():
    """The keep uses claim_card.check_claim with the pipeline's keywords -- the call
    reader_findings.side_finding_review makes for decide-next (no errors, not tests_none)."""
    import ast
    src = (SR_ROOT / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    fn = next(n for n in ast.walk(ast.parse(src))
              if isinstance(n, ast.FunctionDef) and n.name == "_keep_prefilled_claim")
    body = ast.unparse(fn)
    assert "check_claim(pre, **_claim_check_kw())" in body
    assert "res.errors or res.tests_none" in body


# ---------------------------------------------------------------------------
# (b) step 1a receives CLAIM_TESTS_TRADE.md under orchestrator.analyst.enabled only
# ---------------------------------------------------------------------------

HANDOFF_1A = SR_ROOT / "workflow_artifacts" / "templates" / "handoffs" / \
    "research_brief_to_hypothesis.yaml"
TRADE_GUIDE = SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design" / "CLAIM_TESTS_TRADE.md"


def _1a_inputs(run_dir: Path, stage: str = "hypothesis_generation") -> dict:
    handoff = yaml.safe_load(HANDOFF_1A.read_text(encoding="utf-8"))
    rpr._apply_claim_tests_context(stage, handoff, run_dir)
    return handoff


@pytest.mark.parametrize("prefilled", [None, BAR_CLAIM], ids=["no_prefill", "prefill"])
def test_1a_gets_the_trade_guide_iff_the_analyst_is_on(monkeypatch, prefilled):
    _set_orchestrator(ON)
    run_dir = _run("run_970", None, prefilled)
    _flags(monkeypatch, folds=True, analyst=False)
    off = _1a_inputs(run_dir)
    _flags(monkeypatch, folds=True, analyst=True)
    on = _1a_inputs(run_dir)
    rpr._apply_claim_tests_context("hypothesis_generation", on, run_dir)        # idempotent
    off_paths = [r["path"] for r in off["required_inputs"]]
    on_paths = [r["path"] for r in on["required_inputs"]]
    assert rpr.CLAIM_TESTS_TRADE_GUIDE not in off_paths
    assert on_paths.count(rpr.CLAIM_TESTS_TRADE_GUIDE) == 1
    # analyst on adds exactly that one input, right after CLAIM_TESTS.md; nothing else moves
    i = on_paths.index(rpr.CLAIM_TESTS_GUIDE)
    assert on_paths[i + 1] == rpr.CLAIM_TESTS_TRADE_GUIDE
    assert [p for p in on_paths if p != rpr.CLAIM_TESTS_TRADE_GUIDE] == off_paths
    assert {k: v for k, v in on.items() if k != "required_inputs"} == \
        {k: v for k, v in off.items() if k != "required_inputs"}


def test_analyst_off_inputs_are_byte_identical_to_before(monkeypatch):
    """Flag off: the handoff equals what the pre-D-139 code built (the template's inputs,
    CLAIM_TESTS.md, and PREFILLED_CLAIM.md for a pre-filled brief), dumped byte for byte."""
    _set_orchestrator(ON)
    _flags(monkeypatch, folds=True, analyst=False)
    run_dir = _run("run_971", None, BAR_CLAIM)
    got = _1a_inputs(run_dir)
    want = yaml.safe_load(HANDOFF_1A.read_text(encoding="utf-8"))
    want.setdefault("required_inputs", []).extend([
        {"path": rpr.CLAIM_TESTS_GUIDE,
         "reason": "E-068: REQUIRED reading -- every hypothesis card you write carries a "
                   "`claim` block, its tests composed only from the blocks in this file."},
        {"path": rpr.PREFILLED_CLAIM_NOTE,
         "reason": "E-068: this brief's claim is pre-filled (research_brief.yaml "
                   "candidate.claim); copy it unchanged."}])
    assert yaml.safe_dump(got, sort_keys=False) == yaml.safe_dump(want, sort_keys=False)


def test_claim_tests_off_never_adds_the_trade_guide(monkeypatch):
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    _flags(monkeypatch, folds=True, analyst=True)
    run_dir = _run("run_972", None, BAR_CLAIM)
    snapshot = yaml.safe_load(HANDOFF_1A.read_text(encoding="utf-8"))
    assert _1a_inputs(run_dir) == snapshot


def test_1b_and_other_stages_never_get_the_trade_guide(monkeypatch):
    _set_orchestrator(ON)
    _flags(monkeypatch, folds=True, analyst=True)
    run_dir = _run("run_973", None, BAR_CLAIM)
    for stage in ("strategy_config_authoring", "innovation_expansion"):
        handoff = {"required_inputs": []}
        rpr._apply_claim_tests_context(stage, handoff, run_dir)
        assert rpr.CLAIM_TESTS_TRADE_GUIDE not in [r["path"] for r in handoff["required_inputs"]]


def test_the_trade_guide_path_resolves_and_says_who_reads_it():
    run_dir = SR_ROOT / "runs" / "run_x"
    assert (run_dir / rpr.CLAIM_TESTS_TRADE_GUIDE).resolve() == TRADE_GUIDE.resolve()
    head = TRADE_GUIDE.read_text(encoding="utf-8")[:600]
    assert "Not shown to any prompt yet" not in head
    assert "orchestrator.analyst.enabled" in head and "step 1a" in head and "D-139" in head
