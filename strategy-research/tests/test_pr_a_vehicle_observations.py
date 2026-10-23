"""PR-A (operator rulings, 2026-10-19; D-151): a claim always carries a vehicle, and an analyst
session that ends in no_claim may record what it measured as observations.

1. `no_claim.observations` (analyst_session.check_answer): accepted when valid, recorded with
   its code-written spec and its statement's numbers masked; absent / [] accepted; each
   refusal; the reading is the same with and without observations.
2. campaign_memory.analyst_observations / build_memory_entry: copied only from an accepted
   no_claim last attempt; the key is absent when there is none; the schema takes it.
3. analyst_memory_view: the rows "observed, no vehicle yet".
4. reader_proposals: a model's `vehicle: []` is refused for every kind (EMPTY_VEHICLE_KINDS is
   empty); a FILE already written with one loads, its item flagged legacy_no_vehicle
   (operator ruling 2026-10-19 item 3; decide-next's side: test_d089_vehicle_and_coins.py).
5. The skill text: no `vehicle: []` outside a sentence that forbids it.

Fixtures are those of test_e075_pr5_analyst.py (a synthetic query log), test_d089_vehicle_and_coins.py
(the proposal envelope) and test_e058_s2a_regroup_record.py (a seeded run through the real
regroup_record stage).
"""
from __future__ import annotations

import copy
import json
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
import claim_card as cc  # noqa: E402
import reader_proposals as rp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

import test_e075_pr4_queries as q4  # noqa: E402
from test_d089_vehicle_and_coins import EMPTY, _check_model  # noqa: E402
from test_e058_s2a_regroup_record import ALL_ON, _memory, _seed  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
from test_e075_pr5_analyst import LONG, RUN_ID, _entries_for_claim  # noqa: E402
from d178_legacy_fixture import d178_checks_off  # noqa: E402,F401  (D-178)

pytestmark = pytest.mark.usefixtures("d178_checks_off")
from test_e077_pr2_confirm import CAT, CHANGE, _claim, _reading  # noqa: E402

MEM_RUN = "run_980"                                   # the id test_e058's _seed gives its run
ABSENT = object()


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# 1. the answer check
# ---------------------------------------------------------------------------

ROW = {"effect": 0.0123, "n_events": 40, "n_windows_with_events": 5, "n_blocks": 5,
       "windows_claimed_sign": 5, "windows_with_value": 5}


def _ce_entry(qid="q7", *, floor=None, row=None, status="ok", function="conditional_effect",
              spec_hash=None):
    return {qid: {"id": qid, "function": function, "status": status,
                  "params": {"variant": "base"},
                  "result": {"spec_hash": spec_hash or f"h{qid}",
                             "test": {"selector": LONG, "outcome": {"kind": "trade_net_return"},
                                      "baseline": {"kind": "other_trades"},
                                      "statistic": "mean_diff", "direction": "greater",
                                      "floor": floor or {"min_events": 5}},
                             "horizons": {"1": dict(ROW if row is None else row)}}}}


def _entries(**kw):
    return {**_entries_for_claim(), **_ce_entry(**kw)}


def _obs(**over):
    o = {"statement": "Long lots lose more after a large move.", "test": "q7",
         "evidence": ["q7:horizons.1.effect=0.0123"], "floors_met": True}
    o.update(over)
    return o


def _answer(observations=ABSENT, reason="every mechanism failed on another coin"):
    nc = {"reason": reason, "best_rejected": {"statement": "longs lead", "killed_by": "q3"}}
    if observations is not ABSENT:
        nc["observations"] = observations
    return "```yaml\n" + yaml.safe_dump({
        "outcome": "no_claim", "evidence": ["q1:horizons.1.effect=0.0123"],
        "no_claim": nc}, sort_keys=False) + "```"


