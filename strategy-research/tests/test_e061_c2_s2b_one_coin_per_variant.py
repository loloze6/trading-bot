"""
E-061 C2 S2b -- one coin per variant (C2_S1_FINDINGS.md G1-G6; DECISION_LOG
D-016, D-042) and Linear CUL-342 items 1-2.

Covers:
  1. tools/variant_coin.py: per-coin mode, the venue symbol, base/design on the
     base coin, the asset coin (other category, empty patch), D-042's coverage
     rule on the Layer-1 precheck (full, partial >= 60% of the windows -- the
     2-era condition dropped, D-045 -- below the share), the derivation check.
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
import datetime
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
    # 2019-03 .. 2020-03: the windows up to 2019-08 have their midpoint in the
    # pre-2019-09-10 era, the rest in the next (eras: recorded, not a gate).
    windows = _months("2019-03", 13)
    universe, layer1 = _synthetic("2019-05-15T00:00:00Z")  # listed mid-window
    source = _source(windows)
    res = vc.resolve_variant(_asset(), **_ctx(source, universe, layer1))
    assert res["ok"], res
    cov = res["coverage"]
    assert cov["windows_total"] == 13 and len(cov["windows_run"]) == 10
    # review fix H2: 2019-05 ends after the listing (the precheck alone accepts
    # it) but starts before it -- it straddles the listing, so it is not covered
    assert cov["windows_run"][0] == "2019-06" and [u["label"] for u in cov["uncovered"]] == [
        "2019-03", "2019-04", "2019-05"]
    assert "straddles the listing" in cov["uncovered"][2]["reason"]
    assert dag.layer1_price_precheck(layer1, "binance", "XRPUSDT", "1h",
                                     datetime.datetime(2019, 5, 1),
                                     datetime.datetime(2019, 6, 1))[0] is True
    assert len(cov["eras"]) == 2 and cov["fraction"] >= vc.D042_MIN_WINDOW_COVERAGE
    assert [w["label"] for w in res["protocol"]["windows"]] == cov["windows_run"]
    assert res["protocol"]["symbols"] == ["XRPUSDT"] and "exchange" not in res["protocol"]
    assert vc.check_variant_protocol(res["protocol"], source) == []


def test_a_window_on_the_listing_date_counts_and_a_coin_without_a_date_keeps_the_precheck():
    """H2's boundary: earliest == test.start is covered. A coin the Layer-1 audit
    gives no date keeps the precheck's own reading. (Since PR #250 the real audit
    carries per-coin Kraken dates from our local caches.)"""
    universe, layer1 = _synthetic("2019-05-01T00:00:00Z")
    cov = vc.window_coverage(_source(_months("2019-03", 4)), exchange="binance", symbol="XRPUSDT",
                             layer1=layer1, precheck=dag.layer1_price_precheck, era_of=_era_of)
    assert cov["windows_run"] == ["2019-05", "2019-06"]
    assert vc.layer1_earliest(layer1, "kraken", "XRPUSD") is None
    assert vc.layer1_earliest(REAL_LAYER1, "kraken", "XRPUSD") == "2017-05-18T00:00:00Z"
    assert vc.layer1_earliest(layer1, "binance", "XRPUSDT") == "2019-05-01T00:00:00Z"


def test_a_windows_era_is_the_era_of_its_midpoint():
    """A window starting just before the 2019-09-10 boundary whose midpoint is
    past it counts in the later era only (the start would have said the earlier)."""
    eras_seen = []

    def era_of(ts):
        eras_seen.append(ts)
        return _era_of(ts)
    window = [{"label": "w", "test": {"start": "2019-09-01", "end": "2019-10-01"}}]
    cov = vc.window_coverage(_source(window), exchange="binance", symbol="BTCUSDT",
                             layer1=REAL_LAYER1, precheck=dag.layer1_price_precheck, era_of=era_of)
    assert eras_seen == ["2019-09-16T00:00:00"]
    assert cov["eras"] == [_era_of("2019-09-16")] != [_era_of("2019-09-01")]


def test_asset_below_the_window_share_is_not_run():
    universe, layer1 = _synthetic("2020-02-15T00:00:00Z")
    res = vc.resolve_variant(_asset(), **_ctx(_source(_months("2019-06", 13)), universe, layer1))
    assert res["ok"] is False and res["reason"].startswith(vc.COVERAGE_REASON_PREFIX)
    # 2020-02 straddles the listing (H2): 2020-03 .. 2020-06 only
    assert "4/13" in res["reason"] and len(res["coverage"]["windows_run"]) == 4


def test_asset_at_the_share_in_one_era_runs_d045():
    """D-042's 2-era condition was dropped by the operator on 2026-09-28 (D-045):
    a coin covering >= 60% of the windows runs even when every covered window
    sits in one policy era. The eras stay recorded in `coverage` as information."""
    universe, layer1 = _synthetic("2021-04-15T00:00:00Z")
    res = vc.resolve_variant(_asset(), **_ctx(_source(_months("2021-01", 10)), universe, layer1))
    assert res["coverage"]["windows_run"] == [f"2021-{m:02d}" for m in range(5, 11)]
    assert res["coverage"]["fraction"] == 0.6 and len(res["coverage"]["eras"]) == 1
    assert res["ok"] is True, res
    assert [w["label"] for w in res["protocol"]["windows"]] == res["coverage"]["windows_run"]


def test_below_the_share_is_refused_whatever_the_eras():
    """5/9 (56%) across windows in two eras: the share alone decides."""
    universe, layer1 = _synthetic("2019-07-01T00:00:00Z")
    res = vc.resolve_variant(_asset(), **_ctx(_source(_months("2019-03", 9)), universe, layer1))
    assert len(res["coverage"]["windows_run"]) == 5 and len(res["coverage"]["eras"]) == 2
    assert res["ok"] is False and res["reason"].startswith(vc.COVERAGE_REASON_PREFIX)


def test_thresholds_are_named_constants_cited_to_d042():
    assert vc.D042_MIN_WINDOW_COVERAGE == 0.60
    assert not hasattr(vc, "D042_MIN_ERAS")  # dropped, D-045
    text = Path(vc.__file__).read_text(encoding="utf-8")
    assert "D-042" in text and "D-045" in text


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
        raw = (run_dir / e["protocol_path"]).read_bytes()
        assert e["protocol_sha256"] == vc.protocol_sha256(raw)  # review fix M2
        assert vc.verify_variant_protocol(e, raw, source) == []
        proto = json.loads(raw.decode("utf-8"))
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

def _stage_index(run_id, *, per_coin: bool, monkeypatch, windows=None, universe=None,
                 layer1=None) -> tuple:
    """A run after 5a: three validated variants, per-coin (protocol.json each,
    its sha256 and, for the asset, its coverage -- as 5a writes them) or legacy
    (no protocol_path). `universe`/`layer1`: a synthetic coin world (the asset
    coin then runs on the windows it covers)."""
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    source_path = _run_protocol_file(monkeypatch, windows or _months("2022-01", 6))
    source = json.loads(source_path.read_text(encoding="utf-8"))
    # E-062 S2b-3b review fix 1: 5a freezes the run protocol in per-coin mode
    run_sha = rpr._freeze_run_protocol(run_dir, run_id)[1] if per_coin else None
    _copy_coin_configs()  # protocol_execution re-runs the asset's coverage (M2)
    if universe is not None:
        rpr.save_yaml(rpr.ROOT / "config" / "coin_universe.yaml", universe)
        rpr.save_yaml(rpr.ROOT / "config" / "venue_data_capability.yaml", layer1)
    index = {}
    entries = {"base": {"variant_id": "base", "kind": "base", "patch": []},
               "design": {"variant_id": "design", "kind": "design", "patch": DESIGN_PATCH},
               "asset": _asset()}
    for vid, entry in entries.items():
        cfg = rpr._apply_json_pointer_patch(_BASE_CONFIG, DESIGN_PATCH if vid == "design" else [])
        (arts / "variants" / vid).mkdir(parents=True, exist_ok=True)
        (arts / "variants" / vid / "strategy_config.json").write_text(json.dumps(cfg, indent=2),
                                                                      encoding="utf-8")
        index[vid] = {"status": "validated",
                      "config_path": f"artifacts/variants/{vid}/strategy_config.json"}
        if per_coin:
            # exactly what 5a writes (the same resolver, bytes and sha256)
            res = vc.resolve_variant(entry, **_ctx(source, *((universe, layer1) if universe
                                                             else ())))
            assert res["ok"], res
            raw = json.dumps(res["protocol"], indent=2).encode("utf-8")
            (arts / "variants" / vid / "protocol.json").write_bytes(raw)
            index[vid].update({"kind": vid, "symbol": res["symbol"],
                               **({"coverage": res["coverage"]} if res["coverage"] else {}),
                               "protocol_path": f"artifacts/variants/{vid}/protocol.json",
                               "protocol_sha256": vc.protocol_sha256(raw),
                               rpr.RUN_PROTOCOL_SHA_KEY: run_sha})
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": index})
    return run_dir, source_path


def _tool_stub(monkeypatch, calls, gate_outcomes=None):
    """`gate_outcomes`: {variant_id: decline | refine} for the data gate (every
    other variant validates), with the real tool's exit codes (2 / 3)."""
    codes = {"validate": 0, "decline": 2, "refine": 3}

    def _run(cmd, *a, **k):
        argv = [str(c) for c in cmd]
        calls.append(argv)
        out = Path(argv[argv.index("--out-dir") + 1])
        out.mkdir(parents=True, exist_ok=True)
        proto = json.loads(Path(argv[3]).read_text(encoding="utf-8"))
        if Path(argv[1]).name == "data_availability_gate.py":
            outcome = (gate_outcomes or {}).get(out.parent.name, "validate")
            reasons = [] if outcome == "validate" else [
                f"{proto['symbols'][0]} window {proto['windows'][0]['label']}: no data before "
                f"its listing"]
            (out / "data_availability_gate.yaml").write_text(
                yaml.safe_dump({"outcome": outcome, "reasons": reasons}), encoding="utf-8")

            class _Gate:
                returncode, stdout, stderr = codes[outcome], "", ""
            return _Gate()
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


