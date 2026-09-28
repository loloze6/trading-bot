"""
E-061 C2 S2b -- one coin per variant (C2_S1_FINDINGS.md G1-G6; DECISION_LOG
D-016, D-042) and Linear CUL-342 items 1-2.

Covers:
  1. tools/variant_coin.py: per-coin mode, the venue symbol, base/design on the
     base coin, the asset coin (other category, empty patch), D-042's coverage
     rule on the Layer-1 precheck (full, partial >= 60% and >= 2 eras, below
     the share, one era only), the derivation check.
  2. 5a (run_tool_worker backtest_specification) under variant_loop writes one
     protocol.json per variant + index kind/symbol/protocol_path/coverage; a
     coverage-skipped asset is not_tested and never blocks the others.
  3. Flag-off byte identity: variant_loop off (kind/symbol ignored) and a
     legacy variant_patches.yaml under the loop write the same index bytes and
     no protocol.json; the protocol_execution argv and trial rows unchanged.
  4. The data gate and run_protocol.py receive the variant's own protocol;
     per-coin trial rows carry `symbols`.
  5. G6: the DSR dedupe keys on the coin on BOTH paths (lockstep); a row
     without `symbols` dedupes exactly as the pre-S2b key did.
  6. Repeat gate keyed on the variant's coin; residual IC one composite per
     coin group; per-coin conformance.
  7. The data-gate floor and park kind ignore a coverage skip.
  8. CUL-342 item 1 (variant_loop off: the index's other variants are
     untested) and item 2 (the memory's belt check before the registry).

Sandbox: tests/conftest.py's autouse fixture (rpr.ROOT etc. in tmp). No LLM, no
network, no market data, no backtest. Every window date here is before 2023.
"""
import asyncio
import copy
import json
import random
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import campaign_memory as cm  # noqa: E402
import composite_cache as cc  # noqa: E402
import data_availability_gate as dag  # noqa: E402
import deflate_sharpe as ds  # noqa: E402
import protocol_resolution as pres  # noqa: E402
import variant_coin as vc  # noqa: E402

from test_k3_protocol_pinning import _minimal_run  # noqa: E402
from test_e056_config_direct_authoring import _BASE_CONFIG, _write_backtest_spec_and_patches  # noqa: E402

REAL_UNIVERSE = yaml.safe_load((SR_ROOT / "config" / "coin_universe.yaml").read_text(encoding="utf-8"))
REAL_LAYER1 = yaml.safe_load((SR_ROOT / "config" / "venue_data_capability.yaml").read_text(encoding="utf-8"))
ERAS = pres.load_policy_eras(SR_ROOT / "config" / "campaign_data_policy.yaml")
DESIGN_PATCH = [{"path": "/strategies/regimes/unknown/components/0/params/period", "value": 21}]


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _months(first: str, n: int) -> list:
    y, m = int(first[:4]), int(first[5:7])
    out = []
    for _ in range(n):
        ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
        out.append({"label": f"{y:04d}-{m:02d}",
                    "test": {"start": f"{y:04d}-{m:02d}-01", "end": f"{ny:04d}-{nm:02d}-01"}})
        y, m = ny, nm
    return out


def _source(windows, symbols=("BTCUSDT", "ETHUSDT")) -> dict:
    return {"symbols": list(symbols), "timeframe": "1h", "windows": windows,
            "holdout": {"start": "2025-06-01", "end": None},
            "promotion": {"median_sharpe_gt": 0, "max_abs_drawdown_pct_lt": 25,
                          "min_trade_count_gte": 15, "kill_median_sharpe_lt": -1}}


def _era_of(ts):
    return pres.era_id_for_timestamp(ts, ERAS)


def _ctx(source, universe=REAL_UNIVERSE, layer1=REAL_LAYER1) -> dict:
    return {"source": source, "universe": universe, "layer1": layer1,
            "precheck": dag.layer1_price_precheck, "era_of": _era_of}


# A binance-only synthetic world where XRPUSDT (category payment) has a Layer-1
# earliest date, so a partial coverage can be staged without any real data.
def _synthetic(earliest: str):
    universe = {"categories": {
        "store_of_value": {"coins": [{"symbol": "BTCUSDT"}, {"symbol": "ETHUSDT"}]},
        "payment": {"coins": [{"symbol": "XRPUSDT"}]}}}
    layer1 = {"venues": {"binance": {"spot": {
        "timeframes": {"available": ["1h"]},
        "symbols": {"earliest_ohlcv_utc": {"BTCUSDT": "2017-08-17T00:00:00Z",
                                           "XRPUSDT": earliest}}}}}}
    return universe, layer1


def _asset(symbol="XRPUSDT", vid="asset", patch=None):
    return {"variant_id": vid, "kind": "asset", "symbol": symbol, "patch": patch or []}


