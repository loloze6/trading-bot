from collections import deque
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
import logging

from strategies.registry import (
    apply_transform_pipeline, _load_class, component_effective_lookback, standardise_block_forecast,
)
from strategies.strategy_base import MarketRegime, SubStrategyComponent

logger = logging.getLogger("trading_bot")

# E-060 S3a: the opt-in per-regime block combiner (see validate_block_combiner).
BLOCK_COMBINER_KEYS = ("blocks", "block_standardisation")
BLOCK_STANDARDISATION_KEYS = ("target", "window", "min_periods")


def validate_block_combiner(rname: str, rcfg: Dict[str, Any]) -> list:
    """Violations (strings) of the opt-in block combiner of one regime; [] when
    the regime uses neither key (every config written before E-060 S3a).

    Shape (both keys together, nothing else):
      "blocks": [{"id": str, "weight": number > 0, "components": [component id, ...]}, ...]
      "block_standardisation": {"target": number > 0, "window": int >= 2,
                                "min_periods": int, 2 <= min_periods <= window}
    Every component of the regime belongs to exactly one block; block ids are
    unique and differ from every component id (they share the debug columns).
    Used by the engine (raises) and by tools/validate_config.py (V13)."""
    if rcfg is None or not any(k in rcfg for k in BLOCK_COMBINER_KEYS):
        return []
    loc = f"strategies.regimes.{rname}"
    out = []
    missing = [k for k in BLOCK_COMBINER_KEYS if k not in rcfg]
    if missing:
        return [f"{loc}: block combiner needs both {list(BLOCK_COMBINER_KEYS)}, missing {missing}"]
    comp_ids = [c.get("id") for c in rcfg.get("components", [])]
    blocks = rcfg["blocks"]
    if not isinstance(blocks, list) or not blocks:
        return [f"{loc}.blocks: must be a non-empty list, got {blocks!r}"]
    seen_b, owned = set(), []
    for i, b in enumerate(blocks):
        if not isinstance(b, dict) or set(b) != {"id", "weight", "components"}:
            out.append(f"{loc}.blocks[{i}]: must have exactly keys id, weight, components; got {b!r}")
            continue
        bid, w, comps = b["id"], b["weight"], b["components"]
        if not isinstance(bid, str) or not bid or bid in seen_b or bid in comp_ids:
            out.append(f"{loc}.blocks[{i}].id={bid!r}: empty, duplicated, or equal to a component id")
        seen_b.add(bid)
        if isinstance(w, bool) or not isinstance(w, (int, float)) or not np.isfinite(w) or w <= 0:
            out.append(f"{loc}.blocks[{i}].weight={w!r}: must be a finite number > 0")
        if not isinstance(comps, list) or not comps:
            out.append(f"{loc}.blocks[{i}].components: must be a non-empty list of component ids")
            continue
        unknown = [c for c in comps if c not in comp_ids]
        if unknown:
            out.append(f"{loc}.blocks[{i}].components: {unknown} are not components of this regime")
        else:
            cw = [c.get("weight") for c in rcfg["components"] if c.get("id") in comps]
            if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in cw) \
                    or sum(cw) <= 0:
                out.append(f"{loc}.blocks[{i}]: its components' weights {cw} must be numbers "
                           f"summing to > 0 (they set the block's internal ratios)")
        owned.extend(comps)
    dup = sorted({c for c in owned if owned.count(c) > 1}, key=str)
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
    if isinstance(t, bool) or not isinstance(t, (int, float)) or not np.isfinite(t) or t <= 0:
        out.append(f"{loc}.block_standardisation.target={t!r}: must be a finite number > 0")
    ints_ok = all(isinstance(x, int) and not isinstance(x, bool) for x in (win, mp))
    if not ints_ok or win < 2 or not (2 <= mp <= win):
        out.append(f"{loc}.block_standardisation: window={win!r}, min_periods={mp!r} -- need "
                   f"integers with 2 <= min_periods <= window")
    return out