# ---------------------------------------------------------------------------
# 9. Review fixes H1, M1, M2, M3 and the tidy items
# ---------------------------------------------------------------------------

def _pe_ran(calls) -> set:
    return {Path(a[a.index("--out-dir") + 1]).name for a in calls
            if Path(a[1]).name == "run_protocol.py"}


def _run_trial_ids(run_id) -> list:
    return sorted(r["trial_id"] for r in rpr.load_campaign_state().get("trial_sharpes") or []
                  if r["trial_id"].startswith(f"{run_id}:"))


@pytest.mark.parametrize("outcome", ["decline", "refine"])
def test_h1_layer2_decline_of_an_asset_is_non_blocking(monkeypatch, outcome):
    """A per-coin asset the Layer-2 gate declines / refines is a coverage skip:
    not_tested with the layer2 prefix, ignored by the floor and the park kind;
    base and design still run; no trial row and no backtest for the asset."""
    _set_flags(config_direct_authoring=True, variant_loop=True)
    run_dir, _ = _stage_index(f"run_97{outcome[0]}", per_coin=True, monkeypatch=monkeypatch)
    calls: list = []
    _tool_stub(monkeypatch, calls, gate_outcomes={"asset": outcome})
    asyncio.run(rpr.run_tool_worker("data_availability_gate", run_dir.name))
    idx = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]
    a = idx["asset"]
    assert a["status"] == "not_tested"
    assert a["reason"].startswith(vc.LAYER2_COVERAGE_REASON_PREFIX)
    assert a["reason"].startswith(vc.COVERAGE_REASON_PREFIX) and f"outcome={outcome}" in a["reason"]
    assert rpr._is_coverage_skip(a)
    assert idx["base"]["status"] == idx["design"]["status"] == "validated"
    assert rpr._variant_park_kind(idx, run_dir / "artifacts") == (None, [])
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_dir.name))
    assert _pe_ran(calls) == {"base", "design"}
    assert _run_trial_ids(run_dir.name) == [f"{run_dir.name}:base", f"{run_dir.name}:design"]


