"""
E-036 S2a (delivery_plan_v26.md slice 8.1) -- the exact-match repeat check.
Spec: engineering/roadmap/E-036/S1_FINDINGS_SLICE8.md and its operator
decision of 2026-09-27 (binary REPEAT/NOVEL, one key from campaign memory,
Layer 1 advisory only, anti_adjacency_retry retired, the idea-writing input
repointed at the campaign record).

Covers:
  1. tools/novelty.py: the key and lookup -- REPEAT/NOVEL, legacy entries and
     runs with no memory entry never REPEAT, sorted-symbols equality, the key
     reads the PROTOCOL FILE's content (a per-run protocol file name never
     makes two identical runs differ), a run never matches itself.
  2. decide_next is unchanged: it re-exports novelty's functions, and a
     verbatim copy of its pre-extraction key code gives identical indexes; the
     legacy family digest advisory moved to build_exclusion_digest unchanged.
  3. anti_adjacency_gate.layer2_digest_check: binary, no NEIGHBOUR; a
     transform-only change (which the old composition fingerprint collapsed
     to REPEAT) is NOVEL; Layer 1 is recorded as a warning, never a refusal.
  4. The legacy 5a call site (_route_post_variant_selection) and the
     config-direct 5a call site (_gate_config_direct_variants), end to end
     against a memory entry written by the REAL writers
     (_record_backtest_trial -> campaign_memory.build_memory_entry ->
     upsert_memory) -- never a hand-built key on both sides. A skipped repeat
     gets no trial row; every variant a repeat ends the run
     completed_no_new_hypothesis.
  5. Flag-off byte identity for both call sites.

Sandbox: tests/conftest.py's autouse fixture points rpr.ROOT /
rpr.CAMPAIGN_STATE_PATH at a per-test tmp dir. No LLM, no backtest, no
market data. Window dates are in 2021 (nowhere near the sealed holdout).
"""
import asyncio
import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import anti_adjacency_gate as aag  # noqa: E402
import build_exclusion_digest as bed  # noqa: E402
import campaign_memory as cm  # noqa: E402
import decide_next as dn  # noqa: E402
import novelty as nov  # noqa: E402

from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402

WINDOWS = [{"label": "w1", "start": "2021-01-01", "end": "2021-06-30"},
           {"label": "w2", "start": "2021-07-01", "end": "2021-12-31"}]
SYMBOLS = ["ETHUSDT", "BTCUSDT"]  # deliberately unsorted: the key sorts them


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _config(min_abs=0.5, transforms=None):
    return {
        "regime_detector": {"mode": "threshold_rules", "rules": [{"regime": "trending"}]},
        "strategies": {"regimes": {"trending": {"components": [
            {"id": "mom", "class": "strategies.strategy_components.MomentumComponent",
             "params": {"lookback": 24}, "weight": 1.0,
             "transforms": transforms if transforms is not None
             else [{"op": "deadband", "params": {"min_abs": min_abs}}]},
        ]}}},
    }


def _set_flags(**flags):
    cfg_dir = rpr.ROOT / "config"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    (cfg_dir / "campaign_config.yaml").write_text(
        yaml.safe_dump({"orchestrator": {k: {"enabled": v} for k, v in flags.items()}}),
        encoding="utf-8")


def _protocol(name, *, symbols=SYMBOLS, timeframe="1h", windows=WINDOWS):
    return _write_protocol(rpr.ROOT, name, {"symbols": list(symbols), "timeframe": timeframe,
                                            "windows": windows})


def _memory_path():
    return rpr.ROOT / "campaign_record" / "campaign_memory.yaml"


def _write_json(path: Path, obj) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)  # the same serialisation run_loop / run_tool_worker use
    return path


def _grid(run_id, columns):
    cell = {"result": "FAIL", "value": 0.0, "threshold": 0.02, "n_windows": 2, "n_trades": 30}
    return {"result": "GRID_EVALUATED", "criteria": ["ic_median"], "variants": list(columns),
            "grid": {"ic_median": {c: dict(cell) for c in columns}}, "idea_status": "refuted",
            "reason": "at least one criterion FAILed with sufficient data on at least one variant"}


def _prior_run_in_memory(run_id, config, *, protocol_name, symbols=SYMBOLS, timeframe="1h",
                         windows=WINDOWS, variant_loop=False):
    """A finished run recorded through the REAL writers: its trial row by
    rpr._record_backtest_trial (forecast_hash = _compute_forecast_hash of the
    config file it ran), its memory entry by campaign_memory.build_memory_entry
    + upsert_memory (protocol_ref from protocol_result.yaml's protocol_file,
    relative to ROOT -- exactly regroup_record's call)."""
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    proto_path = _protocol(protocol_name, symbols=symbols, timeframe=timeframe, windows=windows)
    rpr.save_yaml(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-PRIOR", "timeframe": timeframe})
    summary = {"per_symbol_summary": {}, "results": []}
    results = [{"symbol": s, "window": w["label"]} for s in symbols for w in windows]
    pr = {"verdict": "kill", "protocol_file": str(proto_path), "results": results}
    if variant_loop:
        cfg_path = _write_json(arts / "variants" / "base" / "strategy_config.json", config)
        rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {"base": {
            "status": "validated", "config_path": "artifacts/variants/base/strategy_config.json"}}})
        rpr._record_backtest_trial(run_id, summary, cfg_path, trial_id=f"{run_id}:base")
        rpr.save_yaml(arts / "variants" / "base" / "protocol_result.yaml", pr)
        columns = ["base"]
    else:
        cfg_path = _write_json(arts / "candidate_strategy_config.json", config)
        rpr._record_backtest_trial(run_id, summary, cfg_path)
        columns = [run_id]
    rpr.save_yaml(arts / "protocol_result.yaml", pr)
    grid = _grid(run_id, columns)
    rpr.save_yaml(arts / "grid_evaluation.yaml", grid)
    rpr.save_yaml(arts / "idea_status.yaml", rpr._build_idea_status_artifact(grid, run_id))
    entry = cm.build_memory_entry(run_dir, run_id,
                                  trial_sharpes=rpr.load_campaign_state().get("trial_sharpes"),
                                  categories=[], protocol_root=rpr.ROOT)
    cm.upsert_memory(_memory_path(), entry)
    return entry