def _check(text, entries=None):
    return asm.check_answer(text, lens="trade_efficiency", run_id=RUN_ID,
                            entries=entries or _entries(), claim_check=lambda c: None,
                            holdout_start=q4.HOLDOUT, fold="A", model_id="m")


def test_a_no_claim_with_valid_observations_is_accepted_and_recorded():
    reading, rec, errors = _check(
        _answer([_obs(), _obs(statement="Short lots lose less.", test="q8",
                              evidence=["q8:horizons.1.effect=0.0123"])]),
        {**_entries(), **_ce_entry("q8")})
    assert errors == []
    recorded = rec["no_claim"]["observations"]
    assert len(recorded) == 2
    for o, (qid, h) in zip(recorded, (("q7", "hq7"), ("q8", "hq8"))):
        # D-178 (operator 2026-10-23): re-pinned with the angle tags on; these LONG-selector trade
        # tests are not regime findings, so no `angle` key is recorded
        assert set(o) == set(asm.OBSERVATION_KEYS) | {"spec"}
        assert o["test"] == qid and o["floors_met"] is True
        # the spec is code-written: the measured test block without its result, plus its hash
        assert o["spec"]["spec_hash"] == h and o["spec"]["selector"] == LONG
        assert o["spec"]["floor"] == {"min_events": 5}
        assert "horizons" not in o["spec"] and "effect" not in o["spec"]
    assert rec["outcome"] == "no_claim" and reading["side_findings"] == []


def test_the_numbers_of_an_observation_statement_are_masked_and_listed_as_unverified():
    _reading_out, rec, errors = _check(_answer([_obs(statement="Long lots lose 9.9% more after "
                                                                "a large move.")]))
    assert errors == []
    (o,) = rec["no_claim"]["observations"]
    assert "9.9" not in o["statement"] and "<n>" in o["statement"]
    assert {"field": "no_claim.observations.0.statement", "written": "9.9%"} \
        in rec["unverified_numbers"]


def test_a_cited_number_in_an_observation_statement_is_kept():
    _r, rec, errors = _check(_answer([_obs(statement="Long lots differ by 0.0123 per lot.")]))
    assert errors == []
    assert "0.0123" in rec["no_claim"]["observations"][0]["statement"]
    assert not [u for u in rec["unverified_numbers"] if "observations" in u["field"]]


def test_the_reading_is_the_same_with_and_without_observations():
    without = _check(_answer())
    with_obs = _check(_answer([_obs()]))
    assert without[2] == [] and with_obs[2] == []
    assert with_obs[0] == without[0]


@pytest.mark.parametrize("observations", [ABSENT, []])
def test_absent_and_empty_observations_are_accepted(observations):
    _r, rec, errors = _check(_answer(observations))
    assert errors == []
    if observations is ABSENT:
        assert "observations" not in rec["no_claim"]            # unchanged from before D-151
    else:
        assert rec["no_claim"]["observations"] == []


_GOOD_ROW_FLOOR = {"min_events": 5, "min_windows": 3}
_BAD_ROW = dict(ROW, n_events=2)


