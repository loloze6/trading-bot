from collections import deque
from typing import Dict, Any, Tuple
import math
import pandas as pd
import numpy as np
import logging

from strategies.registry import (
    apply_transform_pipeline, _load_class, component_effective_lookback, standardise_block_forecast,
)
from strategies.strategy_base import MarketRegime, SubStrategyComponent

logger = logging.getLogger("trading_bot")

# ---------------------------------------------------------------------------
# E-060 S3a: the opt-in per-regime block combiner.
#
# A strategies regime that carries `blocks` + `block_standardisation` combines
# BLOCKS (validated, registry-listed pieces of other configs) instead of
# summing its components directly. Each block runs AS IT WAS VALIDATED:
#   * its own source timing -- `source.required_bars` / `source.warmup` /
#     `source.buffer_bars` are its source AdvancedStrategy's values, and its
#     components and gate see only the last `buffer_bars` bars of the window
#     (with the strategy's calculated columns recomputed on that slice), so a
#     longer window needed by another block never changes what it computes;
#   * its own gate -- `source.regime_detector` (the source config's detector,
#     run by its own ConfigDrivenRegimeEngine) and `source.parts` ({source
#     regime: [component ids]}): on a bar classified into regime r the block's
#     final forecast is the part for r (weights normalised within the part,
#     clipped +-20, exactly the source engine's forecast(r)); in any other
#     regime, or before its source would have been ready, the block ABSTAINS
#     (contributes 0 and records nothing);
#   * its own scale -- standardised past-only: target * v_t / mean(|v|) over
#     the block's last `window` ACTIVE values BEFORE this bar (the current value
#     is not in its own denominator), capped at +-20, 0.0 when that mean is ~0;
#     until `min_periods` past active values exist the block abstains.
# Regime forecast = sum_b (W_b / sum W) * s_b, clipped +-20.
#
# WHY THIS CANNOT LEAK: every quantity at bar t is computed from the data
# window ending at t (components, gate, pipelines) and from block values of
# bars < t (the denominator). Nothing is estimated once over a period.
#
# NaN fails loud: a non-finite block value raises in update() and the fault is
# re-raised by is_ready()/forecast() for that bar, so it never reaches an
# allocation and is never replaced by 0.0.
#
# A regime without these keys never enters any of this: its update(),
# is_ready() and forecast() are the pre-S3a code paths.
#
# E-060 S3b: optional `weight_schedule` on the same regime --
#   [{"from": "YYYY-MM-DD", "weights": {block_id: W > 0, ...}}, ...]
# strictly increasing `from` dates, every entry weighting exactly the blocks.
# On a bar whose timestamp (the data's `timestamp` column, UTC) is on or after
# an entry's `from` (00:00 UTC), the LAST such entry's weights replace the
# blocks' own `weight`; before the first entry the blocks' `weight` applies.
# WHY THIS CANNOT LEAK: an entry is a set of constants fixed before the run;
# the code that writes it (strategy-research/tools/composition.py) estimates
# each entry only from data strictly before its `from`, and the engine applies
# it only to bars at or after `from`. A config without the key never enters it.
# ---------------------------------------------------------------------------
BLOCK_COMBINER_KEYS = ("blocks", "block_standardisation")
WEIGHT_SCHEDULE_KEY = "weight_schedule"
BLOCK_KEYS = ("id", "weight", "components", "source")
BLOCK_SOURCE_KEYS = ("required_bars", "warmup", "buffer_bars", "regime_detector", "parts")
BLOCK_STANDARDISATION_KEYS = ("target", "window", "min_periods")
BLOCK_CAP = 20.0
_REGIME_NAMES = ("trending", "mean_reversion", "chop", "unknown")
# Re-derive the running |h| sum from scratch every this many appends (bounds
# floating-point drift of the incremental add/subtract).
_RESYNC_EVERY = 1000


