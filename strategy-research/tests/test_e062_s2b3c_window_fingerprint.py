"""
E-062 S2b-3c -- the repeat key and the DSR dedupe key carry a partial-coverage
variant's own window fingerprint (engineering/DECISION_LOG.md D-047 (5);
engineering/roadmap/E-062/S2B3_FINDINGS.md Q5, X4, Q8 row S2b-3c, G11, G12;
Linear CUL-344 item 4).

Covers:
  1. The fingerprint: novelty.windows_fingerprint is protocol_spec's window
     hash (one space); novelty_key without it is byte-identical, with it the
     window set is the variant's own; an unresolved protocol never matches.
  2. The DSR dedupe (both lockstep paths): a wider-coverage retest of the same
     config on the same coin is a separate trial (N + 1), the same coverage
     still collapses, a fingerprinted row never collapses onto a row without
     one, a malformed fingerprint raises; ledgers without the field dedupe
     exactly as the pre-S2b-3c key; the committed ledger's N is unchanged.
  3. Trial rows: the recorders add `windows_sha256` only when given;
     protocol_execution writes it for a partial variant only, only under
     orchestrator.profit_bars_v2; an unmeasurable fingerprint refuses THAT
     variant before any backtest.
  4. Campaign memory copies it from the trial row (optional schema field);
     a row without it gives exactly the pre-S2b-3c variant keys.
  5. The repeat gate (5a): same coverage REPEAT, wider NOVEL, full after
     partial NOVEL; a full-coverage key byte-identical; flag off unchanged.
  6. Branch 3: the wider-coverage retest gets its own DSR (no
     `dedup_collapse`), N + 1; the same coverage still reads dedup_collapse.
The cross-copy lockstep (every dedupe copy on mixed rows) is an extension of
tests/test_dedup_predicate_lockstep.py (declared there).
"""
import asyncio
import json
import random
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import campaign_memory as cm  # noqa: E402
import deflate_sharpe as ds  # noqa: E402
import novelty as nov  # noqa: E402
import variant_coin as vc  # noqa: E402

import test_e036_s2a_exact_match_gate as t36  # noqa: E402
import test_e061_c2_s2b_one_coin_per_variant as c2  # noqa: E402
from test_k3_protocol_pinning import _minimal_run  # noqa: E402

DEDUPES = (ds.deduplicate_trials, rpr._dedupe_trials)
WINDOWS4 = c2._months("2021-01", 4)  # 2021-01 .. 2021-04
LABELS = [w["label"] for w in WINDOWS4]


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _fp(labels) -> str:
    """The fingerprint of the run protocol's windows restricted to `labels`."""
    return nov.windows_fingerprint([w for w in WINDOWS4 if w["label"] in labels])


def _pre_s2b3c_dedupe(rows):
    """The pre-S2b-3c key, (forecast_hash, sorted symbols or None, source), for
    ledgers without reproduces_trial -- the reference 'exactly as before'."""
    seen, kept = set(), []
    for r in rows:
        fh = r.get("forecast_hash")
        if fh is None:
            kept.append(r)
            continue
        syms = r.get("symbols")
        key = (fh, tuple(sorted(syms)) if "symbols" in r else None, r.get("source"))
        if key not in seen:
            seen.add(key)
            kept.append(r)
    return kept, len(rows) - len(kept)


def _row(tid, fh="h", source="backtest", **kw):
    return {"trial_id": tid, "source": source, "sharpe": 0.1, "statistic_valid": "sharpe",
            "forecast_hash": fh, **kw}


# ---------------------------------------------------------------------------
# 1. The fingerprint and the novelty key
# ---------------------------------------------------------------------------

def test_fingerprint_is_protocol_specs_window_hash():
    proto = t36._protocol("fp.json", windows=WINDOWS4)
    spec = nov.protocol_spec(rpr.ROOT, "protocols/fp.json", strict=True)
    assert proto.exists() and nov.windows_fingerprint(WINDOWS4) == spec["windows_sha256"]
    assert _fp(LABELS[1:]) != _fp(LABELS) != _fp(LABELS[2:])
    for bad in (None, [], {}, "w"):
        with pytest.raises(nov.NoveltyError, match="non-empty `windows` list"):
            nov.windows_fingerprint(bad)


