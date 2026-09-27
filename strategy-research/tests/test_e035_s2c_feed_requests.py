"""
E-035 S2c (delivery_plan_v26.md slice 8.2) -- the feed-acquisition lane:
a reader proposal may carry an optional `requires_feed: {feed, reason}`
(orthogonal to `kind`). After specialist_readers validates the proposals, each
feed they ask for and do not have becomes ONE campaign_record/data_requests.yaml
row per (run, stage, feed) -- `request: acquisition` for a feed never built,
`request: designation` for a reserved one, none for a feed already wired.
decide_next blocks a candidate (INFEASIBLE, recorded, never dropped) only while
its feed is not wired AND its resolved config consumes it (a new_block, which
has no config before 1b, always counts as consuming): reason
`requires_feed:<feed>` or `requires_feed_reserved:<feed>`. "Wired" is a key of
trading-bot/data/feed_registry.py's FEED_REGISTRY; whether a wired feed covers
the run's venue, symbols and windows stays the data-availability gate's check
at step 3.

Spec: engineering/roadmap/E-036/S1_FINDINGS_SLICE8.md §3, guess 6, §4 S2c and
its operator decision of 2026-09-27; code-review fixes 1-10 of the same day.
No LLM, no backtest, no trial row, no market data, no holdout read.

Measured 2026-09-27: this module (55 tests) run with the 12 source files
(the 5 tools/workflow modules, the 2 schemas, the 5 reader SKILL.md files)
restored from an older commit, the tests unchanged:
  * bb031b5d (master, before S2c): 47 fail, 8 pass. The 8 are invariance
    checks that must hold on any version: the gate writer's bytes; the stage
    writes nothing without requires_feed, on component errors, or with the
    flag off; a malformed requires_feed stops the stage; candidates and
    briefs without the field; a waiting candidate's reasons do not change
    with the registry (vacuous on master, which ignores the field).
  * 19eed731 (S2c before the review fixes): 37 fail, 18 pass. The 18 are
    the 8 above plus what 19eed731 already did right: the loader and schema
    accept the field (3 tests), known_feeds on the real and synthetic
    registries and 4 of its 5 fail-loud shapes (6), and a feasible sibling
    picked over a waiting candidate (1). Some failures there come from the
    renamed input (load_inputs' `available_feeds` became a lazy `feed_set`),
    not only from the behaviour the review changed.
Loader/schema malformed cases, including the trailing-newline one, live
with the agreement test in tests/test_reader_proposals.py.
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
    CLS, _base_config, _by_id, _decide, _one_source, _patch, _sketch, _stage_flag_on_source,
)
from test_halt_quarantine_policy import campaign_root  # noqa: E402,F401  (fixture)

_TBOT = _SR.parent / "trading-bot"
_OI = {"feed": "open_interest", "reason": "slices.overall.x=1: losses cluster where positioning is unseen"}
# A registry shaped like load_feed_registry's output (router), and a feed set
# like load_feed_set's (decide_next).
REG = {"wired": ["fear_greed", "funding_rate"], "reserved": ["whale_cvd_delta"]}
FEEDS = {**REG, "component_feeds": {CLS: ["funding_rate"]}}


def _with_feed(p: dict, rf=None) -> dict:
    return {**copy.deepcopy(p), "requires_feed": copy.deepcopy(rf or _OI)}


def _requests_path() -> Path:
    return rpr.ROOT / "campaign_record" / "data_requests.yaml"


def _rows() -> list:
    return yaml.safe_load(_requests_path().read_text(encoding="utf-8"))["requests"]


def _fake_registry(tmp_path, body: str) -> Path:
    mod = tmp_path / "data" / "feed_registry.py"
    mod.parent.mkdir(parents=True, exist_ok=True)
    mod.write_text(body, encoding="utf-8")
    return tmp_path


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
# 2. The router: one row per (run, stage, feed); acquisition / designation /
#    none for a wired feed; idempotent; lazy registry read
# ---------------------------------------------------------------------------

def _proposals(*, feed_on=("profitability",), second=False, rf=None) -> dict:
    out = {c: [] for c in REPORT_CATEGORIES}
    for c in feed_on:
        out[c] = [_with_feed(_proposal(c), rf)]
        if second:
            out[c].append(_with_feed(_proposal(c, n=2), rf))
    out["forecast_power"] = [_proposal("forecast_power")]  # no requires_feed
    return out


def _route(proposals, run_id=RUN_ID, reg=REG):
    return rpr._route_reader_feed_requests(run_id, proposals, feed_registry=reg)


def test_router_writes_one_row_per_missing_feed():
    n = _route(_proposals(feed_on=("profitability", "regime_power")))
    assert n == 1
    assert _rows() == [{
        "run_id": RUN_ID, "stage": "specialist_reader", "feed": "open_interest",
        "request": "acquisition",
        "proposals": [{"category": c, "proposal_id": f"{c}-{RUN_ID}-1", "reason": _OI["reason"]}
                      for c in ("profitability", "regime_power")],
        "reason": (f"requires_feed:open_interest -- acquisition asked by 2 reader proposal(s): "
                   f"profitability-{RUN_ID}-1, regime_power-{RUN_ID}-1"),
    }]


def test_router_is_idempotent_on_rerun():
    props = _proposals()
    _route(props)
    first = _requests_path().read_bytes()
    _route(props)
    _route(copy.deepcopy(props))
    assert _requests_path().read_bytes() == first
    assert len(_rows()) == 1


def test_a_reattempt_with_reworded_reason_and_new_proposal_id_adds_nothing():
    """Review fix 1: the key is (run, stage, feed) -- never the reader's free
    text nor its per-attempt proposal_id."""
    _route(_proposals())
    first = _requests_path().read_bytes()
    again = {c: [] for c in REPORT_CATEGORIES}
    again["trade_efficiency"] = [_with_feed(_proposal("trade_efficiency", n=7),
                                            {"feed": "open_interest", "reason": "reworded entirely"})]
    assert _route(again) == 1  # offered, then dropped by the key
    assert _requests_path().read_bytes() == first


def test_a_reattempt_asking_for_another_feed_adds_a_row():
    _route(_proposals())
    _route(_proposals(rf={"feed": "liquidations", "reason": "r"}))
    assert [r["feed"] for r in _rows()] == ["open_interest", "liquidations"]


def test_the_same_feed_from_another_run_is_another_row():
    _route(_proposals())
    _route(_proposals(), run_id="run_999")
    assert [(r["run_id"], r["feed"]) for r in _rows()] == [(RUN_ID, "open_interest"),
                                                            ("run_999", "open_interest")]


def test_a_reserved_feed_asks_for_a_designation():
    """Review fix 3: the gate declines a reserved feed until a data-policy
    designation covers it -- a designation request, not an acquisition."""
    _route(_proposals(rf={"feed": "whale_cvd_delta", "reason": "r"}))
    (row,) = _rows()
    assert row["request"] == "designation" and row["feed"] == "whale_cvd_delta"
    assert row["reason"].startswith("requires_feed_reserved:whale_cvd_delta -- designation")


def test_a_wired_feed_files_no_row():
    """Review fix 4: nothing to acquire for a FEED_REGISTRY key."""
    assert _route(_proposals(rf={"feed": "funding_rate", "reason": "r"})) == 0
    assert not _requests_path().exists()
    props = _proposals()
    props["regime_power"] = [_with_feed(_proposal("regime_power"), {"feed": "fear_greed", "reason": "r"})]
    assert _route(props) == 1
    assert [r["feed"] for r in _rows()] == ["open_interest"]


def test_no_requires_feed_writes_nothing_and_never_reads_the_registry(monkeypatch):
    """Review fix 8: the registry is read only when a proposal asks for a feed."""
    def _boom(_root):
        raise AssertionError("feed registry read without any requires_feed")
    monkeypatch.setattr(dn, "load_feed_registry", _boom)
    props = {c: [_proposal(c)] for c in REPORT_CATEGORIES}
    assert rpr._route_reader_feed_requests(RUN_ID, props) == 0
    assert rpr._route_reader_feed_requests(RUN_ID, {c: [] for c in REPORT_CATEGORIES}) == 0
    assert not _requests_path().exists()


def test_router_fails_loud_on_an_unreadable_registry(monkeypatch, tmp_path):
    monkeypatch.setattr(rpr, "_TRADING_BOT_ROOT", _fake_registry(tmp_path, "FEED_REGISTRY = dict()\n"))
    with pytest.raises(dn.DecideNextError, match="FEED_REGISTRY"):
        rpr._route_reader_feed_requests(RUN_ID, _proposals())
    assert not _requests_path().exists()


def test_router_is_additive_to_existing_gate_rows():
    gate_rows = [{"variant_id": "a", "outcome": "decline", "reason": "r", "reasons": ["r"]}]
    rpr._append_data_requests("run_001", gate_rows)
    before = _rows()
    _route(_proposals())
    after = _rows()
    assert after[:1] == before and len(after) == 2
    assert after[1]["stage"] == "specialist_reader"


def test_gate_rows_dedupe_exactly_as_on_master():
    """Review fix 1: request_key is master's (run, stage, variant, reason);
    reader rows use their own key."""
    row = {"run_id": "r", "stage": "data_availability_gate", "variant_id": "v", "reason": "x"}
    assert crr.request_key(row) == ("r", "data_availability_gate", "v", "x")
    rows = [{"variant_id": None, "outcome": "decline", "reason": "same", "reasons": ["a"]}]
    rpr._append_data_requests("run_1", rows, dedupe=True)
    rpr._append_data_requests("run_1", [{**rows[0], "reasons": ["b"]}], dedupe=True)
    rpr._append_data_requests("run_1", [{**rows[0], "reason": "other"}], dedupe=True)
    assert [r["reason"] for r in _rows()] == ["same", "other"]
    assert crr.feed_request_key({"run_id": "r", "stage": "specialist_reader", "feed": "f",
                                 "reason": "x"}) == ("r", "specialist_reader", "f")


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
# 3. The stage body routes after validation (and only then); the readers'
#    prompt carries the canonical feed names
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
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)  # the real FEED_REGISTRY
    assert [(r["stage"], r["feed"], r["request"]) for r in _rows()] == [
        ("specialist_reader", "open_interest", "acquisition")]
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


def test_reader_handoff_carries_the_canonical_feed_names():
    """Review fix 7: wired and reserved names from the registry, plus the
    wishlist's names that are in neither (flagged wishlist-only)."""
    wl = rpr.ROOT / rpr.FEED_WISHLIST_REL
    wl.parent.mkdir(parents=True, exist_ok=True)
    wl.write_text(yaml.safe_dump({"wishlist": [{"feed_name": "liquidation_data"},
                                               {"feed_name": "funding_rate"}]}), encoding="utf-8")
    names = rpr._reader_handoff("profitability", RUN_ID, 0)["injected_context"]["feed_names"]
    reg = dn.load_feed_registry(_TBOT)
    assert names["wired"] == reg["wired"] and names["reserved"] == reg["reserved"]
    assert names["wishlist_only"] == ["liquidation_data"]
    assert "never a synonym" in names["rule"]