def _is_num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _is_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def validate_block_combiner(rname: str, rcfg: Any) -> list:
    """Violations (strings) of the opt-in block combiner of one regime; [] when
    the regime uses neither key (every config written before E-060 S3a).
    Never raises on malformed input -- it reports it.

    Shape (both keys together):
      "blocks": [{"id": str, "weight": number > 0, "components": [id, ...],
                  "source": {"required_bars": int >= 1, "warmup": int >= 1,
                             "buffer_bars": int >= required_bars,
                             "regime_detector": {...},
                             "parts": {regime: [id, ...], ...}}}, ...]
      "block_standardisation": {"target": number > 0, "window": int >= 2,
                                "min_periods": int, 2 <= min_periods <= window}
    Every component of the regime belongs to exactly one block; a block's
    parts partition its components; block ids are unique strings that differ
    from every component id. Used by the engine (raises) and by
    tools/validate_config.py (V13)."""
    loc = f"strategies.regimes.{rname}"
    if isinstance(rcfg, dict) and WEIGHT_SCHEDULE_KEY in rcfg \
            and not all(k in rcfg for k in BLOCK_COMBINER_KEYS):
        return [f"{loc}.{WEIGHT_SCHEDULE_KEY}: only valid with the block combiner "
                f"{list(BLOCK_COMBINER_KEYS)}"]
    if not isinstance(rcfg, dict) or not any(k in rcfg for k in BLOCK_COMBINER_KEYS):
        return []
    missing = [k for k in BLOCK_COMBINER_KEYS if k not in rcfg]
    if missing:
        return [f"{loc}: block combiner needs both {list(BLOCK_COMBINER_KEYS)}, missing {missing}"]
    out = []
    comps = rcfg.get("components")
    if not isinstance(comps, list) or not all(isinstance(c, dict) for c in comps):
        return [f"{loc}.components: must be a list of component specs"]
    comp_ids = [c.get("id") for c in comps]
    if not all(isinstance(c, str) for c in comp_ids):
        return [f"{loc}.components: every component id must be a string, got {comp_ids!r}"]
    weights = {c["id"]: c.get("weight") for c in comps}
    blocks = rcfg["blocks"]
    if not isinstance(blocks, list) or not blocks:
        return [f"{loc}.blocks: must be a non-empty list, got {blocks!r}"]
    seen_b, owned = [], []
    for i, b in enumerate(blocks):
        bl = f"{loc}.blocks[{i}]"
        if not isinstance(b, dict) or set(b) != set(BLOCK_KEYS):
            out.append(f"{bl}: must have exactly keys {list(BLOCK_KEYS)}; got {b!r}")
            continue
        bid, w, bcomps, src = b["id"], b["weight"], b["components"], b["source"]
        if not isinstance(bid, str) or not bid or bid in seen_b or bid in comp_ids:
            out.append(f"{bl}.id={bid!r}: must be a non-empty string, unique, and not a component id")
        else:
            seen_b.append(bid)
        if not _is_num(w) or w <= 0:
            out.append(f"{bl}.weight={w!r}: must be a finite number > 0")
        if not isinstance(bcomps, list) or not bcomps or not all(isinstance(c, str) for c in bcomps):
            out.append(f"{bl}.components: must be a non-empty list of component id strings")
            continue
        unknown = [c for c in bcomps if c not in comp_ids]
        if unknown:
            out.append(f"{bl}.components: {unknown} are not components of this regime")
        owned.extend(bcomps)
        if not isinstance(src, dict) or set(src) != set(BLOCK_SOURCE_KEYS):
            out.append(f"{bl}.source: must have exactly keys {list(BLOCK_SOURCE_KEYS)}; got {src!r}")
            continue
        rb, wu, bb = src["required_bars"], src["warmup"], src["buffer_bars"]
        if not (_is_int(rb) and _is_int(wu) and _is_int(bb) and rb >= 1 and wu >= 1 and bb >= rb):
            out.append(f"{bl}.source: required_bars={rb!r}, warmup={wu!r}, buffer_bars={bb!r} -- "
                       f"need integers >= 1 with buffer_bars >= required_bars")
        if not isinstance(src["regime_detector"], dict):
            out.append(f"{bl}.source.regime_detector: must be the source config's detector mapping")
        parts = src["parts"]
        if not isinstance(parts, dict) or not parts:
            out.append(f"{bl}.source.parts: must be a non-empty mapping regime -> [component ids]")
            continue
        in_parts = []
        for r, ids in parts.items():
            if r not in _REGIME_NAMES:
                out.append(f"{bl}.source.parts: regime {r!r} not in {list(_REGIME_NAMES)}")
            if not isinstance(ids, list) or not ids or not all(isinstance(c, str) for c in ids):
                out.append(f"{bl}.source.parts[{r!r}]: must be a non-empty list of component ids")
                continue
            in_parts.extend(ids)
            pw = [weights.get(c) for c in ids]
            if not all(_is_num(x) for x in pw) or sum(pw) <= 0:
                out.append(f"{bl}.source.parts[{r!r}]: component weights {pw} must be finite "
                           f"numbers summing to > 0")
        if sorted(in_parts) != sorted(bcomps):
            out.append(f"{bl}.source.parts: must partition the block's components exactly "
                       f"(parts {sorted(in_parts)} vs components {sorted(bcomps)})")
    dup = sorted({c for c in owned if owned.count(c) > 1})
    orphan = [c for c in comp_ids if c not in owned]
    if dup:
        out.append(f"{loc}.blocks: component(s) {dup} belong to more than one block")
    if orphan:
        out.append(f"{loc}.blocks: component(s) {orphan} belong to no block")
    st = rcfg["block_standardisation"]
    if not isinstance(st, dict) or set(st) != set(BLOCK_STANDARDISATION_KEYS):
        out.append(f"{loc}.block_standardisation: must have exactly keys "
                   f"{list(BLOCK_STANDARDISATION_KEYS)}; got {st!r}")
        return out
    t, win, mp = st["target"], st["window"], st["min_periods"]
    if not _is_num(t) or t <= 0:
        out.append(f"{loc}.block_standardisation.target={t!r}: must be a finite number > 0")
    if not (_is_int(win) and _is_int(mp)) or win < 2 or not (2 <= mp <= win):
        out.append(f"{loc}.block_standardisation: window={win!r}, min_periods={mp!r} -- need "
                   f"integers with 2 <= min_periods <= window")
    if WEIGHT_SCHEDULE_KEY in rcfg:
        out += _validate_weight_schedule(loc, rcfg[WEIGHT_SCHEDULE_KEY], seen_b)
    return out