@pytest.mark.parametrize("observations,entries,needle", [
    ("an observation", None, "must be a list"),
    ({"statement": "s"}, None, "must be a list"),
    ([{"statement": "s", "test": "q7", "evidence": ["q7:horizons.1.effect=0.0123"]}], None,
     "must have exactly the keys"),
    ([dict(_obs(), extra=1)], None, "must have exactly the keys"),
    (["just text"], None, "must have exactly the keys"),
    ([_obs(statement="   ")], None, "statement must be a non-empty text"),
    ([_obs(statement=3)], None, "statement must be a non-empty text"),
    ([_obs(test="q3")], None, "must be the id of an ok conditional_effect call"),
    ([_obs(test="q99")], None, "must be the id of an ok conditional_effect call"),
    ([_obs()], _entries(status="error"), "must be the id of an ok conditional_effect call"),
    ([_obs(evidence=["q7:horizons.1.effect=0.999"])], None, "returned"),
    ([_obs(evidence=["q7:horizons.9.effect=1"])], None, "has no"),
    ([_obs(evidence=[])], None, "non-empty list"),
    ([_obs(evidence=["q1:horizons.1.effect=0.0123"])], None,
     "must cite its test's own result"),
    ([_obs(floors_met="yes")], None, "floors_met must be true or false"),
    ([_obs(floors_met=1)], None, "floors_met must be true or false"),
    ([_obs(floors_met=None)], None, "floors_met must be true or false"),
    # the logged result clears the floor on every horizon: floors_met false contradicts it
    ([_obs(floors_met=False)], _entries(floor=_GOOD_ROW_FLOOR), "floors_met is false"),
    # the logged result does not clear it (n_events 2 < 5): floors_met true contradicts it
    ([_obs(floors_met=True)], _entries(row=_BAD_ROW), "floors_met is true"),
])
def test_each_observation_refusal(observations, entries, needle):
    reading, _rec, errors = _check(_answer(observations), entries)
    assert any(needle in e for e in errors), errors
    assert any("no_claim.observations" in e for e in errors), errors


def _n_entries(n, **kw):
    out = dict(_entries_for_claim())
    for i in range(n):
        out.update(_ce_entry(f"q{7 + i}", **kw))
    return out


def _n_obs(n):
    return [_obs(statement=f"Behaviour {i}.", test=f"q{7 + i}",
                 evidence=[f"q{7 + i}:horizons.1.effect=0.0123"]) for i in range(n)]


def test_three_observations_citing_three_different_tests_are_accepted():
    _r, rec, errors = _check(_answer(_n_obs(3)), _n_entries(3))
    assert errors == []
    assert [o["test"] for o in rec["no_claim"]["observations"]] == ["q7", "q8", "q9"]


def test_a_fourth_observation_is_refused_with_the_cap_in_the_message():
    _r, _rec, errors = _check(_answer(_n_obs(4)), _n_entries(4))
    assert any("no_claim.observations has 4 entries" in e and "at most 3" in e
               and "different test" in e for e in errors), errors
    assert asm.OBSERVATIONS_MAX == 3


def test_two_observations_citing_the_same_query_are_refused():
    obs = [_obs(), _obs(statement="Same test, other words.")]
    _r, _rec, errors = _check(_answer(obs), _n_entries(1))
    assert any("no_claim.observations[1].test='q7'" in e and "different test" in e
               for e in errors), errors


def test_two_queries_with_the_same_test_block_are_the_same_test():
    entries = {**_entries(), **_ce_entry("q8", spec_hash="hq7")}
    obs = [_obs(), _obs(test="q8", evidence=["q8:horizons.1.effect=0.0123"])]
    _r, _rec, errors = _check(_answer(obs), entries)
    assert any("no_claim.observations[1].test='q8'" in e and "different test" in e
               for e in errors), errors


def test_the_observation_spec_shares_no_object_between_observations():
    """Two observations citing one query: PyYAML would write the second selector as an alias
    (&id001 / *id001). The spec holds copies, and the YAML has no anchor."""
    entry = _entries()["q7"]
    a, b = asm._observation_spec(entry), asm._observation_spec(entry)
    assert a == b and a["selector"] is not b["selector"] and a["floor"] is not b["floor"]
    assert a["selector"] is not LONG
    dumped = yaml.safe_dump([a, b], sort_keys=False)
    assert "&id" not in dumped and "*id" not in dumped


def test_floors_met_matching_the_log_is_accepted_both_ways():
    assert _check(_answer([_obs(floors_met=True)]), _entries(floor=_GOOD_ROW_FLOOR))[2] == []
    assert _check(_answer([_obs(floors_met=False)]), _entries(row=_BAD_ROW))[2] == []


