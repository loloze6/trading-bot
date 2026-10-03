"""E-068 slice 2 (CUL-389): step 1a writes the `claim` block.

Covers:
  1. tools/claim_card.check_claim: text fields, kind, 1-3 tests composed from
     the slots (check_spec's rules), code-fixed alpha/significance, regime
     selectors as effect-size only, tests: none / missing_block, criteria_refs;
  2. the 1a/1b match check (a warning, never a stop);
  3. the schema, CLAIM_TESTS.md and the code agree;
  4. the flag: reader, dependency, flag-off byte identity of every seam;
  5. run_loop: the claim check after 1a with one retry, then fail; the park
     (test_requests.yaml) and the human pause; the match warning after 1b.

No LLM, no backtest, no market data. tests/conftest.py sandboxes rpr.ROOT.
"""
import copy
import json
import re
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import claim_card as cc  # noqa: E402
import claim_tests as ct  # noqa: E402

from test_k3_protocol_pinning import _minimal_run  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
from test_e056_1b_block_manifest import GOOD, _authored_1b  # noqa: E402

SCHEMA = SR_ROOT / "workflow_artifacts" / "schemas" / "hypothesis_card.schema.json"
GUIDE = SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design" / "CLAIM_TESTS.md"
SKILL_1A = SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design" / "SKILL.md"
HANDOFF_1A = SR_ROOT / "workflow_artifacts" / "templates" / "handoffs" / \
    "research_brief_to_hypothesis.yaml"
ON = {"config_direct_authoring": {"enabled": True}, "claim_tests": {"enabled": True}}

UPPER = {"name": "upper_breakout",
         "selector": {"kind": "event", "field": "forecast", "op": ">=", "value": 12},
         "outcome": {"kind": "fwd_return", "horizons": [1, 2, 3, 4, 5]},
         "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "greater",
         "floor": {"min_events": 100, "min_windows": 4},
         "consistency": {"unit": "window", "min_same_sign": 4}}
REGIME = {"name": "trend_label",
          "selector": {"kind": "regime", "value": "trending"},
          "outcome": {"kind": "fwd_volatility", "horizons": [24]},
          "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "less",
          "floor": {"min_events": 200}}
CALENDAR = {"name": "weekend",
            "selector": {"kind": "calendar", "weekdays": [5, 6]},
            "outcome": {"kind": "fwd_volatility", "horizons": [24]},
            "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "less",
            "floor": {"min_events": 100}}
IC = {"name": "ic", "selector": {"kind": "all"},
      "outcome": {"kind": "fwd_return", "horizons": [24]},
      "statistic": "rank_ic", "direction": "greater", "floor": {"min_blocks": 30}}


def _claim(**kw) -> dict:
    c = {"statement": "Breakouts continue for 1-5 days.", "kind": "conditional_behaviour",
         "tests": [copy.deepcopy(UPPER)], "pass_if": "beats other days at every horizon",
         "fail_if": "significantly worse at any horizon", "rationale": "herding after breakouts"}
    for k, v in kw.items():
        if v is None:
            c.pop(k, None)
        else:
            c[k] = v
    return c


# ---------------------------------------------------------------------------
# 1. check_claim
# ---------------------------------------------------------------------------

def test_valid_claim_passes_with_the_engine_hash():
    res = cc.check_claim(_claim())
    assert res.errors == [] and not res.parked
    spec = ct.TestSpec.from_dict({k: v for k, v in UPPER.items() if k != "name"})
    assert res.tests == [{"name": "upper_breakout", "spec_hash": ct.spec_hash(spec),
                          "verdict_possible": True}]
    # the code-fixed defaults are the engine's
    assert spec.alpha == 0.05 and spec.significance == ct.DEFAULT_SIGNIFICANCE


@pytest.mark.parametrize("key", ["statement", "pass_if", "fail_if", "rationale"])
def test_every_text_field_is_required(key):
    assert any(f"claim.{key}" in e for e in cc.check_claim(_claim(**{key: None})).errors)
    assert any(f"claim.{key}" in e for e in cc.check_claim(_claim(**{key: "  "})).errors)


def test_kind_is_a_closed_list_and_unknown_keys_are_refused():
    assert any("claim.kind" in e for e in cc.check_claim(_claim(kind="vibes")).errors)
    assert any("unknown keys" in e for e in cc.check_claim(_claim(verdict="supported")).errors)
    assert cc.check_claim(None).errors and cc.check_claim("x").errors


@pytest.mark.parametrize("key,value", [("alpha", 0.1),
                                       ("significance", {"method": ct.A851A_METHOD})])
def test_alpha_and_significance_are_code_fixed(key, value):
    t = dict(UPPER, **{key: value})
    errs = cc.check_claim(_claim(tests=[t])).errors
    assert any("fixed by code" in e for e in errs)