@pytest.mark.parametrize("per_coin,vid", [(True, "base"), (True, "design"), (False, "asset")])
def test_h1_a_base_or_design_or_legacy_decline_stays_blocking(monkeypatch, per_coin, vid):
    _set_flags(config_direct_authoring=True, variant_loop=True)
    run_dir, _ = _stage_index(f"run_97{int(per_coin)}{vid[0]}", per_coin=per_coin,
                              monkeypatch=monkeypatch)
    _tool_stub(monkeypatch, [], gate_outcomes={vid: "decline"})
    asyncio.run(rpr.run_tool_worker("data_availability_gate", run_dir.name))
    v = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"][vid]
    assert v["status"] == "not_tested"
    assert v["reason"].startswith("data_availability_gate outcome=decline")
    assert not rpr._is_coverage_skip(v)


def _partial_asset_world():
    """13 windows 2019-03 .. 2020-03, XRPUSDT (binance, synthetic) listed
    2019-05-15: it runs on 10 of them -- a partial-coverage asset."""
    return _months("2019-03", 13), *_synthetic("2019-05-15T00:00:00Z")


def test_m2_verify_variant_protocol_catches_each_tamper():
    windows, universe, layer1 = _partial_asset_world()
    source = _source(windows)
    res = vc.resolve_variant(_asset(), **_ctx(source, universe, layer1))
    raw = json.dumps(res["protocol"], indent=2).encode("utf-8")
    entry = {"kind": "asset", "coverage": res["coverage"], "protocol_sha256": vc.protocol_sha256(raw)}

    def recheck(cov):
        return vc.window_coverage(source, exchange=cov["exchange"], symbol=cov["venue_symbol"],
                                  layer1=layer1, precheck=dag.layer1_price_precheck, era_of=_era_of)
    assert vc.verify_variant_protocol(entry, raw, source, recheck=recheck) == []
    # a byte edit: the sha no longer matches
    assert any("sha256" in p for p in vc.verify_variant_protocol(
        entry, raw.replace(b'"XRPUSDT"', b'"XRPUSDT" '), source))
    # drop a window, and forge the sha AND the index's windows_run to match: the
    # fresh coverage re-run still says 10 windows, not 9
    forged = {**res["protocol"], "windows": res["protocol"]["windows"][1:]}
    raw2 = json.dumps(forged, indent=2).encode("utf-8")
    entry2 = {**entry, "protocol_sha256": vc.protocol_sha256(raw2),
              "coverage": {**entry["coverage"], "windows_run": entry["coverage"]["windows_run"][1:]}}
    probs = vc.verify_variant_protocol(entry2, raw2, source, recheck=recheck)
    assert probs and "fresh coverage" in probs[0]
    # a base / design that is not on every run-protocol window, even with a matching sha
    base = vc.variant_protocol(source, symbol="BTCUSDT", windows_run=["2019-04", "2019-05"])
    raw3 = json.dumps(base, indent=2).encode("utf-8")
    probs = vc.verify_variant_protocol({"kind": "design", "protocol_sha256": vc.protocol_sha256(raw3)},
                                       raw3, source)
    assert probs == [f"a design variant runs every window of the run protocol; its windows "
                     f"{['2019-04', '2019-05']} are not the run protocol's"]
    # no recorded sha at all
    assert "no protocol_sha256" in vc.verify_variant_protocol({"kind": "base"}, raw3, source)[0]


