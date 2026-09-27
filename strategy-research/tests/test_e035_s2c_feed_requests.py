"""
E-035 S2c (delivery_plan_v26.md slice 8.2) -- the feed-acquisition lane:
a reader proposal may carry an optional `requires_feed: {feed, reason}`
(orthogonal to `kind`); after specialist_readers validates the proposals each
such proposal appends one row to campaign_record/data_requests.yaml through the
locked, idempotent appender; decide_next marks a candidate from it INFEASIBLE
(reason `requires_feed:<feed> ...`) until <feed> is a key of
trading-bot/data/feed_registry.py's FEED_REGISTRY -- the feed set the
data-availability gate (tools/data_availability_gate.py) accepts.

Spec: engineering/roadmap/E-036/S1_FINDINGS_SLICE8.md §3, guess 6, §4 S2c and
its operator decision of 2026-09-27. No LLM, no backtest, no trial row, no
market data, no holdout read. Every test here fails on bb031b5d (the loader
rejected the field; the router, known_feeds and the gate did not exist).
Loader/schema malformed cases live with the agreement test in
tests/test_reader_proposals.py.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))
sys.path.insert(0, str(Path(__file__).parent))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import campaign_review_retired as crr  # noqa: E402
import decide_next as dn  # noqa: E402
import reader_proposals as rp  # noqa: E402
from build_reports import REPORT_CATEGORIES  # noqa: E402

from test_e046a_slice5b_ii_b_readers_stage import (  # noqa: E402
    ALL_ON, RUN_ID, _fake_llm, _proposal, _seed_run, _set_orchestrator,
    _stub_tbot_python,  # noqa: F401  (autouse fixture)
)
from test_e059_s2a_decide_next import (  # noqa: E402
    _by_id, _decide, _one_source, _patch, _sketch,
)

_TBOT = _SR.parent / "trading-bot"
_OI = {"feed": "open_interest", "reason": "slices.overall.x=1: losses cluster where positioning is unseen"}


def _with_feed(p: dict, rf=None) -> dict:
    return {**copy.deepcopy(p), "requires_feed": copy.deepcopy(rf or _OI)}


def _requests_path() -> Path:
    return rpr.ROOT / "campaign_record" / "data_requests.yaml"


def _rows() -> list:
    return yaml.safe_load(_requests_path().read_text(encoding="utf-8"))["requests"]


# ---------------------------------------------------------------------------
# 1. Loader + schema accept the field on both kinds
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("kind", ["patch", "new_block"])
def test_loader_and_schema_accept_requires_feed_on_either_kind(tmp_path, kind):
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((_SR / "workflow_artifacts" / "schemas" / "proposal.schema.json")
                        .read_text(encoding="utf-8"))
    base = (_patch("profitability-run_061-1") if kind == "patch"
            else _sketch("profitability-run_061-1"))
    p = _with_feed(base)
    assert not list(jsonschema.Draft202012Validator(schema).iter_errors(p))
    d = tmp_path / "proposals"
    d.mkdir()
    (d / "profitability.yaml").write_text(yaml.safe_dump([p]), encoding="utf-8")
    out = rp.load_proposals(d, ["profitability"])
    assert out["profitability"][0]["requires_feed"] == _OI


def test_schema_and_loader_declare_the_same_requires_feed_keys():
    schema = json.loads((_SR / "workflow_artifacts" / "schemas" / "proposal.schema.json")
                        .read_text(encoding="utf-8"))
    rf = schema["properties"]["requires_feed"]
    assert set(rf["required"]) == set(rf["properties"]) == rp.REQUIRES_FEED_KEYS
    assert rf["additionalProperties"] is False
    assert "requires_feed" not in schema["required"]  # optional


# ---------------------------------------------------------------------------
# 2. The router: rows, idempotence, nothing when absent, additive
# ---------------------------------------------------------------------------

def _proposals(*, feed_on=("profitability",), second=False) -> dict:
    out = {c: [] for c in REPORT_CATEGORIES}
    for c in feed_on:
        out[c] = [_with_feed(_proposal(c))]
        if second:
            out[c].append(_with_feed(_proposal(c, n=2)))  # same reason text on purpose
    out["forecast_power"] = [_proposal("forecast_power")]  # no requires_feed: no row
    return out


def test_router_writes_one_row_per_requires_feed_proposal():
    n = rpr._route_reader_feed_requests(RUN_ID, _proposals(feed_on=("profitability", "regime_power")))
    assert n == 2
    assert _rows() == [
        {"run_id": RUN_ID, "stage": "specialist_reader", "category": c,
         "proposal_id": f"{c}-{RUN_ID}-1", "requires_feed": _OI,
         "reason": f"requires_feed:open_interest -- {_OI['reason']}"}
        for c in ("profitability", "regime_power")
    ]


def test_router_is_idempotent_on_rerun():
    props = _proposals()
    rpr._route_reader_feed_requests(RUN_ID, props)
    first = _requests_path().read_bytes()
    rpr._route_reader_feed_requests(RUN_ID, props)
    rpr._route_reader_feed_requests(RUN_ID, copy.deepcopy(props))
    assert _requests_path().read_bytes() == first
    assert len(_rows()) == 1


def test_two_proposals_with_the_same_reason_both_land():
    """request_key now includes proposal_id: on the old key (run, stage,
    variant, reason) the second row would have been silently dropped."""
    rpr._route_reader_feed_requests(RUN_ID, _proposals(second=True))
    assert [r["proposal_id"] for r in _rows()] == [f"profitability-{RUN_ID}-1",
                                                   f"profitability-{RUN_ID}-2"]


def test_a_reattempt_asking_for_another_feed_adds_a_row():
    rpr._route_reader_feed_requests(RUN_ID, _proposals())
    other = _proposals()
    other["profitability"][0]["requires_feed"] = {"feed": "liquidations", "reason": _OI["reason"]}
    rpr._route_reader_feed_requests(RUN_ID, other)
    assert [r["requires_feed"]["feed"] for r in _rows()] == ["open_interest", "liquidations"]


def test_no_requires_feed_writes_nothing():
    props = {c: [_proposal(c)] for c in REPORT_CATEGORIES}
    assert rpr._route_reader_feed_requests(RUN_ID, props) == 0
    assert rpr._route_reader_feed_requests(RUN_ID, {c: [] for c in REPORT_CATEGORIES}) == 0
    assert not _requests_path().exists()


def test_router_is_additive_to_existing_gate_rows():
    gate_rows = [{"variant_id": "a", "outcome": "decline", "reason": "r", "reasons": ["r"]}]
    rpr._append_data_requests("run_001", gate_rows)
    before = _rows()
    rpr._route_reader_feed_requests(RUN_ID, _proposals())
    after = _rows()
    assert after[:1] == before and len(after) == 2
    assert after[1]["stage"] == "specialist_reader"


def test_request_key_is_unchanged_for_rows_without_proposal_id():
    row = {"run_id": "r", "stage": "data_availability_gate", "variant_id": "v", "reason": "x"}
    assert crr.request_key(row) == ("r", "data_availability_gate", "v", None, "x")
    # identity of such rows depends only on the four old fields, as before
    assert crr.request_key(dict(row)) == crr.request_key({**row, "outcome": "decline"})


def test_default_gate_writer_is_byte_identical():
    """The per-variant gate's writer (dedupe off) keeps its exact bytes: the
    new `stage` keyword defaults to data_availability_gate."""
    rows = [{"variant_id": "a", "outcome": "decline", "reason": "r", "reasons": ["r"]}]
    rpr._append_data_requests("run_1", rows)
    expected = rpr.ROOT / "expected.yaml"
    rpr.save_yaml(expected, {"requests": [{"run_id": "run_1", "stage": "data_availability_gate",
                                           **rows[0]}]})
    assert _requests_path().read_bytes() == expected.read_bytes()


# ---------------------------------------------------------------------------
# 3. The stage body routes after validation (and only then)
# ---------------------------------------------------------------------------

def _reader_output(p: dict) -> str:
    return f"```yaml\n- {yaml.safe_dump(p, default_flow_style=True).strip()}\n```"


def test_stage_routes_validated_requires_feed_proposals(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(_SR)
    run_dir = _seed_run()
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm({
        "profitability": _reader_output(_with_feed(_proposal("profitability"))),
        "trade_efficiency": _reader_output(_proposal("trade_efficiency")),
    }))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert [(r["stage"], r["proposal_id"]) for r in _rows()] == [
        ("specialist_reader", f"profitability-{RUN_ID}-1")]
    # a resume re-validates the files (readers not re-run) and adds nothing
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert len(_rows()) == 1


def test_stage_writes_nothing_without_requires_feed(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(_SR)
    run_dir = _seed_run()
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm({
        "profitability": _reader_output(_proposal("profitability"))}))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert not _requests_path().exists()


def test_stage_writes_nothing_on_component_errors(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(errors_count=2)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm())
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert not _requests_path().exists()


def test_a_malformed_requires_feed_stops_before_any_row(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(_SR)
    run_dir = _seed_run()
    bad = _with_feed(_proposal("profitability"), {"feed": "Open Interest", "reason": "r"})
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm({"profitability": _reader_output(bad)}))
    with pytest.raises(rp.ProposalError, match="requires_feed"):
        rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert not _requests_path().exists()


def test_flag_off_the_stage_never_runs_so_nothing_is_written():
    _set_orchestrator(None)
    run_dir = _seed_run()
    with pytest.raises(RuntimeError, match="specialist_readers.enabled"):
        rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert not _requests_path().exists()


# ---------------------------------------------------------------------------
# 4. "Available" = the data-availability gate's FEED_REGISTRY keys
# ---------------------------------------------------------------------------

def test_known_feeds_reads_the_real_feed_registry_keys():
    feeds = dn.known_feeds(_TBOT)
    assert feeds == sorted(feeds) and {"funding_rate", "fear_greed"} <= set(feeds)
    # reserved feeds are declined by the gate unconditionally: not available here
    assert not any(f.startswith("whale_") for f in feeds)


def test_known_feeds_matches_the_imported_registry():
    pytest.importorskip("pandas")
    sys.path.insert(0, str(_TBOT))
    try:
        from data.feed_registry import FEED_REGISTRY  # noqa: E402
    except ImportError as exc:  # the engine's fetchers need the trading-bot venv
        pytest.skip(f"trading-bot data.feed_registry not importable here: {exc}")
    assert dn.known_feeds(_TBOT) == sorted(FEED_REGISTRY)


def _fake_registry(tmp_path, body: str) -> Path:
    mod = tmp_path / "data" / "feed_registry.py"
    mod.parent.mkdir(parents=True)
    mod.write_text(body, encoding="utf-8")
    return tmp_path


def test_known_feeds_from_a_synthetic_registry(tmp_path):
    root = _fake_registry(tmp_path, "FEED_REGISTRY = {'b': 1, 'a': 2}\nOTHER = {'z': 0}\n")
    assert dn.known_feeds(root) == ["a", "b"]


@pytest.mark.parametrize("body", ["X = 1\n", "FEED_REGISTRY = dict(a=1)\n", "FEED_REGISTRY = {}\n",
                                  "FEED_REGISTRY = {k: 1 for k in 'ab'}\n"])
def test_known_feeds_fails_loud_without_a_literal_registry(tmp_path, body):
    with pytest.raises(dn.DecideNextError, match="FEED_REGISTRY"):
        dn.known_feeds(_fake_registry(tmp_path, body))


# ---------------------------------------------------------------------------
# 5. decide_next: infeasible until the feed is available
# ---------------------------------------------------------------------------

AVAILABLE = ["fear_greed", "funding_rate"]


def _feed_inputs(proposals, feeds=AVAILABLE):
    inputs = _one_source(proposals)
    inputs["available_feeds"] = feeds
    return inputs


def _validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((_SR / "workflow_artifacts" / "schemas" / "decision_record.schema.json")
                        .read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


def test_unavailable_feed_is_infeasible_recorded_never_dropped():
    rec = _decide(_feed_inputs([_with_feed(_patch("profitability-run_061-1"))]))
    c = _by_id(rec)["profitability-run_061-1"]
    feas = c["gates"]["feasibility"]
    assert feas["result"] == "INFEASIBLE" and c["eligible"] is False
    assert any(r.startswith("requires_feed:open_interest") for r in feas["reasons"])
    assert feas["requires_feed"] == {"feed": "open_interest", "available": False,
                                     "reason": _OI["reason"]}
    assert rec["picked"] is None and rec["stop"]["reason"] == "no_eligible_candidate"
    assert not list(_validator().iter_errors(rec))


def test_it_becomes_feasible_once_the_feed_is_available():
    props = [_with_feed(_patch("profitability-run_061-1"))]
    rec = _decide(_feed_inputs(props, feeds=AVAILABLE + ["open_interest"]))
    c = _by_id(rec)["profitability-run_061-1"]
    assert c["gates"]["feasibility"]["result"] == "FEASIBLE" and c["eligible"] is True
    assert c["gates"]["feasibility"]["requires_feed"]["available"] is True
    assert not any(r.startswith("requires_feed") for r in c["gates"]["feasibility"]["reasons"])
    assert rec["picked"]["candidate_id"] == "profitability-run_061-1"
    assert not list(_validator().iter_errors(rec))


def test_an_already_wired_feed_is_available():
    p = _with_feed(_patch("profitability-run_061-1"), {"feed": "funding_rate", "reason": "r"})
    c = _by_id(_decide(_feed_inputs([p])))["profitability-run_061-1"]
    assert c["eligible"] is True


def test_no_feed_set_supplied_is_never_read_as_available():
    rec = _decide(_feed_inputs([_with_feed(_patch("profitability-run_061-1"))], feeds=None))
    feas = _by_id(rec)["profitability-run_061-1"]["gates"]["feasibility"]
    assert feas["result"] == "INFEASIBLE"
    assert any(r.startswith("requires_feed:open_interest -- no available feed set")
               for r in feas["reasons"])
    # inputs built without the key at all (older callers) behave the same way
    inputs = _one_source([_with_feed(_patch("profitability-run_061-1"))])
    assert "available_feeds" not in inputs
    assert _by_id(_decide(inputs))["profitability-run_061-1"]["eligible"] is False


def test_new_block_with_unavailable_feed_is_infeasible_then_unknown():
    p = _with_feed(_sketch("profitability-run_061-1"))
    c = _by_id(_decide(_feed_inputs([p])))["profitability-run_061-1"]
    assert c["gates"]["feasibility"]["result"] == "INFEASIBLE" and not c["eligible"]
    c = _by_id(_decide(_feed_inputs([p], feeds=["open_interest"])))["profitability-run_061-1"]
    assert c["gates"]["feasibility"]["result"] == "UNKNOWN" and c["eligible"]


def test_a_feasible_sibling_is_picked_over_a_waiting_feed_candidate():
    props = [_with_feed(_patch("profitability-run_061-1", conf=3)),
             _patch("profitability-run_061-2", after=0.9, conf=1)]
    rec = _decide(_feed_inputs(props))
    assert rec["picked"]["candidate_id"] == "profitability-run_061-2"
    ids = [c["candidate_id"] for c in rec["candidates"]]
    assert "profitability-run_061-1" in ids  # recorded, not dropped


def test_candidates_without_requires_feed_are_byte_identical():
    """The gate only reads proposals that carry the field: the record for
    others is the same whatever feed set is (or is not) supplied."""
    props = [_patch("profitability-run_061-1"), _sketch("profitability-run_061-2")]
    base = yaml.safe_dump(_decide(_one_source(props)), sort_keys=True)
    for feeds in (None, [], AVAILABLE):
        assert yaml.safe_dump(_decide(_feed_inputs(props, feeds)), sort_keys=True) == base
    for c in _decide(_feed_inputs(props))["candidates"]:
        assert "requires_feed" not in c["gates"]["feasibility"]


def test_picked_feed_candidate_brief_carries_the_need():
    props = [_with_feed(_patch("profitability-run_061-1", after=0.8))]
    inputs = _feed_inputs(props, feeds=AVAILABLE + ["open_interest"])
    rec = _decide(inputs)
    _, text = dn.candidate_brief(rec, inputs, decision_ref="runs/run_061/artifacts/decision_record.yaml")
    front = yaml.safe_load(text.split("---")[1])
    assert front["candidate"]["source"]["proposal"]["requires_feed"] == _OI
    assert f"Needs feed open_interest: {_OI['reason']}" in front["research_goal"]


def test_brief_without_requires_feed_has_no_such_key():
    inputs = _one_source([_patch("profitability-run_061-1", after=0.8)])
    _, text = dn.candidate_brief(_decide(inputs), inputs,
                                 decision_ref="runs/run_061/artifacts/decision_record.yaml")
    assert "requires_feed" not in text and "Needs feed" not in text


def test_load_inputs_carries_the_feed_set(tmp_path):
    a = dn.load_inputs(tmp_path, {"queue": []}, categories=["profitability"])
    b = dn.load_inputs(tmp_path, {"queue": []}, categories=["profitability"],
                       available_feeds=["funding_rate", "fear_greed"])
    assert a["available_feeds"] is None
    assert b["available_feeds"] == ["fear_greed", "funding_rate"]
    assert {k: v for k, v in a.items() if k != "available_feeds"} == \
        {k: v for k, v in b.items() if k != "available_feeds"}


def test_run_campaign_passes_the_feed_registry_keys(monkeypatch):
    """_finish_lineage_with_decision reads the same FEED_REGISTRY keys and
    hands them to load_inputs (decide_next is itself behind its flag)."""
    seen = {}

    class _Stop(Exception):
        pass

    def _capture(root, queue, **kw):
        seen.update(kw)
        raise _Stop
    monkeypatch.setattr(dn, "load_inputs", _capture)
    entry = {"id": "E", "status": "done", "outcome": "refuted", "run_ids": ["run_1"]}
    with pytest.raises(_Stop):
        camp._finish_lineage_with_decision({"queue": [entry]}, entry, "run_1")
    assert seen["available_feeds"] == dn.known_feeds(camp._TRADING_BOT_ROOT)