@pytest.mark.parametrize("patch,needle", [
    ({"selector": {"kind": "moon_phase"}}, "unknown selector"),
    ({"selector": {"kind": "event", "field": "fwd_close", "op": ">", "value": 1}}, "bar-t field"),
    ({"outcome": {"kind": "fwd_volatility", "horizons": [1]}}, "horizons >= 2"),
    ({"statistic": "rank_ic"}, "baseline must be null"),
    ({"floor": {"min_trades": 5}}, "unknown unit"),
    ({"direction": "up"}, "direction"),
], ids=["selector", "lookahead_field", "vol_h1", "rank_ic_baseline", "floor_unit", "direction"])
def test_slot_errors_come_from_check_spec(patch, needle):
    errs = cc.check_claim(_claim(tests=[dict(UPPER, **patch)])).errors
    assert errs and all(e.startswith("claim.tests[0]: ") for e in errs)
    assert any(needle in e for e in errs)


def test_missing_and_unknown_test_keys():
    t = {k: v for k, v in UPPER.items() if k != "floor"}
    assert any("missing ['floor']" in e for e in cc.check_claim(_claim(tests=[t])).errors)
    assert any("unknown keys" in e
               for e in cc.check_claim(_claim(tests=[dict(UPPER, horizon=3)])).errors)
    assert any("name" in e
               for e in cc.check_claim(_claim(tests=[dict(UPPER, name="")])).errors)


def test_one_to_three_tests_with_unique_names():
    assert cc.check_claim(_claim(tests=[])).errors
    four = [dict(UPPER, name=f"t{i}") for i in range(4)]
    assert cc.check_claim(_claim(tests=four)).errors
    three = [dict(UPPER, name=f"t{i}") for i in range(3)]
    assert cc.check_claim(_claim(tests=three)).errors == []
    assert any("unique name" in e
               for e in cc.check_claim(_claim(tests=[UPPER, dict(UPPER)])).errors)


@pytest.mark.parametrize("patch", [
    {"selector": {"kind": "calendar", "weekdays": 5}},
    {"statistic": ["mean_diff"]},
    {"name": ["x"]},
    {"selector": {"kind": ["all"]}},
    {"outcome": {"kind": "fwd_return", "horizons": [[1]]}},
    {"floor": [100]},
], ids=["weekdays_int", "statistic_list", "name_list", "kind_list", "nested_horizons",
        "floor_list"])
def test_malformed_values_are_refused_never_raised(patch):
    """review fix 3: LLM slips that make check_spec itself raise become errors
    (so 1a gets its retry), never an exception."""
    res = cc.check_claim(_claim(tests=[dict(UPPER, **patch)]))
    assert res.errors and not res.parked


def test_stray_selector_on_another_baseline_is_ignored():
    """review fix 10: only other_selector has a selector."""
    t = dict(UPPER, baseline={"kind": "complement", "selector": {"kind": "regime", "value": "t"}})
    res = cc.check_claim(_claim(tests=[t]))
    assert res.errors == [] and res.tests[0]["verdict_possible"] is True
    assert cc.signal_columns(t) == {"forecast"}


def test_rank_ic_without_baseline_is_valid():
    assert cc.check_claim(_claim(kind="direction_forecast", tests=[IC])).errors == []
    assert cc.check_claim(_claim(tests=[dict(IC, baseline=None)])).errors == []


# --- regime selectors: effect-size only (operator 2026-10-03, CUL-391) -------

def test_engine_still_refuses_regime_selectors_with_the_expected_message():
    """Drift guard: claim_card drops exactly this check_spec message. If its
    wording changes, this fails (and claim_card would refuse regime tests)."""
    spec = ct.TestSpec.from_dict({k: v for k, v in REGIME.items() if k != "name"})
    errs = ct.check_spec(spec)
    assert len(errs) == 1 and errs[0].startswith("selector: regime cannot be graded under ")
    assert set(ct.NOT_RECOMPUTABLE_SELECTORS) == {"regime", "regime_change"}


def test_regime_selector_is_accepted_as_effect_size_only():
    res = cc.check_claim(_claim(kind="regime_classifier", tests=[REGIME]))
    assert res.errors == [] and not res.parked
    assert res.tests[0]["verdict_possible"] is False
    assert res.tests[0]["reason"] == cc.REGIME_REASON


def test_regime_change_and_regime_in_other_selector_baseline():
    rc = dict(REGIME, name="rc", selector={"kind": "regime_change", "to": "chop"},
              outcome={"kind": "trend_ends", "horizons": [24]}, statistic="hit_rate",
              baseline={"kind": "placebo"})
    other = dict(UPPER, name="vs_trend",
                 baseline={"kind": "other_selector", "selector": {"kind": "regime", "value": "t"}})
    res = cc.check_claim(_claim(kind="regime_transition", tests=[rc, other]))
    assert res.errors == []
    assert [t["verdict_possible"] for t in res.tests] == [False, False]
    # a mixed claim: the non-regime test keeps verdict_possible True
    res = cc.check_claim(_claim(tests=[UPPER, REGIME]))
    assert [t["verdict_possible"] for t in res.tests] == [True, False]


