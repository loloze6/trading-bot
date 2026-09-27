"""
E-036 S2b (delivery_plan_v26.md slice 8) -- tools/replay_repeat_gate.py, the
read-only replay of the 5a exact-match repeat gate over a runs/ corpus.
Findings on the real corpus: engineering/roadmap/E-036/S2B_REPLAY.md.

Covers, on a synthetic corpus in the conftest sandbox (rpr.ROOT):
  1. counts: exact repeats, a near-miss (one parameter different -> NOVEL),
     a different protocol -> NOVEL, an unkeyable run reported with its reason;
  2. chronology: a later run can repeat an earlier one, never the reverse,
     and runs are ordered by run NUMBER (run_9 before run_010);
  3. a run with no backtest results (prescreen stub) is keyed as a candidate
     but never enters memory, so it can never be matched (the safe direction);
  4. the old family-grain outcome (legacy_family_lookup) sees earlier runs only
     and calls a transform-only change a repeat where the new key says NOVEL;
  5. the replay writes nothing under the corpus (file listing + sizes +
     mtimes before/after the CLI) and refuses an --out under it;
  6. the replay key EQUALS the live gate key: the candidate side against
     run_phase1_research._route_post_variant_selection's recorded key, the
     memory side against an entry written by the real writers
     (_record_backtest_trial -> campaign_memory.build_memory_entry ->
     upsert_memory) -- no hand-built key on either side.

No LLM, no backtest, no market data. Window dates are in 2021.
"""
import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import campaign_memory as cm  # noqa: E402
import novelty as nov  # noqa: E402
import replay_repeat_gate as rrg  # noqa: E402

from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402
from test_e036_s2a_exact_match_gate import (  # noqa: E402
    _config, _legacy_candidate, _prior_run_in_memory, _set_flags, SYMBOLS, WINDOWS)


def _protocol(name, *, symbols=("BTCUSDT", "ETHUSDT"), timeframe="1h", windows=WINDOWS):
    return _write_protocol(rpr.ROOT, name, {"symbols": list(symbols), "timeframe": timeframe,
                                            "windows": windows})


def _write_json(path: Path, obj) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    return path


def _corpus_run(run_id, config, protocol_name, *, card=None, backtested=True,
                record_trial=True, relative_protocol_file=True):
    """A finished legacy-flow run as the corpus holds one: card, backtest_spec
    (the old gate's fingerprint source), candidate_strategy_config.json, and
    protocol_result.yaml -- with results (a backtest) or as a prescreen stub
    (no results, protocol in prescreen_result.yaml). The trial row, when
    recorded, is written by the real rpr._record_backtest_trial."""
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card.yaml", card or {
        "hypothesis_id": "KELTNER_BREAKOUT", "timeframe": "1h",
        "target_market": "BTCUSDT, ETHUSDT"})
    if config is not None:
        rpr.save_yaml(arts / "backtest_spec.yaml", {"status": "spec_ready", "config": config})
        cfg_path = _write_json(arts / "candidate_strategy_config.json", config)
    if protocol_name is None:
        return run_dir
    proto = json.loads((rpr.ROOT / "protocols" / protocol_name).read_text(encoding="utf-8"))
    # the corpus records the engine's relative path, Windows separators
    pfile = f"protocols\\{protocol_name}" if relative_protocol_file else str(
        rpr.ROOT / "protocols" / protocol_name)
    if backtested:
        results = [{"symbol": s, "window": w["label"]} for s in proto["symbols"]
                   for w in proto["windows"]]
        rpr.save_yaml(arts / "protocol_result.yaml", {"protocol_file": pfile, "results": results})
        if record_trial and config is not None:
            rpr._record_backtest_trial(run_id, {"per_symbol_summary": {}, "results": []}, cfg_path)
    else:
        rpr.save_yaml(arts / "protocol_result.yaml", {"source": "prescreen_stub", "results": []})
        rpr.save_yaml(arts / "prescreen_result.yaml", {"protocol_version": pfile})
    return run_dir


def _replay(**kw):
    return rrg.replay(rpr.ROOT / "runs", root=rpr.ROOT,
                      campaign_state_path=kw.get("campaign_state_path", rpr.CAMPAIGN_STATE_PATH))