def _validate_weight_schedule(loc: str, sched: Any, block_ids: list) -> list:
    """E-060 S3b: the optional per-date block weights (module comment)."""
    import datetime as _dt
    if not isinstance(sched, list) or not sched:
        return [f"{loc}.{WEIGHT_SCHEDULE_KEY}: must be a non-empty list"]
    out, prev = [], None
    for i, e in enumerate(sched):
        el = f"{loc}.{WEIGHT_SCHEDULE_KEY}[{i}]"
        if not isinstance(e, dict) or set(e) != {"from", "weights"}:
            out.append(f"{el}: must have exactly keys ['from', 'weights']; got {e!r}")
            continue
        try:
            d = _dt.date.fromisoformat(e["from"]) if isinstance(e["from"], str) else None
        except ValueError:
            d = None
        if d is None:
            out.append(f"{el}.from={e['from']!r}: must be an ISO date YYYY-MM-DD")
        elif prev is not None and d <= prev:
            out.append(f"{el}.from={e['from']!r}: dates must be strictly increasing")
        prev = d or prev
        w = e["weights"]
        if not isinstance(w, dict) or sorted(w) != sorted(block_ids) \
                or not all(_is_num(x) and x > 0 for x in w.values()):
            out.append(f"{el}.weights: must weight exactly the blocks {sorted(block_ids)} with "
                       f"finite numbers > 0; got {w!r}")
    return out


class BlockCombinerError(ValueError):
    """A block produced a non-finite value (or the combiner state is invalid)."""