def test_reader_feed_names_never_stop_a_run(monkeypatch, tmp_path):
    """Review fix 8: every reader call builds the names, so an unreadable
    registry or wishlist is reported, not raised."""
    monkeypatch.setattr(rpr, "_TRADING_BOT_ROOT", _fake_registry(tmp_path, "X = 1\n"))
    wl = rpr.ROOT / rpr.FEED_WISHLIST_REL
    wl.parent.mkdir(parents=True, exist_ok=True)
    wl.write_text("wishlist: [unclosed\n", encoding="utf-8")
    names = rpr._reader_feed_vocabulary()
    assert "FEED_REGISTRY" in names["registry_error"] and "wishlist_error" in names
    assert names["wishlist_only"] == [] and "wired" not in names


def test_every_reader_skill_tells_readers_to_use_the_listed_names():
    for c in REPORT_CATEGORIES:
        text = (_SR / "workflow_artifacts" / "skills" / "readers" / f"{c}-reader" / "SKILL.md"
                ).read_text(encoding="utf-8")
        assert "feed_names" in text and "synonym" in text, c


# ---------------------------------------------------------------------------
# 4. Reading the registries and the components' consumes_feeds (ast)
# ---------------------------------------------------------------------------

def _import_engine(module: str):
    pytest.importorskip("pandas")
    sys.path.insert(0, str(_TBOT))
    try:
        return __import__(module, fromlist=["_"])
    except ImportError as exc:  # the engine's fetchers need the trading-bot venv
        pytest.skip(f"trading-bot {module} not importable here: {exc}")