def _rows(result):
    return {r["run_id"]: r for r in result["runs"]}


# ---------------------------------------------------------------------------
# 1 + 2. counts and chronology
# ---------------------------------------------------------------------------

def test_known_repeats_near_miss_other_protocol_and_unkeyable():
    _protocol("p.json")
    _protocol("q.json", timeframe="4h")
    a = _config(min_abs=0.5)
    _corpus_run("run_001", a, "p.json")
    _corpus_run("run_002", copy.deepcopy(a), "p.json")          # exact repeat of 001
    _corpus_run("run_003", _config(min_abs=0.6), "p.json")      # one param different
    _corpus_run("run_004", None, None)                          # no config at all
    _corpus_run("run_005", copy.deepcopy(a), "q.json")          # same config, 4h protocol
    _corpus_run("run_006", copy.deepcopy(a), "p.json", relative_protocol_file=False)
    rows = _rows(_replay())

    assert rows["run_001"]["new"]["outcome"] == "NOVEL"
    assert rows["run_002"]["new"] == {**rows["run_002"]["new"], "outcome": "REPEAT",
                                      "matched": ["run_001:run_001"]}
    assert rows["run_003"]["new"]["outcome"] == "NOVEL"
    assert rows["run_004"]["new"] == {"outcome": "UNKEYED", "reason": rrg.CAND_NO_CONFIG}
    assert rows["run_005"]["new"]["outcome"] == "NOVEL"
    # an absolute protocol_file keys identically to the relative Windows form
    assert rows["run_006"]["new"]["matched"] == ["run_001:run_001", "run_002:run_002"]

    totals = _replay()["totals"]
    assert (totals["new"]["REPEAT"], totals["new"]["NOVEL"], totals["new"]["UNKEYED"]) == (2, 3, 1)
    assert totals["new"]["unkeyed_by_reason"] == {rrg.CAND_NO_CONFIG: 1}
    assert totals["runs"] == totals["variants"] == 6
    assert totals["self_inconsistent_runs"] == []
    assert all(rows[r]["memory"]["self_consistent"] for r in ("run_001", "run_002", "run_003"))
    assert rows["run_001"]["memory"]["forecast_hash_source"] == "trial_ledger"
    collisions = {c["forecast_hash"]: [x["run_id"] for x in c["runs"]]
                  for c in totals["config_hash_collisions"]}
    assert sorted(collisions.values()) == [["run_001", "run_002", "run_005", "run_006"]]


def test_a_later_run_repeats_an_earlier_one_never_the_reverse_in_run_number_order():
    _protocol("p.json")
    c = _config(min_abs=0.7)
    _corpus_run("run_9", c, "p.json")
    _corpus_run("run_010", copy.deepcopy(c), "p.json")  # sorts BEFORE run_9 as a string
    result = _replay()
    assert [r["run_id"] for r in result["runs"]] == ["run_9", "run_010"]
    rows = _rows(result)
    assert rows["run_9"]["new"]["outcome"] == "NOVEL"
    assert rows["run_010"]["new"]["outcome"] == "REPEAT"
    assert rows["run_010"]["new"]["matched"] == ["run_9:run_9"]


# ---------------------------------------------------------------------------
# 3. unkeyable / not-backtested runs never match (the safe direction)
# ---------------------------------------------------------------------------

def test_prescreen_stub_is_a_candidate_but_never_a_memory_entry():
    _protocol("p.json")
    c = _config(min_abs=0.3)
    _corpus_run("run_001", c, "p.json", backtested=False)
    _corpus_run("run_002", copy.deepcopy(c), "p.json")
    rows = _rows(_replay())
    assert rows["run_001"]["new"]["outcome"] == "NOVEL"
    assert rows["run_001"]["new"]["protocol_source"] == "prescreen_result.protocol_version"
    assert rows["run_001"]["memory"]["entry"] is False
    assert rows["run_001"]["memory"]["reason"].startswith("not_backtested")
    assert rows["run_002"]["new"]["outcome"] == "NOVEL"  # nothing TESTED to repeat