def _trial_ids():
    return [t["trial_id"] for t in rpr.load_campaign_state().get("trial_sharpes", [])]


# ---------------------------------------------------------------------------
# 1. tools/novelty.py
# ---------------------------------------------------------------------------

def _mem(*entries):
    return {"schema_version": 1, "legacy_note": "x", "runs": {e["run_id"]: e for e in entries}}


def _entry(run_id, fh="fh-1", symbols=("BTCUSDT",), ref="protocols/p.json", **extra):
    return {"run_id": run_id, "legacy": False, "engineering_fault": None, "timeframe": "1h",
            "protocol_ref": ref,
            "variants": {run_id: {"status": "tested", "forecast_hash": fh,
                                  "symbols": list(symbols)}}, **extra}


def _specs(tmp_root, refs=("protocols/p.json",)):
    return {nov.normalize_ref(r): nov.protocol_spec(tmp_root, r) for r in refs}


def test_novelty_repeat_and_novel():
    _protocol("p.json")
    specs = _specs(rpr.ROOT)
    memory = _mem(_entry("run_001"))
    same = nov.novelty_key("fh-1", ["BTCUSDT"], {"protocol_ref": "protocols/p.json"}, specs)
    other = nov.novelty_key("fh-2", ["BTCUSDT"], {"protocol_ref": "protocols/p.json"}, specs)
    assert nov.lookup(same, memory, specs) == "REPEAT"
    assert nov.exact_matches(same, memory, specs) == [{"run_id": "run_001", "variant_id": "run_001"}]
    assert nov.lookup(other, memory, specs) == "NOVEL"


def test_novelty_legacy_entry_and_missing_entry_never_repeat():
    _protocol("p.json")
    specs = _specs(rpr.ROOT)
    key = nov.novelty_key("fh-1", ["BTCUSDT"], {"protocol_ref": "protocols/p.json"}, specs)
    assert nov.lookup(key, _mem(_entry("run_001", legacy=True)), specs) == "NOVEL"
    assert nov.lookup(key, _mem(), specs) == "NOVEL"  # no memory entry at all
    faulty = _entry("run_001")
    faulty["engineering_fault"] = "component_execution_error"
    assert nov.lookup(key, _mem(faulty), specs) == "NOVEL"


def test_novelty_symbols_compare_sorted():
    _protocol("p.json")
    specs = _specs(rpr.ROOT)
    memory = _mem(_entry("run_001", symbols=("BTCUSDT", "ETHUSDT")))
    key = nov.novelty_key("fh-1", ["ETHUSDT", "BTCUSDT"], {"protocol_ref": "protocols/p.json"}, specs)
    assert nov.lookup(key, memory, specs) == "REPEAT"
    one = nov.novelty_key("fh-1", ["BTCUSDT"], {"protocol_ref": "protocols/p.json"}, specs)
    assert nov.lookup(one, memory, specs) == "NOVEL"


def test_novelty_key_reads_protocol_content_not_its_file_name():
    """Generated protocols are per-run file names; the same windows and
    timeframe under another name are the same test. Different windows or
    timeframe are not."""
    _protocol("run_001_generated.json")
    _protocol("run_002_generated.json")
    _protocol("run_003_generated.json", windows=WINDOWS[:1])
    _protocol("run_004_generated.json", timeframe="4h")
    refs = [f"protocols/run_00{i}_generated.json" for i in range(1, 5)]
    specs = _specs(rpr.ROOT, refs)
    memory = _mem(_entry("run_001", ref=refs[0]))
    keys = [nov.novelty_key("fh-1", ["BTCUSDT"], {"protocol_ref": r}, specs) for r in refs]
    assert [nov.lookup(k, memory, specs) for k in keys] == ["REPEAT", "REPEAT", "NOVEL", "NOVEL"]


def test_novelty_unreadable_protocol_never_matches_a_resolved_one():
    _protocol("p.json")
    specs = _specs(rpr.ROOT, ("protocols/p.json", "protocols/gone.json"))
    memory = _mem(_entry("run_001", ref="protocols/gone.json"))
    key = nov.novelty_key("fh-1", ["BTCUSDT"], {"protocol_ref": "protocols/p.json"}, specs)
    assert nov.lookup(key, memory, specs) == "NOVEL"