def test_m2_a_protocol_that_drops_a_window_is_refused_before_any_backtest(monkeypatch):
    """A hand-edited design protocol.json (one window dropped) is refused by
    protocol_execution before its backtest: no run_protocol.py call, no trial
    row, a `refused:` failed variant; the others run. The conformance check
    names the same problems."""
    _set_flags(config_direct_authoring=True, variant_loop=True)
    run_dir, source_path = _stage_index("run_980", per_coin=True, monkeypatch=monkeypatch)
    arts = run_dir / "artifacts"
    entry = rpr.load_yaml(arts / "variants" / "index.yaml")["variants"]["design"]
    p = arts / "variants" / "design" / "protocol.json"
    proto = json.loads(p.read_text(encoding="utf-8"))
    proto["windows"] = proto["windows"][1:]
    p.write_text(json.dumps(proto, indent=2), encoding="utf-8")
    calls: list = []
    _tool_stub(monkeypatch, calls)
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_dir.name))
    assert _pe_ran(calls) == {"base", "asset"}
    assert _run_trial_ids(run_dir.name) == [f"{run_dir.name}:asset", f"{run_dir.name}:base"]
    d = rpr.load_yaml(arts / "variants" / "index.yaml")["variants"]["design"]
    assert d["status"] == "not_tested" and d["failed_attempt"].startswith("refused:")
    assert "sha256" in d["reason"] and "not the run protocol's" in d["reason"]
    violations = rpr._per_coin_conformance(
        {"protocol_file": str(p), "results": []}, {"protocol": {"symbols": ["BTCUSDT", "ETHUSDT"]}},
        p, source_path, entry)
    assert any("sha256" in v for v in violations)
    assert any("not the run protocol's" in v for v in violations)