# ---------------------------------------------------------------------------
# 1. tools/variant_coin.py
# ---------------------------------------------------------------------------

def test_per_coin_mode_only_when_an_entry_declares_kind_or_symbol():
    assert vc.per_coin_mode([{"variant_id": "base", "patch": []}]) is False
    assert vc.per_coin_mode([]) is False
    assert vc.per_coin_mode([{"variant_id": "base", "kind": "base"}]) is True
    assert vc.per_coin_mode([{"variant_id": "a", "symbol": "XRPUSDT"}]) is True


def test_venue_symbol_reads_the_venue_cache_key():
    _cat, xrp = vc.coin_entry(REAL_UNIVERSE, "XRPUSDT")
    assert _cat == "payment" and vc.venue_symbol(xrp) == "XRPUSD"
    _cat, btc = vc.coin_entry(REAL_UNIVERSE, "BTCUSDT")
    assert _cat == "store_of_value" and vc.venue_symbol(btc) == "BTCUSDT"
    assert vc.coin_entry(REAL_UNIVERSE, "NOPEUSDT") == (None, None)


def test_base_and_design_run_the_base_coin_on_every_window():
    source = _source(_months("2022-01", 6))
    base = vc.resolve_variant({"variant_id": "base", "kind": "base", "patch": []}, **_ctx(source))
    design = vc.resolve_variant({"variant_id": "d", "kind": "design", "symbol": "BTCUSDT",
                                 "patch": DESIGN_PATCH}, **_ctx(source))
    for res in (base, design):
        assert res["ok"] and res["symbol"] == "BTCUSDT" and res["coverage"] is None
        assert res["protocol"] == {**source, "symbols": ["BTCUSDT"]}
        assert vc.check_variant_protocol(res["protocol"], source) == []


def test_asset_full_coverage_on_the_real_layer1_runs_every_window_on_its_venue():
    """XRPUSDT (payment, Kraken) for a BTC base: the real coin_universe.yaml and
    the real Layer-1 audit -- XRPUSD on kraken, every 2022 window covered."""
    source = _source(_months("2022-01", 6))
    res = vc.resolve_variant(_asset(), **_ctx(source))
    assert res["ok"], res
    assert res["protocol"]["symbols"] == ["XRPUSD"] and res["protocol"]["exchange"] == "kraken"
    assert res["protocol"]["windows"] == source["windows"]
    assert res["coverage"]["fraction"] == 1.0 and res["coverage"]["uncovered"] == []
    assert res["coverage"]["venue_symbol"] == "XRPUSD" and res["coverage"]["exchange"] == "kraken"
    assert vc.check_variant_protocol(res["protocol"], source) == []


def test_asset_partial_coverage_runs_on_the_covered_windows_d042():
    windows = _months("2019-06", 13)  # spans the 2019-09-10 era boundary
    universe, layer1 = _synthetic("2019-08-15T00:00:00Z")
    source = _source(windows)
    res = vc.resolve_variant(_asset(), **_ctx(source, universe, layer1))
    assert res["ok"], res
    cov = res["coverage"]
    assert cov["windows_total"] == 13 and len(cov["windows_run"]) == 11
    assert cov["windows_run"][0] == "2019-08" and [u["label"] for u in cov["uncovered"]] == [
        "2019-06", "2019-07"]
    assert len(cov["eras"]) == 2 and cov["fraction"] >= vc.D042_MIN_WINDOW_COVERAGE
    assert [w["label"] for w in res["protocol"]["windows"]] == cov["windows_run"]
    assert res["protocol"]["symbols"] == ["XRPUSDT"] and "exchange" not in res["protocol"]
    assert vc.check_variant_protocol(res["protocol"], source) == []


def test_asset_below_the_window_share_is_not_run():
    universe, layer1 = _synthetic("2020-02-15T00:00:00Z")
    res = vc.resolve_variant(_asset(), **_ctx(_source(_months("2019-06", 13)), universe, layer1))
    assert res["ok"] is False and res["reason"].startswith(vc.COVERAGE_REASON_PREFIX)
    assert "5/13" in res["reason"] and len(res["coverage"]["windows_run"]) == 5


def test_asset_above_the_share_but_one_era_is_not_run():
    universe, layer1 = _synthetic("2021-04-15T00:00:00Z")
    res = vc.resolve_variant(_asset(), **_ctx(_source(_months("2021-01", 10)), universe, layer1))
    assert res["coverage"]["fraction"] >= vc.D042_MIN_WINDOW_COVERAGE
    assert len(res["coverage"]["eras"]) == 1
    assert res["ok"] is False and res["reason"].startswith(vc.COVERAGE_REASON_PREFIX)