def test_a_min_eras_only_floor_cannot_be_contradicted():
    """n_eras_with_events is not in the logged result: floors_met is not checkable, so both
    values are accepted."""
    entries = _entries(floor={"min_eras": 3})
    assert asm.floors_met_in_log(entries["q7"]) is None
    assert _check(_answer([_obs(floors_met=True)]), entries)[2] == []
    assert _check(_answer([_obs(floors_met=False)]), entries)[2] == []


def test_a_floor_with_a_missing_unit_is_not_contradicted_but_a_known_miss_is():
    row = {k: v for k, v in ROW.items() if k != "n_blocks"}
    # min_blocks unreadable, min_events met: cannot tell
    entries = _entries(floor={"min_events": 5, "min_blocks": 2}, row=row)
    assert asm.floors_met_in_log(entries["q7"]) is None
    # min_blocks unreadable, min_events missed: the miss is known
    entries = _entries(floor={"min_events": 500, "min_blocks": 2}, row=row)
    assert asm.floors_met_in_log(entries["q7"]) is False
    assert _check(_answer([_obs(floors_met=True)]), entries)[2]


# ---------------------------------------------------------------------------
# 2. campaign_memory
# ---------------------------------------------------------------------------

def _record_doc(*, outcome="no_claim", attempts=None, observations=ABSENT, lens="trade_efficiency"):
    spec = {"spec_hash": "hq7", "selector": LONG, "outcome": {"kind": "trade_net_return"},
            "baseline": {"kind": "other_trades"}, "statistic": "mean_diff",
            "direction": "greater", "floor": {"min_events": 5}}
    obs = [dict(_obs(), spec=spec)] if observations is ABSENT else observations
    nc = {"reason": "r", "best_rejected": {"statement": "s", "killed_by": "q3"}}
    if obs is not None:
        nc["observations"] = obs
    doc = {"lens": lens, "outcome": outcome,
           "attempts": [{"status": "accepted", "outcome": outcome}] if attempts is None else attempts}
    if outcome == "no_claim":
        doc["no_claim"] = nc
    return doc


def _write_record(run_dir, doc, lens="trade_efficiency"):
    path = Path(run_dir) / asm.record_rel(lens)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return path


def test_observations_of_an_accepted_no_claim_are_copied(tmp_path):
    _write_record(tmp_path, _record_doc())
    (row,) = cm.analyst_observations(tmp_path, "run_080")
    assert row["lens"] == "trade_efficiency"
    assert {k: row[k] for k in cm.OBSERVATION_FIELDS if k != "spec"} == \
        {k: _obs()[k] for k in ("statement", "test", "evidence", "floors_met")}
    assert row["spec"]["spec_hash"] == "hq7"
    assert row["ref"] == f"runs/run_080/{asm.record_rel('trade_efficiency')}"


def test_observations_of_both_lenses_are_copied_in_lens_order(tmp_path):
    _write_record(tmp_path, _record_doc(lens="forecast"), lens="forecast")
    _write_record(tmp_path, _record_doc(), lens="trade_efficiency")
    assert [r["lens"] for r in cm.analyst_observations(tmp_path, "run_080")] == \
        [lens for lens in asm.LENSES if lens in ("forecast", "trade_efficiency")]


def test_a_retry_that_is_accepted_after_a_refusal_is_copied(tmp_path):
    _write_record(tmp_path, _record_doc(attempts=[{"status": "refused"},
                                                  {"status": "accepted",
                                                   "outcome": "no_claim"}]))
    assert len(cm.analyst_observations(tmp_path, "run_080")) == 1


@pytest.mark.parametrize("doc", [
    _record_doc(attempts=[{"status": "accepted", "outcome": "no_claim"},
                          {"status": "refused"}]),                        # refused last attempt
    _record_doc(attempts=[{"status": "refused"}]),
    _record_doc(attempts=[]),
    _record_doc(outcome="claim"),                                       # a claim, not no_claim
    _record_doc(observations=None),                                     # no observations key
    _record_doc(observations=[]),                                       # an empty list
    _record_doc(attempts=[{"status": "accepted", "outcome": "claim"}]),  # last attempt a claim
])
def test_observations_are_skipped_unless_the_last_attempt_is_an_accepted_no_claim(tmp_path, doc):
    _write_record(tmp_path, doc)
    assert cm.analyst_observations(tmp_path, "run_080") == []


