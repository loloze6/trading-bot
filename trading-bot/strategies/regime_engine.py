from collections import deque
from typing import Dict, Any, List, Tuple
import pandas as pd
import logging

from strategies.registry import (
    apply_transform_pipeline,
    _load_class,
    component_effective_lookback,
)
from strategies.strategy_base import MarketRegime, SubStrategyComponent

logger = logging.getLogger("trading_bot")

_REGIME_MAP = {
    "trending": MarketRegime.TRENDING,
    "mean_reversion": MarketRegime.MEAN_REVERSION,
    "chop": MarketRegime.CHOP,
    "unknown": MarketRegime.UNKNOWN,
}


class ConfigDrivenRegimeEngine:
    """
    Two modes, selected by config["mode"]:
    - "threshold_rules" (default): priority-ordered if/else rules with absolute thresholds.
    - "score": weighted transformed components, argmax picks the winner.
    """

    def __init__(self, config: Dict[str, Any]):
        self._mode = config.get("mode", "threshold_rules")
        self.min_score = config.get("min_score", 0.35)
        self.min_margin = config.get("min_margin", 0.05)

        self._veto_cfgs = config.get("vetoes", [])

        # Phase 1: instantiate components (validates class paths at startup)
        self._components: Dict[str, SubStrategyComponent] = {}
        for c in config["components"]:
            cls = _load_class(c["class"])
            self._components[c["id"]] = cls(
                name=c["id"], weight=1.0, parameters=c.get("params", {})
            )

        # Validate veto IDs reference declared components
        veto_ids = {v["id"] for v in self._veto_cfgs}
        missing = veto_ids - self._components.keys()
        if missing:
            raise ValueError(f"Veto references undeclared component IDs: {missing}")

        # Phase 2: derive lookback — max of component requirements AND transform minimums.
        # Detector components have no transforms; score-mode regime components do and share
        # the same history deques, so their transform minimums must also be accounted for.
        base_periods = {
            cid: comp.get_required_periods() for cid, comp in self._components.items()
        }
        # Score mode: each regime's scoring components may declare transforms
        for rcfg in config.get("regimes", {}).values():
            for c_spec in rcfg.get("components", []):
                cid = c_spec["id"]
                needed = component_effective_lookback(c_spec, base_periods.get(cid, 1))
                base_periods[cid] = max(base_periods.get(cid, 1), needed)
        self.lookback = max(base_periods.values(), default=50)

        # Phase 3: create history deques sized to lookback
        self._history: Dict[str, deque] = {
            cid: deque(maxlen=self.lookback) for cid in self._components
        }
        self._veto_bars: Dict[str, int] = {v["id"]: 0 for v in self._veto_cfgs}

        # threshold_rules config
        self._rules = config.get("rules", [])
        self._default_regime = config.get("default_regime", "unknown")

        # score mode config
        self._regime_names = list(config.get("regimes", {}).keys())
        self._regime_cfgs = config.get("regimes", {})

        # State
        self.current_regime = MarketRegime.UNKNOWN
        self.previous_regime = MarketRegime.UNKNOWN
        self.bars_in_current_regime = 0
        self.regime_change_count = 0
        self._data: pd.DataFrame = None

    # ------------------------------------------------------------------
    def update(self, data: pd.DataFrame) -> None:
        self._data = data
        for cid, comp in self._components.items():
            comp.update(data)
            if comp.is_ready():
                self._history[cid].append(comp.raw_value())

    def is_ready(self) -> bool:
        if self._mode == "threshold_rules":
            return all(len(h) >= 1 for h in self._history.values())
        return all(len(h) >= self.lookback for h in self._history.values())

    def get_required_periods(self) -> int:
        return max(
            (c.get_required_periods() for c in self._components.values()), default=0
        )

    def required_feeds(self) -> dict[str, tuple[str, ...]]:
        """Feed name -> sorted tuple of consuming component names (declared via
        SubStrategyComponent.consumes_feeds), for every regime-detector component."""
        by_feed: dict[str, list] = {}
        for comp in self._components.values():
            for feed in comp.consumes_feeds:
                by_feed.setdefault(feed, []).append(comp.name)
        return {feed: tuple(sorted(names)) for feed, names in by_feed.items()}

    # ------------------------------------------------------------------
    def classify(self) -> Tuple[MarketRegime, Dict[str, Any]]:
        if not self.is_ready():
            return MarketRegime.UNKNOWN, {}

        self.previous_regime = self.current_regime
        debug: Dict[str, Any] = {}

        # Vetoes — evaluated first regardless of mode
        for veto in self._veto_cfgs:
            cid = veto["id"]
            val = apply_transform_pipeline(
                self._series(cid), veto["transforms"], self._data
            )
            fired = all(self._compare(val, rule) for rule in veto["rules"])
            self._veto_bars[cid] = self._veto_bars[cid] + 1 if fired else 0
            if self._veto_bars[cid] >= veto.get("consecutive_bars", 1):
                self.current_regime = _REGIME_MAP.get(
                    veto["result"], MarketRegime.UNKNOWN
                )
                self._tick(debug)
                debug["forced_by_veto"] = veto["result"]
                return self.current_regime, debug

        if self._mode == "threshold_rules":
            self.current_regime = self._classify_threshold_rules()
        elif self._mode == "score_product":
            self.current_regime = self._classify_score_product(debug)
        else:
            self.current_regime = self._classify_score(debug)

        self._tick(debug)
        return self.current_regime, debug

    # ------------------------------------------------------------------
    # threshold_rules mode
    # ------------------------------------------------------------------
    def _classify_threshold_rules(self) -> MarketRegime:
        raw = {
            cid: list(self._history[cid])[-1]
            for cid in self._components
            if self._history[cid]
        }
        for rule in self._rules:
            if self._matches_rule(rule, raw):
                return _REGIME_MAP.get(rule["regime"], MarketRegime.UNKNOWN)
        return _REGIME_MAP.get(self._default_regime, MarketRegime.UNKNOWN)

    def _matches_rule(self, rule: Dict, raw: Dict) -> bool:
        for condition_set in rule["any_of"]:
            if all(self._eval_cond(c, raw) for c in condition_set):
                return True
        return False

    @staticmethod
    def _compare(val: float, cond: Dict) -> bool:
        """Evaluate one op/value condition against a scalar. Used by both vetoes and rules."""
        op = cond["op"]
        if op == "gte":
            return val >= cond["value"]
        if op == "gt":
            return val > cond["value"]
        if op == "lte":
            return val <= cond["value"]
        if op == "lt":
            return val < cond["value"]
        if op == "between":
            return cond["low"] <= val <= cond["high"]
        return False

    @staticmethod
    def _eval_cond(cond: Dict, raw: Dict) -> bool:
        val = raw.get(cond["id"])
        return False if val is None else ConfigDrivenRegimeEngine._compare(val, cond)

    # ------------------------------------------------------------------
    # score mode
    # ------------------------------------------------------------------
    def _classify_score(self, debug: Dict) -> MarketRegime:
        scores: Dict[str, float] = {}
        for rname, rcfg in self._regime_cfgs.items():
            total_w = sum(c["weight"] for c in rcfg["components"])
            score = sum(
                c["weight"]
                * apply_transform_pipeline(
                    self._series(c["id"]), c["transforms"], self._data
                )
                for c in rcfg["components"]
            )
            scores[rname] = score / total_w if total_w > 0 else 0.0

        winner = max(scores, key=scores.get)
        sorted_vals = sorted(scores.values(), reverse=True)
        margin = sorted_vals[0] - sorted_vals[1] if len(sorted_vals) > 1 else 1.0

        debug["scores"] = {r: round(s, 4) for r, s in scores.items()}
        debug["winner"] = winner
        debug["margin"] = round(margin, 4)

        if scores[winner] >= self.min_score and margin >= self.min_margin:
            return _REGIME_MAP.get(winner, MarketRegime.UNKNOWN)
        return MarketRegime.UNKNOWN

    # ------------------------------------------------------------------
    # score_product mode
    # ------------------------------------------------------------------
    def _classify_score_product(self, debug: Dict) -> MarketRegime:
        scores: Dict[str, float] = {}
        for rname, rcfg in self._regime_cfgs.items():
            product = 1.0
            for c in rcfg["components"]:
                val = apply_transform_pipeline(
                    self._series(c["id"]), c["transforms"], self._data
                )
                divisor = c.get("divisor", 1.0)
                product *= (val / divisor) if divisor != 0.0 else val
            scores[rname] = product

        winner = max(scores, key=scores.get)
        sorted_vals = sorted(scores.values(), reverse=True)
        margin = sorted_vals[0] - sorted_vals[1] if len(sorted_vals) > 1 else 1.0

        debug["scores"] = {r: round(s, 4) for r, s in scores.items()}
        debug["winner"] = winner
        debug["margin"] = round(margin, 4)

        if scores[winner] >= self.min_score and margin >= self.min_margin:
            return _REGIME_MAP.get(winner, MarketRegime.UNKNOWN)
        return MarketRegime.UNKNOWN

    # ------------------------------------------------------------------
    def _series(self, cid: str) -> pd.Series:
        return pd.Series(list(self._history[cid]))

    def _tick(self, debug: Dict[str, Any]) -> None:
        if self.current_regime == self.previous_regime:
            self.bars_in_current_regime += 1
        else:
            self.bars_in_current_regime = 1
            self.regime_change_count += 1
            logger.debug(
                f"REGIME CHANGE #{self.regime_change_count}: "
                f"{self.previous_regime.value} → {self.current_regime.value}"
            )
        debug["bars_in_regime"] = self.bars_in_current_regime