def test_known_feeds_reads_the_real_feed_registry_keys():
    feeds = dn.known_feeds(_TBOT)
    assert feeds == sorted(feeds) and {"funding_rate", "fear_greed"} <= set(feeds)
    assert not any(f.startswith("whale_") for f in feeds)


def test_load_feed_registry_matches_the_imported_registries():
    mod = _import_engine("data.feed_registry")
    assert dn.load_feed_registry(_TBOT) == {"wired": sorted(mod.FEED_REGISTRY),
                                            "reserved": sorted(mod.RESERVED_FEED_REGISTRY)}


def test_feed_status_is_the_gate_classification():
    """Review fix 3: the same order and sources as
    data_availability_gate.check_aux_feed_window (reserved first, then
    FEED_REGISTRY, else never built). Only the two branches that return
    before any data is read are called."""
    gate = _import_engine("data_availability_gate")
    reg = dn.load_feed_registry(_TBOT)
    for feed in reg["reserved"] + ["open_interest"]:
        res = gate.check_aux_feed_window(feed, "binance", ["BTCUSDT"], "2024-01-01", "2024-02-01")
        want = ("reserved" if "is a RESERVED feed" in res["reason"]
                else "unknown" if "is not a known feed" in res["reason"] else res["reason"])
        assert res["outcome"] == "decline" and dn.feed_status(feed, reg) == want, feed
    assert set(reg["reserved"]) == set(gate._RESERVED_FEED_NAMES)
    assert set(reg["wired"]) == set(gate.FEED_REGISTRY)
    assert all(dn.feed_status(f, reg) == "wired" for f in reg["wired"])
    assert dn.feed_status("open_interest", None) is None