def test_m2_conformance_passes_the_file_5a_wrote(monkeypatch):
    _set_flags(config_direct_authoring=True, variant_loop=True)
    run_dir, source_path = _stage_index("run_981", per_coin=True, monkeypatch=monkeypatch)
    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]
    for vid, entry in index.items():
        p = run_dir / entry["protocol_path"]
        assert rpr._per_coin_conformance(
            {"protocol_file": str(p), "results": []},
            {"protocol": {"symbols": ["BTCUSDT", "ETHUSDT"]}}, p, source_path, entry) == [], vid


def test_m1_partial_coverage_variant_runs_and_is_marked_partial(monkeypatch):
    """The asset runs on its 10 covered windows (graded), yet the grid can at best
    be inconclusive -- the index marks it partial, and the grid carries it."""
    _set_flags(config_direct_authoring=True, variant_loop=True)
    windows, universe, layer1 = _partial_asset_world()
    run_dir, _ = _stage_index("run_982", per_coin=True, monkeypatch=monkeypatch, windows=windows,
                              universe=universe, layer1=layer1)
    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]
    assert vc.is_partial_coverage(index["asset"]) and not vc.is_partial_coverage(index["base"])
    calls: list = []
    _tool_stub(monkeypatch, calls)
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_dir.name))
    assert _pe_ran(calls) == {"asset", "base", "design"}
    part = rpr._partial_coverage_variants(index, ["asset", "base", "design"])
    assert list(part) == ["asset"] and "10/13" in part["asset"] and "E-062 S2b" in part["asset"]


def test_m1_grid_partial_coverage_caps_at_inconclusive_and_a_fail_still_refutes():
    from test_grid_evaluation import _protocol_result, _windows_for_reducer, _menu_shaped_pre_reg
    import verdict_criteria_evaluator as vce
    crit = {"id": "c1", "metric": "net_return_pct", "source": "window", "reducer": "median",
            "comparator": ">", "threshold": 0.0, "floor": {"min_windows": 1}}
    pre = _menu_shaped_pre_reg([crit])
    good = _protocol_result(_windows_for_reducer([1.0, 2.0, 3.0]))
    bad = _protocol_result(_windows_for_reducer([-1.0, -2.0, -3.0]))
    whole = vce.evaluate_grid({"base": good, "asset": good}, pre, {}, {})
    assert whole["idea_status"] == "validated"
    partial = {"asset": "partial coverage: ran on 10/13 run-protocol windows (D-042)"}
    capped = vce.evaluate_grid({"base": good, "asset": good}, pre, {}, {},
                               partial_coverage_variants=partial)
    assert capped["idea_status"] == "inconclusive" and capped["grid"] == whole["grid"]
    assert capped["partial_coverage_variants"] == partial and "E-062 S2b" in capped["reason"]
    refuted = vce.evaluate_grid({"base": bad, "asset": good}, pre, {}, {},
                                partial_coverage_variants=partial)
    assert refuted["idea_status"] == "refuted"
    for kw in ({}, {"partial_coverage_variants": None}, {"partial_coverage_variants": {}}):
        assert yaml.safe_dump(vce.evaluate_grid({"base": good}, pre, {}, {}, **kw)) == \
            yaml.safe_dump(vce.evaluate_grid({"base": good}, pre, {}, {}))
    with pytest.raises(ValueError, match="not graded columns"):
        vce.evaluate_grid({"base": good}, pre, {}, {}, partial_coverage_variants=partial)