def test_novelty_key_is_byte_identical_without_a_fingerprint_and_uses_it_when_given():
    t36._protocol("p.json", windows=WINDOWS4)
    specs = t36._specs(rpr.ROOT)
    entry = {"protocol_ref": "protocols/p.json"}
    old = nov.novelty_key("fh", ["XRPUSD"], entry, specs)
    assert old == ("fh", ("XRPUSD",), "1h", f"windows:{_fp(LABELS)}")
    assert nov.novelty_key("fh", ["XRPUSD"], entry, specs, windows_sha256=None) == old
    own = nov.novelty_key("fh", ["XRPUSD"], entry, specs, windows_sha256=_fp(LABELS[1:]))
    assert own == ("fh", ("XRPUSD",), "1h", f"windows:{_fp(LABELS[1:])}")
    # the full window set as a fingerprint IS the protocol's own key (one space)
    assert nov.novelty_key("fh", ["XRPUSD"], entry, specs, windows_sha256=_fp(LABELS)) == old
    # an unresolved protocol never matches, fingerprint or not
    unresolved = nov.novelty_key("fh", ["XRPUSD"], {"protocol_ref": "protocols/gone.json",
                                                    "timeframe": "1h"}, {},
                                 windows_sha256=_fp(LABELS[1:]))
    assert unresolved[3] == "unresolved:protocols/gone.json"
    for bad in ("", "ABC", "a" * 63, 7, "G" * 64):
        with pytest.raises(nov.NoveltyError, match="windows_sha256"):
            nov.novelty_key("fh", ["XRPUSD"], entry, specs, windows_sha256=bad)


def test_match_index_keys_old_entries_exactly_as_before_and_new_ones_on_their_fingerprint():
    t36._protocol("p.json", windows=WINDOWS4)
    specs = t36._specs(rpr.ROOT)
    old = t36._entry("run_001", fh="fh-1", symbols=("XRPUSD",))
    new = t36._entry("run_002", fh="fh-1", symbols=("XRPUSD",))
    new["variants"]["run_002"]["windows_sha256"] = _fp(LABELS[2:])
    index = nov.match_index(t36._mem(old, new), specs)
    assert index == {
        ("fh-1", ("XRPUSD",), "1h", f"windows:{_fp(LABELS)}"): [
            {"run_id": "run_001", "variant_id": "run_001"}],
        ("fh-1", ("XRPUSD",), "1h", f"windows:{_fp(LABELS[2:])}"): [
            {"run_id": "run_002", "variant_id": "run_002"}]}
    # the old entry's key is what the pre-extraction decide_next code built
    assert t36._old_decide_next_exact_index(t36._mem(old), specs) == \
        nov.exact_index(t36._mem(old), specs)


# ---------------------------------------------------------------------------
# 2. The DSR dedupe (both lockstep paths)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("dedupe", DEDUPES)
def test_wider_coverage_retest_is_a_new_trial_same_coverage_still_collapses(dedupe):
    part = _row("r1:asset", symbols=["XRPUSD"], windows_sha256=_fp(LABELS[2:]))
    wider = _row("r2:asset", symbols=["XRPUSD"], windows_sha256=_fp(LABELS[1:]))
    same = _row("r3:asset", symbols=["XRPUSD"], windows_sha256=_fp(LABELS[2:]))
    kept, removed = dedupe([part, wider])
    assert [r["trial_id"] for r in kept] == ["r1:asset", "r2:asset"] and removed == 0
    kept, removed = dedupe([part, wider, same])
    assert [r["trial_id"] for r in kept] == ["r1:asset", "r2:asset"] and removed == 1
    # a fingerprinted row never collapses onto a row without one (N over-counts)
    full = _row("r4:asset", symbols=["XRPUSD"])
    kept, removed = dedupe([full, part])
    assert len(kept) == 2 and removed == 0
    # nor across sources, nor across coins
    assert len(dedupe([part, {**part, "trial_id": "x", "symbols": ["SOLUSDT"]},
                       {**part, "trial_id": "y", "source": "backtest_failed"}])[0]) == 3