def test_regime_selector_other_rules_still_apply():
    bad = dict(REGIME, selector={"kind": "regime"})                  # no value/values
    errs = cc.check_claim(_claim(tests=[bad])).errors
    assert any("regime needs value or values" in e for e in errs)
    assert not any("cannot be graded" in e for e in errs)
    bad = dict(REGIME, selector={"kind": "regime_change"})           # no `to`
    assert any("needs `to`" in e for e in cc.check_claim(_claim(tests=[bad])).errors)
    bad = dict(REGIME, outcome={"kind": "fwd_volatility", "horizons": [1]})
    assert any("horizons >= 2" in e for e in cc.check_claim(_claim(tests=[bad])).errors)


def test_a_regime_test_does_not_mask_another_tests_refusal():
    # only the regime selector's own refusal is dropped, never another selector's
    sel = dict(REGIME, baseline={"kind": "other_selector",
                                 "selector": {"kind": "event", "field": "nope", "op": ">", "value": 1}})
    errs = cc.check_claim(_claim(tests=[sel])).errors
    assert any("baseline.selector: field 'nope'" in e for e in errs)


# --- tests: none, criteria_refs ---------------------------------------------

def test_tests_none_with_missing_block_parks():
    res = cc.check_claim(_claim(kind="lead_lag", tests="none",
                                missing_block="outcome fwd_return_of(other_symbol, h)"))
    assert res.errors == [] and res.parked
    assert res.missing_block == "outcome fwd_return_of(other_symbol, h)"


def test_tests_none_needs_missing_block_and_missing_block_needs_none():
    assert any("missing_block" in e for e in cc.check_claim(_claim(tests="none")).errors)
    assert not cc.check_claim(_claim(tests="none")).parked
    assert any("only allowed with tests: none"
               in e for e in cc.check_claim(_claim(missing_block="x")).errors)
    res = cc.check_claim(_claim(tests="none", missing_block="x", criteria_refs=["a"]), ["a"])
    assert res.errors and not res.parked


def test_criteria_refs_must_name_the_cards_own_criteria():
    claim = _claim(kind="cost_turnover", tests=None, criteria_refs=["realized_edge_to_cost_ratio"])
    assert cc.check_claim(claim, ["realized_edge_to_cost_ratio"]).errors == []
    errs = cc.check_claim(claim, ["sign_consistent_by_era"]).errors
    assert any("not in this card's `criteria`" in e for e in errs)
    assert cc.check_claim(_claim(criteria_refs=[]), []).errors
    both = _claim(criteria_refs=["realized_edge_to_cost_ratio"])
    assert cc.check_claim(both, ["realized_edge_to_cost_ratio"]).errors == []
    # neither tests nor refs
    assert cc.check_claim(_claim(tests=None)).errors


def test_card_criteria_ids():
    assert cc.card_criteria_ids({"criteria": [{"id": "a"}, {"x": 1}, "b"]}) == ["a"]
    assert cc.card_criteria_ids({}) == []


# ---------------------------------------------------------------------------
# 2. match check (section 2.3)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("test,manifest,expected", [
    (UPPER, "forecast", None), (IC, "forecast", None), (REGIME, "regime", None),
    (UPPER, "regime", "forecast"), (REGIME, "forecast", "regime"),
    (CALENDAR, "forecast", None), (CALENDAR, "regime", None),
], ids=["fc_fc", "ic_fc", "rg_rg", "fc_rg", "rg_fc", "cal_fc", "cal_rg"])
def test_match_rule_table(test, manifest, expected):
    w = cc.match_check(_claim(kind="horizon_decay", tests=[test]), manifest)
    want = cc.expected_block(cc.signal_columns(test))
    assert (want == manifest) == (w == [])
    if w:
        assert w[0]["check"] == "test_reads_vs_block_kind" and w[0]["expected_block"] == want
    if expected is not None:
        assert want == expected


def test_signal_columns():
    assert cc.signal_columns(UPPER) == {"forecast"}
    assert cc.signal_columns(IC) == {"forecast"}
    assert cc.signal_columns(REGIME) == {"regime"}
    assert cc.signal_columns(CALENDAR) == set()
    assert cc.signal_columns(dict(UPPER, selector={"kind": "event", "field": "close",
                                                   "op": ">", "value": 1})) == set()
    mixed = dict(REGIME, statistic="rank_ic", baseline=None)
    assert cc.expected_block(cc.signal_columns(mixed)) == "regime"


def test_claim_kind_vs_block_kind():
    w = cc.match_check(_claim(kind="regime_classifier", tests=[UPPER]), "forecast")
    assert [x["check"] for x in w] == ["claim_kind_vs_block_kind"]
    w = cc.match_check(_claim(kind="calendar_effect", tests=[CALENDAR]), "forecast")
    assert [x["check"] for x in w] == ["test_reads_vs_block_kind", "claim_kind_vs_block_kind"]
    assert cc.match_check(_claim(kind="conditional_behaviour"), "forecast") == []
    # criteria_refs only, or tests: none: nothing to compare but the kind
    assert cc.match_check(_claim(kind="cost_turnover", tests=None), "forecast") == []