class _Block:
    """Runtime state of one block (see the module comment)."""

    def __init__(self, cfg: Dict[str, Any], specs: Dict[str, Dict[str, Any]], window: int):
        from strategies.regime_engine import ConfigDrivenRegimeEngine  # avoid import cycle
        src = cfg["source"]
        self.id = cfg["id"]
        self.weight = float(cfg["weight"])
        self.cids = list(cfg["components"])
        self.required_bars = src["required_bars"]
        self.warmup = src["warmup"]
        self.buffer_bars = src["buffer_bars"]
        self.gate = ConfigDrivenRegimeEngine(src["regime_detector"])
        # regime -> [(cid, transforms, weight / part total)]
        self.parts = {}
        for r, ids in src["parts"].items():
            total = sum(specs[c]["weight"] for c in ids)
            self.parts[r] = [(c, specs[c]["transforms"], specs[c]["weight"] / total) for c in ids]
        self.hist: deque = deque(maxlen=window)  # past ACTIVE final forecasts
        self.abs_sum = 0.0
        self._appends = 0
        self.reset_bar()

    def reset_bar(self) -> None:
        self.raw = 0.0        # this bar's final forecast (0.0 when abstaining)
        self.value = 0.0      # this bar's standardised, capped contribution
        self.active = False   # emitted a standardised value this bar
        self.regime = None

    def clear(self) -> None:
        self.hist.clear()
        self.abs_sum = 0.0
        self._appends = 0
        self.gate.reset_history()
        self.reset_bar()

    def push(self, v: float) -> None:
        if len(self.hist) == self.hist.maxlen:
            self.abs_sum -= abs(self.hist[0])
        self.hist.append(v)
        self.abs_sum += abs(v)
        self._appends += 1
        if self._appends % _RESYNC_EVERY == 0:
            self.abs_sum = math.fsum(abs(x) for x in self.hist)


