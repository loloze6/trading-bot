"""E-068 slice 2 (CUL-389): step 1a writes the `claim` block.

Covers:
  1. tools/claim_card.check_claim: text fields, kind, 1-3 tests composed from
     the slots (check_spec's rules), code-fixed alpha/significance, regime
     selectors as effect-size only, tests: none / missing_block, criteria_refs;
  2. the 1a/1b match check (a warning, never a stop);
  3. the schema, CLAIM_TESTS.md and the code agree;
  4. the flag: reader, dependency, flag-off byte identity of every seam;
  5. run_loop: the claim check after 1a with one shared retry; INFORMATION
     ONLY -- never a stop, park or reroute; the recorded status, the coverage
     count, test_requests.yaml, the gate before 1b, the match warning;
  6. the power warning.

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
    assert res.errors == [] and not res.tests_none
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
    assert res.errors and not res.tests_none


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
    assert res.errors == [] and not res.tests_none
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

def test_tests_none_with_missing_block_is_flagged():
    res = cc.check_claim(_claim(kind="lead_lag", tests="none",
                                missing_block="outcome fwd_return_of(other_symbol, h)"))
    assert res.errors == [] and res.tests_none
    assert res.missing_block == "outcome fwd_return_of(other_symbol, h)"


def test_tests_none_needs_missing_block_and_missing_block_needs_none():
    assert any("missing_block" in e for e in cc.check_claim(_claim(tests="none")).errors)
    assert not cc.check_claim(_claim(tests="none")).tests_none
    assert any("only allowed with tests: none"
               in e for e in cc.check_claim(_claim(missing_block="x")).errors)
    res = cc.check_claim(_claim(tests="none", missing_block="x", criteria_refs=["a"]), ["a"])
    assert res.errors and not res.tests_none


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
    # E-068 3b: every field a selector may read is documented (past_return included)
    for name in ct.BAR_T_FIELDS:
        assert f"`{name}`" in text, name
    for name in ct.FIELDS_WITH_BARS:
        assert f"`{name}` (with `bars`)" in text, name


NOTE_1B = SR_ROOT / "workflow_artifacts" / "skills" / "strategy-config-authoring" / "CLAIM_NOTE.md"
SKILL_1B = SR_ROOT / "workflow_artifacts" / "skills" / "strategy-config-authoring" / "SKILL.md"


def test_claim_instructions_live_only_in_flag_on_inputs():
    """Flag-off prompts are byte-identical: neither SKILL.md mentions the claim
    (hypothesis-design's bytes are pinned by test_e059_s2a_review_fixes); the
    instructions are in CLAIM_TESTS.md / CLAIM_NOTE.md, added only under the flag."""
    for skill in (SKILL_1A, SKILL_1B):
        text = skill.read_text(encoding="utf-8")
        assert "CLAIM_TESTS" not in text and "CLAIM_NOTE" not in text and "claim_tests" not in text
    run_dir = SR_ROOT / "runs" / "run_x"
    assert (run_dir / rpr.CLAIM_TESTS_GUIDE).resolve() == GUIDE.resolve()
    assert (run_dir / rpr.CLAIM_1B_NOTE).resolve() == NOTE_1B.resolve()
    guide = GUIDE.read_text(encoding="utf-8")
    assert "every `hypothesis_card_<n>.yaml` too" in guide and "information only" in guide
    assert "parked" not in guide and "the run fails" not in guide


def test_coverage_path_is_shared_with_run_campaign():
    import run_campaign as camp
    assert camp.CLAIM_COVERAGE_REL == cc.COVERAGE_REL


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


def test_no_park_kind_was_added():
    assert rpr.PARK_KINDS == ("component", "data")


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
    for stage in ("hypothesis_generation", "strategy_config_authoring"):
        handoff = yaml.safe_load(HANDOFF_1A.read_text(encoding="utf-8"))
        snapshot = copy.deepcopy(handoff)
        rpr._apply_claim_tests_context(stage, handoff, run_dir)
        assert handoff == snapshot
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry",
                        lambda *a, **k: pytest.fail("no re-invoke with the flag off"))
    assert rpr._check_claim_after_1a("run_900", run_dir, [], {}) is None
    rpr._record_claim_match(run_dir)
    assert rpr._claim_gate_before_1b(run_dir, "run_900") is None
    assert sorted(p.name for p in (run_dir / "artifacts").iterdir()) == before
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["claim_check_retry"] == {"attempts": 1, "last_error": "x"}   # untouched
    assert state["status"] == "active" and not (run_dir / ".previous_attempts").exists()
    assert not (rpr.ROOT / cc.COVERAGE_REL).exists()


def test_flag_off_post_1b_route_writes_no_match_file():
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    run_dir = _authored_1b("run_901", GOOD)
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert not (run_dir / "artifacts" / "claim_match.yaml").exists()


def test_flag_on_context_adds_the_guide_to_1a_and_the_note_to_1b():
    _set_orchestrator(ON)
    run_dir = _card_run("run_902")
    handoff = yaml.safe_load(HANDOFF_1A.read_text(encoding="utf-8"))
    rpr._apply_claim_tests_context("hypothesis_generation", handoff, run_dir)
    rpr._apply_claim_tests_context("hypothesis_generation", handoff, run_dir)   # idempotent
    paths = [r["path"] for r in handoff["required_inputs"]]
    assert paths.count(rpr.CLAIM_TESTS_GUIDE) == 1 and rpr.CLAIM_1B_NOTE not in paths
    assert "claim_check_error" not in (handoff.get("injected_context") or {})
    h1b = {"required_inputs": []}
    rpr._apply_claim_tests_context("strategy_config_authoring", h1b, run_dir)
    assert [r["path"] for r in h1b["required_inputs"]] == [rpr.CLAIM_1B_NOTE]
    other = {"required_inputs": []}
    rpr._apply_claim_tests_context("innovation_expansion", other, run_dir)
    assert other == {"required_inputs": []}


# ---------------------------------------------------------------------------
# 5. the check after 1a: information only -- never a stop, park or reroute
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


def _status(run_dir) -> dict:
    return rpr.load_yaml(run_dir / "artifacts" / "claim_test_status.yaml")


def _coverage() -> dict:
    return rpr.load_yaml(rpr.ROOT / cc.COVERAGE_REL)["runs"]


def test_good_claim_passes_without_retry(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_910", claim=_claim())
    calls = _fake_1a(monkeypatch, run_dir, [])
    assert rpr._check_claim_after_1a("run_910", run_dir, [], {}) is None
    assert calls == []
    st = _status(run_dir)
    assert st["usable"] is True and st["reason"] is None and st["tests"][0]["verdict_possible"]
    assert _coverage()["run_910"] == {"usable": True, "reason": None, "power_warning": False}


def test_bad_claim_retries_once_with_the_error_then_passes(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_911", claim=_claim(kind="vibes"))
    calls = _fake_1a(monkeypatch, run_dir, [_claim()])
    rpr._check_claim_after_1a("run_911", run_dir, [], {})
    assert len(calls) == 1 and "claim.kind" in calls[0] and "Retry 1/1" in calls[0]
    rec = rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"]
    errs = [bool(a["cards"]["hypothesis_card.yaml"]["errors"]) for a in rec]
    assert errs == [True, False]
    assert _status(run_dir)["usable"] is True
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml")["claim_check_retry"]["attempts"] == 0


def test_bad_claim_twice_is_recorded_and_the_run_continues(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_912", claim=_claim(kind="vibes"))
    calls = _fake_1a(monkeypatch, run_dir, [_claim(tests=[dict(UPPER, alpha=0.2)])])
    assert rpr._check_claim_after_1a("run_912", run_dir, [], {}) is None    # no raise
    assert len(calls) == 1                                                  # one retry only
    st = _status(run_dir)
    assert st["usable"] is False and st["reason"] == "invalid_claim" and "fixed by code" in st["detail"]
    assert _coverage()["run_912"]["reason"] == "invalid_claim"
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml")["status"] == "active"


def test_missing_claim_after_the_retry_is_no_claim(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_913")                                  # no claim at all
    calls = _fake_1a(monkeypatch, run_dir, [None])
    rpr._check_claim_after_1a("run_913", run_dir, [], {})
    assert "a `claim` mapping is required" in calls[0]
    assert _status(run_dir)["reason"] == "no_claim"


def test_a_resume_after_the_retry_does_not_retry_again(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_914", claim=_claim(kind="vibes"))
    rpr.update_state(path=run_dir, claim_check_retry={"attempts": 1, "last_error": "x"})
    calls = _fake_1a(monkeypatch, run_dir, [])
    rpr._check_claim_after_1a("run_914", run_dir, [], {})
    assert calls == [] and _status(run_dir)["reason"] == "invalid_claim"


def test_tests_none_is_recorded_with_a_request_and_never_parks(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_915", claim=_claim(kind="lead_lag", tests="none", missing_block="mb"))
    calls = _fake_1a(monkeypatch, run_dir, [])
    rpr._check_claim_after_1a("run_915", run_dir, [], {})
    rpr._check_claim_after_1a("run_915", run_dir, [], {})          # a re-run: no duplicate row
    assert calls == []                                             # not an error: no retry
    st = _status(run_dir)
    assert st["usable"] is False and st["reason"] == "tests_none" and st["detail"] == "mb"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "active" and not state.get(rpr.PARKED_KEY)
    rows = rpr.load_yaml(rpr.ROOT / cc.TEST_REQUESTS_REL)["requests"]
    assert rows == [{"run_id": "run_915", "stage": "hypothesis_generation",
                     "card": "hypothesis_card.yaml", "hypothesis_id": "H-1",
                     "claim_kind": "lead_lag", "statement": _claim()["statement"],
                     "missing_block": "mb"}]


def test_regime_claim_is_usable_effect_size_only(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_916", claim=_claim(kind="regime_classifier", tests=[REGIME]))
    _fake_1a(monkeypatch, run_dir, [])
    rpr._check_claim_after_1a("run_916", run_dir, [], {})
    st = _status(run_dir)
    assert st["usable"] is True
    assert st["tests"][0]["verdict_possible"] is False and st["tests"][0]["reason"] == cc.REGIME_REASON
    assert not (rpr.ROOT / cc.TEST_REQUESTS_REL).exists()


def test_criteria_only_claim_is_recorded_as_such(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_917", claim=_claim(kind="cost_turnover", tests=None,
                                                criteria_refs=["realized_edge_to_cost_ratio"]),
                        criteria=[{"id": "realized_edge_to_cost_ratio"}])
    _fake_1a(monkeypatch, run_dir, [])
    rpr._check_claim_after_1a("run_917", run_dir, [], {})
    assert _status(run_dir)["reason"] == "criteria_refs_only"


@pytest.mark.parametrize("brief,why", [
    ({"config": {"a": 1}, "manifest": {"b": 1}, "criteria": [{"id": "x"}], "source": "op"},
     "pass_through"),
    ({"candidate": {"composition": {"registry_hash": "h"}}}, "composition"),
], ids=["pass_through", "composition"])
def test_exempt_cards_are_decided_by_the_runs_inputs(monkeypatch, brief, why):
    _set_orchestrator(ON)
    run_dir = _card_run("run_918", pass_through=True)
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", brief)
    calls = _fake_1a(monkeypatch, run_dir, [])
    rpr._check_claim_after_1a("run_918", run_dir, [], {})
    st = _status(run_dir)
    assert calls == [] and st["reason"] == "exempt" and why in st["detail"]


def test_a_card_cannot_exempt_itself(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_919", pass_through=True)
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", {"research_goal": "x"})
    calls = _fake_1a(monkeypatch, run_dir, [_claim()])
    rpr._check_claim_after_1a("run_919", run_dir, [], {})
    assert len(calls) == 1 and "claim` mapping is required" in calls[0]


def test_retry_sets_aside_the_old_card_and_has_its_own_audit_key(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_920", claim=_claim(kind="vibes"))
    seen = []

    def _invoke(stage, run_id, rdir, expected, state):
        seen.append((rdir / "artifacts" / "hypothesis_card.yaml").exists())
        handoff = {"required_inputs": [], "injected_context": {"stage_attempt": "1"}}
        rpr._apply_claim_tests_context(stage, handoff, rdir)
        seen.append(handoff["injected_context"]["stage_attempt"])
        rpr.save_yaml(rdir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    rpr._check_claim_after_1a("run_920", run_dir, [], {})
    assert seen == [False, "1_claim_retry1"]
    kept = (run_dir / ".previous_attempts" / "hypothesis_generation_claim_retry1"
            / "hypothesis_card.yaml")
    assert rpr.load_yaml(kept)["claim"]["kind"] == "vibes"


@pytest.mark.parametrize("failure", ["no_card", "exception", "repeat"])
def test_a_retry_that_produces_nothing_usable_is_undone(monkeypatch, failure):
    """The retry's own outputs are set aside, the first card comes back, the
    run continues with the first card's status recorded."""
    _set_orchestrator(ON)
    run_dir = _card_run("run_921", claim=_claim(kind="vibes"))

    def _invoke(stage, run_id, rdir, expected, state):
        if failure == "no_card":
            raise FileNotFoundError("hypothesis_card.yaml")
        if failure == "exception":
            raise RuntimeError("sdk down")
        rpr.save_yaml(rdir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    if failure == "repeat":
        monkeypatch.setattr(rpr, "_brief_card_is_repeat", lambda rdir: True)
    assert rpr._check_claim_after_1a("run_921", run_dir, [], {}) is None
    card = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")
    assert card["claim"]["kind"] == "vibes"                       # the first card is back
    assert _status(run_dir)["reason"] == "invalid_claim"
    rec = rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"]
    assert any("retry_undone" in a for a in rec)


def test_retry_answer_with_several_cards_is_split(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_922", claim=_claim(kind="vibes"))

    def _invoke(*a, **k):
        raise FileNotFoundError("hypothesis_card.yaml")

    def _split(run_id, rdir):
        rpr.save_yaml(rdir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))
        return True

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    monkeypatch.setattr(rpr, "_decide_next_enabled", lambda *a: True)    # the queue path
    monkeypatch.setattr(rpr, "_handle_hypothesis_generation_multi_card_split", _split)
    monkeypatch.setattr(rpr, "_brief_single_card_check",
                        lambda rdir: pytest.fail("single-card check after a split"))
    rpr._check_claim_after_1a("run_922", run_dir, [], {})
    assert _status(run_dir)["usable"] is True


def test_a_legacy_split_answer_on_the_retry_is_undone(monkeypatch):
    """review 2 #8: decide_next off, the retry answers several cards: the legacy
    split (new sibling runs) is never repeated -- the retry is undone."""
    _set_orchestrator(ON)
    run_dir = _card_run("run_929", claim=_claim(kind="vibes"))

    def _invoke(*a, **k):
        raise FileNotFoundError("hypothesis_card.yaml")

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    monkeypatch.setattr(rpr, "_handle_hypothesis_generation_multi_card_split",
                        lambda *a: pytest.fail("legacy split repeated by the retry"))
    rpr._check_claim_after_1a("run_929", run_dir, [], {})
    assert rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]["kind"] == "vibes"
    assert _status(run_dir)["reason"] == "invalid_claim"


def test_a_retry_card_next_to_an_exhausted_signal_is_undone(monkeypatch):
    """review 2 #8: a card plus brief_status.yaml (exhausted) is contradictory."""
    _set_orchestrator(ON)
    run_dir = _card_run("run_930b", claim=_claim(kind="vibes"))

    def _invoke(stage, run_id, rdir, expected, state):
        rpr.save_yaml(rdir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)

    def _contradiction(rdir):
        raise ValueError("exhausted next to a card")

    monkeypatch.setattr(rpr, "_brief_exhausted_signal", _contradiction)
    rpr._check_claim_after_1a("run_930b", run_dir, [], {})
    assert rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]["kind"] == "vibes"