@pytest.mark.parametrize("dedupe", DEDUPES)
@pytest.mark.parametrize("bad", [None, "", "abc", "A" * 64, 5, ["x"]])
def test_malformed_fingerprint_fails_loud_on_both_paths(dedupe, bad):
    with pytest.raises(ValueError, match="windows_sha256"):
        dedupe([_row("r:asset", symbols=["XRPUSD"], windows_sha256=bad)])


@pytest.mark.parametrize("seed", range(5))
def test_ledgers_without_the_field_dedupe_exactly_as_before_on_both_paths(seed):
    rng = random.Random(seed)
    rows = []
    for i in range(80):
        extra = {"symbols": [rng.choice(["BTCUSDT", "XRPUSD"])]} if rng.random() < 0.5 else {}
        rows.append(_row(f"t{i}", fh=rng.choice(["a", "b", "c", None, "", 0]),
                         source=rng.choice(["backtest", "prescreen", "backtest_failed"]),
                         **extra))
    ref = _pre_s2b3c_dedupe(rows)
    for dedupe in DEDUPES:
        assert dedupe(rows) == ref


@pytest.mark.real_repo_readonly
def test_the_committed_ledger_n_is_unchanged():
    """Read-only. The committed ledger carries no fingerprint, so every dedupe
    copy returns the pre-S2b-3c partition: N is unchanged."""
    state = yaml.safe_load((SR_ROOT / "campaign_record" / "campaign_state.yaml")
                           .read_text(encoding="utf-8"))
    rows = state.get("trial_sharpes") or []
    assert not any("windows_sha256" in r for r in rows)
    valid, _ = ds.exclude_invalidated_trials(rows)
    assert not any(r.get("reproduces_trial") for r in valid)
    ref_n = len(_pre_s2b3c_dedupe(valid)[0])
    for dedupe in DEDUPES:
        assert dedupe(valid) == _pre_s2b3c_dedupe(valid)
    assert ds.select_same_basis_sample(rows)["N"] == ref_n
    assert ds.compute_promotion_audit(hypothesis_id="h", candidate_sr=0.1,
                                      campaign_state={"trial_sharpes": rows},
                                      n_trades=100)["total_hypotheses_tested"] == ref_n


# ---------------------------------------------------------------------------
# 3. Trial rows
# ---------------------------------------------------------------------------

def _cfg(tmp_path) -> Path:
    cfg = tmp_path / "c.json"
    cfg.write_text(json.dumps(c2._BASE_CONFIG), encoding="utf-8")
    return cfg


def test_trial_recorders_add_the_fingerprint_only_when_given(tmp_path):
    cfg = _cfg(tmp_path)
    summary = {"per_symbol_summary": {"XRPUSD": {"median_sharpe": 0.2}}, "results": []}
    fp = _fp(LABELS[1:])
    rpr._record_backtest_trial("run_930", summary, cfg, trial_id="run_930:base",
                               symbols=["BTCUSDT"])
    rpr._record_backtest_trial("run_930", summary, cfg, trial_id="run_930:asset",
                               symbols=["XRPUSD"], windows_sha256=fp)
    rpr._record_failed_backtest_trial("run_931", cfg, "boom", trial_id="run_931:asset",
                                      symbols=["XRPUSD"], windows_sha256=fp)
    rpr._record_failed_backtest_trial("run_931", cfg, "boom", trial_id="run_931:base")
    rows = {(r["trial_id"], r["source"]): r for r in rpr.load_campaign_state()["trial_sharpes"]}
    assert rows[("run_930:asset", "backtest")]["windows_sha256"] == fp
    assert rows[("run_931:asset", "backtest_failed")]["windows_sha256"] == fp
    assert "windows_sha256" not in rows[("run_930:base", "backtest")]
    assert "windows_sha256" not in rows[("run_931:base", "backtest_failed")]
    assert list(rows[("run_930:base", "backtest")]) == [
        "trial_id", "source", "sharpe", "expectancy_bps", "n_trades", "statistic_valid",
        "below_floor_pct", "forecast_hash", "symbols"]  # the pre-S2b-3c keys, in order
    with pytest.raises(ValueError, match="windows_sha256"):
        rpr._record_backtest_trial("run_932", summary, cfg, windows_sha256="nope")