def test_test_requests_are_appended_once(tmp_path):
    row = {"run_id": "run_1", "stage": "hypothesis_generation", "missing_block": "x"}
    assert cc.append_test_requests(tmp_path, [row]) == 1
    assert cc.append_test_requests(tmp_path, [dict(row)]) == 0
    assert cc.append_test_requests(tmp_path, [dict(row, missing_block="y")]) == 1
    doc = yaml.safe_load((tmp_path / cc.TEST_REQUESTS_REL).read_text(encoding="utf-8"))
    assert [r["missing_block"] for r in doc["requests"]] == ["x", "y"]


# ---------------------------------------------------------------------------
# 3. schema, guide and code agree
# ---------------------------------------------------------------------------

def _schema() -> dict:
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


def test_schema_matches_the_code():
    claim = _schema()["properties"]["claim"]
    assert tuple(claim["properties"]["kind"]["enum"]) == cc.CLAIM_KINDS
    assert set(claim["properties"]) == cc.CLAIM_KEYS
    assert set(claim["required"]) == set(cc.TEXT_KEYS) | {"kind"}
    arr = claim["properties"]["tests"]["oneOf"][1]
    assert arr["maxItems"] == cc.MAX_TESTS and arr["minItems"] == 1
    assert claim["properties"]["tests"]["oneOf"][0] == {"const": cc.NO_TEST}
    t = _schema()["$defs"]["claim_test"]
    assert set(t["properties"]) == cc.TEST_KEYS
    assert set(t["properties"]["statistic"]["enum"]) == set(ct.STATISTICS)
    assert tuple(t["properties"]["direction"]["enum"]) == ct.DIRECTIONS


def _validate(card) -> list:
    import jsonschema
    v = jsonschema.Draft7Validator(_schema())
    return [e.message for e in v.iter_errors(card)]


CARD = {"hypothesis_id": "H-1", "thesis": "t", "rationale": "r",
        "edge_source": {"category": "persistent_behavioral_bias", "specific_mechanism": "m",
                        "why_not_arbitraged": "w", "evidence_type": "price_volume_only",
                        "measurable_proxy": "p"},
        "signal_concept": "s", "target_market": "BTC", "timeframe": "1d",
        "assumptions": ["a"], "expected_failure_modes": ["1", "2", "3"]}


def test_schema_accepts_claim_cards_and_still_old_cards():
    assert _validate(CARD) == []                                        # no claim: unchanged
    assert _validate(dict(CARD, claim=_claim())) == []
    assert _validate(dict(CARD, claim=_claim(kind="lead_lag", tests="none",
                                             missing_block="x"))) == []
    assert _validate(dict(CARD, claim=_claim(kind="regime_classifier", tests=[REGIME]))) == []
    assert _validate(dict(CARD, claim=_claim(kind="vibes")))
    assert _validate(dict(CARD, claim=_claim(tests=[dict(UPPER, alpha=0.1)])))
    assert _validate(dict(CARD, claim=_claim(tests="some")))


def test_claim_tests_md_lists_exactly_the_engine_blocks_and_kinds():
    text = GUIDE.read_text(encoding="utf-8")
    rows = set(re.findall(r"^\| `([a-z_]+)` \|", text, flags=re.M))
    engine = set(ct.SELECTORS) | set(ct.OUTCOMES) | set(ct.BASELINES) | set(ct.STATISTICS)
    assert engine <= rows, sorted(engine - rows)
    assert set(cc.CLAIM_KINDS) <= rows, sorted(set(cc.CLAIM_KINDS) - rows)
    assert rows <= engine | set(cc.CLAIM_KINDS), sorted(rows - engine - set(cc.CLAIM_KINDS))
    for unit in ct.FLOOR_UNITS:
        assert f"`{unit}`" in text


def test_skill_section_is_keyed_on_the_guide_and_the_guide_path_resolves():
    skill = SKILL_1A.read_text(encoding="utf-8")
    assert "IMPROVEMENT 10" in skill and "CLAIM_TESTS.md" in skill
    run_dir = SR_ROOT / "runs" / "run_x"
    assert (run_dir / rpr.CLAIM_TESTS_GUIDE).resolve() == GUIDE.resolve()


# ---------------------------------------------------------------------------
# 4. flag reader and flag-off byte identity
# ---------------------------------------------------------------------------

def test_flag_reader():
    assert rpr._claim_tests_enabled({}) is False
    assert rpr._claim_tests_enabled({"orchestrator": {"claim_tests": {"enabled": False}}}) is False
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._claim_tests_enabled({"orchestrator": {"claim_tests": {"enabled": "true"}}})
    with pytest.raises(ValueError, match="requires orchestrator.config_direct_authoring"):
        rpr._claim_tests_enabled({"orchestrator": {"claim_tests": {"enabled": True}}})
    assert rpr._claim_tests_enabled({"orchestrator": ON}) is True


def test_committed_config_has_the_flag_off():
    cfg = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["claim_tests"]["enabled"] is False


def _card_run(run_id: str, claim=None, **extra) -> Path:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    card = dict(CARD, **extra)
    if claim is not None:
        card["claim"] = claim
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", card)
    return run_dir