def test_thresholds_are_named_constants_cited_to_d042():
    assert (vc.D042_MIN_WINDOW_COVERAGE, vc.D042_MIN_ERAS) == (0.60, 2)
    assert "D-042" in Path(vc.__file__).read_text(encoding="utf-8")


@pytest.mark.parametrize("entry,needle", [
    (_asset("ETHUSDT"), "base coin's own category"),
    (_asset(patch=DESIGN_PATCH), "patch must be empty"),
    (_asset("NOPEUSDT"), "not in config/coin_universe.yaml"),
    ({"variant_id": "asset", "kind": "asset", "patch": []}, "must name its coin"),
    ({"variant_id": "x", "patch": []}, "kind None"),
    ({"variant_id": "x", "kind": "weird", "patch": []}, "kind 'weird'"),
    ({"variant_id": "d", "kind": "design", "symbol": "ETHUSDT", "patch": DESIGN_PATCH}, "base coin"),
    ({"variant_id": "d", "kind": "design", "patch": []}, "must not be empty"),
    ({"variant_id": "b2", "kind": "base", "patch": []}, "variant_id 'base'"),
])
def test_malformed_per_coin_entries_are_refused(entry, needle):
    res = vc.resolve_variant(entry, **_ctx(_source(_months("2022-01", 6))))
    assert res["ok"] is False and res["reason"].startswith(vc.COIN_REASON_PREFIX)
    assert needle in res["reason"], res["reason"]


def test_check_variant_protocol_catches_a_tampered_derivation():
    source = _source(_months("2022-01", 6))
    good = vc.variant_protocol(source, symbol="BTCUSDT", windows_run=["2022-02", "2022-04"])
    assert vc.check_variant_protocol(good, source) == []
    assert vc.check_variant_protocol({**good, "timeframe": "4h"}, source)
    assert vc.check_variant_protocol({**good, "windows": good["windows"][::-1]}, source)
    assert vc.check_variant_protocol({**good, "symbols": ["A", "B"]}, source)
    assert vc.check_variant_protocol({**good, "windows": []}, source)


# ---------------------------------------------------------------------------
# 2-3. 5a under the variant loop, and flag-off byte identity
# ---------------------------------------------------------------------------

def _set_flags(**flags):
    cfg_dir = rpr.ROOT / "config"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    (cfg_dir / "campaign_config.yaml").write_text(
        yaml.safe_dump({"orchestrator": {k: {"enabled": v} for k, v in flags.items()}}),
        encoding="utf-8")


def _copy_coin_configs():
    for name in ("coin_universe.yaml", "venue_data_capability.yaml"):
        shutil.copyfile(SR_ROOT / "config" / name, rpr.ROOT / "config" / name)


def _run_protocol_file(monkeypatch, windows) -> Path:
    path = rpr.ROOT / "protocols" / "c2s2b.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_source(windows), indent=2), encoding="utf-8")
    monkeypatch.setattr(rpr, "_resolve_protocol_path", lambda run_dir, run_id: path)
    return path


def _ok_subprocess(monkeypatch, calls=None):
    def _run(cmd, *a, **k):
        if calls is not None:
            calls.append([str(c) for c in cmd])

        class _Ok:
            returncode, stdout, stderr = 0, "", ""
        return _Ok()
    monkeypatch.setattr(rpr.subprocess, "run", _run)


PER_COIN_PATCHES = [
    {"variant_id": "base", "kind": "base", "symbol": "BTCUSDT", "patch": [], "rationale": "b"},
    {"variant_id": "design", "kind": "design", "symbol": "BTCUSDT", "patch": DESIGN_PATCH,
     "rationale": "d"},
    {"variant_id": "asset", "kind": "asset", "symbol": "XRPUSDT", "patch": [], "rationale": "a"},
]


def _strip_coin(patches):
    return [{k: v for k, v in p.items() if k not in ("kind", "symbol")} for p in patches]


def _run_5a(run_id, patches):
    run_dir = _minimal_run(rpr.ROOT, run_id)
    _write_backtest_spec_and_patches(run_dir, copy.deepcopy(patches))
    asyncio.run(rpr.run_tool_worker("backtest_specification", run_id))
    return run_dir