def test_set_aside_and_restore():
    run_dir = _card_run("run_923", claim=_claim())
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card_2.yaml", {"x": 1})
    rpr.save_yaml(arts / "brief_repeat.yaml", {"stale": True})
    rpr.save_yaml(arts / "queued_hypotheses.yaml", {"enqueued": True})
    names = rpr._set_aside_1a_outputs(run_dir, "t")
    assert set(names) == {"hypothesis_card.yaml", "hypothesis_card_2.yaml", "brief_repeat.yaml"}
    assert (arts / "queued_hypotheses.yaml").exists()              # enqueued: stays
    rpr.save_yaml(arts / "hypothesis_card.yaml", {"retry": True})
    rpr._restore_1a_outputs(run_dir, "t", names)
    assert rpr.load_yaml(arts / "hypothesis_card.yaml")["claim"] == _claim()
    assert rpr.load_yaml(arts / "hypothesis_card_2.yaml") == {"x": 1}
    assert (run_dir / ".previous_attempts" / "hypothesis_generation_t_failed"
            / "hypothesis_card.yaml").exists()


def test_a_reused_tag_never_mixes_two_attempts():
    """review 2 #3: the set-aside folder is emptied first, and restore moves back
    only what this call set aside."""
    run_dir = _card_run("run_923b", claim=_claim())
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card_2.yaml", {"old": True})
    rpr._set_aside_1a_outputs(run_dir, "claim_retry1")              # an earlier attempt
    rpr.save_yaml(arts / "hypothesis_card.yaml", dict(CARD, claim=_claim(kind="vibes")))
    names = rpr._set_aside_1a_outputs(run_dir, "claim_retry1")      # this attempt
    assert names == ["hypothesis_card.yaml"]
    folder = run_dir / ".previous_attempts" / "hypothesis_generation_claim_retry1"
    assert sorted(p.name for p in folder.iterdir()) == ["hypothesis_card.yaml"]   # emptied first
    rpr.save_yaml(folder / "stray.yaml", {"x": 1})                  # not set aside by this call
    rpr._restore_1a_outputs(run_dir, "claim_retry1", names)
    assert not (arts / "hypothesis_card_2.yaml").exists()           # the stale card stays away
    assert not (arts / "stray.yaml").exists()                       # only `names` come back