@pytest.mark.parametrize("orch", [None, {"config_direct_authoring": {"enabled": True}},
                                  {"config_direct_authoring": {"enabled": True},
                                   "claim_tests": {"enabled": False}}],
                         ids=["no_config", "cda_only", "explicit_off"])
def test_flag_off_touches_nothing(orch, monkeypatch):
    _set_orchestrator(orch)
    run_dir = _card_run("run_900", claim={"broken": True})
    rpr.update_state(path=run_dir, claim_check_retry={"attempts": 1, "last_error": "x"})
    before = sorted(p.name for p in (run_dir / "artifacts").iterdir())
    handoff = yaml.safe_load(HANDOFF_1A.read_text(encoding="utf-8"))
    snapshot = copy.deepcopy(handoff)
    rpr._apply_claim_tests_context("hypothesis_generation", handoff, run_dir)
    assert handoff == snapshot
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry",
                        lambda *a, **k: pytest.fail("no re-invoke with the flag off"))
    assert rpr._check_claim_after_1a("run_900", run_dir, [], {}) is False
    rpr._record_claim_match(run_dir)
    assert rpr._claim_gate_before_1b(run_dir, "run_900", True) is None
    assert sorted(p.name for p in (run_dir / "artifacts").iterdir()) == before
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["claim_check_retry"] == {"attempts": 1, "last_error": "x"}   # untouched
    assert state["status"] == "active" and not (run_dir / ".previous_attempts").exists()


def test_flag_off_post_1b_route_writes_no_match_file():
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    run_dir = _authored_1b("run_901", GOOD)
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert not (run_dir / "artifacts" / "claim_match.yaml").exists()


def test_flag_on_context_adds_the_guide_to_1a_only():
    _set_orchestrator(ON)
    run_dir = _card_run("run_902")
    handoff = yaml.safe_load(HANDOFF_1A.read_text(encoding="utf-8"))
    rpr._apply_claim_tests_context("hypothesis_generation", handoff, run_dir)
    paths = [r["path"] for r in handoff["required_inputs"]]
    assert paths.count(rpr.CLAIM_TESTS_GUIDE) == 1
    assert "injected_context" not in handoff or "claim_check_error" not in handoff["injected_context"]
    rpr._apply_claim_tests_context("hypothesis_generation", handoff, run_dir)   # idempotent
    assert [r["path"] for r in handoff["required_inputs"]].count(rpr.CLAIM_TESTS_GUIDE) == 1
    other = {"required_inputs": []}
    rpr._apply_claim_tests_context("strategy_config_authoring", other, run_dir)
    assert other == {"required_inputs": []}


# ---------------------------------------------------------------------------
# 5. the check after 1a, the retry, the park, the match warning
# ---------------------------------------------------------------------------

def _fake_1a(monkeypatch, run_dir, claims: list):
    """Each 1a call writes the next claim (None: a card with no claim)."""
    calls = []

    def _invoke(stage, run_id, rdir, expected, state):
        handoff = {"required_inputs": []}
        rpr._apply_claim_tests_context(stage, handoff, rdir)
        calls.append((handoff.get("injected_context") or {}).get("claim_check_error"))
        rpr.save_yaml(rdir / "artifacts" / "hypothesis_card.yaml",
                      dict(CARD, claim=claims[len(calls) - 1]))

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    return calls