def test_novelty_exclude_run_id_never_matches_itself():
    _protocol("p.json")
    specs = _specs(rpr.ROOT)
    key = nov.novelty_key("fh-1", ["BTCUSDT"], {"protocol_ref": "protocols/p.json"}, specs)
    memory = _mem(_entry("run_001"))
    assert nov.lookup(key, memory, specs, exclude_run_id="run_001") == "NOVEL"
    assert nov.lookup(key, memory, specs, exclude_run_id="run_999") == "REPEAT"


# ---------------------------------------------------------------------------
# 2. decide_next unchanged (pin)
# ---------------------------------------------------------------------------

def test_decide_next_reexports_the_shared_key_functions():
    assert dn.novelty_key is nov.novelty_key
    assert dn.protocol_spec is nov.protocol_spec
    assert dn.normalize_ref is nov.normalize_ref
    assert dn.normalize_timeframe is nov.normalize_timeframe
    assert dn._exact_index is nov.exact_index


def _old_decide_next_exact_index(memory, specs):
    """VERBATIM copy of decide_next.novelty_key/_exact_index before E-036 S2a
    extracted them (origin/master 9a6f9d27, tools/decide_next.py) -- the pin."""
    def normalize_timeframe(tf):
        return tf.strip().lower() if isinstance(tf, str) and tf.strip() else None

    def normalize_ref(ref):
        if not isinstance(ref, str) or not ref.strip():
            return None
        out = ref.strip().replace("\\", "/")
        while out.startswith("./"):
            out = out[2:]
        return out

    def novelty_key(forecast_hash, symbols, entry, specs):
        ref = normalize_ref(entry.get("protocol_ref"))
        spec = specs.get(ref) if ref else None
        if spec:
            timeframe, window_set = spec["timeframe"], f"windows:{spec['windows_sha256']}"
        else:
            timeframe, window_set = normalize_timeframe(entry.get("timeframe")), f"unresolved:{ref}"
        return (forecast_hash, tuple(sorted(symbols or [])), timeframe, window_set)

    index = {}
    for run_id in sorted((memory.get("runs") or {})):
        entry = memory["runs"][run_id]
        if entry.get("engineering_fault"):
            continue
        for v in (entry.get("variants") or {}).values():
            if v.get("status") != "tested" or not v.get("forecast_hash"):
                continue
            key = novelty_key(v["forecast_hash"], v.get("symbols"), entry, specs)
            runs = index.setdefault(key, [])
            if run_id not in runs:
                runs.append(run_id)
    return index


def test_decide_next_exact_index_is_byte_identical_to_the_pre_extraction_code():
    _protocol("p.json")
    _protocol("q.json", timeframe="4h")
    specs = _specs(rpr.ROOT, ("protocols/p.json", "./protocols\\q.json", "protocols/gone.json"))
    fault = _entry("run_004", fh="fh-4")
    fault["engineering_fault"] = "component_execution_error"
    multi = _entry("run_005", fh="fh-1")
    multi["variants"]["design"] = {"status": "tested", "forecast_hash": "fh-5", "symbols": ["ETHUSDT"]}
    multi["variants"]["asset"] = {"status": "not_tested", "forecast_hash": None, "symbols": []}
    multi["variants"]["failed"] = {"status": "failed", "forecast_hash": "fh-x", "symbols": []}
    memory = _mem(_entry("run_001"), _entry("run_002", ref="./protocols\\q.json", timeframe=" 4H "),
                  _entry("run_003", ref="protocols/gone.json", timeframe="1H"), fault, multi,
                  _entry("run_006", fh=None))
    new = dn._exact_index(memory, specs)
    old = _old_decide_next_exact_index(memory, specs)
    assert list(new.items()) == list(old.items())  # same keys, values AND order
    assert new  # non-trivial fixture
    # The one declared difference: an entry marked legacy: true (which the
    # memory writer never produces -- campaign_memory.schema.json: const false).
    legacy = _mem(_entry("run_001", legacy=True))
    assert _old_decide_next_exact_index(legacy, specs) and dn._exact_index(legacy, specs) == {}


def _old_layer2_advisory(card, config, symbols, timeframe, digest):
    """VERBATIM behaviour of decide_next._digest_advisory + the old
    anti_adjacency_gate.layer2_digest_check (origin/master 9a6f9d27), reduced
    to the four fields the advisory kept."""
    if not digest or not isinstance(card, dict):
        return {"outcome": "not_available", "family": None, "family_confidence": None, "run_ids": []}
    instrument = (symbols or [None])[0]
    family, confidence = bed.classify_family(card)
    cfp = bed.composition_fingerprint(config) if config else None
    entry = digest.get("families", {}).get(family)
    matches = [t for t in (entry.get("triples", []) if entry else [])
               if t.get("instrument") == instrument and t.get("timeframe") == timeframe]
    if not matches:
        res = {"outcome": "novel", "family": family, "family_confidence": confidence}
    else:
        repeat = next((t for t in matches if t.get("fidelity") == "structured"
                       and t.get("fingerprint") is not None and cfp is not None
                       and t["fingerprint"] == cfp), None)
        if repeat is not None:
            res = {"outcome": "repeat", "family": family, "family_confidence": confidence,
                   "run_ids": repeat["run_ids"]}
        else:
            res = {"outcome": "neighbour", "family": family, "family_confidence": confidence,
                   "neighbours": [{"run_ids": t["run_ids"]} for t in matches]}
    run_ids = list(res.get("run_ids") or sorted(
        {r for n in res.get("neighbours") or [] for r in n.get("run_ids") or []}))
    return {"outcome": res.get("outcome"), "family": res.get("family"),
            "family_confidence": res.get("family_confidence"), "run_ids": run_ids}