def test_5a_writes_one_protocol_per_variant_under_the_loop(monkeypatch):
    _set_flags(config_direct_authoring=True, variant_loop=True)
    _copy_coin_configs()
    source_path = _run_protocol_file(monkeypatch, _months("2022-01", 6))
    _ok_subprocess(monkeypatch)
    run_dir = _run_5a("run_901", PER_COIN_PATCHES)
    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]
    source = json.loads(source_path.read_text(encoding="utf-8"))
    expect = {"base": ("BTCUSDT", ["BTCUSDT"]), "design": ("BTCUSDT", ["BTCUSDT"]),
              "asset": ("XRPUSDT", ["XRPUSD"])}
    for vid, (coin, venue) in expect.items():
        e = index[vid]
        assert e["status"] == "validated" and e["kind"] == vid and e["symbol"] == coin
        assert e["protocol_path"] == f"artifacts/variants/{vid}/protocol.json"
        proto = json.loads((run_dir / e["protocol_path"]).read_text(encoding="utf-8"))
        assert proto["symbols"] == venue and proto["windows"] == source["windows"]
        assert {k: v for k, v in proto.items() if k not in ("symbols", "exchange")} == \
            {k: v for k, v in source.items() if k != "symbols"}
    assert "coverage" in index["asset"] and "coverage" not in index["base"]
    # the index shape is one the campaign memory accepts
    for vid, info in index.items():
        cm._check_index_entry(vid, info, Path("index.yaml"))


def test_5a_coverage_skip_does_not_block_the_other_variants(monkeypatch):
    _set_flags(config_direct_authoring=True, variant_loop=True)
    _copy_coin_configs()
    universe, layer1 = _synthetic("2020-02-15T00:00:00Z")
    rpr.save_yaml(rpr.ROOT / "config" / "coin_universe.yaml", universe)
    rpr.save_yaml(rpr.ROOT / "config" / "venue_data_capability.yaml", layer1)
    _run_protocol_file(monkeypatch, _months("2019-06", 13))
    _ok_subprocess(monkeypatch)
    run_dir = _run_5a("run_902", PER_COIN_PATCHES)
    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]
    assert index["base"]["status"] == index["design"]["status"] == "validated"
    a = index["asset"]
    assert a["status"] == "not_tested" and a["reason"].startswith(vc.COVERAGE_REASON_PREFIX)
    assert a["coverage"]["windows_total"] == 13 and "config_path" not in a
    assert not (run_dir / "artifacts" / "variants" / "asset" / "protocol.json").exists()
    assert rpr._is_coverage_skip(a) and not rpr._is_repeat_skip(a)
    # never a data/engineering shortfall: the park kind ignores it
    assert rpr._variant_park_kind(index, run_dir / "artifacts") == (None, [])


def test_flag_off_and_legacy_patches_write_byte_identical_indexes(monkeypatch):
    """variant_loop OFF: kind/symbol are ignored -- the index is byte-identical to
    the one the same patches without them produce, and no protocol.json exists.
    variant_loop ON with a legacy variant_patches.yaml (no kind/symbol): the same
    bytes again -- the loop's per-coin branch never runs."""
    _copy_coin_configs()
    _run_protocol_file(monkeypatch, _months("2022-01", 6))
    _ok_subprocess(monkeypatch)
    _set_flags(config_direct_authoring=True)
    off_coin = _run_5a("run_910", PER_COIN_PATCHES)
    off_legacy = _run_5a("run_911", _strip_coin(PER_COIN_PATCHES))
    _set_flags(config_direct_authoring=True, variant_loop=True)
    on_legacy = _run_5a("run_912", _strip_coin(PER_COIN_PATCHES))
    idx = [(d / "artifacts" / "variants" / "index.yaml").read_bytes()
           for d in (off_coin, off_legacy, on_legacy)]
    assert idx[0] == idx[1] == idx[2]
    for d in (off_coin, off_legacy, on_legacy):
        assert not list((d / "artifacts" / "variants").glob("*/protocol.json"))
        for vid in ("base", "design", "asset"):
            assert ((d / "artifacts" / "variants" / vid / "strategy_config.json").read_bytes()
                    == (off_legacy / "artifacts" / "variants" / vid / "strategy_config.json")
                    .read_bytes())


# ---------------------------------------------------------------------------
# 4. The data gate and run_protocol.py receive the variant's own protocol
# ---------------------------------------------------------------------------

def _stage_index(run_id, *, per_coin: bool, monkeypatch) -> tuple:
    """A run after 5a: three validated variants, per-coin (protocol.json each)
    or legacy (no protocol_path)."""
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    source_path = _run_protocol_file(monkeypatch, _months("2022-01", 6))
    source = json.loads(source_path.read_text(encoding="utf-8"))
    index = {}
    coins = {"base": "BTCUSDT", "design": "BTCUSDT", "asset": "XRPUSD"}
    for vid in coins:
        cfg = rpr._apply_json_pointer_patch(_BASE_CONFIG, DESIGN_PATCH if vid == "design" else [])
        (arts / "variants" / vid).mkdir(parents=True, exist_ok=True)
        (arts / "variants" / vid / "strategy_config.json").write_text(json.dumps(cfg, indent=2),
                                                                      encoding="utf-8")
        index[vid] = {"status": "validated",
                      "config_path": f"artifacts/variants/{vid}/strategy_config.json"}
        if per_coin:
            proto = vc.variant_protocol(source, symbol=coins[vid],
                                        exchange="kraken" if vid == "asset" else None)
            (arts / "variants" / vid / "protocol.json").write_text(json.dumps(proto, indent=2),
                                                                   encoding="utf-8")
            index[vid].update({"kind": vid, "symbol": "XRPUSDT" if vid == "asset" else "BTCUSDT",
                               "protocol_path": f"artifacts/variants/{vid}/protocol.json"})
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": index})
    return run_dir, source_path