def _partial_pe_run(monkeypatch, run_id):
    c2._set_flags(config_direct_authoring=True, variant_loop=True)
    windows, universe, layer1 = c2._partial_asset_world()
    run_dir, _ = c2._stage_index(run_id, per_coin=True, monkeypatch=monkeypatch,
                                 windows=windows, universe=universe, layer1=layer1)
    return run_dir


@pytest.mark.parametrize("v2", [False, True])
def test_protocol_execution_writes_the_fingerprint_for_a_partial_variant_only_under_v2(
        monkeypatch, v2):
    run_dir = _partial_pe_run(monkeypatch, f"run_95{int(v2)}")
    monkeypatch.setattr(rpr, "_profit_bars_v2_enabled", lambda cfg=None: v2)
    calls: list = []
    c2._tool_stub(monkeypatch, calls)
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_dir.name))
    assert c2._pe_ran(calls) == {"asset", "base", "design"}
    rows = {r["trial_id"]: r for r in rpr.load_campaign_state()["trial_sharpes"]}
    for vid in ("base", "design"):
        assert "windows_sha256" not in rows[f"{run_dir.name}:{vid}"]  # full coverage
    asset = rows[f"{run_dir.name}:asset"]
    if v2:
        own = json.loads((run_dir / "artifacts" / "variants" / "asset" / "protocol.json")
                         .read_text(encoding="utf-8"))["windows"]
        assert len(own) == 10 and asset["windows_sha256"] == nov.windows_fingerprint(own)
    else:
        assert "windows_sha256" not in asset  # flag off: the row byte-identical in keys


@pytest.mark.parametrize("damage", ["delete_frozen", "alter_own"])
def test_an_unmeasurable_fingerprint_refuses_only_that_variant_before_any_backtest(
        monkeypatch, damage):
    run_dir = _partial_pe_run(monkeypatch, "run_953")
    arts = run_dir / "artifacts"
    if damage == "delete_frozen":
        (run_dir / rpr.RUN_PROTOCOL_FROZEN_REL).unlink()
    else:  # a partial index whose protocol.json has the run protocol's windows
        index = rpr.load_yaml(arts / "variants" / "index.yaml")
        full = json.loads((run_dir / rpr.RUN_PROTOCOL_FROZEN_REL).read_text(encoding="utf-8"))
        assert vc.is_partial_coverage(index["variants"]["asset"])
        monkeypatch.setattr(rpr, "_per_coin_protocol_check",
                            lambda *a, **k: ([], ["XRPUSD"]))  # past M2, onto the fingerprint
        raw = json.dumps({**full, "symbols": ["XRPUSD"]}, indent=2).encode("utf-8")
        (arts / "variants" / "asset" / "protocol.json").write_bytes(raw)
        index["variants"]["asset"]["protocol_sha256"] = vc.protocol_sha256(raw)
        rpr.save_yaml(arts / "variants" / "index.yaml", index)
    monkeypatch.setattr(rpr, "_profit_bars_v2_enabled", lambda cfg=None: True)
    calls: list = []
    c2._tool_stub(monkeypatch, calls)
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_dir.name))
    assert c2._pe_ran(calls) == {"base", "design"}
    assert c2._run_trial_ids(run_dir.name) == [f"{run_dir.name}:base", f"{run_dir.name}:design"]
    a = rpr.load_yaml(arts / "variants" / "index.yaml")["variants"]["asset"]
    assert a["status"] == "not_tested" and a["failed_attempt"].startswith("refused:")


# ---------------------------------------------------------------------------
# 4. Campaign memory
# ---------------------------------------------------------------------------