def test_decide_next_digest_advisory_is_byte_identical_to_the_old_layer2():
    card = {"hypothesis_id": "FOO", "thesis": "funding mean reversion"}
    family, _ = bed.classify_family(card)
    fp = bed.composition_fingerprint(_config())
    digests = [
        None,
        {"families": {}},
        {"families": {family: {"triples": [{"instrument": "BTCUSDT", "timeframe": "1h",
                                             "fidelity": "structured", "fingerprint": fp,
                                             "run_ids": ["run_010"]}]}}},
        {"families": {family: {"triples": [
            {"instrument": "BTCUSDT", "timeframe": "1h", "fidelity": "coarse",
             "fingerprint": None, "run_ids": ["run_012", "run_011"]},
            {"instrument": "BTCUSDT", "timeframe": "1h", "fidelity": "structured",
             "fingerprint": bed.composition_fingerprint(_config(0.9)), "run_ids": ["run_013"]}]}}},
        {"families": {family: {"triples": [{"instrument": "ETHUSDT", "timeframe": "1h",
                                             "run_ids": ["run_014"]}]}}},
    ]
    for digest in digests:
        for config in (_config(), None):
            for card_ in (card, None):
                args = (card_, config, ["BTCUSDT"], "1h", digest)
                assert dn._digest_advisory(*args) == _old_layer2_advisory(*args), (digest, config)


# ---------------------------------------------------------------------------
# 3. anti_adjacency_gate: binary layer 2, advisory layer 1
# ---------------------------------------------------------------------------

def test_layer2_is_binary_and_the_neighbour_machinery_is_gone():
    for name in ("_describe_fingerprint_diff", "classify_family", "composition_fingerprint"):
        assert not hasattr(aag, name), name
    _protocol("p.json")
    specs = _specs(rpr.ROOT)
    memory = _mem(_entry("run_001"))
    base = aag.candidate_key("fh-1", ["BTCUSDT"], "protocols/p.json", specs)
    index = nov.match_index(memory, specs)
    assert aag.layer2_digest_check(base, index)["outcome"] == "repeat"
    for key in (aag.candidate_key("fh-2", ["BTCUSDT"], "protocols/p.json", specs),
                aag.candidate_key("fh-1", ["ETHUSDT"], "protocols/p.json", specs)):
        res = aag.layer2_digest_check(key, index)
        assert res.route == "admit" and res["outcome"] == "novel" and "neighbours" not in res


def test_transform_only_change_is_novel_where_the_old_fingerprint_said_repeat():
    """Regression for the old design's documented weakness
    (composition_fingerprint ignores transforms): two configs differing only
    in a transform parameter had IDENTICAL fingerprints -- the old gate would
    REFUSE the second as a repeat. The config hash sees the difference."""
    a, b = _config(min_abs=0.5), _config(min_abs=0.8)
    assert bed.composition_fingerprint(a) == bed.composition_fingerprint(b)
    _protocol("p.json")
    specs = _specs(rpr.ROOT)
    fh_a, fh_b = nov.forecast_hash_of_config(a), nov.forecast_hash_of_config(b)
    memory = _mem(_entry("run_001", fh=fh_a))
    res = aag.layer2_digest_check(aag.candidate_key(fh_b, ["BTCUSDT"], "protocols/p.json", specs),
                                  nov.match_index(memory, specs))
    assert res.route == "admit" and res["outcome"] == "novel"


def test_layer1_is_advisory_only():
    kb = {"findings": [{"id": "widget_closed", "hypothesis_id": "WIDGET_MEAN_REVERSION",
                        "evidence_runs": [], "exhausted": True, "reactivation_condition": None}]}
    assert aag.layer1_kb_check("WIDGET_MEAN_REVERSION", "1h", kb["findings"],
                               rpr.ROOT / "runs").route == "refuse"  # what used to bind
    _protocol("p.json")
    specs = _specs(rpr.ROOT)
    key = aag.candidate_key("fh-1", ["BTCUSDT"], "protocols/p.json", specs)
    res = aag.evaluate_candidate(key, _mem(), specs, kb=kb, candidate_hid="WIDGET_MEAN_REVERSION",
                                 candidate_timeframe="1h", runs_dir=rpr.ROOT / "runs")
    assert res.route == "admit"
    assert res["layer1_advisory"]["status"] == "warn"
    assert res["layer1_advisory"]["kb_finding_id"] == "widget_closed"
    assert aag.evaluate_candidate(key, _mem(), specs)["layer1_advisory"]["status"] == "not_evaluated"


# ---------------------------------------------------------------------------
# 4a. legacy LLM flow: _route_post_variant_selection
# ---------------------------------------------------------------------------