def test_unkeyable_reasons_are_reported_never_dropped():
    _protocol("p.json")
    _protocol("r.json")
    _corpus_run("run_001", _config(), None)                      # config, no protocol at all
    bad = _corpus_run("run_002", _config(), "p.json")
    (bad / "artifacts" / "candidate_strategy_config.json").write_text("{not json", encoding="utf-8")
    _corpus_run("run_003", _config(), "p.json")
    (rpr.ROOT / "protocols" / "p.json").write_text(json.dumps({"windows": WINDOWS}),
                                                   encoding="utf-8")  # no symbols now
    miss = _corpus_run("run_004", _config(0.1), "r.json")
    rpr.save_yaml(miss / "artifacts" / "protocol_result.yaml",
                  {"protocol_file": "protocols\\gone.json", "results": [{"window": "w1"}]})
    result = _replay()
    rows = _rows(result)
    assert rows["run_001"]["new"]["reason"] == rrg.CAND_NO_PROTOCOL
    assert rows["run_002"]["new"]["reason"].startswith(rrg.CAND_CONFIG_UNREADABLE)
    assert rows["run_003"]["new"]["reason"].startswith(rrg.CAND_PROTOCOL_NO_SYMBOLS)
    assert rows["run_004"]["new"]["reason"].startswith(rrg.CAND_PROTOCOL_UNREADABLE)
    assert result["totals"]["new"]["UNKEYED"] == 4
    assert sum(result["totals"]["new"]["unkeyed_by_reason"].values()) == 4


def test_no_memory_entry_without_a_card():
    _protocol("p.json")
    run_dir = _corpus_run("run_001", _config(), "p.json")
    (run_dir / "artifacts" / "hypothesis_card.yaml").unlink()
    _corpus_run("run_002", _config(), "p.json")
    rows = _rows(_replay())
    assert rows["run_001"]["memory"] == {"entry": False, "reason": "no_hypothesis_card",
                                         "forecast_hash_source": None}
    assert rows["run_001"]["old"]["outcome"] == "not_evaluable"
    assert rows["run_002"]["new"]["outcome"] == "NOVEL"


def test_unparseable_card_is_its_own_reason():
    _protocol("p.json")
    run_dir = _corpus_run("run_001", _config(), "p.json")
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text("a: b\n  c d: [\n", encoding="utf-8")
    result = _replay()
    row = _rows(result)["run_001"]
    assert row["memory"]["reason"].startswith("hypothesis_card_unreadable")
    assert row["old"]["reason"].startswith("hypothesis_card_unreadable")
    assert row["new"]["outcome"] == "NOVEL"  # the candidate key needs no card
    assert result["totals"]["old"]["not_evaluable_by_reason"] == {"hypothesis_card_unreadable": 1}


def test_key_hashes_candidate_strategy_config_not_backtest_spec_config():
    """F4d: run_loop injects significance_methodology into backtest_spec's
    config before writing candidate_strategy_config.json -- the file the
    trial row and the live gate hash. The replay must hash that file."""
    _protocol("p.json")
    run_dir = _corpus_run("run_001", _config(), "p.json")
    injected = {**_config(), "significance_methodology": "episode_blocked"}
    cfg_path = _write_json(run_dir / "artifacts" / "candidate_strategy_config.json", injected)
    key = _rows(_replay(campaign_state_path=None))["run_001"]["new"]["key"]
    assert key["forecast_hash"] == rpr._compute_forecast_hash(cfg_path)
    assert key["forecast_hash"] != nov.forecast_hash_of_config(_config())


# ---------------------------------------------------------------------------
# 4. the old family-grain side
# ---------------------------------------------------------------------------