def test_a_run_without_an_analyst_record_has_no_observations(tmp_path):
    assert cm.analyst_observations(tmp_path, "run_080") == []


@pytest.mark.parametrize("observations", [
    "not a list",
    [dict(_obs())],                                                      # no code-written spec
    [dict(_obs(), spec={}, extra=1)],
    ["text"],
])
def test_a_malformed_observation_in_an_accepted_record_raises(tmp_path, observations):
    _write_record(tmp_path, _record_doc(observations=observations))
    with pytest.raises(cm.CampaignMemoryError, match="observations"):
        cm.analyst_observations(tmp_path, "run_080")


def test_a_record_that_is_not_a_mapping_raises(tmp_path):
    path = Path(tmp_path) / asm.record_rel("forecast")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("- a\n- list\n", encoding="utf-8")
    with pytest.raises(cm.CampaignMemoryError):
        cm.analyst_observations(tmp_path, "run_080")


@pytest.mark.usefixtures("reader_docs")
def test_build_memory_entry_has_no_observations_key_when_there_is_none():
    _set_orchestrator(ALL_ON)
    run_dir = _seed(run_id=MEM_RUN)
    _write_record(run_dir, _record_doc(observations=None))
    rpr._run_regroup_record_stage(MEM_RUN, run_dir)
    assert "observations" not in _memory()["runs"][MEM_RUN]


@pytest.mark.usefixtures("reader_docs")
def test_build_memory_entry_carries_the_observations_and_the_schema_takes_them():
    jsonschema = pytest.importorskip("jsonschema")
    _set_orchestrator(ALL_ON)
    run_dir = _seed(run_id=MEM_RUN)
    _write_record(run_dir, _record_doc())
    rpr._run_regroup_record_stage(MEM_RUN, run_dir)
    doc = _memory()
    (row,) = doc["runs"][MEM_RUN]["observations"]
    assert row["lens"] == "trade_efficiency" and row["test"] == "q7"
    assert row["ref"] == f"runs/{MEM_RUN}/{asm.record_rel('trade_efficiency')}"
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas"
                         / "campaign_memory.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(doc, schema)
    bad = copy.deepcopy(doc)
    bad["runs"][MEM_RUN]["observations"][0]["floors_met"] = "yes"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, schema)
    bad = copy.deepcopy(doc)
    del bad["runs"][MEM_RUN]["observations"][0]["spec"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, schema)


# ---------------------------------------------------------------------------
# 3. the memory view
# ---------------------------------------------------------------------------

def _memory_with_observation():
    spec = {"spec_hash": "hq7", "selector": LONG, "outcome": {"kind": "trade_net_return"},
            "baseline": {"kind": "other_trades"}, "statistic": "mean_diff",
            "direction": "greater", "floor": {"min_events": 5}}
    return {"runs": {"run_080": {
        "run_id": "run_080", "fold": "A", "hypothesis_id": "H-1",
        "observations": [{"lens": "trade_efficiency",
                          "statement": "Long lots lose 9.9% more after a large move.",
                          "test": "q7", "evidence": ["q7:horizons.1.effect=0.0123"],
                          "floors_met": True, "spec": spec, "ref": "runs/run_080/x.yaml"}]}}}