def test_known_feeds_from_a_synthetic_registry(tmp_path):
    root = _fake_registry(tmp_path, "FEED_REGISTRY = {'b': 1, 'a': 2}\nOTHER = {'z': 0}\n")
    assert dn.known_feeds(root) == ["a", "b"]


def test_reserved_registry_as_a_comprehension_over_a_named_tuple(tmp_path):
    root = _fake_registry(tmp_path, "FEED_REGISTRY = {'a': 1}\nX = 'x_col'\nNAMES = ('y', X)\n"
                                    "RESERVED_FEED_REGISTRY = {n: 1 for n in NAMES}\n")
    assert dn.load_feed_registry(root) == {"wired": ["a"], "reserved": ["x_col", "y"]}


@pytest.mark.parametrize("body", ["X = 1\n", "FEED_REGISTRY = dict(a=1)\n", "FEED_REGISTRY = {}\n",
                                  "FEED_REGISTRY = {k: 1 for k in 'ab'}\n", "FEED_REGISTRY = {\n"])
def test_known_feeds_fails_loud_without_a_literal_registry(tmp_path, body):
    with pytest.raises(dn.DecideNextError, match="FEED_REGISTRY|cannot be read"):
        dn.known_feeds(_fake_registry(tmp_path, body))


def test_load_feed_registry_fails_loud_without_the_reserved_registry(tmp_path):
    with pytest.raises(dn.DecideNextError, match="RESERVED_FEED_REGISTRY"):
        dn.load_feed_registry(_fake_registry(tmp_path, "FEED_REGISTRY = {'a': 1}\n"))


def test_component_consumed_feeds_matches_the_imported_classes():
    mod = _import_engine("strategies.strategy_components")
    got = dn.component_consumed_feeds(_TBOT)
    want = {f"{dn.COMPONENT_MODULE}.{name}": sorted(set(cls.consumes_feeds))
            for name, cls in vars(mod).items()
            if isinstance(cls, type) and cls.__module__ == mod.__name__
            and getattr(cls, "consumes_feeds", ())}
    assert got == want and got[CLS] == ["funding_rate"]


