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
    layer1_price_precheck, no network, no market data) plus a stricter
    listing-date rule of this module (a window counts only when the coin's
    Layer-1 earliest date is on or before the window's test.start, so a
    window straddling the listing is not covered) -- when it covers at
    least D042_MIN_WINDOW_COVERAGE of the protocol's windows. D-042's second
    condition (at least 2 eras) was dropped by the operator on 2026-09-28
    (D-045): the policy's eras are cut by data-feed availability, not market
    phase, and robustness across eras stays with the sign_consistent_by_era
    criterion. The eras a coin covers are still recorded in `coverage.eras`
    (information only, never a gate; a window's era is the era of its test
    period's midpoint). Below the share it is not run:
    `not_tested` with a reason starting COVERAGE_REASON_PREFIX, which the
    variant loop treats like a repeat skip (never a data or engineering
    shortfall, never blocking the idea or the other variants); the grid then
    lists it in `untested_variants`, so the idea is at best INCONCLUSIVE.
    Full coverage needs no threshold (it is not partial). The Layer-2 data
    gate's decline / refine of an asset variant is non-blocking the same way
    (LAYER2_COVERAGE_REASON_PREFIX, run_phase1_research's per-variant gate).

Not here (E-062 S2b): normalising the time-dependent profit bars (trade
minimum per year, drawdown scaled to the period) for a variant that ran on
fewer windows. The windows a variant ran on are recorded for it: its
protocol.json `windows` and, for an asset coin, the index entry's `coverage`.
TEMPORARY until then (D-042; lifted by E-062 S2b): a partial-coverage variant
(is_partial_coverage) is graded, but it caps the grid at inconclusive (never
`validated`) and its time-dependent bars (D042_TIME_DEPENDENT_BARS) read
NOT_EVALUABLE, so it can never pass the profit bars (never
`profit_bars_reached`).

5a records each variant protocol.json's sha256 in index.yaml
(`protocol_sha256`); verify_variant_protocol re-checks the file against it and
against its derivation before any backtest.

E-061 C2 S2c (G12): check_variant_shape -- the whole list Step 2 wrote (3-4
variants, one base, >= 1 design, 1-2 asset, no multi-coin variant), built on
resolve_variant's per-entry checks.

No lookahead: the only inputs are the protocol file, coin_universe.yaml, the
Layer-1 venue audit (config/venue_data_capability.yaml, structural venue facts)
and the policy's era boundaries -- no bar, no return, no result is read.

No file I/O except `load_protocol_file`; the Layer-1 precheck is passed in by
the caller (data_availability_gate imports trading-bot's DataManager at import
time, so this module does not import it).
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path

# D-042 (engineering/DECISION_LOG.md, 2026-09-28): an asset variant on partial
# coverage runs only if its coin covers at least this share of the protocol's
# windows; below it, it is not run. (D-042's former second condition, at least
# 2 policy eras, was dropped by the operator on 2026-09-28 -- D-045.)
D042_MIN_WINDOW_COVERAGE = 0.60

VARIANT_KINDS = ("base", "design", "asset")
VARIANT_PROTOCOL_FILENAME = "protocol.json"
# index.yaml `reason` prefix of an asset variant skipped for coverage (D-042).
COVERAGE_REASON_PREFIX = "insufficient_coverage:"
# The same skip when it is the Layer-2 data gate (a real data touch) that
# declines / refines an asset variant -- e.g. a coin with no per-coin Layer-1
# date, or with gaps Layer 1 cannot see, lacking data in some windows. It
# starts with COVERAGE_REASON_PREFIX, so it is read exactly like a 5a skip.
LAYER2_COVERAGE_REASON_PREFIX = f"{COVERAGE_REASON_PREFIX} layer2"
# D-042's time-dependent profit bars (config/profitability_bars.yaml names):
# the trade minimum and the drawdown limit, which E-062 S2b normalises to the
# period a variant ran on. Until then they read NOT_EVALUABLE for a
# partial-coverage variant (TEMPORARY, D-042; lifted by E-062 S2b).
D042_TIME_DEPENDENT_BARS = ("trade_count_min", "max_drawdown_pct_max")
# index.yaml `reason` prefix of a per-coin entry refused by 5a's coin checks.
COIN_REASON_PREFIX = "variant_coin:"
# era_id_for_timestamp's value outside every declared era: never counted.
_UNMAPPED_ERA = "era_unmapped"
# E-061 C2 S2c (C2_S1_FINDINGS.md G12, card D): the variant shape Step 2 must
# write under per-coin mode -- 3 or 4 variants: exactly one base, at least one
# design, one or two asset.
VARIANT_SHAPE_MIN, VARIANT_SHAPE_MAX = 3, 4
ASSET_VARIANTS_MIN, ASSET_VARIANTS_MAX = 1, 2
# A variant_id is used as a bare path segment by 5a (artifacts/variants/<id>/).
VARIANT_ID_PATTERN = r"[A-Za-z0-9_-]+"
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


def _window_label(window: dict):
    """A window's label, else its test start (the one fallback, everywhere)."""
    return window.get("label", _window_bounds(window)[0])


def _naive_utc(ts):
    """A pandas Timestamp, tz-naive UTC (a tz-aware one converted first)."""
    import pandas as pd
    t = pd.Timestamp(ts)
    return t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t


def layer1_earliest(layer1: dict, exchange: str, symbol: str):
    """The coin's Layer-1 earliest OHLCV date (venue_data_capability.yaml
    venues.<exchange>.spot.symbols.earliest_ohlcv_utc.<symbol>), or None when
    the audit records none for it (such a coin keeps the precheck's own reading;
    Kraken per-coin dates come from our local caches' first rows since PR #250,
    tools/refresh_coin_start_dates.py)."""
    spot = ((((layer1 or {}).get("venues") or {}).get(exchange) or {}).get("spot") or {})
    earliest = ((spot.get("symbols") or {}).get("earliest_ohlcv_utc") or {})
    value = earliest.get(symbol) if isinstance(earliest, dict) else None
    return value if isinstance(value, str) and value else None


def window_coverage(protocol: dict, *, exchange: str, symbol: str, layer1: dict,
                    precheck, era_of) -> dict:
    """Which protocol windows `symbol` on `exchange` could cover. `precheck(
    layer1, exchange, symbol, timeframe, start_dt, end_dt) -> (ok, reason)` is
    data_availability_gate.layer1_price_precheck; `era_of(ts) -> era_id`.

    A window counts only when the precheck passes AND -- this module's own,
    stricter listing rule (D-042) -- the coin's Layer-1 earliest date
    (layer1_earliest) is on or before the window's test.start: the precheck
    alone accepts a window that merely ends after the listing, i.e. one that
    straddles it and would run on a part-empty window. A coin with no Layer-1
    date keeps the precheck's reading. A window's era is the era of its test
    period's MIDPOINT (so a window just past an era boundary is not counted in
    the era it barely touches). Returns {windows_total, windows_run (labels, in
    protocol order), fraction, eras (sorted, era_unmapped excluded),
    uncovered: [{label, reason}]}."""
    windows = protocol.get("windows")
    if not isinstance(windows, list) or not windows:
        raise VariantCoinError("the run protocol has no `windows` list")
    timeframe = protocol.get("timeframe", "1h")  # run_protocol's own default
    earliest = layer1_earliest(layer1, exchange, symbol)
    earliest_ts = _naive_utc(earliest) if earliest is not None else None
    run, uncovered, eras = [], [], set()
    for w in windows:
        start, end = _window_bounds(w)
        start_ts, end_ts = _naive_utc(start), _naive_utc(end)
        ok, reason = precheck(layer1, exchange, symbol, timeframe,
                              start_ts.to_pydatetime(), end_ts.to_pydatetime())
        if ok and earliest_ts is not None and earliest_ts > start_ts:
            ok, reason = False, (
                f"window test.start {start} is before {symbol}'s Layer-1 earliest OHLCV date "
                f"{earliest} on {exchange}: the window straddles the listing, so part of it has "
                f"no data -- D-042 counts a window only when the coin exists for all of it")
        label = _window_label(w)
        if ok:
            run.append(label)
            era = era_of((start_ts + (end_ts - start_ts) / 2).isoformat())
            if era != _UNMAPPED_ERA:
                eras.add(era)
        else:
            uncovered.append({"label": label, "reason": reason})
    return {"windows_total": len(windows), "windows_run": run,
            "fraction": round(len(run) / len(windows), 6), "eras": sorted(eras),
            "uncovered": uncovered}


def coverage_decision(coverage: dict) -> str | None:
    """None when the asset variant may run (full coverage, or D-042's
    partial-coverage window share met); else the not-run reason. The eras it
    covers are never a gate (D-042's 2-era condition dropped by the operator
    2026-09-28, D-045) -- they appear in the reason as information only."""
    if coverage["windows_run"] and len(coverage["windows_run"]) == coverage["windows_total"]:
        return None
    n, total = len(coverage["windows_run"]), coverage["windows_total"]
    if n and coverage["fraction"] >= D042_MIN_WINDOW_COVERAGE:
        return None
    return (f"{COVERAGE_REASON_PREFIX} the coin covers {n}/{total} protocol windows "
            f"({coverage['fraction']:.0%}; era(s) {coverage.get('eras')}) by the Layer-1 precheck "
            f"and the listing date -- D-042 runs a partial-coverage asset variant only at >= "
            f"{D042_MIN_WINDOW_COVERAGE:.0%} of the windows; not run, the idea is at best "
            f"inconclusive")


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
        out["windows"] = [w for w in out["windows"] if _window_label(w) in keep]
    return out


def protocol_sha256(raw: bytes) -> str:
    """The sha256 5a records in index.yaml (`protocol_sha256`) for the exact
    bytes of a variant's protocol.json."""
    return hashlib.sha256(raw).hexdigest()


def is_partial_coverage(entry) -> bool:
    """True for a per-coin index entry whose coin ran on FEWER windows than
    the run protocol has (D-042 partial coverage: `coverage.windows_run`
    shorter than `coverage.windows_total`). A malformed coverage raises: a
    decision about grading must never read a broken record as "full".

    TEMPORARY consumer rule (D-042; lifted by E-062 S2b, which normalises the
    time-dependent bars): such a variant is graded, but it caps the grid at
    inconclusive and never passes the profit bars."""
    cov = entry.get("coverage") if isinstance(entry, dict) else None
    if cov is None:
        return False
    run, total = (cov.get("windows_run"), cov.get("windows_total")) if isinstance(cov, dict) \
        else (None, None)
    if not (isinstance(run, list) and isinstance(total, int) and not isinstance(total, bool)
            and 0 < len(run) <= total):
        raise VariantCoinError(f"index coverage {cov!r} has no usable windows_run / windows_total")
    return len(run) < total


def verify_variant_protocol(entry: dict, raw: bytes, source: dict, *, recheck=None) -> list:
    """Why a per-coin variant's protocol.json (its exact bytes `raw`) is not
    the file 5a wrote for index entry `entry` from run protocol `source`
    (empty = it is). Checked before any backtest (run_phase1_research's
    protocol_execution loop refuses the variant otherwise: no data touched, no
    trial row) and again by the conformance check:
      * the bytes' sha256 equals the index's `protocol_sha256`;
      * check_variant_protocol (one coin, every other key equal, windows a
        subsequence of the run protocol's);
      * base / design: symbols == [the base coin] and windows == the run
        protocol's windows EXACTLY (they never run on partial coverage);
      * asset: the window labels == the index's `coverage.windows_run`, the
        symbol == its `coverage.venue_symbol`, and D-042's decision on that
        recorded coverage admits it; with `recheck` (cov -> a freshly computed
        window_coverage for the same coin), the decision re-run on the fresh
        coverage admits it too and yields the same windows."""
    problems = []
    sha = entry.get("protocol_sha256")
    if not (isinstance(sha, str) and sha):
        problems.append("index.yaml records no protocol_sha256 for it (5a writes one for every "
                        "per-coin variant)")
    elif protocol_sha256(raw) != sha:
        problems.append("its protocol.json sha256 differs from the protocol_sha256 5a recorded in "
                        "index.yaml -- the file changed after 5a wrote it")
    try:
        variant = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        return problems + [f"its protocol.json is not valid JSON ({exc})"]
    if not isinstance(variant, dict):
        return problems + ["its protocol.json is not a JSON object"]
    problems += check_variant_protocol(variant, source)
    try:
        labels = [_window_label(w) for w in variant.get("windows") or []]
    except (VariantCoinError, AttributeError) as exc:
        return problems + [f"its windows are malformed ({exc})"]
    kind = entry.get("kind")
    if kind in ("base", "design"):
        base = base_coin(source)
        if variant.get("symbols") != [base]:
            problems.append(f"a {kind} variant runs on the base coin {base!r}, not "
                            f"{variant.get('symbols')!r}")
        if variant.get("windows") != source.get("windows"):
            problems.append(f"a {kind} variant runs every window of the run protocol; its "
                            f"windows {labels} are not the run protocol's")
    elif kind == "asset":
        cov = entry.get("coverage")
        if not isinstance(cov, dict):
            return problems + ["an asset variant's index entry has no coverage record"]
        if labels != cov.get("windows_run"):
            problems.append(f"its windows {labels} are not the index's coverage.windows_run "
                            f"{cov.get('windows_run')!r}")
        if variant.get("symbols") != [cov.get("venue_symbol")]:
            problems.append(f"its symbols {variant.get('symbols')!r} are not the index's "
                            f"coverage.venue_symbol {cov.get('venue_symbol')!r}")
        try:
            decided = coverage_decision(cov)
        except (KeyError, TypeError) as exc:
            return problems + [f"its index coverage is malformed ({type(exc).__name__}: {exc})"]
        if decided is not None:
            problems.append(f"D-042's decision on its recorded coverage does not admit it: {decided}")
        if recheck is not None:
            fresh = recheck(cov)
            again = coverage_decision(fresh)
            if again is not None:
                problems.append(f"D-042's decision re-run on a fresh coverage does not admit it: "
                                f"{again}")
            elif fresh["windows_run"] != cov.get("windows_run"):
                problems.append(f"a fresh coverage covers windows {fresh['windows_run']}, not the "
                                f"recorded {cov.get('windows_run')!r}")
    else:
        problems.append(f"index kind {kind!r} is not one of {VARIANT_KINDS}")
    return problems


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


def check_variant_shape(variants, *, source: dict, universe: dict, layer1: dict,
                        precheck, era_of) -> list:
    """E-061 C2 S2c (C2_S1_FINDINGS.md G12, card D): why a per-coin
    variant_patches.yaml `variants` list is not the shape Step 2 must write
    (empty = it is). Called after Step 2 and again before 5a's route lets the
    variants go on (run_phase1_research); the caller only calls it in per-coin
    mode, never for a composition run (G4: its variants are weighting schemes)
    -- or, review fix M1, once the run has produced a per-coin output: a list
    that is then no longer per-coin is refused ("per-coin fields (kind/symbol)
    missing").

      * 3 or 4 variants, each a mapping with a unique, safe `variant_id`;
      * exactly one `base`, at least one `design`, one or two `asset`;
      * G4: no multi-coin (cross-sectional) variant -- a `symbols` key, or a
        list in `symbol` -- since run_protocol.py backtests each coin alone;
      * each entry passes resolve_variant's own per-entry checks (kind, base
        = variant_id `base` with an empty patch, design = a non-empty patch on
        the base coin, asset = an empty patch and a coin_universe.yaml coin of
        another category). They are NOT repeated here: a refusal whose reason
        starts COIN_REASON_PREFIX is a shape problem.

    An asset coin refused ONLY for coverage (COVERAGE_REASON_PREFIX) is not a
    shape problem: D-042 (a binding operator decision) makes that variant untested --
    the idea at best inconclusive -- "instead of blocking the whole idea", and
    5a / the grid already do exactly that. The asset still counts in the kind
    tally, as the variant Step 2 wrote."""
    if not isinstance(variants, list) or not variants:
        return [f"`variants` must be a non-empty list, not {type(variants).__name__}"]
    if not per_coin_mode(variants):
        # Review fix M1: the caller only checks a non-per-coin list once the run
        # has already produced a per-coin output -- a retry that dropped them.
        return ["per-coin fields (kind/symbol) missing: every variant must declare its `kind` "
                "(base / design / asset) and an asset variant its `symbol` -- this run's "
                "variant_patches.yaml is per-coin, a legacy (coin-less) file is not accepted"]
    problems = []
    n = len(variants)
    if not VARIANT_SHAPE_MIN <= n <= VARIANT_SHAPE_MAX:
        problems.append(f"{n} variants: Step 2 writes {VARIANT_SHAPE_MIN} or {VARIANT_SHAPE_MAX} "
                        f"(exactly one base, at least one design, {ASSET_VARIANTS_MIN} or "
                        f"{ASSET_VARIANTS_MAX} asset)")
    kinds = {k: [] for k in VARIANT_KINDS}
    seen = set()
    for i, entry in enumerate(variants):
        where = f"variants[{i}]"
        if not isinstance(entry, dict):
            problems.append(f"{where} is not a mapping")
            continue
        vid = entry.get("variant_id")
        if not (isinstance(vid, str) and re.fullmatch(VARIANT_ID_PATTERN, vid)):
            problems.append(f"{where}: variant_id {vid!r} is not a safe bare identifier "
                            f"(letters, digits, '_', '-')")
        elif vid in seen:
            problems.append(f"{where}: duplicate variant_id {vid!r}")
        else:
            seen.add(vid)
            where = f"variant {vid!r}"
        if "symbols" in entry or isinstance(entry.get("symbol"), (list, tuple)):
            problems.append(f"{where}: a multi-coin (cross-sectional) variant is not built (G4) -- "
                            f"run_protocol.py backtests each coin alone; name ONE coin in `symbol`")
            continue
        res = resolve_variant(entry, source=source, universe=universe, layer1=layer1,
                              precheck=precheck, era_of=era_of)
        if not res["ok"] and str(res["reason"]).startswith(COIN_REASON_PREFIX):
            problems.append(f"{where}: {res['reason']}")
        if entry.get("kind") in VARIANT_KINDS:
            kinds[entry["kind"]].append(vid)
    if len(kinds["base"]) != 1:
        problems.append(f"{len(kinds['base'])} kind-base variant(s) {kinds['base']}: exactly one "
                        f"(variant_id 'base', empty patch)")
    if not kinds["design"]:
        problems.append("no kind-design variant: at least one (a non-empty patch, on the base coin)")
    if not ASSET_VARIANTS_MIN <= len(kinds["asset"]) <= ASSET_VARIANTS_MAX:
        problems.append(f"{len(kinds['asset'])} kind-asset variant(s) {kinds['asset']}: "
                        f"{ASSET_VARIANTS_MIN} or {ASSET_VARIANTS_MAX} (an empty patch, a "
                        f"coin_universe.yaml coin of another category than the base coin)")
    return problems