def test_m1_partial_coverage_variant_never_passes_the_profit_bars():
    """base FAILs its bars; design would PASS every bar but ran on partial
    coverage: its time-dependent bars read NOT_EVALUABLE, it is not `passing`,
    and the branch-3 stop (profit_bars_reached) is never raised."""
    import test_profit_bars_every_backtest as tpb
    tpb._set_orchestrator({**tpb.FULL_ON, **tpb.VARIANT_LOOP_ON})
    tpb._write_bars()
    run_dir = tpb._variant_run({"base": False, "design": True})
    arts = run_dir / "artifacts"
    ev_full = rpr._evaluate_profit_bars_every_backtest(run_dir, tpb.RUN_ID)
    assert ev_full["passing"] == ["design"]  # on full coverage it passes
    index = rpr.load_yaml(arts / "variants" / "index.yaml")
    index["variants"]["design"]["coverage"] = {"windows_run": ["w1"], "windows_total": 2}
    rpr.save_yaml(arts / "variants" / "index.yaml", index)
    ev = rpr._evaluate_profit_bars_every_backtest(run_dir, tpb.RUN_ID)
    d = ev["variants"]["design"]
    assert d["result"] == "FAIL" and ev["passing"] == [] and ev["result"] == "FAIL"
    assert "1/2" in d["partial_coverage"]
    by_name = {b["name"]: b for b in d["bars"]}
    for name in vc.D042_TIME_DEPENDENT_BARS:
        assert by_name[name]["result"] == "NOT_EVALUABLE" and "E-062 S2b" in by_name[name][
            "not_evaluable_reason"]
        assert by_name[name]["actual"] == {b["name"]: b for b in ev_full["variants"]["design"][
            "bars"]}[name]["actual"]  # the raw value is kept
    assert {b["result"] for n, b in by_name.items()
            if n not in vc.D042_TIME_DEPENDENT_BARS} == {"PASS"}
    assert rpr._profit_bars_stop_route(run_dir, tpb.RUN_ID) is None
    assert not (rpr.load_yaml(run_dir / "pipeline_state.yaml").get("flags") or {}).get(
        "profit_bars_reached")
    # the memory reads the capped result consistently
    block = cm.profit_bars_block(run_dir, tpb.RUN_ID, {
        "base": {"status": "tested"}, "design": {"status": "tested"},
        "broken": {"status": "failed"}, "asset": {"status": "not_tested"}})
    assert block["passing"] == [] and block["variants"]["design"]["result"] == "FAIL"


