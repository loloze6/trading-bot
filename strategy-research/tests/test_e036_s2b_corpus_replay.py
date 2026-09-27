"""
E-036 S2b (delivery_plan_v26.md slice 8) -- tools/replay_repeat_gate.py, the
read-only replay of the 5a exact-match repeat gate over a runs/ corpus.
Findings on the real corpus: engineering/roadmap/E-036/S2B_REPLAY.md.

Columns are "<protocol mode>/<memory mode>". PRIMARY = 5a_live/strict (the
protocol the live resolver picks at 5a, the memory the live writer would
have written); every other column is a labelled counterfactual.

Covers, on a synthetic corpus in the conftest sandbox (rpr.ROOT):
  1. counts: exact repeats, a one-parameter near-miss (NOVEL), a different
     protocol (NOVEL), unkeyable runs with their reasons; chronology in
     run-NUMBER order (a later run repeats an earlier one, never the reverse);
  2. the 5a protocol: the live resolver (run_context pin, B10 evidence), a
     5a protocol that would not load -> FAIL_LOUD (never keyed on the
     executed fallback, which is a separate counterfactual column), the D-3
     promotion guard -> FAIL_LOUD (and restored after the set-aside column);
  3. memory: strict (the live writer) vs counterfactual (backfill), the real
     corpus shape (a ledger backtest row WITHOUT forecast_hash), prescreen
     stubs, engineering faults from protocol_result and a variant file;
  4. fail loud: an unreadable / missing campaign_state.yaml aborts; an
     unreadable protocol_result.yaml is its own reason;
  5. the old family-grain caller: one (first) timeframe, variant_selection
     merge, earlier runs only;
  6. read-only: listing + sizes + mtimes of the corpus unchanged by the CLI;
  7. the replay key EQUALS the live gate key (the key the live 5a call site
     records, and the key of a memory entry written by the real writers).

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
import protocol_resolution as pres  # noqa: E402
import replay_repeat_gate as rrg  # noqa: E402

from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402
from test_e036_s2a_exact_match_gate import (  # noqa: E402
    _config, _legacy_candidate, _prior_run_in_memory, _set_flags, SYMBOLS, WINDOWS)

CF = "5a_live/counterfactual"
PRIMARY = rrg.PRIMARY
GENERIC_PROMOTION = {"median_sharpe_gt": 0, "max_abs_drawdown_pct_lt": 30,
                     "min_trade_count_gte": 20, "kill_median_sharpe_lt": -1}


def _protocol(name, *, symbols=("BTCUSDT", "ETHUSDT"), timeframe="1h", windows=WINDOWS, **extra):
    return _write_protocol(rpr.ROOT, name, {"symbols": list(symbols), "timeframe": timeframe,
                                            "windows": windows, **extra})


def _write_json(path: Path, obj) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    return path


def _corpus_run(run_id, config, protocol_name, *, card=None, backtested=True,
                record_trial=True, relative_protocol_file=True, results_extra=None):
    """A finished legacy-flow run as the corpus holds one: card, backtest_spec
    (the old gate's fingerprint source), candidate_strategy_config.json, and
    protocol_result.yaml -- with results (a backtest) or as a prescreen stub
    (no results, protocol in prescreen_result.yaml). No run_context.yaml, so
    the 5a resolver takes its B10 branch. The trial row, when recorded, is
    written by the real rpr._record_backtest_trial."""
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
    pfile = f"protocols\\{protocol_name}" if relative_protocol_file else str(
        rpr.ROOT / "protocols" / protocol_name)
    if backtested:
        results = [{"symbol": s, "window": w["label"], **(results_extra or {})}
                   for s in proto["symbols"] for w in proto["windows"]]
        rpr.save_yaml(arts / "protocol_result.yaml", {"protocol_file": pfile, "results": results})
        if record_trial and config is not None:
            rpr._record_backtest_trial(run_id, {"per_symbol_summary": {}, "results": []}, cfg_path)
    else:
        rpr.save_yaml(arts / "protocol_result.yaml", {"source": "prescreen_stub", "results": []})
        rpr.save_yaml(arts / "prescreen_result.yaml", {"protocol_version": pfile})
    return run_dir


def _replay(campaign_state_path="default"):
    state = rpr.CAMPAIGN_STATE_PATH if campaign_state_path == "default" else campaign_state_path
    if state is not None and not Path(state).exists():
        rpr.save_yaml(Path(state), {"trial_sharpes": []})
    return rrg.replay(rpr.ROOT / "runs", root=rpr.ROOT, campaign_state_path=state)


def _rows(result):
    return {r["run_id"]: r for r in result["runs"]}


# ---------------------------------------------------------------------------
# 1. counts and chronology
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
    result = _replay()
    rows = _rows(result)

    assert rows["run_001"][CF]["outcome"] == "NOVEL"
    assert rows["run_002"][CF]["outcome"] == "REPEAT"
    assert rows["run_002"][CF]["matched"] == ["run_001:run_001"]
    assert rows["run_003"][CF]["outcome"] == "NOVEL"
    assert rows["run_004"][CF] == {"outcome": "UNKEYED", "reason": rrg.CAND_NO_CONFIG}
    assert rows["run_005"][CF]["outcome"] == "NOVEL"
    # an absolute protocol_file keys identically to the relative Windows form
    assert rows["run_006"][CF]["matched"] == ["run_001:run_001", "run_002:run_002"]
    assert rows["run_002"][CF]["protocol_source"] == "protocol_result.protocol_file"

    t = result["totals"]
    cf = t["new"][CF]
    assert (cf["REPEAT"], cf["NOVEL"], cf["FAIL_LOUD"], cf["UNKEYED"]) == (2, 3, 0, 1)
    assert cf["reasons"]["UNKEYED"] == {rrg.CAND_NO_CONFIG: 1}
    # PRIMARY: the live writer admits none of these runs (no grid), so the
    # live gate would have nothing to match -- no REPEAT at all.
    assert t["new"][PRIMARY]["REPEAT"] == 0
    assert t["memory"]["strict"]["entries"] == 0
    assert t["memory"]["strict"]["no_entry_by_reason"]["no_idea_status"] == 5
    assert t["memory"]["counterfactual"]["entries"] == t["memory"]["counterfactual"]["variants"] == 5
    assert t["runs"] == 6 and t["candidate_variants"] == 5
    assert t["counterfactual_self_inconsistent"] == []
    assert rows["run_001"]["memory"]["counterfactual"]["forecast_hash_source"] == "trial_ledger"
    assert sorted(c["runs"] for c in t["config_hash_collisions"]) == [
        ["run_001", "run_002", "run_005", "run_006"]]


def test_a_later_run_repeats_an_earlier_one_never_the_reverse_in_run_number_order():
    _protocol("p.json")
    c = _config(min_abs=0.7)
    _corpus_run("run_9", c, "p.json")
    _corpus_run("run_010", copy.deepcopy(c), "p.json")  # sorts BEFORE run_9 as a string
    result = _replay()
    assert [r["run_id"] for r in result["runs"]] == ["run_9", "run_010"]
    rows = _rows(result)
    assert rows["run_9"][CF]["outcome"] == "NOVEL"
    assert rows["run_010"][CF]["outcome"] == "REPEAT"
    assert rows["run_010"][CF]["matched"] == ["run_9:run_9"]


def test_unkeyable_and_fail_loud_reasons_are_reported_never_dropped():
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
    rows = _rows(_replay())
    assert rows["run_001"][PRIMARY] == {"outcome": "UNKEYED", "reason": rrg.CAND_B10_NO_EVIDENCE}
    assert rows["run_001"]["executed/counterfactual"]["reason"] == rrg.CAND_NO_EXECUTED_PROTOCOL
    assert rows["run_002"][PRIMARY]["reason"].startswith(rrg.CAND_CONFIG_UNREADABLE)
    assert rows["run_003"][PRIMARY]["outcome"] == "FAIL_LOUD"
    assert rows["run_003"][PRIMARY]["reason"].startswith(rrg.FAIL_NO_SYMBOLS)
    assert rows["run_004"][PRIMARY]["outcome"] == "FAIL_LOUD"
    assert rows["run_004"][PRIMARY]["reason"].startswith(rrg.FAIL_NOVELTY)


# ---------------------------------------------------------------------------
# 2. the protocol at 5a
# ---------------------------------------------------------------------------

def test_unloadable_5a_protocol_fails_loud_and_the_executed_key_is_only_a_counterfactual():
    """run_027's shape: the resolved (escalation) protocol path could not be
    opened -- pipeline_state.last_error quotes it -- and the backtest then ran
    the baseline. The live gate would raise; keyed on the executed protocol
    it would be a REPEAT."""
    _protocol("p.json")
    _corpus_run("run_001", _config(), "p.json")
    run_dir = _corpus_run("run_002", _config(), "p.json")
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["last_error"] = ("[Errno 22] Invalid argument: 'protocols\\\\escalation_x_Backtest "
                           "prose about 4h..json'")
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    result = _replay()
    row = _rows(result)["run_002"]
    for col in (PRIMARY, CF, "5a_d3_aside/counterfactual"):
        assert row[col]["outcome"] == "FAIL_LOUD", col
        assert row[col]["reason"].startswith(rrg.FAIL_NOVELTY)
        assert row[col]["protocol_source"] == "pipeline_state.last_error"
        assert "key" not in row[col]
    assert row["executed/counterfactual"]["outcome"] == "REPEAT"
    assert row["executed/counterfactual"]["matched"] == ["run_001:run_001"]
    div = result["totals"]["protocol_at_5a_differs_from_executed"]
    assert [d["run_id"] for d in div] == ["run_002"] and div[0]["executed"] == "protocols/p.json"


def test_run_context_pin_is_the_5a_protocol_not_the_executed_one():
    _protocol("p.json")
    _protocol("q.json", timeframe="4h")
    run_dir = _corpus_run("run_001", _config(), "p.json")
    rpr.save_yaml(run_dir / "artifacts" / "run_context.yaml",
                  {"run_type": "forced_diagnostic", "protocol": "q.json"})
    row = _rows(_replay())["run_001"]
    assert row[CF]["protocol_ref"] == "protocols/q.json" and row[CF]["key"]["timeframe"] == "4h"
    assert row[CF]["protocol_branch"] == "forced_diagnostic"
    assert row["executed/counterfactual"]["protocol_ref"] == "protocols/p.json"


def test_promotion_guard_fails_loud_and_is_restored_after_the_set_aside_column():
    _protocol("p.json", promotion=GENERIC_PROMOTION,
              promotion_provenance={"ratified_by": None})
    _corpus_run("run_001", _config(), "p.json")
    real = pres.assert_promotion_ratified
    row = _rows(_replay())["run_001"]
    assert pres.assert_promotion_ratified is real
    assert row[PRIMARY]["outcome"] == "FAIL_LOUD"
    assert row[PRIMARY]["reason"].startswith(rrg.FAIL_PROMOTION)
    assert row["5a_d3_aside/counterfactual"]["outcome"] == "NOVEL"


def test_prescreen_stub_is_a_candidate_but_never_a_memory_entry():
    _protocol("p.json")
    c = _config(min_abs=0.3)
    _corpus_run("run_001", c, "p.json", backtested=False)
    _corpus_run("run_002", copy.deepcopy(c), "p.json")
    rows = _rows(_replay())
    assert rows["run_001"][CF]["outcome"] == "NOVEL"
    assert rows["run_001"][CF]["protocol_source"] == "prescreen_result.protocol_version"
    assert rows["run_001"]["memory"]["counterfactual"]["entry"] is False
    assert rows["run_001"]["memory"]["counterfactual"]["reason"].startswith("not_backtested")
    assert rows["run_002"][CF]["outcome"] == "NOVEL"  # nothing TESTED to repeat


def test_key_hashes_candidate_strategy_config_not_backtest_spec_config():
    """F4d: run_loop injects significance_methodology into backtest_spec's
    config before writing candidate_strategy_config.json -- the file the
    trial row and the live gate hash. The replay must hash that file."""
    _protocol("p.json")
    run_dir = _corpus_run("run_001", _config(), "p.json")
    injected = {**_config(), "significance_methodology": "episode_blocked"}
    cfg_path = _write_json(run_dir / "artifacts" / "candidate_strategy_config.json", injected)
    key = _rows(_replay(None))["run_001"][CF]["key"]
    assert key["forecast_hash"] == rpr._compute_forecast_hash(cfg_path)
    assert key["forecast_hash"] != nov.forecast_hash_of_config(_config())


# ---------------------------------------------------------------------------
# 3. memory: strict vs counterfactual
# ---------------------------------------------------------------------------

def test_ledger_row_without_forecast_hash_is_out_of_strict_memory_and_backfilled_in_counterfactual():
    """The real corpus shape: a `backtest` ledger row that carries no
    forecast_hash. The live writer refuses the entry; the counterfactual
    backfills the hash from the config file."""
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json")
    state = rpr.load_campaign_state()
    for row in state["trial_sharpes"]:
        row.pop("forecast_hash", None)
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, state)
    _protocol("run_050_generated.json")
    _corpus_run("run_051", _config(), "run_050_generated.json", record_trial=False)
    result = _replay()
    rows = _rows(result)
    strict = rows["run_050"]["memory"]["strict"]
    assert strict["entry"] is False and strict["reason"].startswith("ledger_row_without_forecast_hash")
    assert rows["run_050"]["memory"]["ledger_rule"] == "backtest_row_without_forecast_hash"
    assert rows["run_050"]["memory"]["counterfactual"]["forecast_hash_source"] == \
        "backfill: ledger row without forecast_hash"
    assert rows["run_051"][PRIMARY]["outcome"] == "NOVEL"
    assert rows["run_051"][CF]["outcome"] == "REPEAT"
    assert rows["run_051"][CF]["matched"] == ["run_050:run_050"]
    assert result["totals"]["ledger_rule"]["backtest_row_without_forecast_hash"] == 1


@pytest.mark.parametrize("where", ["protocol_result", "variant"])
def test_component_errors_make_a_fault_entry_that_never_matches(where):
    _protocol("p.json")
    if where == "protocol_result":
        run_dir = _corpus_run("run_001", _config(), "p.json",
                              results_extra={"component_errors": {"count": 2, "samples": []}})
    else:
        run_dir = _corpus_run("run_001", _config(), "p.json")
        rpr.save_yaml(run_dir / "artifacts" / "variants" / "v2" / "protocol_result.yaml",
                      {"results": [{"window": "w1", "component_errors": {"count": 1}}]})
    _corpus_run("run_002", _config(), "p.json")
    result = _replay()
    rows = _rows(result)
    for mode in ("strict", "counterfactual"):
        mem = rows["run_001"]["memory"][mode]
        assert mem["entry"] is True and mem["fault"] is True and mem["reason"] == "engineering_fault"
        assert result["totals"]["memory"][mode]["fault_entries"] == 1
    assert rows["run_002"][CF]["outcome"] == "NOVEL"


def test_strict_memory_with_the_real_writers_gives_a_primary_repeat():
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json")
    _protocol("run_050_generated.json")
    _corpus_run("run_051", _config(), "run_050_generated.json", record_trial=False)
    result = _replay()
    rows = _rows(result)
    strict = rows["run_050"]["memory"]["strict"]
    assert (strict["entry"], strict["fault"], strict["reason"]) == (True, False, None)
    assert rows["run_051"][PRIMARY]["outcome"] == "REPEAT"
    assert rows["run_051"][PRIMARY]["matched"] == ["run_050:run_050"]
    assert result["totals"]["memory"]["strict"]["entries"] == 1


# ---------------------------------------------------------------------------
# 4. fail loud on unreadable inputs
# ---------------------------------------------------------------------------

def test_unreadable_or_missing_campaign_state_aborts_the_replay(tmp_path):
    _protocol("p.json")
    _corpus_run("run_001", _config(), "p.json")
    bad = tmp_path / "campaign_state.yaml"
    bad.write_text("trial_sharpes: [\n  - a: b\n c", encoding="utf-8")
    with pytest.raises(rrg.ReplayError, match="unreadable"):
        rrg.replay(rpr.ROOT / "runs", root=rpr.ROOT, campaign_state_path=bad)
    with pytest.raises(rrg.ReplayError, match="does not exist"):
        rrg.replay(rpr.ROOT / "runs", root=rpr.ROOT, campaign_state_path=tmp_path / "gone.yaml")
    bad.write_text("trial_sharpes: 3\n", encoding="utf-8")
    with pytest.raises(rrg.ReplayError, match="not a list"):
        rrg.replay(rpr.ROOT / "runs", root=rpr.ROOT, campaign_state_path=bad)


def test_unreadable_protocol_result_is_its_own_reason():
    _protocol("p.json")
    run_dir = _corpus_run("run_001", _config(), "p.json")
    (run_dir / "artifacts" / "protocol_result.yaml").write_text("a: [\n b: c", encoding="utf-8")
    row = _rows(_replay())["run_001"]
    for mode in ("strict", "counterfactual"):
        assert row["memory"][mode]["reason"].startswith(rrg.CAND_ARTIFACT_UNREADABLE)
    assert row["executed/counterfactual"]["reason"].startswith(rrg.CAND_ARTIFACT_UNREADABLE)
    assert row[CF]["reason"].startswith(rrg.CAND_ARTIFACT_UNREADABLE)


def test_unparseable_card_is_its_own_reason():
    _protocol("p.json")
    run_dir = _corpus_run("run_001", _config(), "p.json")
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text("a: b\n  c d: [\n", encoding="utf-8")
    result = _replay()
    row = _rows(result)["run_001"]
    assert row["memory"]["counterfactual"]["reason"].startswith(rrg.CAND_ARTIFACT_UNREADABLE)
    assert row["old"]["reason"].startswith(rrg.CAND_ARTIFACT_UNREADABLE)
    assert row[CF]["outcome"] == "NOVEL"  # the candidate key needs no card
    assert result["totals"]["old"]["not_evaluable_by_reason"] == {rrg.CAND_ARTIFACT_UNREADABLE: 1}


# ---------------------------------------------------------------------------
# 5. the old family-grain side (the retired 5a caller)
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
    assert rows["run_001"]["old"]["outcome"] == "novel"
    assert rows["run_002"]["old"]["outcome"] == "repeat"
    assert rows["run_002"]["old"]["run_ids"] == ["run_001"]
    assert rows["run_002"][CF]["outcome"] == "NOVEL"
    assert rows["run_003"]["old"]["outcome"] == "novel"   # card says 4h: another triple
    assert rows["run_003"][CF]["outcome"] == "REPEAT"      # but it RAN p.json (1h)
    m = result["totals"]["agreement_old_x_new"][CF]
    assert m["repeat"] == {"REPEAT": 0, "NOVEL": 1, "FAIL_LOUD": 0, "UNKEYED": 0}
    assert m["novel"] == {"REPEAT": 1, "NOVEL": 1, "FAIL_LOUD": 0, "UNKEYED": 0}


def test_old_side_checks_one_timeframe_and_merges_variant_selection():
    _protocol("p.json")
    _corpus_run("run_001", _config(0.5), "p.json",
                card={"hypothesis_id": "KELTNER_A", "timeframe": "4h", "target_market": "ETHUSDT"})
    # names 1h and 4h: the old caller checked extract_timeframes()[0] == "1h" only
    _corpus_run("run_002", _config(0.6), "p.json",
                card={"hypothesis_id": "KELTNER_B", "timeframe": "4h and 1h",
                      "target_market": "ETHUSDT"})
    # its card alone is unclassifiable; the selection's variant_definition
    # (merged into the card, as the old caller did) makes it keltner, 4h, ETH
    sel = _corpus_run("run_003", _config(0.7), "p.json",
                      card={"hypothesis_id": "IDEA_C", "timeframe": "1h",
                            "target_market": "BTCUSDT"})
    rpr.save_yaml(sel / "artifacts" / "variant_selection.yaml",
                  {"instrument": "ETHUSDT", "timeframe": "4h",
                   "variant_definition": {"thesis": "Keltner channel variant."}})
    rows = _rows(_replay())
    assert rows["run_002"]["old"]["timeframe"] == "1h"
    assert rows["run_002"]["old"]["outcome"] == "novel"
    old3 = rows["run_003"]["old"]
    assert old3["selection_source"] == "variant_selection.yaml"
    assert (old3["family"], old3["instrument"], old3["timeframe"]) == ("keltner_channel", "ETHUSDT", "4h")
    # _config(0.5/0.6/0.7) differ only in a transform: the old fingerprint collapses them
    assert old3["outcome"] == "repeat" and old3["run_ids"] == ["run_001", "run_002"]


# ---------------------------------------------------------------------------
# 6. read-only on the corpus
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
    text = out.read_text(encoding="utf-8")
    doc = yaml.safe_load(text)
    assert doc["totals"]["new"][CF]["REPEAT"] == 1
    # no machine-specific absolute path (the writer's messages quote full paths)
    assert str(rpr.ROOT.resolve()) not in text and rpr.ROOT.resolve().as_posix() not in text
    assert "no_idea_status" in text
    with pytest.raises(rrg.ReplayError, match="never writes into the corpus"):
        rrg.main(["--runs-dir", str(runs), "--root", str(rpr.ROOT),
                  "--out", str(runs / "run_001" / "x.yaml")])
    assert _snapshot(runs) == before


# ---------------------------------------------------------------------------
# 7. replay key == live gate key
# ---------------------------------------------------------------------------

def test_replay_key_equals_the_live_gate_key_on_both_sides():
    # memory side: a prior run recorded through the REAL writers
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json")
    live_memory = cm.load_memory(rpr.ROOT / "campaign_record" / "campaign_memory.yaml")
    live_mem_keys = list(nov.match_index(live_memory, nov.protocol_specs(rpr.ROOT, live_memory)))

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
        rows = _rows(_replay(state))
        for col in ((PRIMARY, CF) if state else (CF,)):
            assert rows["run_061"][col]["key"] == live["key"], col
            assert rows["run_061"][col]["outcome"] == "REPEAT"
            assert rows["run_061"][col]["matched"] == [
                f"{m['run_id']}:{m['variant_id']}" for m in live["matched"]]
        assert rows["run_061"][CF]["protocol_branch"] == "protocol_ref_pinned"
        assert rows["run_050"]["memory"]["counterfactual"]["self_consistent"] is True
        assert rows["run_050"]["memory"]["counterfactual"]["forecast_hash_source"] == (
            "trial_ledger" if state else "backfill: no ledger row")
    # the memory side: the replay's strict entry (the live writer itself) and
    # its counterfactual entry both key exactly as the live memory entry does
    mem = _rows(_replay())["run_050"]["memory"]
    for mode in ("strict", "counterfactual"):
        k = mem[mode]["key"]
        assert [(k["forecast_hash"], tuple(k["symbols"]), k["timeframe"], k["window_set"])] == \
            live_mem_keys, mode