def test_good_claim_passes_without_retry(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_910", claim=_claim())
    calls = _fake_1a(monkeypatch, run_dir, [])
    assert rpr._check_claim_after_1a("run_910", run_dir, [], {}) is False
    assert calls == []
    rec = rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"]
    assert len(rec) == 1 and rec[0]["errors"] == [] and rec[0]["tests"][0]["verdict_possible"]


def test_bad_claim_retries_once_with_the_error_then_passes(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_911", claim=_claim(kind="vibes"))
    calls = _fake_1a(monkeypatch, run_dir, [_claim()])
    assert rpr._check_claim_after_1a("run_911", run_dir, [], {}) is False
    assert len(calls) == 1 and "claim.kind" in calls[0] and "Retry 1/1" in calls[0]
    rec = rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"]
    assert [bool(a["errors"]) for a in rec] == [True, False]
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml")["claim_check_retry"]["attempts"] == 0


def test_bad_claim_twice_fails_the_run(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_912", claim=_claim(kind="vibes"))
    _fake_1a(monkeypatch, run_dir, [_claim(tests=[dict(UPPER, alpha=0.2)])])
    with pytest.raises(RuntimeError, match="still invalid after 1 retry.*fixed by code"):
        rpr._check_claim_after_1a("run_912", run_dir, [], {})
    # review fix 9: the recorded error is the latest one
    retry = rpr.load_yaml(run_dir / "pipeline_state.yaml")["claim_check_retry"]
    assert "fixed by code" in retry["last_error"] and "claim.kind" not in retry["last_error"]


def test_retry_sets_aside_the_old_card_and_has_its_own_audit_key(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_918", claim=_claim(kind="vibes"))
    seen = []

    def _invoke(stage, run_id, rdir, expected, state):
        # the stale card is gone before the retry's 1a call
        seen.append((rdir / "artifacts" / "hypothesis_card.yaml").exists())
        handoff = {"required_inputs": [], "injected_context": {"stage_attempt": "1"}}
        rpr._apply_claim_tests_context(stage, handoff, rdir)
        seen.append(handoff["injected_context"]["stage_attempt"])
        rpr.save_yaml(rdir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    assert rpr._check_claim_after_1a("run_918", run_dir, [], {}) is False
    assert seen == [False, "1_claim_retry1"]
    kept = (run_dir / ".previous_attempts" / "hypothesis_generation_claim_retry1"
            / "hypothesis_card.yaml")
    assert rpr.load_yaml(kept)["claim"]["kind"] == "vibes"


def test_retry_answer_with_several_cards_is_split_not_refused(monkeypatch):
    """review fix 1: a multi-card retry answer goes through the split handler,
    and the single-card check is skipped for it, as run_loop does."""
    _set_orchestrator(ON)
    run_dir = _card_run("run_919", claim=_claim(kind="vibes"))

    def _invoke(*a, **k):
        raise FileNotFoundError("hypothesis_card.yaml")

    def _split(run_id, rdir):
        rpr.save_yaml(rdir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))
        return True

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    monkeypatch.setattr(rpr, "_handle_hypothesis_generation_multi_card_split", _split)
    monkeypatch.setattr(rpr, "_brief_single_card_check",
                        lambda rdir: pytest.fail("single-card check after a split"))
    assert rpr._check_claim_after_1a("run_919", run_dir, [], {}) is False


def test_set_aside_moves_1a_outputs_but_not_enqueued_cards():
    run_dir = _card_run("run_922", claim=_claim())
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card_2.yaml", {"x": 1})
    rpr.save_yaml(arts / "queued_hypotheses.yaml", {"enqueued": True})
    rpr._set_aside_1a_outputs(run_dir, "t")
    assert not (arts / "hypothesis_card.yaml").exists()
    assert not (arts / "hypothesis_card_2.yaml").exists()
    assert (arts / "queued_hypotheses.yaml").exists()
    rpr.save_yaml(arts / "queued_hypotheses.yaml", {"enqueued": False})
    rpr._set_aside_1a_outputs(run_dir, "u")
    assert (run_dir / ".previous_attempts" / "hypothesis_generation_u"
            / "queued_hypotheses.yaml").exists()


def test_a_resume_after_the_retry_does_not_retry_again(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_913", claim=_claim(kind="vibes"))
    rpr.update_state(path=run_dir, claim_check_retry={"attempts": 1, "last_error": "x"})
    _fake_1a(monkeypatch, run_dir, [])
    with pytest.raises(RuntimeError, match="still invalid"):
        rpr._check_claim_after_1a("run_913", run_dir, [], {})


def test_missing_claim_is_refused_and_tests_none_parks(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_914")                       # no claim at all
    calls = _fake_1a(monkeypatch, run_dir, [_claim(kind="lead_lag", tests="none",
                                                   missing_block="fwd_return_of")])
    assert rpr._check_claim_after_1a("run_914", run_dir, [], {}) is True
    assert "a `claim` mapping is required" in calls[0]


def test_regime_claim_is_not_parked(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_915", claim=_claim(kind="regime_classifier", tests=[REGIME]))
    _fake_1a(monkeypatch, run_dir, [])
    assert rpr._check_claim_after_1a("run_915", run_dir, [], {}) is False
    rec = rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"][0]
    assert rec["tests"][0] == {"name": "trend_label", "spec_hash": rec["tests"][0]["spec_hash"],
                               "verdict_possible": False, "reason": cc.REGIME_REASON}
    assert not (rpr.ROOT / cc.TEST_REQUESTS_REL).exists()


@pytest.mark.parametrize("brief,why", [
    ({"config": {"a": 1}, "manifest": {"b": 1}, "criteria": [{"id": "x"}], "source": "op"},
     "pass_through"),
    ({"candidate": {"composition": {"registry_hash": "h"}}}, "composition"),
], ids=["pass_through", "composition"])
def test_exempt_cards_are_decided_by_the_runs_inputs(monkeypatch, brief, why):
    _set_orchestrator(ON)
    run_dir = _card_run("run_916", pass_through=True)
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", brief)
    _fake_1a(monkeypatch, run_dir, [])
    assert rpr._check_claim_after_1a("run_916", run_dir, [], {}) is False
    assert why in rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"][0]["exempt"]


def test_a_card_cannot_exempt_itself(monkeypatch):
    """review fix 5: `pass_through: true` written by 1a without a brief that
    supplies the four fields is checked like any card."""
    _set_orchestrator(ON)
    run_dir = _card_run("run_917", pass_through=True)
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", {"research_goal": "x"})
    calls = _fake_1a(monkeypatch, run_dir, [_claim()])
    assert rpr._check_claim_after_1a("run_917", run_dir, [], {}) is False
    assert len(calls) == 1 and "claim` mapping is required" in calls[0]


def test_park_under_retired_routing_writes_marker_and_one_request():
    _set_orchestrator(ON)
    run_dir = _card_run("run_920", claim=_claim(kind="lead_lag", tests="none", missing_block="mb"))
    assert rpr._park_for_missing_test(run_dir, "run_920", True) == "human_pause"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "paused_for_human"
    marker = state[rpr.PARKED_KEY]
    assert marker["kind"] == "test" and marker["stage"] == "hypothesis_generation"
    assert marker["resume_stage"] == "hypothesis_generation"
    assert cc.TEST_REQUESTS_REL in marker["request_refs"]
    rpr._park_for_missing_test(run_dir, "run_920", True)               # a re-run
    rows = rpr.load_yaml(rpr.ROOT / cc.TEST_REQUESTS_REL)["requests"]
    assert rows == [{"run_id": "run_920", "stage": "hypothesis_generation", "hypothesis_id": "H-1",
                     "claim_kind": "lead_lag", "statement": _claim()["statement"],
                     "missing_block": "mb"}]


def test_park_without_retired_routing_is_a_plain_pause():
    _set_orchestrator(ON)
    run_dir = _card_run("run_921", claim=_claim(kind="lead_lag", tests="none", missing_block="mb"))
    assert rpr._park_for_missing_test(run_dir, "run_921", False) == "human_pause"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "paused_for_human" and not state.get(rpr.PARKED_KEY)
    assert len(rpr.load_yaml(rpr.ROOT / cc.TEST_REQUESTS_REL)["requests"]) == 1


def test_match_warning_never_changes_the_route():
    _set_orchestrator(ON)
    run_dir = _authored_1b("run_930", GOOD)                       # a forecast block
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml",
                  dict(CARD, claim=_claim(kind="regime_classifier", tests=[REGIME])))
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    doc = rpr.load_yaml(run_dir / "artifacts" / "claim_match.yaml")
    assert doc["status"] == "mismatch" and doc["manifest_kind"] == "forecast"
    assert {w["check"] for w in doc["warnings"]} == {"test_reads_vs_block_kind",
                                                     "claim_kind_vs_block_kind"}


def test_match_ok_and_match_crash_is_recorded_not_raised(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _authored_1b("run_931", GOOD)
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert rpr.load_yaml(run_dir / "artifacts" / "claim_match.yaml")["status"] == "match"

    def _boom(*a, **k):
        raise KeyError("boom")

    monkeypatch.setattr(cc, "match_check", _boom)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    doc = rpr.load_yaml(run_dir / "artifacts" / "claim_match.yaml")
    assert doc["status"] == "error" and "boom" in doc["error"]


def test_no_match_check_when_the_manifest_is_refused():
    _set_orchestrator(ON)
    run_dir = _authored_1b("run_932", None)
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    assert not (run_dir / "artifacts" / "claim_match.yaml").exists()


# --- run_loop end to end on fixtures ----------------------------------------

def _loop_run(run_id: str) -> Path:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["pending_stage"] = "hypothesis_generation"
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    (run_dir / "handoffs").mkdir(exist_ok=True)
    shutil.copy(HANDOFF_1A, run_dir / "handoffs" / HANDOFF_1A.name)
    shutil.copy(HANDOFF_1A.parent / "hypothesis_to_strategy_config_authoring.yaml",
                run_dir / "handoffs" / "hypothesis_to_strategy_config_authoring.yaml")
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", {"research_goal": "x"})
    for name in ("available_feeds.yaml", "indicator_library.yaml"):   # 1a's required inputs
        rpr.save_yaml(rpr.ROOT / "config" / name, {"stub": True})
    docs = rpr.ROOT / "docs"                                          # 1b's required inputs
    docs.mkdir(parents=True, exist_ok=True)
    for name in ("COMPONENT_CATALOG.md", "STRATEGY_DESIGN_GUIDE.md"):
        (docs / name).write_text("stub\n", encoding="utf-8")
    return run_dir


def _fake_agent(monkeypatch, run_dir, claims):
    """async_invoke_agent stand-in: 1a writes the next claim; 1b answers
    component_gap (a pause, so the loop stops right after 1b)."""
    seen = []

    async def _invoke(stage_name, run_id, retry_context=None):
        handoff = {"required_inputs": []}
        rpr._apply_claim_tests_context(stage_name, handoff, run_dir)
        seen.append((stage_name, (handoff.get("injected_context") or {}).get("claim_check_error")))
        arts = run_dir / "artifacts"
        if stage_name == "hypothesis_generation":
            n = sum(1 for s, _ in seen if s == stage_name)
            rpr.save_yaml(arts / "hypothesis_card.yaml", dict(CARD, claim=claims[n - 1]))
        else:
            rpr.save_yaml(arts / "decision.yaml", {"stage": stage_name, "status": "component_gap",
                                                   "rationale": "stop here",
                                                   "blocking_issues": ["x"]})
            rpr.save_yaml(arts / "backtest_spec.yaml", {"status": "component_gap", "config": {}})

    monkeypatch.setattr(rpr, "async_invoke_agent", _invoke)
    return seen


def test_run_loop_retries_1a_once_then_goes_to_1b(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _loop_run("run_940")
    seen = _fake_agent(monkeypatch, run_dir, [_claim(kind="vibes"), _claim()])
    rpr.run_loop("run_940")
    assert [s for s, _ in seen] == ["hypothesis_generation", "hypothesis_generation",
                                    "strategy_config_authoring"]
    assert seen[0][1] is None and "claim.kind" in seen[1][1]


def test_run_loop_fails_on_a_second_bad_claim_before_any_spend(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _loop_run("run_941")
    seen = _fake_agent(monkeypatch, run_dir, [_claim(kind="vibes"), _claim(kind="vibes")])
    rpr.run_loop("run_941")
    assert [s for s, _ in seen] == ["hypothesis_generation", "hypothesis_generation"]
    final = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert final["status"] == "failed" and "still invalid" in final["last_error"]


def test_run_loop_pauses_on_tests_none_before_1b(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _loop_run("run_942")
    seen = _fake_agent(monkeypatch, run_dir, [_claim(kind="lead_lag", tests="none",
                                                     missing_block="fwd_return_of")])
    rpr.run_loop("run_942")
    assert [s for s, _ in seen] == ["hypothesis_generation"]
    final = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert final["status"] == "paused_for_human"
    assert final["pending_stage"] == "hypothesis_generation"
    assert rpr.load_yaml(rpr.ROOT / cc.TEST_REQUESTS_REL)["requests"][0]["run_id"] == "run_942"


def test_run_loop_flag_off_never_checks_a_claim(monkeypatch):
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    run_dir = _loop_run("run_943")
    seen = _fake_agent(monkeypatch, run_dir, [{"broken": True}])
    rpr.run_loop("run_943")
    assert [s for s, _ in seen] == ["hypothesis_generation", "strategy_config_authoring"]
    assert not (run_dir / "artifacts" / "claim_check.yaml").exists()
    assert not (rpr.ROOT / cc.TEST_REQUESTS_REL).exists()


# --- review fixes: the gate before 1b (queued cards), repeat before claim ---

def test_gate_before_1b_checks_a_queued_card_once():
    _set_orchestrator(ON)
    run_dir = _card_run("run_950", claim=_claim(kind="vibes"))   # no 1a ran in this run
    with pytest.raises(RuntimeError, match="its step 1a ran elsewhere"):
        rpr._claim_gate_before_1b(run_dir, "run_950", True)
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))
    assert rpr._claim_gate_before_1b(run_dir, "run_950", True) is None
    n = len(rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"])
    assert rpr._claim_gate_before_1b(run_dir, "run_950", True) is None       # passed: not again
    assert len(rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"]) == n


def test_gate_before_1b_parks_a_queued_tests_none_card_at_1b():
    _set_orchestrator(ON)
    run_dir = _card_run("run_951", claim=_claim(kind="lead_lag", tests="none", missing_block="mb"))
    assert rpr._claim_gate_before_1b(run_dir, "run_951", True) == "human_pause"
    marker = rpr.load_yaml(run_dir / "pipeline_state.yaml")[rpr.PARKED_KEY]
    assert marker["kind"] == "test" and marker["resume_stage"] == "strategy_config_authoring"
    row = rpr.load_yaml(rpr.ROOT / cc.TEST_REQUESTS_REL)["requests"][0]
    assert row["stage"] == "strategy_config_authoring"


def test_gate_before_1b_skips_a_run_whose_1a_check_passed(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_952", claim=_claim())
    _fake_1a(monkeypatch, run_dir, [])
    rpr._check_claim_after_1a("run_952", run_dir, [], {})
    monkeypatch.setattr(rpr, "_claim_check_once", lambda *a, **k: pytest.fail("checked twice"))
    assert rpr._claim_gate_before_1b(run_dir, "run_952", True) is None


def test_run_loop_queued_card_is_checked_before_1b_spends(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _loop_run("run_953")
    rpr.update_state(path=run_dir, pending_stage="strategy_config_authoring")
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml",
                  dict(CARD, claim=_claim(kind="lead_lag", tests="none", missing_block="mb")))
    seen = _fake_agent(monkeypatch, run_dir, [])
    rpr.run_loop("run_953")
    assert seen == []                                            # 1b never called
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml")["status"] == "paused_for_human"


def test_run_loop_repeat_card_ends_the_run_without_a_claim_retry(monkeypatch):
    """review fix 6: a repeated card ends completed_no_new_hypothesis; its bad
    claim spends no retry."""
    _set_orchestrator(ON)
    run_dir = _loop_run("run_954")
    seen = _fake_agent(monkeypatch, run_dir, [_claim(kind="vibes")])
    monkeypatch.setattr(rpr, "_brief_card_is_repeat", lambda rdir: True)
    rpr.run_loop("run_954")
    assert [s for s, _ in seen] == ["hypothesis_generation"]
    assert not (run_dir / "artifacts" / "claim_check.yaml").exists()