def _tool_stub(monkeypatch, calls):
    def _run(cmd, *a, **k):
        argv = [str(c) for c in cmd]
        calls.append(argv)
        out = Path(argv[argv.index("--out-dir") + 1])
        out.mkdir(parents=True, exist_ok=True)
        proto = json.loads(Path(argv[3]).read_text(encoding="utf-8"))
        if Path(argv[1]).name == "data_availability_gate.py":
            (out / "data_availability_gate.yaml").write_text(
                yaml.safe_dump({"outcome": "validate", "reasons": []}), encoding="utf-8")
        else:
            results = [{"symbol": s, "window": w["label"], "run_id": f"{s}_{w['label']}",
                        "core": {"trade_count": 20, "sharpe": 0.1}}
                       for s in proto["symbols"] for w in proto["windows"]]
            (out / "protocol_summary.json").write_text(json.dumps({
                "protocol_file": argv[3], "results": results,
                "per_symbol_summary": {s: {"median_sharpe": 0.1} for s in proto["symbols"]},
                "verdict": None, "hypothesis_verdict": None}), encoding="utf-8")

        class _Done:
            returncode, stdout, stderr = 0, "", ""
        return _Done()
    monkeypatch.setattr(rpr.subprocess, "run", _run)


@pytest.mark.parametrize("per_coin", [True, False])
def test_data_gate_and_protocol_execution_argv_and_trial_symbols(monkeypatch, per_coin):
    _set_flags(config_direct_authoring=True, variant_loop=True)
    run_dir, source_path = _stage_index(f"run_92{int(per_coin)}", per_coin=per_coin,
                                        monkeypatch=monkeypatch)
    calls: list = []
    _tool_stub(monkeypatch, calls)
    asyncio.run(rpr.run_tool_worker("data_availability_gate", run_dir.name))
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_dir.name))
    by_tool = {"data_availability_gate.py": {}, "run_protocol.py": {}}
    for argv in calls:
        out = Path(argv[argv.index("--out-dir") + 1])  # variants/<vid>[/data_availability]
        vid = out.parent.name if out.name == "data_availability" else out.name
        by_tool[Path(argv[1]).name][vid] = Path(argv[3])
    for tool, seen in by_tool.items():
        assert sorted(seen) == ["asset", "base", "design"], (tool, seen)
        for vid, proto in seen.items():
            want = (run_dir / "artifacts" / "variants" / vid / "protocol.json" if per_coin
                    else source_path)
            assert proto.resolve() == want.resolve(), (tool, vid)
    rows = {r["trial_id"]: r for r in rpr.load_campaign_state()["trial_sharpes"]}
    for vid, coin in {"base": "BTCUSDT", "design": "BTCUSDT", "asset": "XRPUSD"}.items():
        row = rows[f"{run_dir.name}:{vid}"]
        if per_coin:
            assert row["symbols"] == [coin]
        else:
            assert "symbols" not in row  # the pre-S2b row, byte-identical keys
    pr = rpr.load_yaml(run_dir / "artifacts" / "variants" / "asset" / "protocol_result.yaml")
    assert {r["symbol"] for r in pr["results"]} == ({"XRPUSD"} if per_coin else
                                                    {"BTCUSDT", "ETHUSDT"})


# ---------------------------------------------------------------------------
# 5. G6: DSR dedupe keys on the coin, both paths, legacy byte-identical
# ---------------------------------------------------------------------------

def _row(tid, fh="h", source="backtest", **kw):
    return {"trial_id": tid, "source": source, "sharpe": 0.1, "statistic_valid": "sharpe",
            "forecast_hash": fh, **kw}


def _legacy_dedupe(rows):
    """The pre-S2b key, (forecast_hash, source), for ledgers without reproduces_trial."""
    seen, kept = set(), []
    for r in rows:
        fh = r.get("forecast_hash")
        if fh is None:
            kept.append(r)
            continue
        key = (fh, r.get("source"))
        if key not in seen:
            seen.add(key)
            kept.append(r)
    return kept, len(rows) - len(kept)


