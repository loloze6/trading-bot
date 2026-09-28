"""
variant_coin -- one coin per variant (E-061 C2 S2b; C2_S1_FINDINGS.md G1-G6,
DECISION_LOG D-016 and D-042).

Pure helpers for step 5a (run_phase1_research's tool-only
backtest_specification) under orchestrator.variant_loop: each
variant_patches.yaml entry may carry `kind` (base | design | asset) and
`symbol` (a coin_universe.yaml symbol). The coin is a BACKTEST INPUT, never a
strategy-config field (D-016): 5a writes one protocol file per variant,
artifacts/variants/<id>/protocol.json = the run protocol with
`symbols: [<venue symbol>]` (and, for an asset coin whose coin_universe.yaml
entry names one, its `exchange`). run_protocol.py and data_availability_gate.py
read that file unchanged (G1).

  * base / design: the run protocol's symbols[0] (G2); every window.
  * asset: an empty patch and a coin from a DIFFERENT coin_universe.yaml
    category than the base coin (G3). D-042 (supersedes G3's full-coverage
    rule, resolves G13): the variant runs on the windows its coin covers --
    judged by the existing Layer-1 precheck (data_availability_gate.
    layer1_price_precheck, no network, no market data) -- when it covers at
    least D042_MIN_WINDOW_COVERAGE of the protocol's windows AND at least
    D042_MIN_ERAS eras of config/campaign_data_policy.yaml. Below that it is
    not run: `not_tested` with a reason starting COVERAGE_REASON_PREFIX, which
    the variant loop treats like a repeat skip (never a data or engineering
    shortfall, never blocking the idea or the other variants); the grid then
    lists it in `untested_variants`, so the idea is at best INCONCLUSIVE.
    Full coverage needs no threshold (it is not partial).

Not here (E-062 S2b): normalising the time-dependent profit bars (trade
minimum per year, drawdown scaled to the period) for a variant that ran on
fewer windows. The windows a variant ran on are recorded for it: its
protocol.json `windows` and, for an asset coin, the index entry's `coverage`.

No lookahead: the only inputs are the protocol file, coin_universe.yaml, the
Layer-1 venue audit (config/venue_data_capability.yaml, structural venue facts)
and the policy's era boundaries -- no bar, no return, no result is read.

No file I/O except `load_protocol_file`; the Layer-1 precheck is passed in by
the caller (data_availability_gate imports trading-bot's DataManager at import
time, so this module does not import it).
"""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

# D-042 (engineering/DECISION_LOG.md, 2026-09-28): an asset variant on partial
# coverage runs only if its coin covers at least this share of the protocol's
# windows AND at least this many policy eras. Below either, it is not run.
D042_MIN_WINDOW_COVERAGE = 0.60
D042_MIN_ERAS = 2

VARIANT_KINDS = ("base", "design", "asset")
VARIANT_PROTOCOL_FILENAME = "protocol.json"
# index.yaml `reason` prefix of an asset variant skipped for coverage (D-042).
COVERAGE_REASON_PREFIX = "insufficient_coverage:"
# index.yaml `reason` prefix of a per-coin entry refused by 5a's coin checks.
COIN_REASON_PREFIX = "variant_coin:"
# era_id_for_timestamp's value outside every declared era: never counted.
_UNMAPPED_ERA = "era_unmapped"
# protocol keys a variant's protocol.json may differ on from its run protocol.
_VARIANT_KEYS = ("symbols", "exchange", "windows")


class VariantCoinError(ValueError):
    """An input this module needs is malformed (a protocol without symbols or
    windows, a policy without eras when an era count decides) -- an
    engineering fault, never a per-variant outcome."""


def per_coin_mode(variants) -> bool:
    """True when any variant_patches.yaml entry declares `kind` or `symbol`:
    the run's variants each carry their coin. False keeps the pre-S2b
    behaviour (every variant on the run protocol), so a legacy
    variant_patches.yaml is unchanged."""
    return any(isinstance(v, dict) and ("kind" in v or "symbol" in v) for v in (variants or []))


def load_protocol_file(path) -> dict:
    """A protocol file as run_protocol.py reads it (JSON)."""
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise VariantCoinError(f"{path}: a protocol must be a JSON object")
    return doc


def base_coin(protocol: dict) -> str:
    """G2: the run protocol's symbols[0]."""
    symbols = protocol.get("symbols")
    if not (isinstance(symbols, list) and symbols and all(isinstance(s, str) and s for s in symbols)):
        raise VariantCoinError(f"the run protocol has no usable `symbols` list ({symbols!r})")
    return symbols[0]