def test_m1_promote_path_bars_are_capped_when_the_bridge_is_a_partial_variant():
    """Legacy promote path (_evaluate_profit_bars): if the bridge
    protocol_result.yaml mirrors a partial-coverage per-coin variant (base and
    design failed), its time-dependent bars are capped too -- no PASS, so no
    profit_bars_reached. Without a per-coin index the evaluation is unchanged."""
    import test_profit_bars_every_backtest as tpb
    tpb._set_orchestrator({**tpb.FULL_ON, **tpb.VARIANT_LOOP_ON})
    tpb._write_bars()
    run_dir = tpb._variant_run({"base": False, "design": True})
    arts = run_dir / "artifacts"
    bridge = rpr.load_yaml(arts / "variants" / "design" / "protocol_result.yaml")
    vproto = arts / "variants" / "design" / "protocol.json"
    vproto.write_text("{}", encoding="utf-8")
    bridge["protocol_file"] = str(vproto)
    rpr.save_yaml(arts / "protocol_result.yaml", bridge)
    rpr.save_yaml(arts / "promotion_audit.yaml", {"raw_median_sharpe": 1.4,
                                                  "deflated_sharpe_ratio": 0.99})
    before = rpr._evaluate_profit_bars(run_dir, tpb.RUN_ID, portfolio_basis=True)
    assert before["result"] == "PASS"  # the index has no per-coin entry yet
    index = rpr.load_yaml(arts / "variants" / "index.yaml")
    index["variants"]["design"].update({
        "protocol_path": "artifacts/variants/design/protocol.json",
        "coverage": {"windows_run": ["w1"], "windows_total": 2}})
    rpr.save_yaml(arts / "variants" / "index.yaml", index)
    after = rpr._evaluate_profit_bars(run_dir, tpb.RUN_ID, portfolio_basis=True)
    assert after["result"] == "FAIL"
    capped = {b["name"]: b["result"] for b in after["bars"]}
    assert all(capped[n] == "NOT_EVALUABLE" for n in vc.D042_TIME_DEPENDENT_BARS)
    assert [b for b in before["bars"] if b["name"] not in vc.D042_TIME_DEPENDENT_BARS] == \
        [b for b in after["bars"] if b["name"] not in vc.D042_TIME_DEPENDENT_BARS]


def test_m1_memory_refuses_a_validated_grid_with_a_partial_variant():
    import test_e058_s2a_regroup_record as t58
    t58._set_orchestrator(t58.ALL_ON)
    run_dir = t58._seed(idea_status="validated", variant_loop=True)
    grid = rpr.load_yaml(run_dir / "artifacts" / "grid_evaluation.yaml")
    grid["partial_coverage_variants"] = {"design": "partial coverage: 1/2"}
    rpr.save_yaml(run_dir / "artifacts" / "grid_evaluation.yaml", grid)
    with pytest.raises(cm.CampaignMemoryError, match="partial_coverage_variants"):
        rpr._run_regroup_record_stage(t58.RUN_ID, run_dir)


def test_m3_a_per_coin_memory_entry_records_the_run_protocol(monkeypatch):
    """protocol_result.yaml (the bridge) mirrors one variant's own protocol.json;
    a per-coin run's memory entry names the RUN protocol instead -- the key the
    repeat gate builds. Without a per-coin index nothing changes."""
    import test_e058_s2a_regroup_record as t58
    t58._set_orchestrator(t58.ALL_ON)
    run_dir = t58._seed(idea_status="refuted", variant_loop=True)
    arts = run_dir / "artifacts"
    kw = dict(trial_sharpes=rpr.load_campaign_state()["trial_sharpes"],
              categories=rpr._reader_categories(), protocol_root=rpr.ROOT, recorded_at="t")
    legacy = cm.build_memory_entry(run_dir, t58.RUN_ID, **kw)
    assert legacy["protocol_ref"] == "protocols/p.json"  # unchanged without a per-coin index
    index = rpr.load_yaml(arts / "variants" / "index.yaml")
    for vid in ("base", "design"):
        index["variants"][vid]["protocol_path"] = f"artifacts/variants/{vid}/protocol.json"
    rpr.save_yaml(arts / "variants" / "index.yaml", index)
    bridge = rpr.load_yaml(arts / "protocol_result.yaml")
    bridge["protocol_file"] = str(arts / "variants" / "asset" / "protocol.json")  # partial asset
    rpr.save_yaml(arts / "protocol_result.yaml", bridge)
    with pytest.raises(cm.CampaignMemoryError, match="run_protocol_file"):
        cm.build_memory_entry(run_dir, t58.RUN_ID, **kw)
    run_proto = rpr.ROOT / "protocols" / "run_m3.json"
    monkeypatch.setattr(rpr, "_resolve_protocol_path", lambda rd, rid: run_proto)
    rpr._run_regroup_record_stage(t58.RUN_ID, run_dir)
    assert t58._memory()["runs"][t58.RUN_ID]["protocol_ref"] == "protocols/run_m3.json"