def test_component_consumed_feeds_inherits_and_fails_loud(tmp_path):
    mod = tmp_path / "strategies" / "strategy_components.py"
    mod.parent.mkdir(parents=True)
    mod.write_text("from strategies.strategy_base import Base\nCOL = 'oi'\n"
                   "class A(Base):\n    consumes_feeds = (COL, 'x')\n"
                   "class B(A):\n    pass\nclass C(Base):\n    pass\n", encoding="utf-8")
    assert dn.component_consumed_feeds(tmp_path) == {
        f"{dn.COMPONENT_MODULE}.A": ["oi", "x"], f"{dn.COMPONENT_MODULE}.B": ["oi", "x"]}
    mod.write_text("class A:\n    consumes_feeds = tuple(['x'])\n", encoding="utf-8")
    with pytest.raises(dn.DecideNextError, match="consumes_feeds"):
        dn.component_consumed_feeds(tmp_path)


# ---------------------------------------------------------------------------
# 5. decide_next: blocked only while not wired AND consumed
# ---------------------------------------------------------------------------

def _feed_inputs(proposals, feeds=FEEDS, config=None):
    inputs = _one_source(proposals, **({"config": config} if config is not None else {}))
    inputs["feed_set"] = copy.deepcopy(feeds)
    return inputs


def _reading(*feeds):
    """The source base config, declaring `feeds` in aux_feeds (as the
    data-availability gate reads them)."""
    return {**_base_config(), "aux_feeds": list(feeds)}