def coin_entry(universe: dict, symbol: str):
    """(category, entry) for `symbol` in coin_universe.yaml, or (None, None)."""
    for category, block in ((universe or {}).get("categories") or {}).items():
        for coin in (block or {}).get("coins") or []:
            if isinstance(coin, dict) and coin.get("symbol") == symbol:
                return category, coin
    return None, None


def venue_symbol(coin: dict) -> str:
    """The symbol the backtest runs for a coin_universe.yaml entry. A coin on a
    non-Binance venue is cached and fetched under the venue's own name --
    `cache_key: kraken_XRPUSD_1h` for `symbol: XRPUSDT, exchange: kraken`
    (data/fetchers/ccxt_fetcher.py cache_key: "<exchange>_<symbol>_<tf>") -- and
    the Layer-1 audit lists Kraken coins by that name (confirmed_universe:
    XRPUSD, ...). So the venue symbol is read from the entry's cache_key when it
    names the entry's exchange; otherwise the coin_universe symbol itself."""
    exchange = coin.get("exchange")
    key = coin.get("cache_key")
    if isinstance(exchange, str) and isinstance(key, str):
        m = re.fullmatch(rf"{re.escape(exchange)}_([A-Za-z0-9]+)_[A-Za-z0-9]+", key)
        if m:
            return m.group(1)
    return coin["symbol"]


def _window_bounds(window: dict) -> tuple:
    test = (window or {}).get("test") or {}
    start, end = test.get("start"), test.get("end")
    if not (isinstance(start, str) and isinstance(end, str)):
        raise VariantCoinError(f"protocol window {window!r} has no test.start/test.end strings")
    return start, end


def window_coverage(protocol: dict, *, exchange: str, symbol: str, layer1: dict,
                    precheck, era_of) -> dict:
    """Which protocol windows `symbol` on `exchange` could cover, by the
    Layer-1 precheck alone. `precheck(layer1, exchange, symbol, timeframe,
    start_dt, end_dt) -> (ok, reason)` is data_availability_gate.
    layer1_price_precheck; `era_of(date_str) -> era_id`. A window's era is the
    era of its test start. Returns {windows_total, windows_run (labels, in
    protocol order), fraction, eras (sorted, era_unmapped excluded),
    uncovered: [{label, reason}]}."""
    import pandas as pd  # the precheck's own timestamp parsing
    windows = protocol.get("windows")
    if not isinstance(windows, list) or not windows:
        raise VariantCoinError("the run protocol has no `windows` list")
    timeframe = protocol.get("timeframe", "1h")  # run_protocol's own default
    run, uncovered, eras = [], [], set()
    for w in windows:
        start, end = _window_bounds(w)
        ok, reason = precheck(layer1, exchange, symbol, timeframe,
                              pd.Timestamp(start).to_pydatetime(), pd.Timestamp(end).to_pydatetime())
        label = w.get("label", start)
        if ok:
            run.append(label)
            era = era_of(start)
            if era != _UNMAPPED_ERA:
                eras.add(era)
        else:
            uncovered.append({"label": label, "reason": reason})
    return {"windows_total": len(windows), "windows_run": run,
            "fraction": round(len(run) / len(windows), 6), "eras": sorted(eras),
            "uncovered": uncovered}


def coverage_decision(coverage: dict) -> str | None:
    """None when the asset variant may run (full coverage, or D-042's
    partial-coverage floor met); else the not-run reason."""
    if coverage["windows_run"] and len(coverage["windows_run"]) == coverage["windows_total"]:
        return None
    n, total = len(coverage["windows_run"]), coverage["windows_total"]
    if coverage["fraction"] >= D042_MIN_WINDOW_COVERAGE and len(coverage["eras"]) >= D042_MIN_ERAS:
        return None
    return (f"{COVERAGE_REASON_PREFIX} the coin covers {n}/{total} protocol windows "
            f"({coverage['fraction']:.0%}) in {len(coverage['eras'])} era(s) {coverage['eras']} by the "
            f"Layer-1 precheck -- D-042 runs a partial-coverage asset variant only at >= "
            f"{D042_MIN_WINDOW_COVERAGE:.0%} of the windows and >= {D042_MIN_ERAS} eras; not run, "
            f"the idea is at best inconclusive")


def variant_protocol(source: dict, *, symbol: str, exchange: str | None = None,
                     windows_run: list | None = None) -> dict:
    """The per-variant protocol: `source` with symbols [symbol], `exchange`
    when given, and only the windows labelled in `windows_run` when given (in
    source order). Every other key byte-equal to the source."""
    out = copy.deepcopy(source)
    out["symbols"] = [symbol]
    if exchange is not None:
        out["exchange"] = exchange
    if windows_run is not None:
        keep = set(windows_run)
        out["windows"] = [w for w in out["windows"] if w.get("label", _window_bounds(w)[0]) in keep]
    return out