def test_old_side_sees_earlier_runs_only_and_collapses_a_transform_change():
    _protocol("p.json")
    _corpus_run("run_001", _config(min_abs=0.5), "p.json")
    _corpus_run("run_002", _config(min_abs=0.9), "p.json")  # transform-only change
    _corpus_run("run_003", _config(min_abs=0.5), "p.json",
                card={"hypothesis_id": "KELTNER_BREAKOUT", "timeframe": "4h",
                      "target_market": "BTCUSDT"})
    result = _replay()
    rows = _rows(result)
    assert rows["run_001"]["old"]["outcome"] == "novel"  # run_002/003 are later
    assert rows["run_002"]["old"]["outcome"] == "repeat"  # same fingerprint (transforms ignored)
    assert rows["run_002"]["old"]["run_ids"] == ["run_001"]
    assert rows["run_002"]["new"]["outcome"] == "NOVEL"   # the config hash sees it
    assert rows["run_003"]["old"]["outcome"] == "novel"   # card says 4h: another triple
    assert rows["run_003"]["new"]["outcome"] == "REPEAT"  # but it RAN p.json (1h)
    m = result["totals"]["agreement_old_x_new"]
    assert m["repeat"] == {"REPEAT": 0, "NOVEL": 1, "UNKEYED": 0}
    assert m["novel"] == {"REPEAT": 1, "NOVEL": 1, "UNKEYED": 0}


# ---------------------------------------------------------------------------
# 5. read-only on the corpus
# ---------------------------------------------------------------------------

def _snapshot(root: Path) -> dict:
    return {p.relative_to(root).as_posix(): ((p.stat().st_size, p.stat().st_mtime_ns)
                                             if p.is_file() else "dir")
            for p in sorted(root.rglob("*"))}


def test_replay_writes_nothing_under_the_corpus(tmp_path):
    _protocol("p.json")
    _corpus_run("run_001", _config(), "p.json")
    _corpus_run("run_002", _config(), "p.json")
    _corpus_run("run_003", None, None)
    runs = rpr.ROOT / "runs"
    before = _snapshot(runs)
    out = tmp_path / "elsewhere" / "replay.yaml"
    assert rrg.main(["--runs-dir", str(runs), "--root", str(rpr.ROOT),
                     "--campaign-state", str(rpr.CAMPAIGN_STATE_PATH), "--out", str(out)]) == 0
    assert _snapshot(runs) == before
    doc = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert doc["totals"]["new"]["REPEAT"] == 1
    with pytest.raises(rrg.ReplayError, match="never writes into the corpus"):
        rrg.main(["--runs-dir", str(runs), "--root", str(rpr.ROOT),
                  "--out", str(runs / "run_001" / "x.yaml")])
    assert _snapshot(runs) == before


# ---------------------------------------------------------------------------
# 6. replay key == live gate key
# ---------------------------------------------------------------------------

def test_replay_key_equals_the_live_gate_key_on_both_sides():
    # memory side: a prior run recorded through the REAL writers
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json")
    live_memory = cm.load_memory(rpr.ROOT / "campaign_record" / "campaign_memory.yaml")
    live_specs = nov.protocol_specs(rpr.ROOT, live_memory)
    live_mem_keys = list(nov.match_index(live_memory, live_specs))

    # candidate side: the live legacy 5a gate on an identical config
    run_dir = _legacy_candidate("run_061", copy.deepcopy(_config()), "run_061_generated.json")
    _set_flags(variant_selection_record=True, variant_anti_adjacency_gate=True)
    assert rpr._route_post_variant_selection(run_dir, "run_061") == "human_pause"
    live = rpr.load_yaml(run_dir / "artifacts" / "variant_anti_adjacency_result.yaml")
    # ...then its backtest ran on the pinned protocol (as the corpus records it)
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", {
        "protocol_file": str(rpr.ROOT / "protocols" / "run_061_generated.json"),
        "results": [{"symbol": s, "window": w["label"]} for s in SYMBOLS for w in WINDOWS]})

    for state in (rpr.CAMPAIGN_STATE_PATH, None):  # ledger hash, then file backfill
        rows = _rows(_replay(campaign_state_path=state))
        assert rows["run_061"]["new"]["key"] == live["key"]
        assert rows["run_061"]["new"]["outcome"] == "REPEAT"
        assert rows["run_061"]["new"]["matched"] == [
            f"{m['run_id']}:{m['variant_id']}" for m in live["matched"]]
        mem_key = rows["run_050"]["memory"]["key"]
        assert [(mem_key["forecast_hash"], tuple(mem_key["symbols"]), mem_key["timeframe"],
                 mem_key["window_set"])] == live_mem_keys
        assert rows["run_050"]["memory"]["forecast_hash_source"] == (
            "trial_ledger" if state else "config_file_backfill (no ledger row)")