class ConfigDrivenStrategyEngine:
    """
    Applies transforms and combines component values per regime per config.
    Returns forecast in [-20, +20]. Regime with null config → 0.0.
    """

    def __init__(self, config: Dict[str, Any]):
        self._regime_cfgs = config["regimes"]
        self._data: pd.DataFrame = None

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

        # E-060 S3a: opt-in block combiner. A regime without `blocks` (every
        # config written before it) never enters these dicts, so its update(),
        # is_ready() and forecast() paths are exactly the code above/below.
        self._block_cfgs:  Dict[str, Dict[str, Any]]   = {}
        self._block_hist:  Dict[str, Dict[str, deque]] = {}
        self._block_seq:   Dict[str, Dict[str, int]]   = {}
        self._update_seq = 0
        for rname, rcfg in self._regime_cfgs.items():
            errors = validate_block_combiner(rname, rcfg)
            if errors:
                raise ValueError("; ".join(errors))
            if rcfg is None or "blocks" not in rcfg:
                continue
            self._block_cfgs[rname] = {"blocks": rcfg["blocks"],
                                       "std": rcfg["block_standardisation"]}
            win = rcfg["block_standardisation"]["window"]
            self._block_hist[rname] = {b["id"]: deque(maxlen=win) for b in rcfg["blocks"]}
            self._block_seq[rname] = {b["id"]: -1 for b in rcfg["blocks"]}

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

    def update(self, data: pd.DataFrame) -> None:
        self._data = data
        for rname, regime_comps in self._components.items():
            for cid, comp in regime_comps.items():
                comp.update(data)
                if comp.is_ready():
                    raw = comp.raw_value()
                    tfs = self._history_tf[rname][cid]
                    if tfs:
                        raw = apply_transform_pipeline(pd.Series([raw]), tfs, data)
                    self._history[rname][cid].append(raw)
        if self._block_cfgs:
            self._update_seq += 1
            for rname in self._block_cfgs:
                self._append_block_values(rname)

    # -- E-060 S3a block combiner -------------------------------------------
    def _block_raw_forecast(self, rname: str, block: Dict[str, Any]) -> float:
        """The block's FINAL forecast as it was validated stand-alone: its
        components' pipelines, weighted by their own weights normalised within
        the block, clipped to +-20 -- the same arithmetic as forecast() below
        on a regime made of only these components."""
        specs = {c["id"]: c for c in self._regime_cfgs[rname]["components"]}
        total_w = sum(specs[cid]["weight"] for cid in block["components"])
        value = 0.0
        for cid in block["components"]:
            h = self._history[rname][cid]
            v = apply_transform_pipeline(pd.Series(list(h)), specs[cid]["transforms"], self._data)
            value += (specs[cid]["weight"] / total_w) * v
        return float(np.clip(value, -20.0, 20.0))

    def _append_block_values(self, rname: str) -> None:
        """Once per update(): append each block's final forecast for THIS bar to
        its rolling history -- only when every one of its components is warm
        (the same len >= warmup the engine's is_ready() requires, and >= 2 as
        forecast() requires), i.e. only values the block would really have
        emitted. Past-only: computed from histories and data up to this bar."""
        need = max(2, self._warmup)
        for block in self._block_cfgs[rname]["blocks"]:
            if all(len(self._history[rname][cid]) >= need for cid in block["components"]):
                self._block_hist[rname][block["id"]].append(self._block_raw_forecast(rname, block))
                self._block_seq[rname][block["id"]] = self._update_seq

    def _forecast_blocks(self, rkey: str) -> Tuple[float, Dict[str, Any]]:
        """Σ (W_b / ΣW) × standardise(block b's final-forecast history), clipped
        to +-20. 0.0 until every block has `min_periods` values of its own
        history and a value for the current bar."""
        cfg = self._block_cfgs[rkey]
        std = cfg["std"]
        total_w = sum(b["weight"] for b in cfg["blocks"])
        ensemble = 0.0
        debug: Dict[str, Any] = {}
        for b in cfg["blocks"]:
            bid = b["id"]
            h = self._block_hist[rkey][bid]
            if len(h) < std["min_periods"] or self._block_seq[rkey][bid] != self._update_seq:
                return 0.0, {"not_ready_block": bid}
            value = standardise_block_forecast(pd.Series(list(h)), std["target"])
            w_norm = b["weight"] / total_w
            ensemble += w_norm * value
            # Same four keys as a component row, so bars.csv consumers read a
            # block as one unit: last_history_value = the block's final
            # (pre-standardisation) forecast, post_pipeline_value = standardised.
            debug[bid] = {
                "last_history_value":    float(h[-1]),
                "post_pipeline_value":   float(value),
                "weight_normalized":     float(w_norm),
                "weighted_contribution": float(w_norm * value),
            }
        return float(np.clip(ensemble, -20.0, 20.0)), debug

    def reset_history(self) -> None:
        """CUL-271: large-gap segment split -- drop accumulated per-regime
        component history so post-gap readiness re-derives from real post-gap
        bars only. Deques keep their maxlen."""
        for regime_hist in self._history.values():
            for h in regime_hist.values():
                h.clear()
        for regime_hist in self._block_hist.values():  # E-060 S3a (empty unless opted in)
            for h in regime_hist.values():
                h.clear()

    def is_ready(self, regime: MarketRegime) -> bool:
        rkey = regime.value
        if rkey not in self._components:
            return True
        ready = all(
            len(h) >= self._warmup
            for h in self._history[rkey].values()
        )
        if ready and rkey in self._block_cfgs:  # E-060 S3a: standardisation warm-up too
            mp = self._block_cfgs[rkey]["std"]["min_periods"]
            ready = all(len(h) >= mp for h in self._block_hist[rkey].values())
        return ready

    def get_required_periods(self) -> int:
        all_comps = [c for rc in self._components.values() for c in rc.values()]
        return max((c.get_required_periods() for c in all_comps), default=0)

    def required_feeds(self) -> dict[str, tuple[str, ...]]:
        """Feed name -> sorted tuple of consuming component names (declared via
        SubStrategyComponent.consumes_feeds), for every strategy component across
        all regimes -- configuration = intent, regardless of which regime is active."""
        by_feed: dict[str, list] = {}
        for regime_comps in self._components.values():
            for comp in regime_comps.values():
                for feed in comp.consumes_feeds:
                    by_feed.setdefault(feed, []).append(comp.name)
        return {feed: tuple(sorted(names)) for feed, names in by_feed.items()}

    def forecast(self, regime: MarketRegime) -> Tuple[float, Dict[str, Any]]:
        rkey = regime.value
        cfg  = self._regime_cfgs.get(rkey)
        if cfg is None:
            return 0.0, {}
        if rkey in self._block_cfgs:  # E-060 S3a opt-in combiner
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