def test_a_failed_retry_restores_the_runs_queued_card_copies(monkeypatch):
    """review 2 #2: the retry's split rewrites campaign_record/queued_cards/<run>/;
    undoing the retry brings the first copies back, so every card_ref resolves."""
    _set_orchestrator(ON)
    run_dir = _card_run("run_931b", claim=_claim(kind="vibes"))
    qdir = rpr.ROOT / "campaign_record" / "queued_cards" / "run_931b"
    qdir.mkdir(parents=True)
    rpr.save_yaml(qdir / "hypothesis_card_2.yaml", {"first": True})
    rpr.save_yaml(run_dir / "artifacts" / "queued_hypotheses.yaml",
                  {"enqueued": False, "cards": [{"card_ref":
                   "campaign_record/queued_cards/run_931b/hypothesis_card_2.yaml"}]})
    monkeypatch.setattr(rpr, "_decide_next_enabled", lambda *a: True)

    def _invoke(*a, **k):
        raise FileNotFoundError("hypothesis_card.yaml")

    def _split(run_id, rdir):                 # rewrites the copies, then the retry fails
        shutil.rmtree(qdir)
        rpr.save_yaml(rdir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))
        return True

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    monkeypatch.setattr(rpr, "_handle_hypothesis_generation_multi_card_split", _split)
    monkeypatch.setattr(rpr, "_brief_card_is_repeat", lambda rdir: True)
    rpr._check_claim_after_1a("run_931b", run_dir, [], {})
    assert rpr.load_yaml(qdir / "hypothesis_card_2.yaml") == {"first": True}
    assert rpr.load_yaml(run_dir / "artifacts" / "queued_hypotheses.yaml")["enqueued"] is False