def _validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((_SR / "workflow_artifacts" / "schemas" / "decision_record.schema.json")
                        .read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


def test_an_unwired_feed_the_config_reads_is_infeasible_recorded_never_dropped():
    rec = _decide(_feed_inputs([_with_feed(_patch("profitability-run_061-1"))],
                               config=_reading("open_interest")))
    c = _by_id(rec)["profitability-run_061-1"]
    feas = c["gates"]["feasibility"]
    assert feas["result"] == "INFEASIBLE" and c["eligible"] is False
    assert "requires_feed:open_interest -- not wired in data.feed_registry.FEED_REGISTRY" \
        in feas["reasons"]
    assert feas["requires_feed"] == {"feed": "open_interest", "status": "unknown", "consumed": True,
                                     "available": False, "reason": _OI["reason"]}
    assert rec["picked"] is None and rec["stop"]["reason"] == "no_eligible_candidate"
    assert not list(_validator().iter_errors(rec))


def test_a_patch_whose_config_does_not_read_the_feed_is_not_blocked():
    """Review fix 5: the patched config reads funding_rate only -- testable
    today (its request row is still filed at stage 16)."""
    rec = _decide(_feed_inputs([_with_feed(_patch("profitability-run_061-1"))]))
    c = _by_id(rec)["profitability-run_061-1"]
    feas = c["gates"]["feasibility"]
    assert feas["result"] == "FEASIBLE" and c["eligible"] is True
    assert feas["requires_feed"]["consumed"] is False and feas["requires_feed"]["available"] is False
    assert not any(r.startswith("requires_feed") for r in feas["reasons"])
    assert rec["picked"]["candidate_id"] == "profitability-run_061-1"
    assert not list(_validator().iter_errors(rec))


def test_a_component_class_consuming_the_feed_counts_as_reading_it():
    feeds = {**FEEDS, "component_feeds": {CLS: ["funding_rate", "open_interest"]}}
    c = _by_id(_decide(_feed_inputs([_with_feed(_patch("profitability-run_061-1"))], feeds)))[
        "profitability-run_061-1"]
    assert c["eligible"] is False and c["gates"]["feasibility"]["requires_feed"]["consumed"] is True


def test_it_becomes_feasible_once_the_feed_is_wired():
    props = [_with_feed(_patch("profitability-run_061-1"))]
    feeds = {**FEEDS, "wired": FEEDS["wired"] + ["open_interest"]}
    rec = _decide(_feed_inputs(props, feeds, config=_reading("open_interest")))
    c = _by_id(rec)["profitability-run_061-1"]
    assert c["gates"]["feasibility"]["result"] == "FEASIBLE" and c["eligible"] is True
    assert c["gates"]["feasibility"]["requires_feed"]["status"] == "wired"
    assert rec["picked"]["candidate_id"] == "profitability-run_061-1"
    assert not list(_validator().iter_errors(rec))


def test_a_reserved_feed_has_its_own_reason():
    """Review fix 3."""
    p = _with_feed(_patch("profitability-run_061-1"), {"feed": "whale_cvd_delta", "reason": "r"})
    c = _by_id(_decide(_feed_inputs([p], config=_reading("whale_cvd_delta"))))[
        "profitability-run_061-1"]
    feas = c["gates"]["feasibility"]
    assert c["eligible"] is False and feas["requires_feed"]["status"] == "reserved"
    assert [r for r in feas["reasons"] if "whale" in r] == [
        "requires_feed_reserved:whale_cvd_delta -- a reserved feed: the data-availability gate "
        "declines it until a campaign_data_policy.yaml designation covers it"]


def test_an_already_wired_feed_is_available():
    p = _with_feed(_patch("profitability-run_061-1"), {"feed": "funding_rate", "reason": "r"})
    c = _by_id(_decide(_feed_inputs([p])))["profitability-run_061-1"]
    assert c["eligible"] is True
    assert c["gates"]["feasibility"]["requires_feed"]["consumed"] is True


def test_no_feed_set_supplied_is_never_read_as_available():
    rec = _decide(_feed_inputs([_with_feed(_patch("profitability-run_061-1"))], feeds=None))
    feas = _by_id(rec)["profitability-run_061-1"]["gates"]["feasibility"]
    assert feas["result"] == "INFEASIBLE"
    assert "requires_feed:open_interest -- no feed set was supplied" in feas["reasons"]
    assert feas["requires_feed"]["status"] is None and feas["requires_feed"]["consumed"] is None
    assert "feed_set_sha256" not in rec["inputs"]
    inputs = _one_source([_with_feed(_patch("profitability-run_061-1"))])  # no key at all
    assert "feed_set" not in inputs
    assert _by_id(_decide(inputs))["profitability-run_061-1"]["eligible"] is False


def test_new_block_with_an_unwired_feed_is_infeasible_then_unknown():
    """A sketch has no config before 1b: it cannot show it does without the feed."""
    p = _with_feed(_sketch("profitability-run_061-1"))
    c = _by_id(_decide(_feed_inputs([p])))["profitability-run_061-1"]
    assert c["gates"]["feasibility"]["result"] == "INFEASIBLE" and not c["eligible"]
    assert c["gates"]["feasibility"]["requires_feed"]["consumed"] is None
    wired = {**FEEDS, "wired": ["open_interest"]}
    c = _by_id(_decide(_feed_inputs([p], wired)))["profitability-run_061-1"]
    assert c["gates"]["feasibility"]["result"] == "UNKNOWN" and c["eligible"]


def test_a_feasible_sibling_is_picked_over_a_waiting_feed_candidate():
    props = [_with_feed(_sketch("profitability-run_061-1", conf=3)),
             _patch("profitability-run_061-2", after=0.9, conf=1)]
    rec = _decide(_feed_inputs(props))
    assert rec["picked"]["candidate_id"] == "profitability-run_061-2"
    ids = [c["candidate_id"] for c in rec["candidates"]]
    assert "profitability-run_061-1" in ids  # recorded, not dropped


def test_reasons_name_only_the_missing_feed():
    """Review fix 6: an unrelated registry addition leaves a waiting
    candidate's reasons unchanged."""
    props = [_with_feed(_sketch("profitability-run_061-1"))]
    a = _by_id(_decide(_feed_inputs(props)))["profitability-run_061-1"]
    more = {**FEEDS, "wired": FEEDS["wired"] + ["liquidations"], "reserved": ["whale_x"]}
    b = _by_id(_decide(_feed_inputs(props, more)))["profitability-run_061-1"]
    assert a["gates"]["feasibility"] == b["gates"]["feasibility"]
    assert not any("funding_rate" in r for r in a["gates"]["feasibility"]["reasons"])


def test_feed_set_sha_is_recorded_only_with_a_feed_set():
    props = [_with_feed(_sketch("profitability-run_061-1"))]
    rec = _decide(_feed_inputs(props))
    assert rec["inputs"]["feed_set_sha256"] == dn._canonical_sha(FEEDS)
    assert not list(_validator().iter_errors(rec))
    assert "feed_set_sha256" not in _decide(_one_source(props))["inputs"]


def test_candidates_without_requires_feed_are_byte_identical():
    """The gate only reads proposals that carry the field: their candidates
    are the same whatever feed set is (or is not) supplied."""
    props = [_patch("profitability-run_061-1"), _sketch("profitability-run_061-2")]
    base = yaml.safe_dump(_decide(_one_source(props))["candidates"], sort_keys=True)
    for feeds in (None, {"wired": [], "reserved": [], "component_feeds": {}}, FEEDS):
        assert yaml.safe_dump(_decide(_feed_inputs(props, feeds))["candidates"],
                              sort_keys=True) == base
    for c in _decide(_feed_inputs(props))["candidates"]:
        assert "requires_feed" not in c["gates"]["feasibility"]


def test_picked_feed_candidate_brief_carries_the_need():
    props = [_with_feed(_patch("profitability-run_061-1", after=0.8))]
    inputs = _feed_inputs(props)
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


# ---------------------------------------------------------------------------
# 6. Lazy: the feed set is computed only when a proposal carries the field
# ---------------------------------------------------------------------------

def _load(campaign_root, feed_set):
    root = campaign_root["root"]
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    return dn.load_inputs(root, queue, categories=["profitability"], feed_set=feed_set)


def test_load_inputs_never_calls_the_feed_set_without_requires_feed(campaign_root):
    """Review fix 8."""
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])

    def _boom():
        raise AssertionError("feed set computed without any requires_feed")
    assert _load(campaign_root, _boom)["feed_set"] is None
    assert _load(campaign_root, FEEDS)["feed_set"] is None