def _legacy_candidate(run_id, config, protocol_name):
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-NEW", "timeframe": "1h",
                                                  "target_market": "BTCUSDT"})
    rpr.save_yaml(arts / "expanded_hypothesis_card.yaml", {"base_hypothesis_id": "H-NEW",
                                                           "expanded_variants": [{"variant_id": "V1"}]})
    rpr.save_yaml(arts / "backtest_spec.yaml", {"status": "spec_ready", "config": config,
                                                "selected_variant_id": "V1"})
    rpr.save_yaml(arts / "decision.yaml", {"status": "spec_ready", "rationale": "x"})
    _set_flags(variant_selection_record=True)
    rpr._record_variant_selection(run_dir)
    _protocol(protocol_name)
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": f"protocols/{protocol_name}"})
    _write_json(arts / "candidate_strategy_config.json", config)  # what run_loop writes
    return run_dir


def test_legacy_call_site_refuses_a_real_repeat_end_to_end():
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json")
    run_dir = _legacy_candidate("run_061", copy.deepcopy(_config()), "run_061_generated.json")
    _set_flags(variant_selection_record=True, variant_anti_adjacency_gate=True)
    assert rpr._route_post_variant_selection(run_dir, "run_061") == "human_pause"
    res = rpr.load_yaml(run_dir / "artifacts" / "variant_anti_adjacency_result.yaml")
    assert res["route"] == "refuse" and res["outcome"] == "repeat"
    assert res["matched"] == [{"run_id": "run_050", "variant_id": "run_050"}]
    assert res["selected_variant_id"] == "V1"
    assert res["key"]["symbols"] == sorted(SYMBOLS) and res["key"]["timeframe"] == "1h"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "paused_for_human"
    assert state["flags"]["variant_anti_adjacency_gate_refused"] is True


def test_legacy_call_site_admits_a_changed_config_and_its_own_rerun():
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json")
    run_dir = _legacy_candidate("run_061", _config(min_abs=0.9), "run_061_generated.json")
    _set_flags(variant_selection_record=True, variant_anti_adjacency_gate=True)
    assert rpr._route_post_variant_selection(run_dir, "run_061") is None
    assert rpr.load_yaml(run_dir / "artifacts" / "variant_anti_adjacency_result.yaml")["route"] == "admit"
    # the recorded run itself, re-run (its memory entry is replaced on re-run)
    rerun = _legacy_candidate("run_050", _config(), "run_050_generated.json")
    assert rpr._route_post_variant_selection(rerun, "run_050") is None


def test_legacy_call_site_flag_off_reads_and_writes_nothing():
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json")
    run_dir = _legacy_candidate("run_061", _config(), "run_061_generated.json")
    _set_flags(variant_selection_record=True, variant_anti_adjacency_gate=False)
    before = (run_dir / "pipeline_state.yaml").read_bytes()
    assert rpr._route_post_variant_selection(run_dir, "run_061") is None
    assert (run_dir / "pipeline_state.yaml").read_bytes() == before
    assert not (run_dir / "artifacts" / "variant_anti_adjacency_result.yaml").exists()


def test_gate_on_without_memory_and_regroup_off_fails_loud():
    run_dir = _legacy_candidate("run_061", _config(), "run_061_generated.json")
    _set_flags(variant_selection_record=True, variant_anti_adjacency_gate=True)
    with pytest.raises(RuntimeError, match="regroup_record"):
        rpr._route_post_variant_selection(run_dir, "run_061")


def test_gate_on_fresh_campaign_with_regroup_on_admits():
    run_dir = _legacy_candidate("run_061", _config(), "run_061_generated.json")
    _set_flags(variant_selection_record=True, variant_anti_adjacency_gate=True,
               grid_evaluation=True, category_reports=True, specialist_readers=True,
               regroup_record=True)
    assert rpr._route_post_variant_selection(run_dir, "run_061") is None
    res = rpr.load_yaml(run_dir / "artifacts" / "variant_anti_adjacency_result.yaml")
    assert res["route"] == "admit" and res["memory_present"] is False


def test_legacy_gate_runs_after_candidate_config_is_written_in_run_loop():
    """The call moved below the candidate_strategy_config.json write: the
    key must hash the file protocol_execution runs (F4d's injection
    included), not backtest_spec.yaml's pre-injection config."""
    import inspect
    src = inspect.getsource(rpr.run_loop)
    write = src.index('json.dump(config_obj, f, indent=2)')
    gate = src.index("_route_post_variant_selection(RUN_DIR, run_id)")
    validator = src.index('validator  = Path("..") / "trading-bot"', write)
    assert write < gate < validator


# ---------------------------------------------------------------------------
# 4b. config-direct 5a: _gate_config_direct_variants
# ---------------------------------------------------------------------------

def _config_direct_candidate(run_id, configs: dict, protocol_name):
    """A config-direct run after run_tool_worker's backtest_specification
    branch: one strategy_config.json per variant, index.yaml, and the base
    copy at candidate_strategy_config.json."""
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-CD", "timeframe": "1h"})
    index = {}
    for vid, cfg in configs.items():
        _write_json(arts / "variants" / vid / "strategy_config.json", cfg)
        index[vid] = {"status": "validated",
                      "config_path": f"artifacts/variants/{vid}/strategy_config.json"}
        if vid == "base":
            _write_json(arts / "candidate_strategy_config.json", cfg)
    index["dropped"] = {"status": "not_tested", "reason": "patch application failed: /x"}
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": index})
    _protocol(protocol_name)
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": f"protocols/{protocol_name}"})
    return run_dir