@pytest.mark.parametrize("dedupe", [ds.deduplicate_trials, rpr._dedupe_trials])
def test_same_config_on_another_coin_is_its_own_trial(dedupe):
    rows = [_row("r:base", symbols=["BTCUSDT"]), _row("r:asset", symbols=["XRPUSD"]),
            _row("r2:asset", symbols=["XRPUSD"])]  # a real repeat of r:asset collapses
    kept, removed = dedupe(rows)
    assert [r["trial_id"] for r in kept] == ["r:base", "r:asset"] and removed == 1
    # a symbols row never collapses onto a legacy row of the same hash
    kept, removed = dedupe([_row("old"), _row("r:base", symbols=["BTCUSDT"])])
    assert removed == 0 and len(kept) == 2


@pytest.mark.parametrize("dedupe", [ds.deduplicate_trials, rpr._dedupe_trials])
@pytest.mark.parametrize("bad", [None, [], "BTCUSDT", [""], [1]])
def test_malformed_symbols_fail_loud_on_both_paths(dedupe, bad):
    with pytest.raises(ValueError, match="symbols"):
        dedupe([_row("r:asset", symbols=bad)])


@pytest.mark.parametrize("seed", range(5))
def test_legacy_ledgers_dedupe_exactly_as_before_on_both_paths(seed):
    rng = random.Random(seed)
    rows = [_row(f"t{i}", fh=rng.choice(["a", "b", "c", None, "", 0]),
                 source=rng.choice(["backtest", "prescreen", "backtest_failed"]))
            for i in range(60)]
    ref = _legacy_dedupe(rows)
    for dedupe in (ds.deduplicate_trials, rpr._dedupe_trials):
        kept, removed = dedupe(rows)
        assert kept == ref[0] and removed == ref[1]


@pytest.mark.real_repo_readonly
def test_the_committed_ledger_dedupes_exactly_as_before():
    state = yaml.safe_load((SR_ROOT / "campaign_record" / "campaign_state.yaml")
                           .read_text(encoding="utf-8"))
    rows = [r for r in state.get("trial_sharpes") or [] if not r.get("invalidated_artifact")]
    assert not any("symbols" in r for r in rows)
    assert not any(r.get("reproduces_trial") for r in rows)
    ref = _legacy_dedupe(rows)
    for dedupe in (ds.deduplicate_trials, rpr._dedupe_trials):
        assert dedupe(rows) == ref


def test_trial_recorders_add_symbols_only_when_given(tmp_path):
    cfg = tmp_path / "c.json"
    cfg.write_text(json.dumps(_BASE_CONFIG), encoding="utf-8")
    summary = {"per_symbol_summary": {"XRPUSD": {"median_sharpe": 0.2}}, "results": []}
    rpr._record_backtest_trial("run_930", summary, cfg, trial_id="run_930:base")
    rpr._record_backtest_trial("run_930", summary, cfg, trial_id="run_930:asset",
                               symbols=["XRPUSD"])
    rpr._record_failed_backtest_trial("run_930", cfg, "x", trial_id="run_930:design")
    rpr._record_failed_backtest_trial("run_930", cfg, "x", trial_id="run_930:asset2",
                                      symbols=["XRPUSD"])
    rows = {r["trial_id"]: r for r in rpr.load_campaign_state()["trial_sharpes"]}
    assert "symbols" not in rows["run_930:base"] and "symbols" not in rows["run_930:design"]
    assert rows["run_930:asset"]["symbols"] == rows["run_930:asset2"]["symbols"] == ["XRPUSD"]
    assert list(rows["run_930:base"]) == ["trial_id", "source", "sharpe", "expectancy_bps",
                                          "n_trades", "statistic_valid", "below_floor_pct",
                                          "forecast_hash"]
    with pytest.raises(ValueError):
        rpr._record_backtest_trial("run_930", summary, cfg, trial_id="run_930:x", symbols=[])


# ---------------------------------------------------------------------------
# 6. Repeat gate, residual IC, conformance
# ---------------------------------------------------------------------------