def test_the_memory_view_shows_an_observation_as_observed_no_vehicle_yet():
    view = amv.build_memory_view(_memory_with_observation(), {})
    assert view["observations_note"] == amv.OBSERVATIONS_NOTE
    (row,) = view["observations"]
    assert row["status"] == "observed, no vehicle yet" == amv.OBSERVED
    assert row["source_run"] == "run_080" and row["lens"] == "trade_efficiency"
    assert row["fold_observed"] == "A" and row["floors_met"] is True
    assert "9.9" not in row["statement"] and "<n>" in row["statement"]
    # the mechanical spec and its floor (counts): no result, no evidence, no query id
    assert set(row["test"]) <= {"spec_hash", "floor", *amv.TEST_SPEC_KEYS}
    assert row["test"]["spec_hash"] == "hq7" and row["test"]["selector"] == LONG
    assert row["test"]["floor"] == {"min_events": 5}
    blob = json.dumps(view)
    for leaked in ("0.0123", "9.9", '"q7"', "q7:", "evidence"):
        assert leaked not in blob, leaked
    assert row["source_strategy"]["hypothesis_id"] == "H-1"
    # it is not a claim: nothing joins the claims or their counts
    assert view["claims"] == [] and view["n_claims"] == 0


def test_the_floor_is_counts_only_and_a_claims_test_row_is_unchanged():
    memory = _memory_with_observation()
    spec = memory["runs"]["run_080"]["observations"][0]["spec"]
    spec["floor"] = {"min_events": 5, "min_windows": 3, "effect": 0.0123, "min_blocks": 2.5,
                     "min_eras": True}
    (row,) = amv.build_memory_view(memory, {})["observations"]
    assert row["test"]["floor"] == {"min_events": 5, "min_windows": 3}
    assert "0.0123" not in json.dumps(row)
    spec.pop("floor")
    (row,) = amv.build_memory_view(memory, {})["observations"]
    assert "floor" not in row["test"]
    assert "floor" not in amv.TEST_SPEC_KEYS                      # claims keep their keys
    claim_memory = {"runs": {"run_080": {"run_id": "run_080", "finding": {
        "finding_id": "F-1", "statement": "s", "kind": "event_behaviour",
        "tests": [{"spec_hash": "h", "spec": dict(spec, floor={"min_events": 5})}]}}}}
    (claim,) = amv.build_memory_view(claim_memory, {})["claims"]
    assert "floor" not in claim["tests"][0]


def test_observation_rows_share_no_object_so_the_yaml_has_no_alias():
    """Two runs whose observations hold the same spec object: the view copies it."""
    memory = _memory_with_observation()
    second = copy.copy(memory["runs"]["run_080"])
    second["run_id"] = "run_081"
    second["observations"] = [dict(memory["runs"]["run_080"]["observations"][0])]
    assert second["observations"][0]["spec"] is memory["runs"]["run_080"]["observations"][0]["spec"]
    memory["runs"]["run_081"] = second
    view = amv.build_memory_view(memory, {})
    a, b = view["observations"]
    assert a["test"]["selector"] == b["test"]["selector"] == LONG
    assert a["test"]["selector"] is not b["test"]["selector"]
    assert a["test"]["floor"] is not b["test"]["floor"]
    dumped = yaml.safe_dump(view, sort_keys=False)
    assert "&id" not in dumped and "*id" not in dumped


def _memory_with_runs(n, *, recorded_at):
    memory = _memory_with_observation()
    proto = memory["runs"].pop("run_080")
    for i in range(1, n + 1):
        run = copy.deepcopy(proto)
        run["run_id"] = f"run_{i:03d}"
        run["recorded_at"] = recorded_at(i)
        run["observations"][0]["statement"] = f"Behaviour of run {i}."
        memory["runs"][run["run_id"]] = run
    return memory


def test_the_view_keeps_the_newest_20_observation_rows_and_counts_the_rest():
    assert amv.OBSERVATION_ROWS_MAX == 20
    view = amv.build_memory_view(
        _memory_with_runs(21, recorded_at=lambda i: f"2026-10-01T00:00:{i:02d}"), {})
    rows = view["observations"]
    assert len(rows) == 20
    assert rows[0]["source_run"] == "run_002" and rows[-1]["source_run"] == "run_021"
    assert view["observations_max_rows"] == 20
    assert view["observations_in_memory"] == 21 and view["omitted_older_observations"] == 1
    assert all("source_strategy" in r for r in rows)