def _prior_partial_run(run_id, config, *, windows_sha256, protocol_name="prior.json",
                       coin="XRPUSD"):
    """A finished per-coin run whose asset ran on part of the run protocol,
    recorded through the REAL writers: the trial row by _record_backtest_trial
    (symbols + fingerprint as protocol_execution passes them) and the memory
    entry by campaign_memory.build_memory_entry + upsert_memory."""
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    proto = t36._protocol(protocol_name, windows=WINDOWS4)
    rpr.save_yaml(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-PRIOR", "timeframe": "1h"})
    cfg_path = t36._write_json(arts / "variants" / "asset" / "strategy_config.json", config)
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {"asset": {
        "status": "validated", "config_path": "artifacts/variants/asset/strategy_config.json"}}})
    rpr._record_backtest_trial(run_id, {"per_symbol_summary": {}, "results": []}, cfg_path,
                               trial_id=f"{run_id}:asset", symbols=[coin],
                               windows_sha256=windows_sha256)
    pr = {"verdict": "kill", "protocol_file": str(proto),
          "results": [{"symbol": coin, "window": w["label"]} for w in WINDOWS4]}
    rpr.save_yaml(arts / "variants" / "asset" / "protocol_result.yaml", pr)
    rpr.save_yaml(arts / "protocol_result.yaml", pr)
    grid = t36._grid(run_id, ["asset"])
    rpr.save_yaml(arts / "grid_evaluation.yaml", grid)
    rpr.save_yaml(arts / "idea_status.yaml", rpr._build_idea_status_artifact(grid, run_id))
    entry = cm.build_memory_entry(run_dir, run_id,
                                  trial_sharpes=rpr.load_campaign_state().get("trial_sharpes"),
                                  categories=[], protocol_root=rpr.ROOT)
    cm.upsert_memory(t36._memory_path(), entry)
    return entry


def test_memory_copies_the_fingerprint_from_the_trial_row_and_the_schema_accepts_it():
    import jsonschema
    fp = _fp(LABELS[2:])
    entry = _prior_partial_run("run_040", t36._config(), windows_sha256=fp)
    assert entry["variants"]["asset"]["windows_sha256"] == fp
    plain = _prior_partial_run("run_041", t36._config(0.7), windows_sha256=None)
    assert list(plain["variants"]["asset"]) == ["status", "reason", "config_ref",
                                                "forecast_hash", "symbols", "n_windows",
                                                "trial_id"]  # the pre-S2b-3c keys
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas" /
                         "campaign_memory.schema.json").read_text(encoding="utf-8"))
    memory = yaml.safe_load(t36._memory_path().read_text(encoding="utf-8"))
    jsonschema.validate(memory, schema)
    memory["runs"]["run_040"]["variants"]["asset"]["windows_sha256"] = "not-a-sha"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(memory, schema)


def test_memory_refuses_a_malformed_fingerprint_on_the_trial_row():
    state = {"campaign_id": "t", "runs": [], "trial_sharpes": []}
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, state)
    _prior_partial_run("run_042", t36._config(), windows_sha256=_fp(LABELS[1:]))
    state = rpr.load_yaml(rpr.CAMPAIGN_STATE_PATH)
    for r in state["trial_sharpes"]:
        r["windows_sha256"] = "bad"
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, state)
    with pytest.raises(cm.CampaignMemoryError, match="windows_sha256"):
        cm.build_memory_entry(rpr.ROOT / "runs" / "run_042", "run_042",
                              trial_sharpes=state["trial_sharpes"], categories=[],
                              protocol_root=rpr.ROOT)


# ---------------------------------------------------------------------------
# 5. The repeat gate (5a)
# ---------------------------------------------------------------------------