def test_repeat_gate_refuses_only_the_variant_with_a_broken_protocol():
    """Tidy: a missing / malformed protocol.json refuses THAT variant (not_tested,
    variant_coin: reason, never a repeat skip); the other is still checked."""
    import test_e036_s2a_exact_match_gate as t36
    cfg = t36._config()
    t36._prior_run_in_memory("run_050", cfg, protocol_name="run_050_generated.json",
                             symbols=["XRPUSD"], variant_loop=True)
    run_dir = t36._config_direct_candidate("run_062", {"base": cfg, "asset": cfg},
                                           "run_062_generated.json")
    source = json.loads((rpr.ROOT / "protocols" / "run_062_generated.json").read_text("utf-8"))
    arts = run_dir / "artifacts"
    index = rpr.load_yaml(arts / "variants" / "index.yaml")["variants"]
    (arts / "variants" / "base" / "protocol.json").write_text(
        json.dumps(vc.variant_protocol(source, symbol="BTCUSDT")), encoding="utf-8")
    for vid in ("base", "asset"):  # asset's protocol.json is never written
        index[vid].update({"kind": vid, "protocol_path": f"artifacts/variants/{vid}/protocol.json"})
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": index})
    t36._set_flags(**t36._CD_ON)
    assert rpr._gate_config_direct_variants(run_dir, "run_062") is None
    after = rpr.load_yaml(arts / "variants" / "index.yaml")["variants"]
    assert after["asset"]["status"] == "not_tested"
    assert after["asset"]["reason"].startswith(vc.COIN_REASON_PREFIX)
    assert not rpr._is_repeat_skip(after["asset"]) and not rpr._is_coverage_skip(after["asset"])
    assert after["base"]["status"] == "validated"
    res = rpr.load_yaml(arts / "variant_anti_adjacency_result.yaml")
    assert res["refused"] == ["asset"] and res["repeats"] == []
    assert res["variants"]["base"]["route"] == "admit"


def test_d056_a_probe_that_cannot_run_on_an_asset_is_a_coverage_skip(monkeypatch):
    """C4 run_064 (2026-10-02): the D-056 size probe could not run the AAVE asset
    variant (no cost model for its venue). Like the data gate's H1, an asset whose
    coin cannot be run is a D-042 coverage skip -- it must not raise the floor for
    base and design; a base/design probe failure stays a plain not_tested."""
    _set_flags(config_direct_authoring=True, variant_loop=True, forecast_size_probe=True)
    _copy_coin_configs()
    _run_protocol_file(monkeypatch, _months("2022-01", 6))
    _ok_subprocess(monkeypatch)

    def fake_probe(config, protocol_path, run_dir, stage, variant_id):
        if variant_id in ("asset", "design"):
            raise RuntimeError("forecast_size_probe failed: UnknownCostModelError")
        return []
    monkeypatch.setattr(rpr, "_forecast_size_violations", fake_probe)
    run_dir = _run_5a("run_909", PER_COIN_PATCHES)
    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]
    a, d = index["asset"], index["design"]
    assert a["status"] == "not_tested" and rpr._is_coverage_skip(a)
    assert a["reason"].startswith(vc.LAYER2_COVERAGE_REASON_PREFIX)
    assert d["status"] == "not_tested" and not rpr._is_coverage_skip(d)
    assert d["reason"] == rpr.FORECAST_SIZE_PROBE_ERROR_REASON
    assert index["base"]["status"] == "validated"
    remaining, min_needed = rpr._variant_floor(index)
    assert min_needed == 2  # the asset no longer counts against the floor