_CD_ON = dict(config_direct_authoring=True, variant_loop=True, variant_anti_adjacency_gate=True,
              data_availability_gate=False)


def test_config_direct_partial_repeat_skips_only_the_repeat_and_it_gets_no_trial_row(monkeypatch):
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json",
                         variant_loop=True)
    run_dir = _config_direct_candidate(
        "run_061", {"base": _config(), "design": _config(0.7), "asset": _config(0.9)},
        "run_061_generated.json")
    _set_flags(**_CD_ON)
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "protocol_execution"
    idx = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]
    assert idx["base"]["status"] == "not_tested"
    assert idx["base"]["reason"].startswith("repeat:") and "run_050:base" in idx["base"]["reason"]
    assert idx["base"]["config_path"] == "artifacts/variants/base/strategy_config.json"
    assert idx["design"]["status"] == idx["asset"]["status"] == "validated"
    assert idx["dropped"] == {"status": "not_tested", "reason": "patch application failed: /x"}
    res = rpr.load_yaml(run_dir / "artifacts" / "variant_anti_adjacency_result.yaml")
    assert res["repeats"] == ["base"] and res["run_end"] is None
    assert res["variants"]["base"]["matched"] == [{"run_id": "run_050", "variant_id": "base"}]
    # a skipped repeat is never backtested: protocol_execution's loop records
    # a trial row for the two remaining variants only.
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    ran = []

    def _fake_run(cmd, *a, **k):
        ran.append(Path(cmd[2]).parent.name)
        out = Path(cmd[cmd.index("--out-dir") + 1])
        out.mkdir(parents=True, exist_ok=True)
        (out / "protocol_summary.json").write_text(json.dumps(
            {"protocol_file": "p", "results": [], "per_symbol_summary": {}, "verdict": "kill"}),
            encoding="utf-8")

        class _Ok:
            returncode, stdout, stderr = 0, "", ""
        return _Ok()
    monkeypatch.setattr(rpr.subprocess, "run", _fake_run)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_061"))
    assert sorted(ran) == ["asset", "design"]
    assert [t for t in _trial_ids() if t.startswith("run_061")] == ["run_061:asset", "run_061:design"]


def test_config_direct_all_repeat_ends_the_run_completed_no_new_hypothesis():
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json",
                         variant_loop=True)
    _prior_run_in_memory("run_051", _config(0.7), protocol_name="run_051_generated.json")
    run_dir = _config_direct_candidate("run_061", {"base": _config(), "design": _config(0.7)},
                                       "run_061_generated.json")
    _set_flags(**_CD_ON)
    assert (rpr._route_post_config_direct_backtest_specification(run_dir)
            == rpr.NO_NEW_HYPOTHESIS_STAGE == "completed_no_new_hypothesis")
    res = rpr.load_yaml(run_dir / "artifacts" / "variant_anti_adjacency_result.yaml")
    assert res["repeats"] == ["base", "design"] and res["run_end"] == "completed_no_new_hypothesis"
    assert res["variants"]["design"]["matched"] == [{"run_id": "run_051", "variant_id": "run_051"}]
    assert not [t for t in _trial_ids() if t.startswith("run_061")]
    import verdict_criteria_evaluator as vce
    assert "completed_no_new_hypothesis" in vce._NON_VERDICT_OUTCOMES


def test_config_direct_variant_loop_off_checks_base_via_candidate_config():
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json")
    run_dir = _config_direct_candidate("run_061", {"base": _config(), "design": _config(0.7)},
                                       "run_061_generated.json")
    _set_flags(config_direct_authoring=True, variant_anti_adjacency_gate=True)
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "completed_no_new_hypothesis"
    res = rpr.load_yaml(run_dir / "artifacts" / "variant_anti_adjacency_result.yaml")
    assert res["checked"] == ["base"]
    assert res["variants"]["base"]["config_ref"] == "runs/run_061/artifacts/candidate_strategy_config.json"


def test_config_direct_flag_off_is_byte_identical_to_no_gate(monkeypatch):
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json",
                         variant_loop=True)
    flags = dict(_CD_ON, variant_anti_adjacency_gate=False)
    outs = []
    for gate_present in (True, False):
        run_dir = _config_direct_candidate(f"run_06{int(gate_present)}",
                                           {"base": _config(), "design": _config(0.7)},
                                           f"run_06{int(gate_present)}_generated.json")
        _set_flags(**flags)
        if not gate_present:
            monkeypatch.setattr(rpr, "_gate_config_direct_variants", lambda *a: None)
        index_path = run_dir / "artifacts" / "variants" / "index.yaml"
        before = index_path.read_bytes()
        outs.append(rpr._route_post_config_direct_backtest_specification(run_dir))
        assert index_path.read_bytes() == before
        assert not (run_dir / "artifacts" / "variant_anti_adjacency_result.yaml").exists()
    assert outs == ["protocol_execution", "protocol_execution"]


def test_register_and_config_keep_the_gate_off():
    reg = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))
    entry = next(f for f in reg["flags"] if f["name"] == "variant_anti_adjacency_gate")
    assert entry["state"] == "off_incomplete"
    assert "S2b" in entry["blocked_on"]
    cfg = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["variant_anti_adjacency_gate"]["enabled"] is False



