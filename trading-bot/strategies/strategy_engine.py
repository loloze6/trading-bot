from collections import deque
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
import logging

from strategies.registry import apply_transform_pipeline, _load_class, component_effective_lookback
from strategies.strategy_base import MarketRegime, SubStrategyComponent

logger = logging.getLogger("trading_bot")


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

    def reset_history(self) -> None:
        """CUL-271: large-gap segment split -- drop accumulated per-regime
        component history so post-gap readiness re-derives from real post-gap
        bars only. Deques keep their maxlen."""
        for regime_hist in self._history.values():
            for h in regime_hist.values():
                h.clear()

    def is_ready(self, regime: MarketRegime) -> bool:
        rkey = regime.value
        if rkey not in self._components:
            return True
        return all(
            len(h) >= self._warmup
            for h in self._history[rkey].values()
        )

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