def _candidate(run_id, config, covered: list | None, coin="XRPUSD",
               protocol_name="cand.json") -> Path:
    """A config-direct per-coin run after 5a: base (BTCUSDT, every window) and
    asset (`coin`, the `covered` window labels, None = every window), with 5a's
    frozen run protocol, protocol.json files, their sha256 and the coverage."""
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-CD", "timeframe": "1h"})
    t36._protocol(protocol_name, windows=WINDOWS4)
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": f"protocols/{protocol_name}"})
    source, run_sha = rpr._freeze_run_protocol(run_dir, run_id)
    index = {}
    for vid, sym, wr in (("base", "BTCUSDT", None), ("asset", coin, covered)):
        t36._write_json(arts / "variants" / vid / "strategy_config.json", config)
        if vid == "base":
            t36._write_json(arts / "candidate_strategy_config.json", config)
        raw = json.dumps(vc.variant_protocol(source, symbol=sym, windows_run=wr),
                         indent=2).encode("utf-8")
        (arts / "variants" / vid / "protocol.json").write_bytes(raw)
        index[vid] = {"status": "validated",
                      "config_path": f"artifacts/variants/{vid}/strategy_config.json",
                      "kind": vid, "symbol": sym,
                      "protocol_path": f"artifacts/variants/{vid}/protocol.json",
                      "protocol_sha256": vc.protocol_sha256(raw), rpr.RUN_PROTOCOL_SHA_KEY: run_sha}
        if vid == "asset":
            index[vid]["coverage"] = {"windows_run": list(wr or LABELS),
                                      "windows_total": len(LABELS)}
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": index})
    return run_dir


def _gate(monkeypatch, run_dir, *, v2=True) -> dict:
    t36._set_flags(**t36._CD_ON)
    monkeypatch.setattr(rpr, "_profit_bars_v2_enabled", lambda cfg=None: v2)
    rpr._gate_config_direct_variants(run_dir, run_dir.name)
    return rpr.load_yaml(run_dir / "artifacts" / "variant_anti_adjacency_result.yaml")


@pytest.mark.parametrize("covered,route", [
    (LABELS[2:], "refuse"),   # same coverage: still a repeat
    (LABELS[1:], "admit"),    # wider coverage: a new trial
    (None, "admit"),          # full coverage after partial: a new trial
])
def test_repeat_gate_same_coverage_repeats_wider_or_full_is_novel(monkeypatch, covered, route):
    cfg = t36._config()
    _prior_partial_run("run_050", cfg, windows_sha256=_fp(LABELS[2:]))
    run_dir = _candidate("run_061", cfg, covered)
    res = _gate(monkeypatch, run_dir)
    assert res["variants"]["asset"]["route"] == route
    want = _fp(covered) if covered else _fp(LABELS)
    assert res["variants"]["asset"]["key"]["window_set"] == f"windows:{want}"
    assert res["repeats"] == (["asset"] if route == "refuse" else [])


def test_full_coverage_keys_are_byte_identical_flag_on_and_off(monkeypatch):
    cfg = t36._config()
    _prior_partial_run("run_050", t36._config(0.9), windows_sha256=_fp(LABELS[2:]))
    run_dir = _candidate("run_062", cfg, None)
    on = _gate(monkeypatch, run_dir, v2=True)
    off = _gate(monkeypatch, run_dir, v2=False)
    assert on["variants"] == off["variants"]
    assert on["variants"]["asset"]["key"]["window_set"] == f"windows:{_fp(LABELS)}"


def test_flag_off_a_partial_variant_keys_on_the_run_protocol_as_before(monkeypatch):
    cfg = t36._config()
    # the same config / coin / coverage already tested flag-on: flag off, the
    # candidate keys on the run protocol's windows exactly as before S2b-3c
    _prior_partial_run("run_050", cfg, windows_sha256=_fp(LABELS[2:]))
    run_dir = _candidate("run_063", cfg, LABELS[2:])
    called = []
    monkeypatch.setattr(rpr, "_variant_window_fingerprint",
                        lambda *a, **k: called.append(a) or "x")
    off = _gate(monkeypatch, run_dir, v2=False)
    assert called == []  # never computed flag-off
    assert off["variants"]["asset"]["key"]["window_set"] == f"windows:{_fp(LABELS)}"