def test_the_safety_net_never_raises_on_a_broken_coverage_file(monkeypatch):
    """review 2 #1: a coverage file that is not a mapping makes record_coverage
    raise; the claim check and the gate still never raise."""
    _set_orchestrator(ON)
    path = rpr.ROOT / cc.COVERAGE_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("- a list\n", encoding="utf-8")
    run_dir = _card_run("run_932b", claim=_claim())
    _fake_1a(monkeypatch, run_dir, [])
    assert rpr._check_claim_after_1a("run_932b", run_dir, [], {}) is None
    assert _status(run_dir)["reason"] == "check_error"
    run_dir2 = _card_run("run_933b", claim=_claim())
    assert rpr._claim_gate_before_1b(run_dir2, "run_933b") is None


def test_summary_survives_an_unreadable_coverage_file(tmp_path):
    path = tmp_path / cc.COVERAGE_REL
    path.parent.mkdir(parents=True)
    path.write_text("runs: [unclosed\n", encoding="utf-8")
    assert "unreadable" in "\n".join(cc.coverage_summary_lines(tmp_path))


# --- (3) every card 1a wrote is checked ---------------------------------------

def test_every_card_is_checked_and_an_extra_cards_error_gets_the_retry(monkeypatch):
    _set_orchestrator(ON)
    _set_orchestrator(dict(ON, decide_next={"enabled": False}))
    run_dir = _card_run("run_924", claim=_claim())
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card_1.yaml", dict(CARD, claim=_claim()))
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card_2.yaml",
                  dict(CARD, hypothesis_id="H-2", claim=_claim(kind="vibes")))
    monkeypatch.setattr(rpr, "_decide_next_enabled", lambda *a: True)    # the queue path

    def _invoke(stage, run_id, rdir, expected, state):
        arts = rdir / "artifacts"
        rpr.save_yaml(arts / "hypothesis_card.yaml", dict(CARD, claim=_claim()))
        rpr.save_yaml(arts / "hypothesis_card_2.yaml",
                      dict(CARD, hypothesis_id="H-2", claim=_claim()))

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    rpr._check_claim_after_1a("run_924", run_dir, [], {})
    first = rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"][0]["cards"]
    assert set(first) == {"hypothesis_card.yaml", "hypothesis_card_2.yaml"}   # _1 == kept card
    assert first["hypothesis_card_2.yaml"]["errors"]
    assert _status(run_dir)["usable"] is True
    assert "other_cards_without_a_usable_claim_test" not in _status(run_dir)