def test_load_inputs_calls_it_when_a_proposal_carries_requires_feed(campaign_root):
    _stage_flag_on_source(campaign_root, [_with_feed(_patch("profitability-run_061-1"))])
    calls = []

    def _feeds():
        calls.append(1)
        return copy.deepcopy(FEEDS)
    assert _load(campaign_root, _feeds)["feed_set"] == FEEDS and calls == [1]

    def _unreadable():
        raise dn.DecideNextError("unreadable")
    with pytest.raises(dn.DecideNextError, match="unreadable"):
        _load(campaign_root, _unreadable)


def test_run_campaign_passes_a_lazy_feed_set(monkeypatch):
    """_finish_lineage_with_decision hands load_inputs a callable over the
    public load_feed_set (no private helper, nothing read up front)."""
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
    assert callable(seen["feed_set"])
    assert seen["feed_set"]() == dn.load_feed_set(camp._TRADING_BOT_ROOT)


def test_a_campaign_without_requires_feed_never_reads_the_registry(campaign_root, monkeypatch):
    """End to end through process_once, with the registry reader broken."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")

    def _boom(_root):
        raise AssertionError("feed set computed without any requires_feed")
    monkeypatch.setattr(dn, "load_feed_set", _boom)
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])
    assert camp.process_once() is True
    record = yaml.safe_load((campaign_root["root"] / "runs" / "run_061" / "artifacts" /
                             "decision_record.yaml").read_text(encoding="utf-8"))
    assert "feed_set_sha256" not in record["inputs"]
    assert record["picked"]["candidate_id"] == "profitability-run_061-1"


def test_a_campaign_with_requires_feed_records_the_feed_set(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    _stage_flag_on_source(campaign_root, [_with_feed(_patch("profitability-run_061-1"))])
    assert camp.process_once() is True
    record = yaml.safe_load((campaign_root["root"] / "runs" / "run_061" / "artifacts" /
                             "decision_record.yaml").read_text(encoding="utf-8"))
    assert record["inputs"]["feed_set_sha256"] == dn._canonical_sha(
        dn.load_feed_set(camp._TRADING_BOT_ROOT))
    c = _by_id(record)["profitability-run_061-1"]
    # the real base config reads funding_rate only: not blocked by open_interest
    assert c["eligible"] is True and c["gates"]["feasibility"]["requires_feed"]["consumed"] is False
