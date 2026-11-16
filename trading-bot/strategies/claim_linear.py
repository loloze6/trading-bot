"""ClaimStrengthComponent: runs a research claim's own code and emits its continuous strength.

The claim's code defines `event` (bool Series) and `strength` (signed numeric Series). The raw value is the
current bar's strength on every bar (0 where not finite). `event` is only reported in debug_info (branch 1
measures the claim on event bars); `horizon` is accepted and ignored. Never clipped or scaled: the engine's
`standardise` transform grades it.
No lookahead: the window holds only bars at or before the current close; code with a future shift is refused.
Config: {"class": "strategies.claim_linear.ClaimStrengthComponent",
         "params": {"code": "...", "horizon": 12, "min_bars": 200}}
"""
import re
from typing import Any, Dict, Optional
import numpy as np
import pandas as pd
from strategies.strategy_base import SubStrategyComponent

_FORBIDDEN = re.compile(r"shift\(\s*-|center\s*=\s*True|\[::-1\]|import\s|open\(|exec\(|eval\(")


def _spaced(cond: pd.Series, n: int) -> pd.Series:
    cond = cond.fillna(False).astype(bool)
    prior = cond.shift(1).rolling(n, min_periods=1).max().fillna(0).astype(bool)
    return cond & ~prior


class ClaimStrengthComponent(SubStrategyComponent):
    report_debug = True   # the engine copies event and strength into the per-bar output
    def __init__(self, name: str = "ClaimStrength", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.code = str(self.parameters.get("code", ""))
        if not self.code.strip():
            raise ValueError("ClaimStrengthComponent: params.code is required")
        if _FORBIDDEN.search(self.code):
            raise ValueError("ClaimStrengthComponent: params.code uses a forbidden form (future shift, import, io)")
        self.horizon = int(self.parameters.get("horizon", 12))
        self.min_bars = int(self.parameters.get("min_bars", 200))
        self._compiled = compile(self.code, "<claim_code>", "exec")
        self._last_ts = None

    def update(self, data: pd.DataFrame):
        self.data = data
        if not self.is_ready():
            return
        df = data[["open", "high", "low", "close", "volume"]].copy()
        if "timestamp" in data.columns:
            df.index = pd.to_datetime(data["timestamp"])
        ts = df.index[-1]
        if self._last_ts is not None and ts == self._last_ts:
            return  # same bar fed twice: no double count
        self._last_ts = ts
        ns = {"df": df, "ret": df["close"].pct_change(), "hour": pd.Series(df.index.hour, index=df.index),
              "dow": pd.Series(df.index.dayofweek, index=df.index), "spaced": _spaced, "pd": pd, "np": np}
        exec(self._compiled, ns)  # the claim's own few lines
        ev, st = ns.get("event"), ns.get("strength")
        event = bool(ev.iloc[-1]) if isinstance(ev, pd.Series) and len(ev) else False
        s = float(st.iloc[-1]) if isinstance(st, pd.Series) and len(st) else float("nan")
        s = s if np.isfinite(s) else 0.0
        self._raw_value = s   # strength on every bar, 0 where not finite; event only goes to debug_info
        self.confidence = 1.0
        self.debug_info = {"event": event, "strength": s}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.min_bars

    def get_required_periods(self) -> int:
        return self.min_bars