def test_extra_card_without_a_claim_is_recorded_on_the_run(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_925", claim=_claim())
    rpr.update_state(path=run_dir, claim_check_retry={"attempts": 1, "last_error": "x"})
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card_2.yaml",
                  dict(CARD, hypothesis_id="H-2"))
    monkeypatch.setattr(rpr, "_decide_next_enabled", lambda *a: True)
    _fake_1a(monkeypatch, run_dir, [])
    rpr._check_claim_after_1a("run_925", run_dir, [], {})
    st = _status(run_dir)
    assert st["usable"] is True
    assert st["other_cards_without_a_usable_claim_test"] == {"hypothesis_card_2.yaml": "no_claim"}


def test_legacy_split_never_retries(monkeypatch):
    """decide_next off: a retry would scaffold a second set of 1b-skipping
    siblings (CUL-392), so there is no retry -- the gaps are recorded."""
    _set_orchestrator(ON)
    run_dir = _card_run("run_926", claim=_claim(kind="vibes"))
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card_2.yaml",
                  dict(CARD, hypothesis_id="H-2", claim=_claim()))
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry",
                        lambda *a, **k: pytest.fail("legacy split retried"))
    rpr._check_claim_after_1a("run_926", run_dir, [], {})
    assert _status(run_dir)["reason"] == "invalid_claim"


def test_a_check_bug_is_recorded_never_raised(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_927", claim=_claim())

    def _boom(*a, **k):
        raise KeyError("bug")

    monkeypatch.setattr(rpr, "_claim_check_cards", _boom)
    assert rpr._check_claim_after_1a("run_927", run_dir, [], {}) is None
    assert rpr._claim_gate_before_1b(run_dir, "run_927") is None
    assert _status(run_dir)["reason"] == "check_error"


# --- the match warning after 1b -------------------------------------------------

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


# --- the gate before 1b: warn-only for every card -------------------------------

@pytest.mark.parametrize("claim,reason", [
    (_claim(kind="vibes"), "invalid_claim"),
    (None, "no_claim"),                                            # queued before the flag
    (_claim(kind="lead_lag", tests="none", missing_block="mb"), "tests_none"),
], ids=["invalid", "no_claim", "tests_none"])
def test_gate_before_1b_records_and_never_raises(claim, reason):
    _set_orchestrator(ON)
    run_dir = _card_run("run_950", claim=claim)                    # no 1a ran in this run
    assert rpr._claim_gate_before_1b(run_dir, "run_950") is None
    st = _status(run_dir)
    assert st["reason"] == reason and st["stage"] == "strategy_config_authoring"
    assert not rpr.load_yaml(run_dir / "pipeline_state.yaml").get(rpr.PARKED_KEY)


def test_gate_before_1b_exempts_a_real_pass_through_card():
    _set_orchestrator(ON)
    run_dir = _card_run("run_951", pass_through=True)
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                  {"config": {"a": 1}, "manifest": {"b": 1}, "criteria": [{"id": "x"}],
                   "source": "op"})
    assert rpr._claim_gate_before_1b(run_dir, "run_951") is None
    assert _status(run_dir)["reason"] == "exempt"