def test_repeat_gate_keys_a_per_coin_variant_on_its_own_coin():
    import test_e036_s2a_exact_match_gate as t36
    cfg = t36._config()
    t36._prior_run_in_memory("run_050", cfg, protocol_name="run_050_generated.json",
                             symbols=["XRPUSD"], variant_loop=True)
    run_dir = t36._config_direct_candidate("run_061", {"base": cfg, "asset": cfg},
                                           "run_061_generated.json")
    source = json.loads((rpr.ROOT / "protocols" / "run_061_generated.json").read_text("utf-8"))
    arts = run_dir / "artifacts"
    index = rpr.load_yaml(arts / "variants" / "index.yaml")["variants"]
    for vid, sym in (("base", "BTCUSDT"), ("asset", "XRPUSD")):
        (arts / "variants" / vid / "protocol.json").write_text(
            json.dumps(vc.variant_protocol(source, symbol=sym)), encoding="utf-8")
        index[vid].update({"kind": vid, "protocol_path": f"artifacts/variants/{vid}/protocol.json"})
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": index})
    t36._set_flags(**t36._CD_ON)
    assert rpr._gate_config_direct_variants(run_dir, "run_061") is None
    res = rpr.load_yaml(arts / "variant_anti_adjacency_result.yaml")
    assert res["repeats"] == ["asset"]  # same config already tested on XRPUSD
    assert res["variants"]["asset"]["key"]["symbols"] == ["XRPUSD"]
    assert res["variants"]["base"]["route"] == "admit"
    assert res["variants"]["base"]["key"]["symbols"] == ["BTCUSDT"]


def _bars(results_dir, wrid, forecasts, data_sha):
    import test_e060_s2_residual_ic as t60
    t60._write_bars(results_dir, wrid, forecasts, data_sha=data_sha)


def test_residual_ic_runs_one_composite_per_coin_group():
    import test_e060_s2_residual_ic as t60
    rel, sha = t60._config_on_disk()
    reg = t60._registry_file([t60._block("H1:run_700", ref=rel, sha=sha)])
    base_proto = t60._write_protocol(rpr.ROOT, "p1h.json", t60._protocol())
    xrp = {**t60._protocol(), "symbols": ["XRPUSD"], "exchange": "kraken"}
    xrp_proto = t60._write_protocol(rpr.ROOT, "p1h_xrp.json", xrp)
    shas = {"BTCUSDT": "d" * 64, "XRPUSD": "e" * 64}
    run_dir = rpr.ROOT / "runs" / "run_940"
    n = 900
    coins = {"base": "BTCUSDT", "design": "BTCUSDT", "asset": "XRPUSD"}
    results, summaries = {}, {}
    for vid, coin in coins.items():
        res = run_dir / "variants" / vid / "results"
        _bars(res, f"wr_{vid}", (t60.Z_CAND if vid == "asset" else t60.Z_COMP)[:n], shas[coin])
        results[vid] = res
        summaries[vid] = {**t60._summary(f"wr_{vid}")}
        summaries[vid]["results"] = [{**summaries[vid]["results"][0], "symbol": coin}]
    calls = []

    def runner(config_path, protocol_path, out_dir):
        coin = json.loads(Path(protocol_path).read_text(encoding="utf-8"))["symbols"][0]
        calls.append(coin)
        _bars(Path(out_dir) / "results", "wr_comp", t60.Z_COMP[:n], shas[coin])
        s = t60._summary("wr_comp")
        s["results"] = [{**s["results"][0], "symbol": coin}]
        (Path(out_dir) / "protocol_summary.json").write_text(json.dumps(s), encoding="utf-8")

    kw = dict(root=rpr.ROOT, protocol_path=base_proto, registry_path=reg,
              compositions_path=rpr.ROOT / "campaign_record" / "compositions.yaml",
              holdout_range=t60._seal(), runner=runner)
    with pytest.raises(cc.CompositeError, match="different market data"):
        cc.residual_ic_by_variant(summaries, results, **kw)  # one composite: refused
    doc = cc.residual_ic_by_variant(
        summaries, results, **kw,
        variant_protocol_paths={"base": base_proto, "design": base_proto, "asset": xrp_proto})
    assert sorted(calls) == ["BTCUSDT", "XRPUSD"]
    dirs = doc["composite"]["cache_dirs"]
    assert dirs["base"] == dirs["design"] == doc["composite"]["cache_dir"] != dirs["asset"]
    assert doc["variants"]["base"]["fully_explained"] is True
    assert doc["variants"]["asset"]["value"] is not None


def test_per_coin_conformance_checks_the_run_protocol_and_the_derivation(monkeypatch):
    _set_flags(config_direct_authoring=True, variant_loop=True)
    run_dir, source_path = _stage_index("run_950", per_coin=True, monkeypatch=monkeypatch)
    vproto = run_dir / "artifacts" / "variants" / "asset" / "protocol.json"
    constraints = {"protocol": {"symbols": ["BTCUSDT", "ETHUSDT"]}}
    pr = {"protocol_file": str(vproto), "results": []}
    assert rpr._per_coin_conformance(pr, constraints, vproto, source_path) == []
    # the flag-off check alone would flag the per-coin variant's own symbols
    assert rpr._check_protocol_execution_conformance(
        pr, constraints, json.loads(vproto.read_text(encoding="utf-8")))
    other = run_dir / "artifacts" / "variants" / "base" / "protocol.json"
    assert "not its own" in rpr._per_coin_conformance(
        {**pr, "protocol_file": str(other)}, constraints, vproto, source_path)[0]
    tampered = json.loads(vproto.read_text(encoding="utf-8"))
    tampered["timeframe"] = "4h"
    vproto.write_text(json.dumps(tampered), encoding="utf-8")
    assert any("timeframe" in v for v in rpr._per_coin_conformance(pr, constraints, vproto,
                                                                   source_path))
    assert rpr._per_coin_conformance(pr, {"protocol": {"symbols": ["SOLUSDT"]}}, vproto,
                                     source_path)