# ---------------------------------------------------------------------------
# Code-review fixes (E-036 S2a review)
# ---------------------------------------------------------------------------

def test_forecast_hash_is_the_trial_rows_canonicalisation(tmp_path):
    """One canonicalisation: novelty.forecast_hash_of_config ==
    run_phase1_research._compute_forecast_hash == decide_next.config_sha256."""
    cfg = _config(0.3)
    path = _write_json(tmp_path / "c.json", cfg)
    assert (rpr._compute_forecast_hash(path) == nov.forecast_hash_of_config(cfg)
            == dn.config_sha256(cfg)
            == hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest())


def test_decide_next_legacy_true_entry_no_longer_refuses():
    """Review fix 5: the intended decide_next exact-match change -- a memory
    entry marked legacy: true never makes a candidate a REPEAT."""
    import test_e059_s2a_decide_next as t
    p = t._patch("profitability-run_061-1", after=0.8)
    inputs = t._one_source([p])
    inputs["memory"]["runs"]["run_050"] = t._memory_entry(
        "run_050", fh=dn.config_sha256(t._base_config(min_abs=0.8)))
    c = t._by_id(t._decide(inputs))["profitability-run_061-1"]
    assert c["gates"]["novelty"]["exact_match"] == "REPEAT"   # same entry, not legacy
    inputs["memory"]["runs"]["run_050"]["legacy"] = True
    c = t._by_id(t._decide(inputs))["profitability-run_061-1"]
    assert c["gates"]["novelty"]["exact_match"] == "NOVEL" and c["eligible"] is True


def test_memory_protocol_unreadable_degrades_with_a_warning_candidate_fails_loud():
    """Review fix 4."""
    bad = rpr.ROOT / "protocols" / "bad.json"
    bad.parent.mkdir(parents=True, exist_ok=True)
    bad.write_text("{not json", encoding="utf-8")
    _protocol("p.json")
    warnings = []
    assert nov.protocol_spec(rpr.ROOT, "protocols/bad.json", warnings=warnings) is None
    assert warnings and warnings[0]["protocol_ref"] == "protocols/bad.json"
    with pytest.raises(nov.NoveltyError):
        nov.protocol_spec(rpr.ROOT, "protocols/bad.json", strict=True)
    with pytest.raises(nov.NoveltyError):
        nov.protocol_spec(rpr.ROOT, "protocols/missing.json", strict=True)
    # a memory entry on the bad protocol can never match a resolved candidate
    memory = _mem(_entry("run_001", ref="protocols/bad.json"))
    specs = nov.protocol_specs(rpr.ROOT, memory, extra_refs=["protocols/p.json"])
    key = nov.novelty_key("fh-1", ["BTCUSDT"], {"protocol_ref": "protocols/p.json"}, specs)
    assert nov.lookup(key, memory, specs) == "NOVEL"


def test_tried_ideas_prompt_survives_one_bad_old_protocol():
    """Review fix 4: the prompt path lists the problem, it does not crash."""
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json")
    (rpr.ROOT / "protocols" / "run_050_generated.json").write_text("{broken", encoding="utf-8")
    _set_flags(exclusion_digest_input=True)
    run_dir = _minimal_run(rpr.ROOT, "run_061")
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_exclusion_digest_input("hypothesis_generation", handoff, run_dir)
    view = rpr.load_yaml(run_dir / "artifacts" / "tried_ideas.yaml")
    assert view["runs"][0]["timeframe"] == "1h"  # the card timeframe fallback
    assert view["warnings"][0]["protocol_ref"] == "protocols/run_050_generated.json"


def test_candidate_with_a_malformed_own_protocol_fails_loud():
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json")
    run_dir = _legacy_candidate("run_061", _config(), "run_061_generated.json")
    (rpr.ROOT / "protocols" / "run_061_generated.json").write_text(
        json.dumps({"symbols": ["BTCUSDT"], "timeframe": "1h"}), encoding="utf-8")  # no windows
    _set_flags(variant_selection_record=True, variant_anti_adjacency_gate=True)
    with pytest.raises(nov.NoveltyError, match="windows"):
        rpr._route_post_variant_selection(run_dir, "run_061")


def test_advisory_and_index_are_built_once_per_run(monkeypatch):
    """Review fixes 6 + 7: three variants, one KB advisory, one index."""
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json",
                         variant_loop=True)
    run_dir = _config_direct_candidate(
        "run_061", {"base": _config(0.6), "design": _config(0.7), "asset": _config(0.9)},
        "run_061_generated.json")
    _set_flags(**_CD_ON)
    calls = {"adv": 0, "idx": 0}
    real_adv, real_idx = aag.layer1_advisory, nov.match_index

    def _adv(*a, **k):
        calls["adv"] += 1
        return real_adv(*a, **k)

    def _idx(*a, **k):
        calls["idx"] += 1
        return real_idx(*a, **k)
    monkeypatch.setattr(aag, "layer1_advisory", _adv)
    monkeypatch.setattr(nov, "match_index", _idx)
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "protocol_execution"
    assert calls == {"adv": 1, "idx": 1}
    res = rpr.load_yaml(run_dir / "artifacts" / "variant_anti_adjacency_result.yaml")
    assert sorted(res["variants"]) == ["asset", "base", "design"]