def test_newest_means_the_latest_recorded_at_not_the_highest_run_number():
    # run_001 was recorded last: it is kept, and run_002 (the oldest recorded) is dropped
    view = amv.build_memory_view(
        _memory_with_runs(21, recorded_at=lambda i: "2026-10-02T00:00:00" if i == 1
                          else f"2026-10-01T00:00:{i:02d}"), {})
    runs = [r["source_run"] for r in view["observations"]]
    assert len(runs) == 20 and "run_001" in runs and "run_002" not in runs
    assert runs[-1] == "run_001"                                    # oldest first, newest last


def test_twenty_or_fewer_observation_rows_are_all_shown_with_nothing_omitted():
    view = amv.build_memory_view(
        _memory_with_runs(20, recorded_at=lambda i: f"2026-10-01T00:00:{i:02d}"), {})
    assert len(view["observations"]) == 20 and view["omitted_older_observations"] == 0


def test_a_memory_view_without_observations_has_no_observation_keys():
    memory = _memory_with_observation()
    del memory["runs"]["run_080"]["observations"]
    view = amv.build_memory_view(memory, {})
    assert "observations" not in view and "observations_note" not in view
    assert "omitted_older_observations" not in view
    assert set(view) == {"schema_version", "note", "n_claims", "by_status", "claims"}
    assert "observations" not in amv.build_memory_view({}, None)


def test_observations_come_in_run_order_and_a_malformed_row_is_skipped():
    memory = _memory_with_observation()
    first = copy.deepcopy(memory["runs"]["run_080"])
    first["fold"] = "B"
    first["observations"][0]["statement"] = "Earlier behaviour."
    first["observations"].append("not a mapping")
    memory["runs"]["run_070"] = first
    view = amv.build_memory_view(memory, {})
    assert [o["source_run"] for o in view["observations"]] == ["run_070", "run_080"]
    assert view["observations"][0]["fold_observed"] == "B"


# ---------------------------------------------------------------------------
# 4. the vehicle rule in reader_proposals
# ---------------------------------------------------------------------------

_KINDS = ("execution_behaviour", "event_behaviour", "direction_forecast", "cost_turnover",
          "conditional_behaviour")


def test_the_constants():
    assert rp.EMPTY_VEHICLE_KINDS == ()
    assert cc.FOLDS_CLAIM_KINDS == ("execution_behaviour",)
    assert rp.LEGACY_NO_VEHICLE == "legacy_no_vehicle"
    assert not hasattr(rp, "WRITTEN_EMPTY_VEHICLE_KINDS")


@pytest.mark.parametrize("kind", _KINDS)
def test_a_models_empty_vehicle_is_refused_for_every_kind(kind):
    with pytest.raises(rp.ProposalError, match=rf"an empty vehicle is refused for every claim "
                                               rf"kind, '{kind}' included"):
        _check_model(_claim(kind=kind), **EMPTY)
    _check_model(_claim(kind=kind), **dict(EMPTY, vehicle=copy.deepcopy(CHANGE)))   # a real one


def test_the_refusal_does_not_offer_an_exception():
    with pytest.raises(rp.ProposalError) as exc:
        _check_model(_claim(kind="execution_behaviour"), **EMPTY)
    msg = str(exc.value)
    assert "no exception" in msg and "no_claim.observations" in msg
    assert "allowed only" not in msg