def test_gate_before_1b_skips_a_run_whose_1a_check_ran(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_952", claim=_claim(kind="vibes"))
    _fake_1a(monkeypatch, run_dir, [_claim(kind="vibes")])
    rpr._check_claim_after_1a("run_952", run_dir, [], {})
    monkeypatch.setattr(rpr, "_claim_check_cards", lambda *a, **k: pytest.fail("checked twice"))
    assert rpr._claim_gate_before_1b(run_dir, "run_952") is None


# --- coverage and the campaign summary -------------------------------------------

def test_coverage_counts_and_summary_lines(tmp_path):
    assert cc.coverage_summary_lines(tmp_path) == []               # no file: unchanged
    cc.record_coverage(tmp_path, "run_1", {"usable": True, "reason": None})
    cc.record_coverage(tmp_path, "run_2", {"usable": False, "reason": "no_claim"})
    cc.record_coverage(tmp_path, "run_3", {"usable": False, "reason": "tests_none"})
    cc.record_coverage(tmp_path, "run_4", {"usable": True, "reason": None,
                                           "power_warnings": [{"x": 1}]})
    cc.record_coverage(tmp_path, "run_2", {"usable": True, "reason": None})   # latest wins
    text = "\n".join(cc.coverage_summary_lines(tmp_path))
    assert "Runs with a usable claim test: 3" in text and "Runs without one: 1" in text
    assert "tests_none: 1 (run_3)" in text and "power warning): 1 (run_4)" in text


def test_campaign_summary_shows_claim_tests_only_when_recorded(monkeypatch):
    import run_campaign as camp
    queue = {"version": "1.0", "queue": []}
    camp._regenerate_summary(queue)
    assert "Claim tests" not in camp.CAMPAIGN_SUMMARY_PATH.read_text(encoding="utf-8")
    cc.record_coverage(camp.ROOT, "run_1", {"usable": False, "reason": "invalid_claim"})
    camp._regenerate_summary(queue)
    text = camp.CAMPAIGN_SUMMARY_PATH.read_text(encoding="utf-8")
    assert "## Claim tests" in text and "invalid_claim: 1 (run_1)" in text


# --- run_loop end to end on fixtures ----------------------------------------------

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
            # O-21: a complete gap (tried, with a transform) so the loop still stops here
            rpr.save_yaml(arts / "decision.yaml", {"stage": stage_name, "status": "component_gap",
                                                   "rationale": "stop here",
                                                   "blocking_issues": ["x"],
                                                   "tried": [{"config": "X + [zscore]",
                                                              "fails_on": "x"}]})
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


def test_run_loop_second_bad_claim_still_reaches_1b(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _loop_run("run_941")
    seen = _fake_agent(monkeypatch, run_dir, [_claim(kind="vibes"), _claim(kind="vibes")])
    rpr.run_loop("run_941")
    assert [s for s, _ in seen] == ["hypothesis_generation", "hypothesis_generation",
                                    "strategy_config_authoring"]
    assert _status(run_dir)["reason"] == "invalid_claim"


def test_run_loop_tests_none_reaches_1b(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _loop_run("run_942")
    seen = _fake_agent(monkeypatch, run_dir, [_claim(kind="lead_lag", tests="none",
                                                     missing_block="fwd_return_of")])
    rpr.run_loop("run_942")
    assert [s for s, _ in seen] == ["hypothesis_generation", "strategy_config_authoring"]
    assert rpr.load_yaml(rpr.ROOT / cc.TEST_REQUESTS_REL)["requests"][0]["run_id"] == "run_942"


def test_run_loop_flag_off_never_checks_a_claim(monkeypatch):
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    run_dir = _loop_run("run_943")
    seen = _fake_agent(monkeypatch, run_dir, [{"broken": True}])
    rpr.run_loop("run_943")
    assert [s for s, _ in seen] == ["hypothesis_generation", "strategy_config_authoring"]
    assert not (run_dir / "artifacts" / "claim_check.yaml").exists()
    assert not (run_dir / "artifacts" / "claim_test_status.yaml").exists()
    assert not (rpr.ROOT / cc.TEST_REQUESTS_REL).exists()


def test_run_loop_queued_card_is_checked_warn_only_and_1b_runs(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _loop_run("run_953")
    rpr.update_state(path=run_dir, pending_stage="strategy_config_authoring")
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", dict(CARD))   # no claim
    seen = _fake_agent(monkeypatch, run_dir, [])
    rpr.run_loop("run_953")
    assert [s for s, _ in seen] == ["strategy_config_authoring"]
    assert _status(run_dir)["reason"] == "no_claim"


def test_run_loop_repeat_card_ends_the_run_without_a_claim_check(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _loop_run("run_954")
    seen = _fake_agent(monkeypatch, run_dir, [_claim(kind="vibes")])
    monkeypatch.setattr(rpr, "_brief_card_is_repeat", lambda rdir: True)
    rpr.run_loop("run_954")
    assert [s for s, _ in seen] == ["hypothesis_generation"]
    assert not (run_dir / "artifacts" / "claim_check.yaml").exists()


# ---------------------------------------------------------------------------
# 6. power warning (operator, 2026-10-03): can the floor be reached at all?
# ---------------------------------------------------------------------------

DAILY_2M = [{"label": "2022-01", "test": {"start": "2022-01-01", "end": "2022-01-31"}},
            {"label": "2022-02", "test": {"start": "2022-02-01", "end": "2022-02-28"}}]


def test_timeframe_seconds():
    assert cc.timeframe_seconds("15m") == 900
    assert cc.timeframe_seconds("1h") == 3600
    assert cc.timeframe_seconds("4h") == 14400
    assert cc.timeframe_seconds("1d") == 86400
    assert cc.timeframe_seconds("1x") is None and cc.timeframe_seconds("h") is None
    assert cc.timeframe_seconds(None) is None


def test_window_bars_counts_the_end_day():
    assert cc.window_bars(DAILY_2M, 86400) == 31 + 28
    assert cc.window_bars(DAILY_2M[:1], 3600) == 31 * 24
    with pytest.raises(ValueError):
        cc.window_bars([{"label": "x"}], 86400)


def test_power_bound_is_bars_over_longest_horizon_times_coins():
    claim = _claim(tests=[dict(UPPER, floor={"min_events": 100})])   # horizons 1..5
    w = cc.power_warnings(claim, 59, 1)                                # 59 // 5 * 1 = 11
    assert len(w) == 1 and w[0]["bound"] == 11 and w[0]["floor"] == 100
    assert w[0]["message"] == ("test 'upper_breakout': at most 11 separate events are possible, "
                               "the floor is 100: shorten the horizon or widen the data")
    assert cc.power_warnings(claim, 59, 9)[0]["bound"] == 99           # x coins
    assert cc.power_warnings(claim, 500, 1) == []                      # 100 == floor: reachable
    assert cc.power_warnings(claim, 499, 1)[0]["bound"] == 99
    assert cc.power_warnings(_claim(tests=[dict(UPPER, floor={"min_windows": 4})]), 1, 1) == []
    assert cc.power_warnings(_claim(tests=None, criteria_refs=["x"]), 1, 1) == []


def _protocol(run_id, windows=DAILY_2M, symbols=("BTCUSD",), tf="1d"):
    d = rpr.ROOT / "protocols"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{run_id}_generated.json").write_text(json.dumps(
        {"symbols": list(symbols), "timeframe": tf, "windows": windows}), encoding="utf-8")


LOW = dict(UPPER, floor={"min_events": 100})       # bound 11 on DAILY_2M, one coin
REACHABLE = dict(UPPER, floor={"min_events": 10})


def test_power_shortfall_retries_1a_once_with_the_message(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_960", claim=_claim(tests=[LOW]))
    _protocol("run_960")
    calls = _fake_1a(monkeypatch, run_dir, [_claim(tests=[REACHABLE])])
    rpr._check_claim_after_1a("run_960", run_dir, [], {})
    assert len(calls) == 1 and "cannot reach their floor" in calls[0]
    assert "at most 11 separate events are possible, the floor is 100: shorten the horizon " \
           "or widen the data" in calls[0]
    checks = rpr.load_yaml(run_dir / "artifacts" / "claim_power.yaml")["checks"]
    assert [c["status"] for c in checks] == ["below_floor", "ok"]
    assert checks[0]["bars"] == 59 and checks[0]["coins"] == 1
    assert _status(run_dir)["usable"] is True and "power_warnings" not in _status(run_dir)


def test_power_shortfall_after_the_retry_is_recorded_and_never_stops(monkeypatch, capsys):
    _set_orchestrator(ON)
    run_dir = _card_run("run_961", claim=_claim(tests=[LOW]))
    _protocol("run_961")
    calls = _fake_1a(monkeypatch, run_dir, [_claim(tests=[LOW])])
    assert rpr._check_claim_after_1a("run_961", run_dir, [], {}) is None
    assert len(calls) == 1
    checks = rpr.load_yaml(run_dir / "artifacts" / "claim_power.yaml")["checks"]
    assert [c["status"] for c in checks] == ["below_floor", "below_floor"]
    st = _status(run_dir)
    assert st["usable"] is True and st["power_warnings"][0]["bound"] == 11
    assert _coverage()["run_961"]["power_warning"] is True
    assert "power warning" in capsys.readouterr().out


def test_power_warning_then_an_invalid_retry_continues_with_a_warning(monkeypatch):
    """(4): the power shortfall spends the one retry; the retry writes an
    invalid claim; nothing stops -- the run continues with the gap recorded."""
    _set_orchestrator(ON)
    run_dir = _card_run("run_962", claim=_claim(tests=[LOW]))
    _protocol("run_962")
    calls = _fake_1a(monkeypatch, run_dir, [_claim(kind="vibes", tests=[REACHABLE])])
    assert rpr._check_claim_after_1a("run_962", run_dir, [], {}) is None
    assert len(calls) == 1 and "cannot reach their floor" in calls[0]
    # review 2 #4: the retry left the card worse (usable -> invalid), so it is
    # undone: the first claim is kept with its power warning
    st = _status(run_dir)
    assert st["usable"] is True and st["power_warnings"][0]["bound"] == 11
    assert rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]["tests"] == [LOW]
    rec = rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"]
    assert any(a.get("retry_undone") == "worse than the first answer" for a in rec)
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml")["status"] == "active"


def test_power_and_claim_share_one_retry(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_963", claim=_claim(kind="vibes", tests=[LOW]))
    _protocol("run_963")
    calls = _fake_1a(monkeypatch, run_dir, [_claim(tests=[LOW])])
    rpr._check_claim_after_1a("run_963", run_dir, [], {})
    assert len(calls) == 1 and "claim.kind" in calls[0]                 # spent on the claim
    assert _status(run_dir)["power_warnings"]                          # then recorded only


def test_power_check_is_skipped_without_a_readable_protocol(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_964", claim=_claim(tests=[LOW]))
    calls = _fake_1a(monkeypatch, run_dir, [])
    rpr._check_claim_after_1a("run_964", run_dir, [], {})
    assert calls == []
    check = rpr.load_yaml(run_dir / "artifacts" / "claim_power.yaml")["checks"][0]
    assert check["status"] == "skipped" and "no protocol readable" in check["reason"]


def test_power_inputs_from_protocol_ref_and_from_constraints():
    run_dir = _card_run("run_965")
    d = rpr.ROOT / "protocols"
    d.mkdir(parents=True, exist_ok=True)
    (d / "pinned.json").write_text(json.dumps({"symbols": ["A", "B"], "timeframe": "4h",
                                               "windows": DAILY_2M}), encoding="utf-8")
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml",
                  {"machine_constraints": {"protocol_ref": "protocols/pinned.json"}})
    windows, symbols, tf, _ = rpr._claim_power_inputs(run_dir, "run_965")
    assert symbols == ["A", "B"] and tf == "4h" and windows == DAILY_2M
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", {"machine_constraints": {
        "protocol": {"symbols": ["A"], "timeframe": "1d", "start": "2022-01-01",
                     "end": "2022-02-28", "window_months": 1}}})
    windows, symbols, tf, _ = rpr._claim_power_inputs(run_dir, "run_965")
    assert cc.window_bars(windows, 86400) == 59 and symbols == ["A"]


def test_gate_before_1b_records_a_power_warning_and_proceeds():
    _set_orchestrator(ON)
    run_dir = _card_run("run_966", claim=_claim(tests=[LOW]))
    _protocol("run_966")
    assert rpr._claim_gate_before_1b(run_dir, "run_966") is None
    check = rpr.load_yaml(run_dir / "artifacts" / "claim_power.yaml")["checks"][0]
    assert check["status"] == "below_floor" and check["stage"] == "strategy_config_authoring"
    assert _status(run_dir)["power_warnings"]


def test_run_loop_power_shortfall_twice_still_reaches_1b(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _loop_run("run_967")
    _protocol("run_967")
    seen = _fake_agent(monkeypatch, run_dir, [_claim(tests=[LOW]), _claim(tests=[LOW])])
    rpr.run_loop("run_967")
    assert [s for s, _ in seen] == ["hypothesis_generation", "hypothesis_generation",
                                    "strategy_config_authoring"]
    assert "separate events" in seen[1][1]


def test_flag_off_writes_no_power_file():
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    run_dir = _card_run("run_968", claim=_claim(tests=[LOW]))
    _protocol("run_968")
    assert rpr._check_claim_after_1a("run_968", run_dir, [], {}) is None
    assert not (run_dir / "artifacts" / "claim_power.yaml").exists()


def test_a_gate_bug_on_a_fresh_run_is_recorded_never_raised(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_928", claim=_claim())

    def _boom(*a, **k):
        raise KeyError("bug")

    monkeypatch.setattr(rpr, "_claim_check_cards", _boom)
    assert rpr._claim_gate_before_1b(run_dir, "run_928") is None
    st = _status(run_dir)
    assert st["reason"] == "check_error" and st["stage"] == "strategy_config_authoring"


def test_test_requests_of_two_cards_with_the_same_missing_block_are_both_kept(tmp_path):
    row = {"run_id": "run_1", "stage": "hypothesis_generation", "missing_block": "x"}
    assert cc.append_test_requests(tmp_path, [dict(row, hypothesis_id="H-1"),
                                              dict(row, hypothesis_id="H-2")]) == 2


def test_a_worse_retry_after_two_splits_restores_the_first_queue(monkeypatch):
    """Both answers split; the retry is worse, so it is undone: the first
    queued_hypotheses.yaml comes back and every card_ref resolves to the
    first answer's copies."""
    _set_orchestrator(ON)
    run_dir = _card_run("run_934", claim=_claim(tests=[LOW]))           # usable, power warning
    _protocol("run_934")
    qdir = rpr.ROOT / "campaign_record" / "queued_cards" / "run_934"
    qdir.mkdir(parents=True)
    rpr.save_yaml(qdir / "hypothesis_card_2.yaml", {"first": True})
    ref = "campaign_record/queued_cards/run_934/hypothesis_card_2.yaml"
    rpr.save_yaml(run_dir / "artifacts" / "queued_hypotheses.yaml",
                  {"enqueued": False, "cards": [{"card_ref": ref}], "attempt": "first"})
    monkeypatch.setattr(rpr, "_decide_next_enabled", lambda *a: True)

    def _invoke(*a, **k):
        raise FileNotFoundError("hypothesis_card.yaml")

    def _split(run_id, rdir):                                          # the retry's own split
        shutil.rmtree(qdir)
        qdir.mkdir()
        rpr.save_yaml(qdir / "hypothesis_card_2.yaml", {"retry": True})
        rpr.save_yaml(rdir / "artifacts" / "queued_hypotheses.yaml",
                      {"enqueued": False, "cards": [{"card_ref": ref}], "attempt": "retry"})
        rpr.save_yaml(rdir / "artifacts" / "hypothesis_card.yaml",
                      dict(CARD, claim=_claim(kind="vibes")))           # worse: invalid
        return True

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    monkeypatch.setattr(rpr, "_handle_hypothesis_generation_multi_card_split", _split)
    rpr._check_claim_after_1a("run_934", run_dir, [], {})
    queue = rpr.load_yaml(run_dir / "artifacts" / "queued_hypotheses.yaml")
    assert queue["attempt"] == "first"
    assert rpr.load_yaml(rpr.ROOT / queue["cards"][0]["card_ref"]) == {"first": True}
    assert _status(run_dir)["usable"] is True


def test_a_failing_set_aside_on_the_retry_is_undone_and_never_raises(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_935", claim=_claim(kind="vibes"))
    real = rpr._set_aside_1a_outputs
    calls = []

    def _flaky(rdir, tag, run_id=None):
        calls.append(tag)
        if len(calls) == 1:                    # the retry's set-aside: move, then fail
            real(rdir, tag)
            raise OSError("locked file")
        return real(rdir, tag, run_id)

    monkeypatch.setattr(rpr, "_set_aside_1a_outputs", _flaky)
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry",
                        lambda *a, **k: pytest.fail("1a re-invoked after a failed set-aside"))
    assert rpr._check_claim_after_1a("run_935", run_dir, [], {}) is None
    assert rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]["kind"] == "vibes"
    assert _status(run_dir)["reason"] == "invalid_claim"


def test_legacy_undo_message_says_what_happened(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _card_run("run_936", claim=_claim(kind="vibes"))

    def _invoke(*a, **k):
        raise FileNotFoundError("hypothesis_card.yaml")

    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _invoke)
    rpr._check_claim_after_1a("run_936", run_dir, [], {})
    rec = rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"]
    undone = [a["retry_undone"] for a in rec if "retry_undone" in a]
    assert undone and "wrote no hypothesis_card.yaml" in undone[0]


def test_run_loop_first_set_aside_failure_never_stops_1a(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _loop_run("run_955")

    def _boom(*a, **k):
        raise OSError("locked")

    monkeypatch.setattr(rpr, "_set_aside_1a_outputs", _boom)
    seen = _fake_agent(monkeypatch, run_dir, [_claim()])
    rpr.run_loop("run_955")
    assert [s for s, _ in seen] == ["hypothesis_generation", "strategy_config_authoring"]


def test_a_lone_numbered_card_from_the_claim_retry_is_kept(monkeypatch):
    """run_067: 1a answered ONE card named hypothesis_card_2.yaml. Through the
    real _invoke_agent_with_yaml_retry, the claim retry's lone numbered card is
    the run's card (it used to be undone as 'no hypothesis_card.yaml')."""
    _set_orchestrator(ON)
    run_dir = _card_run("run_970", claim=_claim(kind="vibes"))
    arts = run_dir / "artifacts"

    async def _agent(stage, run_id, retry_context=None):
        rpr.save_yaml(arts / "hypothesis_card_2.yaml", dict(CARD, claim=_claim()))

    monkeypatch.setattr(rpr, "async_invoke_agent", _agent)
    rpr._check_claim_after_1a("run_970", run_dir, [arts / "hypothesis_card.yaml"],
                              {"yaml_retry_count": 0})
    assert rpr.load_yaml(arts / "hypothesis_card.yaml")["claim"]["kind"] != "vibes"
    assert not (arts / "hypothesis_card_2.yaml").exists()
    assert _status(run_dir)["usable"] is True