def test_composition_runs_are_never_gated(monkeypatch):
    """Review fix 3: a composite gets no novelty gate (E-060 S3b design)."""
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json",
                         variant_loop=True)
    run_dir = _config_direct_candidate("run_061", {"base": _config(), "design": _config(0.7)},
                                       "run_061_generated.json")
    _set_flags(**_CD_ON)
    monkeypatch.setattr(rpr, "_composition_mode", lambda d: True)
    before = (run_dir / "artifacts" / "variants" / "index.yaml").read_bytes()
    assert rpr._gate_config_direct_variants(run_dir, "run_061") is None
    assert (run_dir / "artifacts" / "variants" / "index.yaml").read_bytes() == before
    assert not (run_dir / "artifacts" / "variant_anti_adjacency_result.yaml").exists()


def test_cli_accepts_a_yaml_protocol_and_derives_the_same_key(tmp_path, monkeypatch):
    """Review fix 9: the CLI keys a candidate exactly as the 5a gate does."""
    _prior_run_in_memory("run_050", _config(), protocol_name="run_050_generated.json")
    proto = rpr.ROOT / "protocols" / "cand.yaml"
    proto.write_text(yaml.safe_dump({"symbols": SYMBOLS, "timeframe": "1h", "windows": WINDOWS}),
                     encoding="utf-8")
    cfg = _write_json(tmp_path / "cfg.json", _config())
    monkeypatch.setattr(aag, "_SR", rpr.ROOT)
    out = tmp_path / "res.yaml"
    rc = aag.main([str(cfg), str(proto), "--memory", str(_memory_path()),
                   "--kb", str(tmp_path / "nokb.yaml"), "--out", str(out)])
    assert rc == 1
    res = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert res["matched"] == [{"run_id": "run_050", "variant_id": "run_050"}]


# --- review fix 2: a repeat skip is never a data shortfall --------------------

class _StopAtProtocolExecution(Exception):
    pass


def _data_gate_run(monkeypatch, run_id, variants: dict, retired: bool):
    import test_e059_6c_s2c_parked_states as ps
    from test_e033_slice4b_gate_conformance_promotion import (_minimal_run_at,
                                                              _play_seeded_stage)

    async def _invoke(stage_name, rid, retry_context=None):
        if stage_name == "protocol_execution":
            raise _StopAtProtocolExecution("reached protocol_execution")
        # E-061 C1.2: the seeded gate outputs, as written by this attempt.
        _play_seeded_stage(rpr.ROOT / "runs" / rid, stage_name)
    monkeypatch.setattr(rpr, "async_invoke_agent", _invoke)
    monkeypatch.setattr(rpr, "_check_specialist_readers_preflight", lambda run_dir: None)
    cfg = {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}}
    if retired:
        cfg = {**ps.RETIRED_ON, **cfg}
    ps._set_flag(rpr.ROOT, cfg)
    run_dir = _minimal_run_at(rpr.ROOT, run_id, "data_availability_gate")
    ps._write_handoff(run_dir, "backtest_spec_to_data_availability_gate.yaml")
    ps._write_handoff(run_dir, "backtest_spec_to_protocol_execution.yaml")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": variants})
    return run_dir


def _repeat_nt():
    return {"status": "not_tested", "reason": "repeat: exact match of tested variant(s) "
            "['run_050:base'] in campaign_record/campaign_memory.yaml",
            "config_path": "artifacts/variants/x/strategy_config.json"}


@pytest.mark.parametrize("retired", [True, False])
def test_four_variants_two_repeats_proceed_past_the_data_gate(monkeypatch, retired):
    import test_e059_6c_s2c_parked_states as ps
    variants = {"base": ps._ok(), "design": ps._ok(), "asset": _repeat_nt(), "extra": _repeat_nt()}
    run_dir = _data_gate_run(monkeypatch, "run_970", variants, retired)
    rpr.run_loop("run_970")
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["pending_stage"] == "protocol_execution"  # reached, then the stub stopped it
    assert "variant_gate_insufficient" not in (state.get("flags") or {})
    assert rpr.PARKED_KEY not in state


def test_one_repeat_and_two_fetchable_declines_park_waiting_for_data(monkeypatch):
    import test_e059_6c_s2c_parked_states as ps
    variants = {"base": ps._ok(), "asset": _repeat_nt(),
                "design_v2": ps._nt(ps.DATA), "asset_v2": ps._nt(ps.DATA)}
    run_dir = _data_gate_run(monkeypatch, "run_971", variants, retired=True)
    ps._write_variant_gate(run_dir, "design_v2")
    ps._write_variant_gate(run_dir, "asset_v2")
    rpr.run_loop("run_971")
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "paused_for_human"
    assert "variant_gate_insufficient" not in (state.get("flags") or {})
    marker = state[rpr.PARKED_KEY]
    assert marker["kind"] == "data" and "need >= 3" in marker["reason"]


def test_park_kind_ignores_repeat_skips():
    import test_e059_6c_s2c_parked_states as ps
    assert rpr._variant_park_kind({"a": _repeat_nt()}) == (None, [])
    assert rpr._variant_park_kind({"a": _repeat_nt(), "b": ps._nt("patch application failed: x")}) \
        == (None, [])  # the patch failure is still "other"