# ---------------------------------------------------------------------------
# 7-8. CUL-342 items 1 and 2
# ---------------------------------------------------------------------------

def test_single_column_grid_lists_the_index_variants_as_untested():
    arts = rpr.ROOT / "runs" / "run_960" / "artifacts"
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {
        "base": {"status": "validated", "config_path": "x"},
        "design": {"status": "validated", "config_path": "y"},
        "asset": {"status": "not_tested", "reason": "r"}}})
    _set_flags()
    assert rpr._single_column_untested_kw(arts, "run_960") == {}  # config-direct off
    _set_flags(config_direct_authoring=True)
    kw = rpr._single_column_untested_kw(arts, "run_960")
    assert sorted(kw["untested_variants"]) == ["asset", "design"]
    assert "variant_loop off" in kw["untested_variants"]["design"]
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {
        "base": {"status": "validated", "config_path": "x"}}})
    assert rpr._single_column_untested_kw(arts, "run_960") == {}  # base only: unchanged


def test_belt_check_refuses_a_validated_idea_with_ungraded_variants():
    import test_e058_s2a_regroup_record as t58
    t58._set_orchestrator(t58.ALL_ON)
    # single column, variant loop off, index lists design: only base ran
    run_dir = t58._seed(idea_status="validated")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        "base": {"status": "validated", "config_path": "artifacts/variants/base/strategy_config.json"},
        "design": {"status": "validated",
                   "config_path": "artifacts/variants/design/strategy_config.json"}}})
    with pytest.raises(cm.CampaignMemoryError, match="only the base config ran"):
        rpr._run_regroup_record_stage(t58.RUN_ID, run_dir)
    assert not t58._memory_path().exists()


@pytest.mark.parametrize("key,value,needle", [
    ("untested_variants", {"asset": "insufficient_coverage: x"}, "untested_variants"),
    ("failed_variants", {"asset": "backtest_failed: x"}, "failed_variants"),
])
def test_belt_check_refuses_a_validated_grid_carrying_unscored_variants(key, value, needle):
    import test_e058_s2a_regroup_record as t58
    t58._set_orchestrator(t58.ALL_ON)
    run_dir = t58._seed(idea_status="validated", variant_loop=True)
    arts = run_dir / "artifacts"
    index = rpr.load_yaml(arts / "variants" / "index.yaml")
    index["variants"]["asset"] = {"status": "validated",
                                  "config_path": "artifacts/variants/base/strategy_config.json"}
    rpr.save_yaml(arts / "variants" / "index.yaml", index)
    grid = rpr.load_yaml(arts / "grid_evaluation.yaml")
    grid[key] = value  # a hand-edited grid: its own rollup would say inconclusive
    rpr.save_yaml(arts / "grid_evaluation.yaml", grid)
    with pytest.raises(cm.CampaignMemoryError, match=needle):
        rpr._run_regroup_record_stage(t58.RUN_ID, run_dir)
    assert not t58._memory_path().exists()


def test_belt_check_passes_a_whole_validated_idea():
    import test_e058_s2a_regroup_record as t58
    t58._set_orchestrator(t58.ALL_ON)
    run_dir = t58._seed(idea_status="validated", variant_loop=True)
    rpr._run_regroup_record_stage(t58.RUN_ID, run_dir)
    e = t58._memory()["runs"][t58.RUN_ID]
    assert e["idea_status"] == "validated"
    assert {v["status"] for v in e["variants"].values()} == {"tested"}


def test_data_gate_floor_counts_a_coverage_skip_like_a_repeat():
    cov = {"status": "not_tested", "reason": f"{vc.COVERAGE_REASON_PREFIX} 3/13"}
    rep = {"status": "not_tested", "reason": "repeat: x"}
    other = {"status": "not_tested", "reason": "validate_config.py violations"}
    assert rpr._is_coverage_skip(cov) and not rpr._is_coverage_skip(rep)
    assert not rpr._is_coverage_skip(other) and not rpr._is_coverage_skip(
        {"status": "validated", "reason": cov["reason"]})
    assert rpr._variant_park_kind({"a": cov, "b": rep}) == (None, [])
