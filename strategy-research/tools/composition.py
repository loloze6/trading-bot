"""
Composition assembly, the deterministic half (E-060 S3a; delivery_plan_v26.md
slice 7 items 7.2/7.3; spec: engineering/roadmap/E-060/S1_FINDINGS.md guesses
2, 3, 11, 12 and the operator decisions of 2026-09-26). Used only under
orchestrator.composition_runs.enabled: every public writer takes `enabled`
and raises CompositionError unless it is True, so nothing here can run while
the flag is off. S3b (R1 brief writer, 1a/1b composition mode, 5a check,
profit_bars grid source) is the caller; nothing calls this module yet.

What it does, given the block registry and ONE exact timeframe (operator
decision 3 -- only blocks with the SAME exact bar size are combined; the
selection is tools/composite_cache.forecast_blocks_on_timeframe, so a
timeframe-less block is excluded loudly and regime blocks never enter):

  1. weights for the three schemes (operator decision 2), code-computed:
       * equal       -- 1/N;
       * vol_scaled  -- proportional to 1/sigma of each block's stand-alone
                        DAILY returns (sample std, ddof=1);
       * ic_weighted -- proportional to each block's residual IC.
     E-060 S3b (code review fix 5, no lookahead): vol_scaled and ic_weighted
     are estimated PER COMPOSITE WINDOW from data strictly before that
     window's start (window_weight_schedule), equal where there is too little
     prior data; the pure scheme functions below are applied to that prior
     data. Missing inputs raise CompositionError (fail loud).
  2. the three variant configs -- `base` (equal), `vol_scaled`, `ic_weighted`
     -- each the SAME composite config except for the block weights:
     every block combined AS VALIDATED under the engine's opt-in block
     combiner (`strategies.regimes.unknown.blocks` + `block_standardisation`,
     trading-bot/strategies/strategy_engine.py): its components copied
     verbatim from its registry `config_fragment` (id prefixed with the
     block's config id so two blocks cannot collide; `lookback` pinned to the
     source engine's deque length), its source timing (required_bars,
     warmup, buffer length) and its source regime_detector as its own gate --
     a gated block abstains outside its validated regime(s). The composite's
     own detector is the trivial ungated pattern (§7e) that routes every bar
     to the combiner. Each block's FINAL forecast is standardised at
     combination time on its own past active values only (operator decision
     1), capped +-20, then weighted;
  3. a composition manifest listing every block, its components' pointers in
     the composite config, and its weight under each scheme;
  4. campaign_record/compositions.yaml (record_composition): locked, atomic,
     append-only; the read contract of tools/composite_cache.py
     (`registry_hash`, `base_config_ref`, `base_config_sha256`, timeframe).

E-060 S3b adds the pieces its callers need (run_campaign's R1 wiring, the
orchestrator's composition mode and 5a):
  5. load_block_daily_returns -- the stand-alone daily returns of one block,
     read from the run that validated it (fail loud when missing or short);
  6. variant_patches_from_manifest -- the code-written variant_patches.yaml
     (the three variants differ only in the block weights);
  7. check_composition_config -- the 5a check of a composite config against
     its composition manifest: every block present, gated and pinned as its
     source, no component outside the blocks, the scheme's weights within
     tolerance.

What it never does: register a composite as a block (the registry is not
touched -- guess 11), write a trial row, run a backtest, choose a run, or
read anything under local_data/holdout_sealed/.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re
import statistics
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

import composite_cache as _cc  # tools/ sibling (imports residual_ic -> trading-bot on sys.path)
import composition_names as _names  # tools/ sibling: the shared names (review fix 10)
import json_pointer as _jp  # tools/ sibling
import portfolio_daily as _pd  # tools/ sibling: the one daily-returns definition (fix 9)

SCHEMA_VERSION = 1
SCHEMES = ("equal", "vol_scaled", "ic_weighted")
# Variant id per scheme. `base` = equal weight: composite_cache reads the base
# variant's config as "the current composite" (S1 guess 4).
VARIANT_BY_SCHEME = {"equal": "base", "vol_scaled": "vol_scaled", "ic_weighted": "ic_weighted"}
COMPOSITE_REGIME = "unknown"  # the ungated pattern's regime (§7e)
# Block standardisation (engine key block_standardisation). target 10 = the
# forecast scale's target average absolute value (operator decision 1; design
# guide §5 "≈ average signal = 10"); window 500 = the design guide's
# ratio_to_mean normalisation window ("legacy parity: 500"); min_periods 30 =
# registry.TRANSFORM_MIN_PERIODS["ratio_to_mean"].
STANDARDISATION = {"target": 10.0, "window": 500, "min_periods": 30}
# A vol_scaled weight needs a sigma estimated on at least this many daily
# returns (same order as the residual-IC n_eff >= 30 floor). Placeholder.
MIN_DAILY_RETURNS = 30
MANIFEST_FILENAME = _names.MANIFEST_FILENAME
COMPOSITIONS_LOCK_FILENAME = ".compositions.lock"
COMPOSITION_ENTRY_FIELDS = (
    "registry_hash", "registry_revision", "timeframe", "timeframe_category", "block_ids",
    "base_config_ref", "base_config_sha256", "manifest_ref", "recorded_at",
)
_VOLATILE_ENTRY_FIELDS = frozenset({"recorded_at"})
_ALLOWED_TOP_KEYS = ("regime_detector", "strategies", "aux_feeds")
_ALLOWED_STRATEGY_KEYS = ("regimes", "warmup", "min_allocation_change")
# trading-bot strategies/strategy_engine.WEIGHT_SCHEDULE_KEY (E-060 S3b): the
# regime key carrying the per-window block weights.
WEIGHT_SCHEDULE_KEY = "weight_schedule"
_UNGATED_DETECTOR = {"mode": "threshold_rules", "components": [], "rules": [],
                     "default_regime": COMPOSITE_REGIME}


class CompositionError(ValueError):
    """A composition cannot be assembled or recorded. Never caught here."""


def _require_enabled(enabled) -> None:
    if enabled is not True:
        raise CompositionError("orchestrator.composition_runs is off -- composition assembly "
                               "runs only with the flag on (pass enabled=True from "
                               "run_phase1_research._composition_runs_enabled())")


def _normalise(raw: dict) -> dict:
    total = sum(raw.values())
    return {k: raw[k] / total for k in sorted(raw)}


# ---------------------------------------------------------------------------
# 1. weighting schemes
# ---------------------------------------------------------------------------

def _check_block_ids(block_ids) -> list:
    ids = list(block_ids)
    if len(ids) != len(set(ids)):
        raise CompositionError(f"duplicate block ids {ids}")
    if len(ids) < 2:
        raise CompositionError(f"a composition needs at least two blocks, got {len(ids)} "
                               f"({ids}) -- a single block is its own tested config")
    return ids


def equal_weights(block_ids) -> dict:
    ids = _check_block_ids(block_ids)
    return {b: 1.0 / len(ids) for b in sorted(ids)}


def daily_return_vol(returns, block_id: str = "?") -> float:
    """Sample std (ddof=1) of one block's stand-alone daily returns. Raises on
    a missing / short / non-finite / zero-variance series."""
    if returns is None:
        raise CompositionError(f"block {block_id!r}: no stand-alone daily return series")
    try:
        vals = [float(r) for r in returns]
    except (TypeError, ValueError) as exc:
        raise CompositionError(f"block {block_id!r}: daily returns are not numbers ({exc})") from exc
    if len(vals) < MIN_DAILY_RETURNS:
        raise CompositionError(f"block {block_id!r}: {len(vals)} daily return(s), at least "
                               f"{MIN_DAILY_RETURNS} are needed to estimate its volatility")
    if not all(math.isfinite(v) for v in vals):
        raise CompositionError(f"block {block_id!r}: non-finite daily return(s)")
    sigma = statistics.stdev(vals)
    if not math.isfinite(sigma) or sigma <= 0.0:
        raise CompositionError(f"block {block_id!r}: daily returns have no variance "
                               f"(sigma={sigma!r}) -- inverse volatility undefined")
    return sigma


def inverse_vol_weights(daily_returns_by_block: dict, block_ids) -> dict:
    """w_b proportional to 1 / sigma_b of block b's stand-alone daily returns
    (the block's own validating backtest, not the composite's)."""
    ids = _check_block_ids(block_ids)
    missing = [b for b in ids if b not in (daily_returns_by_block or {})]
    if missing:
        raise CompositionError(f"no stand-alone daily return series for block(s) {missing}")
    return _normalise({b: 1.0 / daily_return_vol(daily_returns_by_block[b], b) for b in ids})


def residual_ic_value(block: dict) -> float:
    """The registry's residual IC of one block, strictly positive and finite,
    else CompositionError."""
    bid = block.get("block_id")
    ric = block.get("residual_ic")
    if not isinstance(ric, dict):
        raise CompositionError(f"block {bid!r}: no residual IC in the registry (registered with "
                               f"orchestrator.composition_runs off?) -- ic_weighted undefined")
    if ric.get("fully_explained"):
        raise CompositionError(f"block {bid!r}: residual IC marked fully_explained -- the block "
                               f"adds nothing, it cannot carry an IC weight")
    v = ric.get("value")
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise CompositionError(f"block {bid!r}: residual IC value {v!r} is not a finite number")
    if v <= 0.0:
        raise CompositionError(f"block {bid!r}: residual IC {v!r} is zero or negative -- an "
                               f"IC-proportional weight would be zero or short the block")
    return float(v)


def ic_weights(blocks: list) -> dict:
    """w_b proportional to the registry residual IC of block b."""
    _check_block_ids([b.get("block_id") for b in blocks])
    return _normalise({b["block_id"]: residual_ic_value(b) for b in blocks})


def scheme_weights(blocks: list, daily_returns_by_block: dict) -> dict:
    """{scheme: {block_id: weight}} for the three schemes; weights sum to 1."""
    ids = [b.get("block_id") for b in blocks]
    return {"equal": equal_weights(ids),
            "vol_scaled": inverse_vol_weights(daily_returns_by_block, ids),
            "ic_weighted": ic_weights(blocks)}


# ---------------------------------------------------------------------------
# 2. assembling the composite config
# ---------------------------------------------------------------------------

def block_component_specs(block: dict) -> list:
    """[(source regime, component spec)] from a registry block's
    config_fragment. Supported pointer shapes (a forecast block's pieces):
    /strategies/regimes/<r> (a regime's `components`),
    /strategies/regimes/<r>/components (the list) and
    /strategies/regimes/<r>/components/<i> (one spec). Anything else -- a
    param-level pointer, a piece outside a named regime -- cannot be combined
    by code and raises."""
    bid = block.get("block_id")
    frag = block.get("config_fragment")
    if not isinstance(frag, dict) or not frag:
        raise CompositionError(f"block {bid!r}: empty or malformed config_fragment")
    out = []
    for ptr, value in frag.items():
        segs = _jp.split_json_pointer(ptr, error_cls=CompositionError)
        if len(segs) < 3 or segs[:2] != ["strategies", "regimes"]:
            raise CompositionError(f"block {bid!r}: pointer {ptr!r} is not inside a named regime")
        if len(segs) == 3:
            if not isinstance(value, dict) or set(value) != {"components"}:
                raise CompositionError(f"block {bid!r}: regime piece {ptr!r} must hold only "
                                       f"`components` (got keys {sorted(value or {})})")
            got = value["components"]
        elif len(segs) == 4 and segs[3] == "components":
            got = value
        elif len(segs) == 5 and segs[3] == "components" and segs[4].isdigit():
            got = [value]
        else:
            raise CompositionError(f"block {bid!r}: pointer {ptr!r} is below a component spec -- "
                                   f"code combines whole component specs only")
        if not isinstance(got, list) or not got or not all(isinstance(c, dict) for c in got):
            raise CompositionError(f"block {bid!r}: {ptr!r} holds no component spec list")
        for c in got:
            missing = [k for k in ("id", "class", "weight", "transforms") if k not in c]
            if missing:
                raise CompositionError(f"block {bid!r}: component {c.get('id')!r} lacks {missing}")
            out.append((segs[2], copy.deepcopy(c)))
    keys = [(r, c["id"]) for r, c in out]
    if len(keys) != len(set(keys)):
        raise CompositionError(f"block {bid!r}: a component appears twice in its fragment {keys}")
    return out


def _load_source_config(block: dict, root: Path) -> tuple:
    """(path, config) of the block's tested base config, sha-checked against
    the registry; top-level / strategies keys the writer cannot carry raise."""
    bid = block["block_id"]
    path = Path(root) / block["source_config_ref"]
    _cc._refuse_sealed(path)
    if not path.exists():
        raise CompositionError(f"block {bid!r}: source config {path} is missing")
    sha = _cc._canonical_config_sha256(path)
    if sha != block.get("source_config_sha256"):
        raise CompositionError(f"block {bid!r}: {path} sha256 {sha} differs from the registry's "
                               f"{block.get('source_config_sha256')} -- changed after it was tested")
    cfg = json.loads(path.read_text(encoding="utf-8"))
    extra = sorted(set(cfg) - set(_ALLOWED_TOP_KEYS))
    extra_s = sorted(set(cfg.get("strategies") or {}) - set(_ALLOWED_STRATEGY_KEYS))
    if extra or extra_s:
        raise CompositionError(f"block {bid!r}: source config carries key(s) {extra + extra_s} "
                               f"the composition writer does not know how to merge")
    return path, cfg


def assemble_block(block: dict, cbid: str, root: Path) -> dict:
    """One block AS VALIDATED:
      * each component spec copied verbatim, id prefixed with `cbid`, and its
        `lookback` pinned to the deque length its SOURCE engine used;
      * `source`: the source AdvancedStrategy's required_bars, strategy-engine
        warmup and buffer length, the source regime_detector (the block's own
        gate) and `parts` {source regime: [component ids]};
      * every part must be the WHOLE component list of that source regime, so
        the part's forecast is exactly the source's forecast in that regime.
    The numbers are read from a real AdvancedStrategy built on the source
    config, not re-derived. Memoised per process by (block_id, source config
    sha256, config block id, root) -- code review fix 8: 5a checks three
    variants of the same blocks; the source config is sha-checked on the
    first build and a different sha is a different key."""
    key = (block.get("block_id"), block.get("source_config_sha256"), cbid, str(Path(root).resolve()))
    if key not in _ASSEMBLED:
        _ASSEMBLED[key] = _assemble_block(block, cbid, root)
    return copy.deepcopy(_ASSEMBLED[key])


_ASSEMBLED: dict = {}


def _assemble_block(block: dict, cbid: str, root: Path) -> dict:
    from strategies.main_strategy import AdvancedStrategy  # trading-bot/ on sys.path
    bid = block["block_id"]
    path, src_cfg = _load_source_config(block, root)
    pieces = block_component_specs(block)
    src = AdvancedStrategy(config_path=str(path))
    se = src.strategy_engine
    src_regimes = src_cfg["strategies"].get("regimes") or {}
    parts, comps = {}, []
    for regime, spec in pieces:
        src_ids = [c["id"] for c in (src_regimes.get(regime) or {}).get("components", [])]
        if spec["id"] not in src_ids:
            raise CompositionError(f"block {bid!r}: component {spec['id']!r} is not in its source "
                                   f"config's regime {regime!r}")
        new = copy.deepcopy(spec)
        new["lookback"] = se._history[regime][spec["id"]].maxlen
        new["id"] = f"{cbid}__{spec['id']}"
        comps.append(new)
        parts.setdefault(regime, []).append((spec["id"], new["id"]))
    for regime, pairs in parts.items():
        src_ids = [c["id"] for c in src_regimes[regime]["components"]]
        if sorted(o for o, _n in pairs) != sorted(src_ids):
            raise CompositionError(
                f"block {bid!r}: its fragment holds {sorted(o for o, _n in pairs)} of source regime "
                f"{regime!r}, whose forecast is made of {sorted(src_ids)} -- the block's validated "
                f"forecast cannot be reproduced from a partial regime")
    return {"block_id": bid, "config_block_id": cbid, "components": comps,
            "source": {"required_bars": int(src.required_bars),
                       "warmup": int(se._warmup),
                       "buffer_bars": int(src.data_buffer.max_size),
                       "regime_detector": copy.deepcopy(src_cfg["regime_detector"]),
                       "parts": {r: [n for _o, n in pairs] for r, pairs in sorted(parts.items())}},
            "scaffolding": {"aux_feeds": list(src_cfg.get("aux_feeds") or []),
                            "min_allocation_change":
                                (src_cfg.get("strategies") or {}).get("min_allocation_change")}}


def _feed_name(entry):
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict) and isinstance(entry.get("name"), str):
        return entry["name"]
    raise CompositionError(f"aux_feeds entry {entry!r} has no name")


def _merge_scaffolding(parts: dict) -> dict:
    """aux_feeds: union by feed name; the same name declared differently by two
    blocks raises (never duplicated, never last-wins). min_allocation_change:
    all blocks must agree."""
    feeds, by_name = [], {}
    for bid in sorted(parts):
        for f in parts[bid]["aux_feeds"]:
            name = _feed_name(f)
            if name in by_name:
                if json.dumps(by_name[name][1], sort_keys=True) != json.dumps(f, sort_keys=True):
                    raise CompositionError(
                        f"blocks {by_name[name][0]!r} and {bid!r} declare aux feed {name!r} "
                        f"differently ({by_name[name][1]!r} vs {f!r}) -- a person decides")
                continue
            by_name[name] = (bid, f)
            feeds.append(copy.deepcopy(f))
    macs = {json.dumps(p["min_allocation_change"]) for p in parts.values()}
    if len(macs) > 1:
        raise CompositionError(f"blocks disagree on strategies.min_allocation_change "
                               f"({ {b: p['min_allocation_change'] for b, p in parts.items()} })"
                               f" -- a person decides")
    return {"aux_feeds": feeds,
            "min_allocation_change": next(iter(parts.values()))["min_allocation_change"]}


def assemble_composite_config(assembled: list, weights: dict, scaffolding: dict,
                              schedule: list | None = None) -> dict:
    """The composite config for one weighting. `assembled`: assemble_block()
    results in config order; `weights`: {block_id: w} (the blocks' own
    `weight`, used before the first schedule entry); `schedule` (E-060 S3b):
    [{from, weights: {block_id: w}}] -> the regime's `weight_schedule`, keyed
    by config block id. The composite's own detector is the trivial ungated
    one (every bar -> `unknown`); each block is gated by its OWN source
    detector inside the engine's block combiner."""
    comps, blocks = [], []
    for a in assembled:
        comps.extend(copy.deepcopy(a["components"]))
        blocks.append({"id": a["config_block_id"], "weight": weights[a["block_id"]],
                       "components": [c["id"] for c in a["components"]],
                       "source": copy.deepcopy(a["source"])})
    strategies: dict = {}
    if scaffolding["min_allocation_change"] is not None:
        strategies["min_allocation_change"] = scaffolding["min_allocation_change"]
    regime = {"components": comps, "blocks": blocks,
              "block_standardisation": dict(STANDARDISATION)}
    if schedule:
        cbid = {a["block_id"]: a["config_block_id"] for a in assembled}
        regime[WEIGHT_SCHEDULE_KEY] = [
            {"from": e["from"], "weights": {cbid[b]: w for b, w in sorted(e["weights"].items())}}
            for e in schedule]
    strategies["regimes"] = {
        COMPOSITE_REGIME: regime,
        "trending": None, "mean_reversion": None, "chop": None,
    }
    cfg = {"regime_detector": copy.deepcopy(_UNGATED_DETECTOR), "strategies": strategies}
    if scaffolding["aux_feeds"]:
        cfg["aux_feeds"] = copy.deepcopy(scaffolding["aux_feeds"])
    return cfg


def _validate_engine_config(cfg: dict, where: str) -> None:
    """trading-bot/tools/validate_config.py (V1-V13; V13 = the block combiner),
    loaded by file path (`tools` is also this directory's name, so a package
    import could resolve to the wrong one)."""
    import importlib.util
    path = Path(_cc._ric._TBOT) / "tools" / "validate_config.py"
    spec = importlib.util.spec_from_file_location("_tbot_validate_config", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    errs = mod.validate(cfg)
    if errs:
        raise CompositionError(f"{where}: composite config fails validate_config: {errs}")


def _write_bytes_once(path: Path, data: bytes) -> None:
    """Write `data`, or accept an identical existing file; different bytes raise."""
    if path.exists():
        if path.read_bytes() != data:
            raise CompositionError(f"{path} exists with different content -- refusing to "
                                   f"overwrite a written composition")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def _as_date(x) -> date:
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x
    try:
        return date.fromisoformat(str(x).strip()[:10])
    except ValueError as exc:
        raise CompositionError(f"{x!r} is not an ISO date") from exc


def window_weight_schedule(scheme: str, blocks: list, window_starts, *,
                           daily_returns_by_block: dict | None = None, prior_ic=None) -> list:
    """[{from, weights: {block_id: w}, basis}] for `vol_scaled` or
    `ic_weighted`: one entry per composite window start d (sorted, unique).

    WHY THIS CANNOT LEAK (CLAUDE.fork.md hard rule 3; code review fix 5): the
    weights of the entry dated d are estimated ONLY from data strictly before
    d -- vol_scaled from each block's stand-alone daily returns dated < d
    (a return dated D is the change to D's last close, all of it before d);
    ic_weighted from each block's residual IC recomputed on bars whose next
    return is realised before d (prior_ic(block, d), see
    load_block_prior_residual_ic). The engine applies the entry only to bars
    on or after d (trading-bot strategy_engine weight_schedule). A window
    with too little prior data (the first one always) gets EQUAL weights, and
    the entry records why (`basis.estimated: false`). Data inside or after a
    window can therefore never change that window's weights."""
    ids = sorted(b["block_id"] for b in blocks)
    _check_block_ids(ids)
    equal = equal_weights(ids)
    out = []
    for d in sorted({_as_date(s) for s in window_starts}):
        weights, basis = equal, None
        if scheme == "vol_scaled":
            prior = {b: [r for day, r in daily_returns_by_block[b] if _as_date(day) < d]
                     for b in ids}
            short = {b: len(v) for b, v in prior.items() if len(v) < MIN_DAILY_RETURNS}
            if short:
                basis = {"estimated": False,
                         "reason": f"fewer than {MIN_DAILY_RETURNS} stand-alone daily returns "
                                   f"before {d}: {short} -- equal weights"}
            else:
                try:
                    weights = inverse_vol_weights(prior, ids)
                    basis = {"estimated": True, "data_before": d.isoformat(),
                             "n_daily_returns": {b: len(v) for b, v in prior.items()}}
                except CompositionError as exc:
                    basis = {"estimated": False, "reason": f"{exc} -- equal weights"}
        elif scheme == "ic_weighted":
            diags = {b["block_id"]: prior_ic(b, d) for b in blocks}
            bad = {b: _prior_ic_problem(diag) for b, diag in diags.items()}
            bad = {b: why for b, why in bad.items() if why}
            if bad:
                basis = {"estimated": False,
                         "reason": f"no usable residual IC before {d}: {bad} -- equal weights"}
            else:
                weights = _normalise({b: float(diags[b]["value"]) for b in ids})
                basis = {"estimated": True, "data_before": d.isoformat(),
                         "residual_ic": {b: diags[b]["value"] for b in ids},
                         "n_eff": {b: diags[b]["n_eff"] for b in ids}}
        else:
            raise CompositionError(f"no weight schedule for scheme {scheme!r}")
        out.append({"from": d.isoformat(), "weights": dict(weights), "basis": basis})
    return out


# A per-window residual IC is used as an ic_weighted weight only above the
# residual-IC criterion's own n_eff floor (config/criterion_menu.yaml
# residual_ic floor.min_n_eff = 30). Placeholder, mirrored from that entry.
MIN_PRIOR_IC_N_EFF = 30


def _prior_ic_problem(diag) -> str | None:
    if not isinstance(diag, dict):
        return "no measurement"
    if diag.get("fully_explained"):
        return "fully explained by the composite"
    v, n = diag.get("value"), diag.get("n_eff")
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        return diag.get("reason") or "value not a number"
    if v <= 0:
        return f"value {v} <= 0"
    if not isinstance(n, int) or n < MIN_PRIOR_IC_N_EFF:
        return f"n_eff {n} < {MIN_PRIOR_IC_N_EFF}"
    return None


def write_composition_variants(registry_doc: dict, timeframe, out_dir: Path, *, root: Path,
                               daily_returns_by_block: dict, window_starts, prior_ic,
                               enabled) -> dict:
    """Write <out_dir>/{base,vol_scaled,ic_weighted}.json and
    <out_dir>/composition_manifest.yaml for the forecast blocks registered on
    exactly `timeframe`. Returns the manifest. Raises CompositionError on any
    degenerate input before writing anything.
    `daily_returns_by_block`: {block_id: [(date, return)]} (load_block_daily_returns);
    `window_starts`: the composite protocol's window test starts;
    `prior_ic`: callable(block, date) -> residual-IC diagnostic on data before
    that date (load_block_prior_residual_ic). `base` is equal weight; the
    other two carry the per-window weight_schedule (window_weight_schedule --
    no lookahead), their blocks' own weight being equal (before any entry)."""
    _require_enabled(enabled)
    root, out_dir = Path(root), Path(out_dir)
    _cc._refuse_sealed(out_dir)
    blocks, excluded = _cc.forecast_blocks_on_timeframe(registry_doc, timeframe)
    blocks = sorted(blocks, key=lambda b: b["block_id"])
    ids = _check_block_ids([b["block_id"] for b in blocks])  # raises for < 2 blocks
    missing = [b for b in ids if b not in (daily_returns_by_block or {})]
    if missing:
        raise CompositionError(f"no stand-alone daily return series for block(s) {missing}")
    if not list(window_starts or []):
        raise CompositionError("no composite window start dates -- the per-window weights "
                               "cannot be placed")
    equal = equal_weights(ids)
    schedules = {"equal": [],
                 "vol_scaled": window_weight_schedule(
                     "vol_scaled", blocks, window_starts,
                     daily_returns_by_block=daily_returns_by_block),
                 "ic_weighted": window_weight_schedule("ic_weighted", blocks, window_starts,
                                                       prior_ic=prior_ic)}
    assembled, parts, manifest_blocks = [], {}, []
    for k, block in enumerate(blocks):
        bid = block["block_id"]
        a = assemble_block(block, f"b{k}", root)
        assembled.append(a)
        parts[bid] = a["scaffolding"]
        ric = block.get("residual_ic")
        manifest_blocks.append({"block_id": bid, "config_block_id": a["config_block_id"],
                                "source_config_ref": block["source_config_ref"],
                                "source_config_sha256": block["source_config_sha256"],
                                "source_regimes": sorted(a["source"]["parts"]),
                                "source_required_bars": a["source"]["required_bars"],
                                "source_warmup": a["source"]["warmup"],
                                "component_ids": [c["id"] for c in a["components"]],
                                "registry_residual_ic": (ric.get("value")
                                                         if isinstance(ric, dict) else None),
                                "n_daily_returns": len(daily_returns_by_block[bid])})
    scaffolding = _merge_scaffolding(parts)
    configs = {}
    for scheme in SCHEMES:
        vid = VARIANT_BY_SCHEME[scheme]
        cfg = assemble_composite_config(assembled, equal, scaffolding,
                                        [{"from": e["from"], "weights": e["weights"]}
                                         for e in schedules[scheme]])
        _validate_engine_config(cfg, f"variant {vid}")
        configs[vid] = cfg
    # pointers of each block's components in the composite config (same in every variant)
    pos = 0
    for mb in manifest_blocks:
        n = len(mb["component_ids"])
        mb["config_paths"] = [f"/strategies/regimes/{COMPOSITE_REGIME}/components/{i}"
                              for i in range(pos, pos + n)]
        pos += n
    variants, payloads = {}, {}
    for scheme in SCHEMES:
        vid = VARIANT_BY_SCHEME[scheme]
        path = out_dir / f"{vid}.json"
        payloads[path] = (json.dumps(configs[vid], indent=2) + "\n").encode("utf-8")
        canon = json.dumps(configs[vid], sort_keys=True).encode("utf-8")
        variants[vid] = {"scheme": scheme, "config_ref": _rel(path, root),
                         "config_sha256": hashlib.sha256(canon).hexdigest(),
                         "weights": dict(equal), "weight_schedule": schedules[scheme]}
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "kind": "composition",
        "registry_hash": _cc.composite_registry_hash(blocks),
        "registry_revision": registry_doc.get("revision"),
        "timeframe": timeframe,
        "timeframe_category": _cc.timeframe_category(timeframe),
        "composite_regime": COMPOSITE_REGIME,
        "standardisation": dict(STANDARDISATION),
        "blocks": manifest_blocks,
        "excluded_blocks": excluded,
        "scaffolding": ["/regime_detector", "/strategies/regimes/trending",
                        "/strategies/regimes/mean_reversion", "/strategies/regimes/chop",
                        f"/strategies/regimes/{COMPOSITE_REGIME}/blocks",
                        f"/strategies/regimes/{COMPOSITE_REGIME}/block_standardisation",
                        f"/strategies/regimes/{COMPOSITE_REGIME}/{WEIGHT_SCHEDULE_KEY}"]
                       + (["/strategies/min_allocation_change"]
                          if scaffolding["min_allocation_change"] is not None else [])
                       + (["/aux_feeds"] if scaffolding["aux_feeds"] else []),
        "variants": variants,
        "rationale": ("code-written composition (E-060 S3a/S3b): same-timeframe registry forecast "
                      "blocks, each run as validated (gated by its own source detector, its "
                      "source lookbacks and warm-up), each block's final forecast "
                      "standardised past-only (value / mean |past active values| x target, "
                      "capped +-20) at combination time, then weighted by the scheme. The "
                      "variants differ only in the block weights; vol_scaled and ic_weighted "
                      "weights change per composite window and are estimated only from data "
                      "before that window (equal weights where there is too little). "
                      "A composite never registers as a block."),
    }
    payloads[out_dir / MANIFEST_FILENAME] = yaml.safe_dump(manifest, sort_keys=False).encode("utf-8")
    clash = [str(p) for p, data in payloads.items() if p.exists() and p.read_bytes() != data]
    if clash:
        raise CompositionError(f"{clash} exist with different content -- refusing to overwrite "
                               f"a written composition (nothing written)")
    for p, data in payloads.items():
        _write_bytes_once(p, data)
    for vid, v in variants.items():  # what was written hashes to what the manifest records
        if _cc._canonical_config_sha256(out_dir / f"{vid}.json") != v["config_sha256"]:
            raise CompositionError(f"{vid}.json: written config does not hash to its manifest sha")
    return manifest


def _rel(path: Path, root: Path) -> str:
    try:
        return Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError as exc:
        raise CompositionError(f"{path} is not under root {root}") from exc


# ---------------------------------------------------------------------------
# 4. campaign_record/compositions.yaml
# ---------------------------------------------------------------------------

def composition_entry(manifest: dict, manifest_ref: str, recorded_at: str | None = None) -> dict:
    """The compositions.yaml entry for a written manifest."""
    base = manifest["variants"][VARIANT_BY_SCHEME["equal"]]
    return {"registry_hash": manifest["registry_hash"],
            "registry_revision": manifest["registry_revision"],
            "timeframe": manifest["timeframe"],
            "timeframe_category": manifest["timeframe_category"],
            "block_ids": [b["block_id"] for b in manifest["blocks"]],
            "base_config_ref": base["config_ref"],
            "base_config_sha256": base["config_sha256"],
            "manifest_ref": manifest_ref,
            "recorded_at": recorded_at or datetime.now(timezone.utc).isoformat()}


def validate_composition_entry(entry, *, root: Path) -> dict:
    """Every field present, no other; base_config_sha256 equals the canonical
    sha256 of the file at base_config_ref (composite_cache checks the same)."""
    if not isinstance(entry, dict):
        raise CompositionError(f"compositions entry must be a mapping, got {entry!r}")
    missing = [f for f in COMPOSITION_ENTRY_FIELDS if entry.get(f) in (None, "", [])]
    extra = sorted(set(entry) - set(COMPOSITION_ENTRY_FIELDS))
    if missing or extra:
        raise CompositionError(f"compositions entry missing/empty {missing} / unknown {extra}")
    if _cc.timeframe_category(entry["timeframe"]) != entry["timeframe_category"]:
        raise CompositionError(f"timeframe {entry['timeframe']!r} is not category "
                               f"{entry['timeframe_category']!r}")
    path = Path(root) / entry["base_config_ref"]
    _cc._refuse_sealed(path)
    if not path.exists():
        raise CompositionError(f"base config {path} is missing")
    sha = _cc._canonical_config_sha256(path)
    if sha != entry["base_config_sha256"]:
        raise CompositionError(f"{path}: sha256 {sha} differs from base_config_sha256 "
                               f"{entry['base_config_sha256']}")
    return entry


def record_composition(path: Path, entry: dict, *, root: Path, enabled) -> bool:
    """Append `entry` to compositions.yaml under the lock (atomic write).
    Returns True when appended, False when an identical entry (all fields but
    recorded_at) already exists. An entry with the same registry_hash and
    different content raises: append-only, a person decides."""
    _require_enabled(enabled)
    import campaign_memory as _cm  # tools/ sibling: lock + atomic write primitives
    validate_composition_entry(entry, root=root)
    path = Path(path)
    stable = {k: v for k, v in entry.items() if k not in _VOLATILE_ENTRY_FIELDS}
    with _cm._file_lock(path.parent / COMPOSITIONS_LOCK_FILENAME, "compositions.yaml",
                        error_cls=CompositionError):
        if path.exists():
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
            if (not isinstance(doc, dict) or doc.get("schema_version") != SCHEMA_VERSION
                    or not isinstance(doc.get("compositions"), list)):
                raise CompositionError(f"{path}: expected {{schema_version: {SCHEMA_VERSION}, "
                                       f"compositions: [...]}}")
        else:
            doc = {"schema_version": SCHEMA_VERSION, "updated_at": None, "compositions": []}
        for old in doc["compositions"]:
            if isinstance(old, dict) and old.get("registry_hash") == entry["registry_hash"]:
                if {k: v for k, v in old.items() if k not in _VOLATILE_ENTRY_FIELDS} == stable:
                    return False
                raise CompositionError(f"{path}: registry_hash {entry['registry_hash']} is "
                                       f"already recorded with different content -- "
                                       f"append-only, a person decides")
        doc["compositions"].append(dict(entry))
        doc["updated_at"] = datetime.now(timezone.utc).isoformat()
        _cm._atomic_write(path, doc)
    return True


# ---------------------------------------------------------------------------
# 4b. failure rows in compositions.yaml (E-060 S3b code review fix 2)
# ---------------------------------------------------------------------------

FAILURE_FIELDS = ("registry_hash", "timeframe", "entry_id", "reason", "recorded_at", "resolved")


def record_composition_failure(path: Path, *, registry_hash: str, timeframe, entry_id: str,
                               reason: str, enabled) -> dict:
    """Append a failure row {registry_hash, timeframe, entry_id, reason,
    recorded_at, resolved: false} to compositions.yaml's `failures` list
    (locked, atomic). R1 treats an unresolved row for a block set as fired:
    it never re-fires that set by itself. The operator resolves it by setting
    `resolved: true` (R1 may then fire the same set again); a new block-set
    revision (another registry_hash) fires regardless. A row for the same
    entry_id already present is left as it is (a retried decision)."""
    _require_enabled(enabled)
    import campaign_memory as _cm
    path = Path(path)
    row = {"registry_hash": registry_hash, "timeframe": timeframe, "entry_id": entry_id,
           "reason": str(reason)[:2000], "recorded_at": datetime.now(timezone.utc).isoformat(),
           "resolved": False}
    with _cm._file_lock(path.parent / COMPOSITIONS_LOCK_FILENAME, "compositions.yaml",
                        error_cls=CompositionError):
        if path.exists():
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
            if (not isinstance(doc, dict) or doc.get("schema_version") != SCHEMA_VERSION
                    or not isinstance(doc.get("compositions"), list)):
                raise CompositionError(f"{path}: expected {{schema_version: {SCHEMA_VERSION}, "
                                       f"compositions: [...]}}")
        else:
            doc = {"schema_version": SCHEMA_VERSION, "updated_at": None, "compositions": []}
        failures = doc.setdefault("failures", [])
        if not isinstance(failures, list):
            raise CompositionError(f"{path}: `failures` is not a list")
        if any(isinstance(f, dict) and f.get("entry_id") == entry_id for f in failures):
            return next(f for f in failures if f.get("entry_id") == entry_id)
        failures.append(row)
        doc["updated_at"] = datetime.now(timezone.utc).isoformat()
        _cm._atomic_write(path, doc)
    return row


def load_composition_failures(path: Path) -> list:
    """compositions.yaml's `failures` rows ([] when the file or key is absent)."""
    path = Path(path)
    if not path.exists():
        return []
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    rows = (doc or {}).get("failures") if isinstance(doc, dict) else None
    if rows is None:
        return []
    if not isinstance(rows, list):
        raise CompositionError(f"{path}: `failures` is not a list")
    return [r for r in rows if isinstance(r, dict)]


# ---------------------------------------------------------------------------
# 5. stand-alone daily returns and prior residual IC of a block (E-060 S3b)
# ---------------------------------------------------------------------------

_SOURCE_VARIANT_CONFIG_RE = re.compile(
    r"^runs/(?P<run>[A-Za-z0-9_-]+)/artifacts/variants/(?P<vid>[A-Za-z0-9_-]+)/strategy_config\.json$")


def _validating_variant(block: dict, root: Path) -> tuple:
    """(run_dir, variant_id, protocol_result) of the base variant that
    validated `block` -- the variant its registry source_config_ref names --
    with the source config sha-checked. Raises CompositionError."""
    bid = block.get("block_id")
    ref = str(block.get("source_config_ref") or "").replace("\\", "/")
    m = _SOURCE_VARIANT_CONFIG_RE.match(ref)
    if not m:
        raise CompositionError(f"block {bid!r}: source_config_ref {ref!r} is not "
                               f"runs/<run>/artifacts/variants/<variant>/strategy_config.json -- "
                               f"its validating run's per-variant results cannot be located")
    run, vid = m.group("run"), m.group("vid")
    if run != block.get("validated_by_run"):
        raise CompositionError(f"block {bid!r}: source_config_ref names {run!r}, the block was "
                               f"validated by {block.get('validated_by_run')!r}")
    cfg_path = Path(root) / ref
    _cc._refuse_sealed(cfg_path)
    if not cfg_path.exists():
        raise CompositionError(f"block {bid!r}: source config {cfg_path} is missing")
    if _cc._canonical_config_sha256(cfg_path) != block.get("source_config_sha256"):
        raise CompositionError(f"block {bid!r}: {cfg_path} changed after it was validated")
    run_dir = Path(root) / "runs" / run
    pr_path = run_dir / "artifacts" / "variants" / vid / "protocol_result.yaml"
    if not pr_path.exists():
        raise CompositionError(f"block {bid!r}: {pr_path} is missing -- no stand-alone returns")
    pr = yaml.safe_load(pr_path.read_text(encoding="utf-8"))
    if not isinstance(pr, dict) or not isinstance(pr.get("results"), list) or not pr["results"]:
        raise CompositionError(f"block {bid!r}: {pr_path} has no per-window results")
    return run_dir, vid, pr


def load_block_daily_returns(block: dict, *, root: Path) -> list:
    """[(UTC date, return)]: the block's stand-alone daily returns -- the
    equal-weight portfolio of every coin of the base variant that VALIDATED
    it, with the profit bars' own definition (tools/portfolio_daily.py, the
    one shared helper: code review fix 9). Every missing file, malformed row,
    coin-set mismatch or thin window raises CompositionError -- as does a
    series shorter than MIN_DAILY_RETURNS. Dated, so each composite window's
    vol_scaled weights use only the returns before it (window_weight_schedule)."""
    bid = block.get("block_id")
    run_dir, vid, pr = _validating_variant(block, root)
    try:
        returns = _pd.portfolio_daily_returns(run_dir, pr)
    except ValueError as exc:  # PortfolioNotEvaluable included
        raise CompositionError(f"block {bid!r}: stand-alone returns of {run_dir.name}/{vid}: "
                               f"{exc}") from exc
    if len(returns) < MIN_DAILY_RETURNS:
        raise CompositionError(f"block {bid!r}: {len(returns)} stand-alone daily return(s) in "
                               f"{run_dir.name}/{vid}, at least {MIN_DAILY_RETURNS} are needed to "
                               f"estimate its volatility")
    return returns


def load_daily_returns_by_block(blocks: list, *, root: Path) -> dict:
    """{block_id: load_block_daily_returns(block)} -- raises on the first bad block."""
    return {b["block_id"]: load_block_daily_returns(b, root=root) for b in blocks}


def _results_dir(run_dir: Path, pr: dict, bid) -> Path:
    """The results/ directory holding every window of `pr` (located through
    portfolio_daily.find_window_equity_file, never a hard-coded path)."""
    dirs = set()
    for r in pr.get("results") or []:
        path = _pd.find_window_equity_file(run_dir, str((r or {}).get("run_id")))
        if path is None:
            raise CompositionError(f"block {bid!r}: no results for window run "
                                   f"{(r or {}).get('run_id')!r} under {run_dir}")
        dirs.add(path.parent.parent)
    if len(dirs) != 1:
        raise CompositionError(f"block {bid!r}: its windows' results sit in {sorted(map(str, dirs))}")
    return dirs.pop()


def load_block_prior_residual_ic(block: dict, before, *, root: Path, timeframe) -> dict:
    """The block's residual IC measured ONLY on bars whose next return is
    realised before `before` (00:00 UTC): its validating run's base-variant
    forecasts, residualised against the composite it was measured against at
    registration (artifacts/residual_ic.yaml: none / block / composition, the
    S2 cache), recomputed on the prefix with tools/residual_ic (past-only
    expanding fit). A bar at t enters only if t + 2 bars <= `before`, whatever
    the timestamp convention (open or close stamp). A composite that was stale
    at registration gives no measurement (the caller then uses equal weights).
    Missing artifacts raise CompositionError."""
    import pandas as pd
    import residual_ic as _ric
    import timeframe as _tf
    bid = block.get("block_id")
    run_dir, vid, pr = _validating_variant(block, root)
    ric_path = run_dir / "artifacts" / "residual_ic.yaml"
    if not ric_path.exists():
        raise CompositionError(f"block {bid!r}: {ric_path} is missing -- its residual IC basis "
                               f"is unknown")
    doc = yaml.safe_load(ric_path.read_text(encoding="utf-8")) or {}
    kind = ((doc.get("composite") or {}) if isinstance(doc.get("composite"), dict) else {}).get("kind")
    if doc.get("skipped") or kind not in ("none", "block", "composition", "stale"):
        raise CompositionError(f"block {bid!r}: {ric_path} has no usable composite basis "
                               f"(skipped={doc.get('skipped')!r}, kind={kind!r})")
    if kind == "stale":
        return {"value": None, "n_eff": None, "reason": "composite was stale at registration"}
    cutoff = pd.Timestamp(_as_date(before)).tz_localize("UTC")
    step = pd.Timedelta(seconds=_tf.timeframe_seconds(timeframe))

    def _prefix(records):
        return {s: [r for r in recs if r["timestamp"] + 2 * step <= cutoff]
                for s, recs in records.items()}
    cand, steps = _ric.symbol_records_from_protocol_result(pr, _results_dir(run_dir, pr, bid))
    comp = None
    if kind != "none":
        cache_dir = Path(root) / str((doc.get("composite") or {}).get("cache_dir"))
        _cc._refuse_sealed(cache_dir)
        summary_path = cache_dir / "protocol_summary.json"
        if not summary_path.exists():
            raise CompositionError(f"block {bid!r}: composite cache {summary_path} is missing")
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        comp, _ = _ric.symbol_records_from_protocol_result(summary, cache_dir / "results")
        comp = _prefix(comp)
    cand = {s: recs for s, recs in _prefix(cand).items() if recs}
    if not cand:
        return {"value": None, "n_eff": 0, "reason": f"no bar before {_as_date(before)}"}
    return _ric.compute_residual_ic(cand, comp, block_size=_tf.bars_per_day(timeframe),
                                    expected_step_by_symbol=steps,
                                    composite_label=kind if kind != "none" else _ric.COMPOSITE_NONE)


# ---------------------------------------------------------------------------
# 6. the code-written variant_patches.yaml (guess 12)
# ---------------------------------------------------------------------------

def _weight_pointer(i: int) -> str:
    return f"/strategies/regimes/{COMPOSITE_REGIME}/blocks/{i}/weight"


def variant_patches_from_manifest(manifest: dict) -> dict:
    """variant_patches.yaml for a composition run: one variant per scheme
    (`base` = equal, `vol_scaled`, `ic_weighted`), each a patch setting every
    block's weight to that scheme's static weight and, for a scheme with a
    per-window schedule, the regime's weight_schedule (block weights keyed by
    config block id). The block order is the manifest's. Written by code,
    never by an LLM: the variants differ ONLY in the weights."""
    _check_manifest_shape(manifest)
    cbid = {mb["block_id"]: mb["config_block_id"] for mb in manifest["blocks"]}
    variants = []
    for scheme in SCHEMES:
        vid = VARIANT_BY_SCHEME[scheme]
        v = manifest["variants"][vid]
        patch = [{"path": _weight_pointer(i), "value": v["weights"][mb["block_id"]]}
                 for i, mb in enumerate(manifest["blocks"])]
        if v.get("weight_schedule"):
            patch.append({"path": f"/strategies/regimes/{COMPOSITE_REGIME}/{WEIGHT_SCHEDULE_KEY}",
                          "value": [{"from": e["from"],
                                     "weights": {cbid[b]: w for b, w in sorted(e["weights"].items())}}
                                    for e in v["weight_schedule"]]})
        variants.append({"variant_id": vid, "patch": patch,
                         "rationale": f"composition scheme {scheme} (code-written, E-060 S3b)"})
    return {"generated_by": "tools/composition.py (E-060 S3b, code-written -- no LLM)",
            "composition_registry_hash": manifest["registry_hash"], "variants": variants}


# ---------------------------------------------------------------------------
# 7. the 5a check of a composite config against its manifest
# ---------------------------------------------------------------------------

WEIGHT_TOLERANCE = 1e-6  # S1_FINDINGS.md §5: normalised weights within 1e-6


def _check_manifest_shape(manifest) -> None:
    if not isinstance(manifest, dict) or manifest.get("kind") != "composition" \
            or manifest.get("schema_version") != SCHEMA_VERSION:
        raise CompositionError("not a composition manifest (kind: composition, "
                               f"schema_version: {SCHEMA_VERSION})")
    blocks = manifest.get("blocks")
    if not isinstance(blocks, list) or len(blocks) < 2:
        raise CompositionError("composition manifest lists fewer than two blocks")
    ids = [b.get("block_id") for b in blocks if isinstance(b, dict)]
    if len(ids) != len(blocks) or len(set(ids)) != len(ids):
        raise CompositionError(f"composition manifest blocks malformed or duplicated: {ids}")
    for b in blocks:
        paths, cids = b.get("config_paths"), b.get("component_ids")
        if not isinstance(paths, list) or not isinstance(cids, list) or not cids \
                or len(paths) != len(cids):
            raise CompositionError(f"composition manifest block {b.get('block_id')!r}: "
                                   f"config_paths {paths!r} do not match component_ids {cids!r} "
                                   f"one to one")
    variants = manifest.get("variants")
    for scheme in SCHEMES:
        vid = VARIANT_BY_SCHEME[scheme]
        v = (variants or {}).get(vid) or {}
        w = v.get("weights")
        if not isinstance(w, dict) or sorted(w) != sorted(ids):
            raise CompositionError(f"composition manifest variant {vid!r} does not weight exactly "
                                   f"the listed blocks {sorted(ids)}")
        for e in v.get("weight_schedule") or []:
            if not isinstance(e, dict) or sorted((e.get("weights") or {})) != sorted(ids):
                raise CompositionError(f"composition manifest variant {vid!r}: a weight_schedule "
                                       f"entry does not weight exactly the listed blocks")


def _weights_off(got: dict, want: dict) -> dict:
    bad = {b: w for b, w in got.items()
           if isinstance(w, bool) or not isinstance(w, (int, float)) or not math.isfinite(w) or w <= 0}
    if bad:
        raise CompositionError(f"block weight(s) {bad} are not positive finite numbers")
    g, w = _normalise(got), _normalise(want)
    return {b: (g[b], w[b]) for b in w if abs(g[b] - w[b]) > WEIGHT_TOLERANCE}


def check_composition_config(config: dict, manifest: dict, variant_id: str, *, root: Path,
                             registry_doc: dict) -> None:
    """5a (S1_FINDINGS.md §5, as built for the block combiner): raise
    CompositionError unless `config` is the composite the manifest describes,
    weighted by `variant_id`'s scheme:
      * the composite's own detector is the ungated one; only its regime
        carries anything; its block_standardisation is the manifest's;
      * scaffolding (code review fix 7): no top-level key but regime_detector,
        strategies and aux_feeds; no strategies key but regimes and
        min_allocation_change (a composite has no strategies.warmup -- each
        block keeps its own); aux_feeds and min_allocation_change equal what
        the blocks' source configs merge to;
      * every manifest block is present exactly once (by config block id), no
        other block, every component belongs to exactly one block, and every
        manifest pointer holds its component (a pointer/id mismatch raises);
      * each block is gated and pinned AS ITS SOURCE: its `source` (source
        detector, required_bars, warm-up, buffer, parts) and each component's
        id, class and pinned lookback equal what assemble_block derives from
        the registry block and its sha-checked source config (memoised, fix
        8). A component's params/transforms are not compared: an R1 run's
        config is pinned byte for byte by the brief's config sha256, and a
        reader patch (7.5) may change them;
      * the block weights, and every weight_schedule entry (dates and
        weights), normalised, equal the scheme's within WEIGHT_TOLERANCE."""
    _check_manifest_shape(manifest)
    if variant_id not in manifest["variants"]:
        raise CompositionError(f"variant {variant_id!r} is not in the composition manifest "
                               f"({sorted(manifest['variants'])})")
    if not isinstance(config, dict):
        raise CompositionError("composite config is not a mapping")
    extra = sorted(set(config) - set(_ALLOWED_TOP_KEYS))
    strat = config.get("strategies") if isinstance(config.get("strategies"), dict) else {}
    extra_s = sorted(set(strat) - {"regimes", "min_allocation_change"})
    if extra or extra_s:
        raise CompositionError(f"the composite carries key(s) {extra + extra_s} outside its "
                               f"scaffolding (a composite has no strategies.warmup)")
    if config.get("regime_detector") != _UNGATED_DETECTOR:
        raise CompositionError("the composite's regime_detector is not the ungated pattern "
                               f"(every bar -> {COMPOSITE_REGIME!r})")
    regimes = strat.get("regimes") or {}
    others = sorted(r for r, v in regimes.items() if r != COMPOSITE_REGIME and v is not None)
    if others:
        raise CompositionError(f"regime(s) {others} carry components -- a composite has only "
                               f"{COMPOSITE_REGIME!r}")
    reg = regimes.get(COMPOSITE_REGIME)
    if not isinstance(reg, dict) or not isinstance(reg.get("blocks"), list) \
            or not isinstance(reg.get("components"), list):
        raise CompositionError(f"regime {COMPOSITE_REGIME!r} has no blocks/components lists")
    extra_r = sorted(set(reg) - {"components", "blocks", "block_standardisation",
                                 WEIGHT_SCHEDULE_KEY})
    if extra_r:
        raise CompositionError(f"regime {COMPOSITE_REGIME!r} carries unknown key(s) {extra_r}")
    if reg.get("block_standardisation") != manifest.get("standardisation"):
        raise CompositionError(f"block_standardisation {reg.get('block_standardisation')!r} is "
                               f"not the manifest's {manifest.get('standardisation')!r}")
    cfg_blocks = {}
    for b in reg["blocks"]:
        bid = b.get("id") if isinstance(b, dict) else None
        if bid in cfg_blocks:
            raise CompositionError(f"config block {bid!r} appears twice")
        cfg_blocks[bid] = b
    want = [mb["config_block_id"] for mb in manifest["blocks"]]
    if sorted(cfg_blocks, key=str) != sorted(want):
        raise CompositionError(f"config blocks {sorted(cfg_blocks, key=str)} are not the "
                               f"manifest's {sorted(want)}")
    comps_by_id = {}
    for c in reg["components"]:
        cid = c.get("id") if isinstance(c, dict) else None
        if cid in comps_by_id:
            raise CompositionError(f"component {cid!r} appears twice")
        comps_by_id[cid] = c
    owned = [cid for mb in manifest["blocks"] for cid in mb["component_ids"]]
    if len(owned) != len(set(owned)) or set(owned) != set(comps_by_id):
        raise CompositionError(f"components {sorted(map(str, set(comps_by_id) ^ set(owned)))} (or "
                               f"a component listed by two blocks) -- every component must be "
                               f"owned by exactly one manifest block")
    registry_blocks = {b.get("block_id"): b for b in (registry_doc or {}).get("blocks") or []}
    parts = {}
    for mb in manifest["blocks"]:
        bid, cbid = mb["block_id"], mb["config_block_id"]
        blk = cfg_blocks[cbid]
        if blk.get("components") != mb["component_ids"]:
            raise CompositionError(f"block {bid!r}: its components {blk.get('components')} are "
                                   f"not the manifest's {mb['component_ids']}")
        for ptr, cid in zip(mb["config_paths"], mb["component_ids"], strict=True):
            if not _jp.json_pointer_exists(config, ptr) or \
                    (_jp.resolve_json_pointer(config, ptr) or {}).get("id") != cid:
                raise CompositionError(f"block {bid!r}: manifest pointer {ptr} does not hold "
                                       f"component {cid!r}")
        reg_block = registry_blocks.get(bid)
        if reg_block is None:
            raise CompositionError(f"block {bid!r} is not in the block registry")
        if reg_block.get("source_config_sha256") != mb.get("source_config_sha256"):
            raise CompositionError(f"block {bid!r}: the registry's source config sha differs "
                                   f"from the manifest's")
        expected = assemble_block(reg_block, cbid, root)
        parts[bid] = expected["scaffolding"]
        if blk.get("source") != expected["source"]:
            raise CompositionError(f"block {bid!r} is not gated/timed as its source: config "
                                   f"source {blk.get('source')!r} != {expected['source']!r}")
        for exp in expected["components"]:
            got = comps_by_id.get(exp["id"]) or {}
            for key in ("class", "lookback"):
                if got.get(key) != exp.get(key):
                    raise CompositionError(f"block {bid!r}: component {exp['id']!r} {key} "
                                           f"{got.get(key)!r} != its source's {exp.get(key)!r}")
    scaf = _merge_scaffolding(parts)
    if (config.get("aux_feeds") or []) != scaf["aux_feeds"]:
        raise CompositionError(f"aux_feeds {config.get('aux_feeds')!r} are not the blocks' merged "
                               f"{scaf['aux_feeds']!r}")
    if strat.get("min_allocation_change") != scaf["min_allocation_change"]:
        raise CompositionError(f"strategies.min_allocation_change "
                               f"{strat.get('min_allocation_change')!r} is not the blocks' "
                               f"{scaf['min_allocation_change']!r}")
    mv = manifest["variants"][variant_id]
    by_cbid = {mb["config_block_id"]: mb["block_id"] for mb in manifest["blocks"]}
    off = _weights_off({by_cbid[c]: b.get("weight") for c, b in cfg_blocks.items()}, mv["weights"])
    if off:
        raise CompositionError(f"variant {variant_id!r}: normalised block weights differ from the "
                               f"{mv.get('scheme')!r} scheme beyond {WEIGHT_TOLERANCE}: {off}")
    got_sched = reg.get(WEIGHT_SCHEDULE_KEY) or []
    want_sched = mv.get("weight_schedule") or []
    if [e.get("from") for e in got_sched] != [e["from"] for e in want_sched]:
        raise CompositionError(f"variant {variant_id!r}: weight_schedule dates "
                               f"{[e.get('from') for e in got_sched]} are not the manifest's "
                               f"{[e['from'] for e in want_sched]}")
    for g, w in zip(got_sched, want_sched):
        gw = g.get("weights") or {}
        if sorted(gw) != sorted(by_cbid):
            raise CompositionError(f"variant {variant_id!r}: weight_schedule {g.get('from')} "
                                   f"weights blocks {sorted(gw)}")
        off = _weights_off({by_cbid[c]: x for c, x in gw.items()}, w["weights"])
        if off:
            raise CompositionError(f"variant {variant_id!r}: weight_schedule {g.get('from')} "
                                   f"weights differ from the manifest beyond {WEIGHT_TOLERANCE}: "
                                   f"{off}")