@pytest.mark.parametrize("kind", _KINDS)
def test_a_written_empty_vehicle_loads_flagged_legacy_no_vehicle(kind, tmp_path):
    """Operator ruling 2026-10-19 item 3: a written item with `vehicle: []` loads (any kind;
    only execution_behaviour could be written before the ruling), flagged on the loaded item
    only -- never in the file, never by flatten_reading alone."""
    doc = _reading(_claim(kind=kind), **EMPTY)
    rp.check_reading(doc, CAT, "file")                       # from_model False: loads as it stands
    assert rp.LEGACY_NO_VEHICLE not in rp.flatten_reading(doc)[0]
    path = tmp_path / f"{CAT}.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    before = path.read_bytes()
    (item,) = rp.load_proposals(tmp_path, [CAT])[CAT]
    assert item[rp.LEGACY_NO_VEHICLE] is True and item["vehicle"] == []
    assert path.read_bytes() == before
    # a written item with a real vehicle is not flagged
    path.write_text(yaml.safe_dump(_reading(_claim(kind=kind), **dict(
        EMPTY, vehicle=copy.deepcopy(CHANGE))), sort_keys=False), encoding="utf-8")
    (item,) = rp.load_proposals(tmp_path, [CAT])[CAT]
    assert rp.LEGACY_NO_VEHICLE not in item


# ---------------------------------------------------------------------------
# 5. the skill text
# ---------------------------------------------------------------------------

SKILL_DIR = SR_ROOT / "workflow_artifacts" / "skills" / "analyst"


@pytest.mark.parametrize("name", ["SKILL.md", "forecast.md", "trade_efficiency.md"])
def test_no_skill_file_offers_an_empty_vehicle(name):
    text = " ".join((SKILL_DIR / name).read_text(encoding="utf-8").split())
    assert "vehicle: []" not in text


def test_the_skill_states_the_vehicle_rule_and_the_observation_shape():
    text = " ".join((SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").split())
    assert "No empty vehicle." in text
    assert "observations:" in text and "floors_met:" in text
    assert "observed, no vehicle yet" in text
    assert "the child run on the next fold is the proof" in text
    assert "A `no_claim` carries at most 3 observations, each citing a different test." in text
    assert ("While every bar's regime is unknown: no claim on regime or regime_at_entry; a market "
            "condition is claimed through past_return, trailing_vol or any selector in the "
            "vocabulary.") in text
    assert ("run the selector by window, then describe `past_return_<n>` or `trailing_vol_<n>` "
            "by window to name the condition; claim it with all_of.") in text
    assert "then condition it on" not in text
    assert "The detector's label is unknown" not in text
    te = " ".join((SKILL_DIR / "trade_efficiency.md").read_text(encoding="utf-8").split())
    assert ("The pipeline rule itself is not a vehicle; the vehicle changes the forecast the rule "
            "acts on (for example a smoothing span that cuts sign flips).") in te
    assert "Profit and cost are measurements of this run" in text
    for lens in ("forecast.md", "trade_efficiency.md"):
        assert "Profit and cost are measurements of this run" in " ".join(
            (SKILL_DIR / lens).read_text(encoding="utf-8").split())
    assert "`window_economics`" in (SKILL_DIR / "trade_efficiency.md").read_text(encoding="utf-8")


def test_the_prompt_claim_example_has_a_vehicle_that_passes_the_shape_check():
    import re
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```yaml\r?\n(.*?)```", text, flags=re.S)
    claim = next(yaml.safe_load(b) for b in blocks if b.lstrip().startswith("outcome: claim"))
    assert claim["vehicle"] and claim["vehicle"] != []
    rp._check_change_items(claim["vehicle"], "example.vehicle")
    no_claim = next(yaml.safe_load(b) for b in blocks if b.lstrip().startswith("outcome: no_claim"))
    (obs,) = no_claim["no_claim"]["observations"]
    # D-178: the example also shows the optional keys that apply (mechanism_query)
    assert set(asm.OBSERVATION_KEYS) <= set(obs) <= set(asm.OBSERVATION_KEYS) | set(asm.OBSERVATION_OPTIONAL)