def check_variant_protocol(variant: dict, source: dict) -> list:
    """Why `variant` is not a faithful 5a derivation of `source` (empty = it
    is): one symbol; every key outside symbols/exchange/windows equal; windows a
    subsequence of the source's (same dicts, same order). The conformance
    check applies it to every executed per-variant protocol."""
    problems = []
    syms = variant.get("symbols")
    if not (isinstance(syms, list) and len(syms) == 1 and isinstance(syms[0], str) and syms[0]):
        problems.append(f"variant protocol symbols {syms!r} is not one symbol")
    for key in sorted((set(variant) | set(source)) - set(_VARIANT_KEYS)):
        if variant.get(key) != source.get(key):
            problems.append(f"variant protocol key {key!r} differs from the run protocol's")
    if "exchange" in source and "exchange" not in variant:
        problems.append("variant protocol dropped the run protocol's `exchange`")
    src_windows = source.get("windows") or []
    it = iter(src_windows)
    if not all(any(w == s for s in it) for w in (variant.get("windows") or [])):
        problems.append("variant protocol windows are not a subsequence of the run protocol's")
    if not variant.get("windows"):
        problems.append("variant protocol has no windows")
    return problems


def resolve_variant(entry: dict, *, source: dict, universe: dict, layer1: dict,
                    precheck, era_of) -> dict:
    """One per-coin variant_patches.yaml entry -> {"ok": True, "kind", "symbol",
    "protocol", "coverage" (asset only)} or {"ok": False, "kind", "symbol",
    "reason", "coverage" (when computed)}. A refusal reason starts with
    COIN_REASON_PREFIX (a malformed entry: an engineering / authoring fault) or
    COVERAGE_REASON_PREFIX (D-042: the coin covers too little)."""
    kind, symbol = entry.get("kind"), entry.get("symbol")
    patch = entry.get("patch") or []
    out = {"kind": kind, "symbol": symbol}

    def refuse(why):
        return {**out, "ok": False, "reason": f"{COIN_REASON_PREFIX} {why}"}

    if kind not in VARIANT_KINDS:
        return refuse(f"kind {kind!r} is not one of {VARIANT_KINDS} (every entry of a per-coin "
                      f"variant_patches.yaml declares its kind)")
    if symbol is not None and not (isinstance(symbol, str) and symbol):
        return refuse(f"symbol {symbol!r} is not a non-empty string")
    base = base_coin(source)
    if kind in ("base", "design"):
        if kind == "base" and (entry.get("variant_id") != "base" or patch):
            return refuse("the kind-base variant must be variant_id 'base' with an empty patch")
        if kind == "design" and not patch:
            return refuse("a design variant changes the config: its patch must not be empty")
        if symbol is not None and symbol != base:
            return refuse(f"a {kind} variant runs on the base coin {base!r} (the run protocol's "
                          f"symbols[0], G2), not {symbol!r}")
        out["symbol"] = base
        return {**out, "ok": True, "protocol": variant_protocol(source, symbol=base),
                "coverage": None}
    # asset (G3 + D-042)
    if patch:
        return refuse("an asset variant changes only the coin: its patch must be empty")
    if symbol is None:
        return refuse("an asset variant must name its coin (`symbol`)")
    base_cat, _ = coin_entry(universe, base)
    if base_cat is None:
        return refuse(f"the base coin {base!r} is not in config/coin_universe.yaml -- its category, "
                      f"which the asset coin must differ from, is unknown")
    cat, coin = coin_entry(universe, symbol)
    if cat is None:
        return refuse(f"{symbol!r} is not in config/coin_universe.yaml")
    if cat == base_cat:
        return refuse(f"{symbol!r} is in the base coin's own category {cat!r}; an asset variant "
                      f"uses a coin from a different category (card D)")
    exchange = coin.get("exchange") if isinstance(coin.get("exchange"), str) else None
    vsym = venue_symbol(coin)
    resolved_exchange = exchange or source.get("exchange") or "binance"  # dag.resolve_exchange order
    coverage = window_coverage(source, exchange=resolved_exchange, symbol=vsym, layer1=layer1,
                               precheck=precheck, era_of=era_of)
    coverage = {"venue_symbol": vsym, "exchange": resolved_exchange, **coverage}
    why = coverage_decision(coverage)
    if why is not None:
        return {**out, "ok": False, "reason": why, "coverage": coverage}
    full = len(coverage["windows_run"]) == coverage["windows_total"]
    proto = variant_protocol(source, symbol=vsym, exchange=exchange,
                             windows_run=None if full else coverage["windows_run"])
    return {**out, "ok": True, "protocol": proto, "coverage": coverage}