class ConfigDrivenStrategyEngine:
    """
    Applies transforms and combines component values per regime per config.
    Returns forecast in [-20, +20]. Regime with null config → 0.0.
    """

    def __init__(self, config: Dict[str, Any]):
        self._regime_cfgs = config["regimes"]
        self._data: pd.DataFrame = None
        # E-060 S3a: the block combiner's shape is checked before anything is
        # built ([] -- nothing happens -- for a config without `blocks`).
        errors = []
        for rname, rcfg in self._regime_cfgs.items():
            errors += validate_block_combiner(rname, rcfg)
        if errors:
            raise ValueError("; ".join(errors))

        self._components:  Dict[str, Dict[str, SubStrategyComponent]] = {}
        self._history:     Dict[str, Dict[str, deque]]                = {}
        self._history_tf:  Dict[str, Dict[str, list]]                 = {}

        # Phase 1: instantiate all components (validates class paths at startup)
        for rname, rcfg in self._regime_cfgs.items():
            if rcfg is None:
                continue
            self._components[rname] = {}
            for c in rcfg["components"]:
                cls = _load_class(c["class"])
                self._components[rname][c["id"]] = cls(
                    name=f"{rname}.{c['id']}",
                    weight=1.0,
                    parameters=c.get("params", {}),
                )

        # Phase 2: derive lookback — max of component requirements AND transform minimums
        effective = []
        for rname, rcfg in self._regime_cfgs.items():
            if rcfg is None:
                continue
            for c_spec in rcfg["components"]:
                comp = self._components[rname][c_spec["id"]]
                effective.append(component_effective_lookback(c_spec, comp.get_required_periods()))
        self.lookback = max(effective, default=50)

        # Phase 3: create history deques and capture append-time transform specs
        for rname, rcfg in self._regime_cfgs.items():
            if rcfg is None:
                continue
            self._history[rname]    = {}
            self._history_tf[rname] = {}
            for c_spec in rcfg["components"]:
                cid = c_spec["id"]
                buf = c_spec.get("lookback", self.lookback)
                self._history[rname][cid]    = deque(maxlen=buf)
                self._history_tf[rname][cid] = c_spec.get("history_transforms", [])

        # warmup: cap against the smallest actual deque, not self.lookback.
        # Per-component "lookback" overrides can make individual deques smaller than
        # self.lookback; capping against self.lookback could set warmup above maxlen.
        self._min_buf = min(
            (h.maxlen for rc in self._history.values() for h in rc.values()),
            default=self.lookback,
        )
        # CUL-273: this is the class's OWN default, used when nobody calls
        # set_warmup() -- kept so a standalone/test construction of this class
        # (e.g. tests/test_engine_warmth.py) is byte-identical to before this
        # ticket. AdvancedStrategy (the real live/backtest path) overrides it
        # via set_warmup(required_bars) right after required_bars is known --
        # see main_strategy.py. Measured on the real strategy_config.json this
        # fork uses: the two numbers had already drifted (51 vs required_bars=120,
        # the architecture doc's own documented "~120 bars" warmup) -- this
        # class's own config-driven default was silently wrong for the real
        # strategy, not just theoretically inconsistent.
        self._warmup = min(config.get("warmup", self.lookback), self._min_buf)
        logger.debug(f"StrategyEngine: lookback={self.lookback}, warmup={self._warmup}")

        # E-060 S3a: opt-in block combiner (module comment). A regime without
        # `blocks` never enters these dicts.
        self._block_regimes: Dict[str, Dict[str, Any]] = {}
        self._indicators: Dict[str, Any] = {}
        self._block_fault = None
        self._n_data = 0
        for rname, rcfg in self._regime_cfgs.items():
            if rcfg is None or "blocks" not in rcfg:
                continue
            specs = {c["id"]: c for c in rcfg["components"]}
            st = rcfg["block_standardisation"]
            self._block_regimes[rname] = {
                "blocks": [_Block(b, specs, st["window"]) for b in rcfg["blocks"]],
                "target": float(st["target"]),
                "min_periods": st["min_periods"],
                # E-060 S3b: [(from date, {block_id: weight})], [] when absent
                "schedule": [(pd.Timestamp(e["from"]).date(), dict(e["weights"]))
                             for e in rcfg.get(WEIGHT_SCHEDULE_KEY) or []],
            }
            for b in self._block_regimes[rname]["blocks"]:
                short = {c: self._history[rname][c].maxlen for c in b.cids
                         if self._history[rname][c].maxlen < max(2, b.warmup)}
                if short:
                    raise ValueError(
                        f"strategies.regimes.{rname}: block {b.id!r} has source warmup "
                        f"{b.warmup} but component deque(s) {short} are shorter -- it could "
                        f"never become ready (pin each component's source lookback)")

    def set_warmup(self, required_bars: int) -> None:
        """CUL-273: single source of truth for warmup. Called by AdvancedStrategy
        right after it computes required_bars, so this engine's own internal
        per-regime readiness (is_ready()) agrees with the outer buffer-size gate
        instead of drifting from it via its own independent min(config.warmup,
        min_buf) calculation. Still capped at _min_buf -- a per-component
        "lookback" override can make an individual deque smaller than
        required_bars, and warmup must never exceed the smallest deque's maxlen
        or that component could never satisfy len(h) >= warmup."""
        self._warmup = min(required_bars, self._min_buf)

    def set_indicators(self, indicators: Dict[str, Any]) -> None:
        """E-060 S3a: the calculated columns of the strategy's RollingBuffer
        (name -> func(df)), recomputed on each block's source-length slice so
        the slice equals the block's source buffer. Unused without blocks."""
        self._indicators = dict(indicators)

    def update(self, data: pd.DataFrame) -> None:
        self._data = data
        for rname, regime_comps in self._components.items():
            if rname in self._block_regimes:
                continue  # E-060 S3a: updated per block below, on the block's own window
            for cid, comp in regime_comps.items():
                comp.update(data)
                if comp.is_ready():
                    raw = comp.raw_value()
                    tfs = self._history_tf[rname][cid]
                    if tfs:
                        raw = apply_transform_pipeline(pd.Series([raw]), tfs, data)
                    self._history[rname][cid].append(raw)
        if self._block_regimes:
            self._update_blocks(data)

    # -- E-060 S3a block combiner -------------------------------------------
    def _block_window(self, data: pd.DataFrame, block: _Block) -> pd.DataFrame:
        """The last `buffer_bars` bars -- what the block's source RollingBuffer
        would hold -- with calculated columns recomputed on the slice."""
        if data is None or len(data) <= block.buffer_bars:
            return data
        sl = data.iloc[-block.buffer_bars:].reset_index(drop=True)
        if self._indicators:
            sl = sl.copy()
            for name, func in self._indicators.items():
                sl[name] = func(sl)
        return sl

    def _update_blocks(self, data: pd.DataFrame) -> None:
        self._block_fault = None
        self._n_data = 0 if data is None else len(data)
        faults = []
        for rname, reg in self._block_regimes.items():
            for block in reg["blocks"]:  # every block advances every bar, fault or not
                try:
                    self._update_block(rname, block, data, reg)
                except BlockCombinerError as exc:
                    faults.append(str(exc))
        if faults:
            self._block_fault = "; ".join(faults)
            raise BlockCombinerError(self._block_fault)

    def _update_block(self, rname: str, block: _Block, data: pd.DataFrame, reg: Dict[str, Any]) -> None:
        block.reset_bar()
        window = self._block_window(data, block)
        for cid in block.cids:
            comp = self._components[rname][cid]
            comp.update(window)
            if comp.is_ready():
                raw = comp.raw_value()
                tfs = self._history_tf[rname][cid]
                if tfs:
                    raw = apply_transform_pipeline(pd.Series([raw]), tfs, window)
                self._history[rname][cid].append(raw)
        block.gate.update(window)
        # The source classifies only once its buffer holds required_bars and its
        # detector is ready (AdvancedStrategy.is_ready), once per bar.
        if self._n_data < block.required_bars or not block.gate.is_ready():
            return
        regime, _ = block.gate.classify()
        block.regime = regime.value
        part = block.parts.get(regime.value)
        if part is None:
            return  # outside its validated regime(s): abstain, record nothing
        need = max(2, block.warmup)
        if any(len(self._history[rname][cid]) < need for cid, _t, _w in part):
            return  # the source would still be NOT_READY in this regime
        v = 0.0
        for cid, tfs, w in part:
            h = self._history[rname][cid]
            v += w * apply_transform_pipeline(pd.Series(list(h)), tfs, window)
        v = float(np.clip(v, -BLOCK_CAP, BLOCK_CAP))
        if not math.isfinite(v):
            raise BlockCombinerError(
                f"block {block.id!r} (regime {rname!r}) produced a non-finite final forecast "
                f"{v!r} at bar {self._n_data} of the window -- refusing to combine it")
        if not math.isfinite(block.abs_sum):
            raise BlockCombinerError(f"block {block.id!r}: non-finite value in its past history")
        block.raw = v
        if len(block.hist) >= reg["min_periods"]:
            mean_abs = block.abs_sum / len(block.hist)  # past values only (bars < t)
            block.value = standardise_block_forecast(v, mean_abs, reg["target"], BLOCK_CAP)
            block.active = True
        block.push(v)

    def _block_ready(self, rname: str, block: _Block) -> bool:
        return (self._n_data >= block.required_bars and block.gate.is_ready()
                and all(len(self._history[rname][c]) >= max(2, block.warmup) for c in block.cids))

    def _block_weights(self, reg: Dict[str, Any]) -> Dict[str, float]:
        """Each block's weight on this bar: its own `weight`, or -- with a
        weight_schedule (E-060 S3b) -- the last entry whose `from` date is on
        or before this bar's UTC date. A schedule without a bar timestamp
        fails loud."""
        weights = {b.id: b.weight for b in reg["blocks"]}
        if not reg["schedule"]:
            return weights
        if self._data is None or "timestamp" not in self._data.columns or not len(self._data):
            raise BlockCombinerError("weight_schedule needs the bar's `timestamp` column")
        ts = pd.Timestamp(self._data["timestamp"].iloc[-1])
        if ts.tzinfo is not None:
            ts = ts.tz_convert("UTC")
        day = ts.date()
        for start, w in reg["schedule"]:
            if start <= day:
                weights = {k: float(v) for k, v in w.items()}
        return weights

    def _forecast_blocks(self, rkey: str) -> Tuple[float, Dict[str, Any]]:
        reg = self._block_regimes[rkey]
        weights = self._block_weights(reg)
        total_w = sum(weights[b.id] for b in reg["blocks"])
        ensemble = 0.0
        debug: Dict[str, Any] = {}
        for b in reg["blocks"]:
            if not self._block_ready(rkey, b):
                return 0.0, {"not_ready_block": b.id}
        for b in reg["blocks"]:
            w_norm = weights[b.id] / total_w
            ensemble += w_norm * b.value
            # Same four keys as a component row (bars.csv consumers read a block
            # as one unit) plus `active`: last_history_value = the block's final
            # forecast this bar, post_pipeline_value = standardised and capped.
            debug[b.id] = {
                "last_history_value":    float(b.raw),
                "post_pipeline_value":   float(b.value),
                "weight_normalized":     float(w_norm),
                "weighted_contribution": float(w_norm * b.value),
                "active":                1.0 if b.active else 0.0,
            }
        return float(np.clip(ensemble, -20.0, 20.0)), debug

    def reset_history(self) -> None:
        """CUL-271: large-gap segment split -- drop accumulated per-regime
        component history so post-gap readiness re-derives from real post-gap
        bars only. Deques keep their maxlen."""
        for regime_hist in self._history.values():
            for h in regime_hist.values():
                h.clear()
        for reg in self._block_regimes.values():  # E-060 S3a (empty unless opted in)
            for b in reg["blocks"]:
                b.clear()
        self._block_fault = None

    def is_ready(self, regime: MarketRegime) -> bool:
        rkey = regime.value
        if rkey not in self._components:
            return True
        if rkey in self._block_regimes:  # E-060 S3a: per-block source readiness
            if self._block_fault:
                raise BlockCombinerError(self._block_fault)
            return all(self._block_ready(rkey, b) for b in self._block_regimes[rkey]["blocks"])
        return all(
            len(h) >= self._warmup
            for h in self._history[rkey].values()
        )

    def get_required_periods(self) -> int:
        all_comps = [c for rc in self._components.values() for c in rc.values()]
        base = max((c.get_required_periods() for c in all_comps), default=0)
        if not self._block_regimes:
            return base
        # E-060 S3a: a block is ready at its source's required_bars + warmup at
        # the latest, and standardised after min_periods more active values.
        chained = max(b.required_bars + b.warmup + reg["min_periods"]
                      for reg in self._block_regimes.values() for b in reg["blocks"])
        return max(base, chained)

    def required_feeds(self) -> dict[str, tuple[str, ...]]:
        """Feed name -> sorted tuple of consuming component names (declared via
        SubStrategyComponent.consumes_feeds), for every strategy component across
        all regimes -- configuration = intent, regardless of which regime is active."""
        by_feed: dict[str, list] = {}
        for regime_comps in self._components.values():
            for comp in regime_comps.values():
                for feed in comp.consumes_feeds:
                    by_feed.setdefault(feed, []).append(comp.name)
        for reg in self._block_regimes.values():  # E-060 S3a: each block's own gate
            for b in reg["blocks"]:
                for feed, names in b.gate.required_feeds().items():
                    by_feed.setdefault(feed, []).extend(f"{b.id}.gate.{n}" for n in names)
        return {feed: tuple(sorted(names)) for feed, names in by_feed.items()}

    def forecast(self, regime: MarketRegime) -> Tuple[float, Dict[str, Any]]:
        rkey = regime.value
        cfg  = self._regime_cfgs.get(rkey)
        if cfg is None:
            return 0.0, {}
        if rkey in self._block_regimes:  # E-060 S3a opt-in combiner
            if self._block_fault:
                raise BlockCombinerError(self._block_fault)
            return self._forecast_blocks(rkey)

        comp_refs = cfg["components"]
        total_w   = sum(c["weight"] for c in comp_refs)
        ensemble  = 0.0
        debug: Dict[str, Any] = {}

        for c in comp_refs:
            cid = c["id"]
            h   = self._history.get(rkey, {}).get(cid)
            if not h or len(h) < 2:
                return 0.0, {"not_ready_component": cid}
            value  = apply_transform_pipeline(pd.Series(list(h)), c["transforms"], self._data)
            w_norm = c["weight"] / total_w
            ensemble += w_norm * value
            debug[cid] = {
                "last_history_value":    float(h[-1]),
                "post_pipeline_value":   float(value),
                "weight_normalized":     float(w_norm),
                "weighted_contribution": float(w_norm * value),
            }
        return float(np.clip(ensemble, -20.0, 20.0)), debug