def test_repeat_gate_refuses_only_the_variant_whose_fingerprint_is_unmeasurable(monkeypatch):
    cfg = t36._config()
    _prior_partial_run("run_050", t36._config(0.9), windows_sha256=_fp(LABELS[2:]))
    run_dir = _candidate("run_064", cfg, LABELS[1:])
    (run_dir / rpr.RUN_PROTOCOL_FROZEN_REL).write_text("{}", encoding="utf-8")  # altered
    res = _gate(monkeypatch, run_dir)
    assert res["refused"] == ["asset"] and res["variants"]["base"]["route"] == "admit"
    after = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]
    assert after["asset"]["status"] == "not_tested"
    assert after["asset"]["reason"].startswith(vc.COIN_REASON_PREFIX)
    assert "frozen run protocol" in after["asset"]["reason"]


# ---------------------------------------------------------------------------
# 6. Branch 3: the retest's own DSR
# ---------------------------------------------------------------------------

def _retest_evaluation(monkeypatch, prior_fp):
    """S2b-3b's graded 60%-coverage asset (run_053's last 58 windows) whose
    ledger row carries its fingerprint, after an earlier trial of the same
    config on the same coin with fingerprint `prior_fp`."""
    import test_e062_s2b3b_normalisation_wiring as t3b
    import test_e062_s2b2b_dsr_wiring as t2b
    run_dir = t3b._partial_run(monkeypatch)
    arts = run_dir / "artifacts"
    own = json.loads((arts / "variants" / "asset" / "protocol.json")
                     .read_text(encoding="utf-8"))["windows"]
    own_fp = nov.windows_fingerprint(own)
    tid = f"{t3b.RUN_ID}:asset"

    def edit(rows):
        mine = next(r for r in rows if r["trial_id"] == tid and r["source"] == "backtest")
        mine.update(symbols=["SOLUSDT"], windows_sha256=own_fp)
        rows.insert(0, {"trial_id": "run_100:asset", "source": "backtest",
                        "statistic_valid": "sharpe", "sharpe": 0.2,
                        "forecast_hash": mine["forecast_hash"], "symbols": ["SOLUSDT"],
                        "whole_test": t2b._block(0.04),
                        **({"windows_sha256": prior_fp(own_fp)} if prior_fp else {})})
    t2b._edit_rows(edit)
    return t3b._evaluate(run_dir), t3b, own_fp


def test_wider_coverage_retest_gets_its_own_dsr_and_n_grows_by_one(monkeypatch):
    narrower = "0" * 64  # the earlier, narrower coverage's fingerprint
    ev, t3b, _ = _retest_evaluation(monkeypatch, lambda own: narrower)
    row = t3b._rows(ev)["deflated_sharpe_threshold"]
    assert row["result"] != "NOT_EVALUABLE" and isinstance(row["actual"], float), row
    n_total = ev["dsr_basis"]["n_dsr_total"]
    assert row["detail"]["N"] == n_total
    # N counts both trials: one more than the same ledger with the retest collapsed
    rows = rpr.load_campaign_state()["trial_sharpes"]
    stripped = [{k: v for k, v in r.items() if k != "windows_sha256"} for r in rows]
    assert len(ds.deduplicate_trials(stripped)[0]) + 1 == n_total
    assert rpr._promotion_dsr_context()["n_dsr_total"] == n_total


def test_same_coverage_retest_still_reads_dedup_collapse(monkeypatch):
    ev, t3b, _ = _retest_evaluation(monkeypatch, lambda own: own)
    row = t3b._rows(ev)["deflated_sharpe_threshold"]
    assert row["result"] == "NOT_EVALUABLE" and "dedup_collapse" in row["not_evaluable_reason"]
    assert "'run_100:asset'" in row["not_evaluable_reason"]


def test_an_earlier_full_coverage_row_never_absorbs_the_partial_retest(monkeypatch):
    """No fingerprint on the earlier row (full coverage, or written flag-off):
    the partial row is a separate trial -- the conservative direction."""
    ev, t3b, _ = _retest_evaluation(monkeypatch, None)
    row = t3b._rows(ev)["deflated_sharpe_threshold"]
    assert row["result"] != "NOT_EVALUABLE", row
