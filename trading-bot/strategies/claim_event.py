"""ClaimEventComponent: a strategy component that runs a research claim's own code.

A validated claim (strategy_designer_v2) is a few lines of pandas defining `a` (event bars) and
`signal` (+1/-1). This component evaluates that code on the history window at every bar and
emits `signal * scaling_factor` for `horizon` bars after an event, 0 otherwise; one position
at a time (an event during a hold is ignored). No lookahead: the window holds only bars at or
before the current close, and the code is refused if it shifts into the future.

Added 2026-11-05 at the first ask of a strategy_designer_v2 run (the engine had no event rule).
Config: {"class": "strategies.claim_event.ClaimEventComponent",
         "params": {"code": "...", "horizon": 12, "scaling_factor": 10.0, "min_bars": 200}}
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


class ClaimEventComponent(SubStrategyComponent):
    def __init__(self, name: str = "ClaimEvent", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.code = str(self.parameters.get("code", ""))
        if not self.code.strip():
            raise ValueError("ClaimEventComponent: params.code is required")
        if _FORBIDDEN.search(self.code):
            raise ValueError("ClaimEventComponent: params.code uses a forbidden form (future shift, import, io)")
        self.horizon = int(self.parameters.get("horizon", 12))
        self.scaling_factor = float(self.parameters.get("scaling_factor", 10.0))
        self.min_bars = int(self.parameters.get("min_bars", 200))
        self._compiled = compile(self.code, "<claim_code>", "exec")
        self._active = 0.0
        self._remaining = 0
        self._last_ts = None

    def _frame(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data[["open", "high", "low", "close", "volume"]].copy()
        if "timestamp" in data.columns:
            df.index = pd.to_datetime(data["timestamp"])
        return df

    def update(self, data: pd.DataFrame):
        self.data = data
        if not self.is_ready():
            return
        df = self._frame(data)
        ts = df.index[-1]
        if self._last_ts is not None and ts == self._last_ts:
            return  # same bar fed twice: no double count
        self._last_ts = ts
        ns = {"df": df, "ret": df["close"].pct_change(), "hour": pd.Series(df.index.hour, index=df.index),
              "dow": pd.Series(df.index.dayofweek, index=df.index), "spaced": _spaced, "pd": pd, "np": np}
        exec(self._compiled, ns)  # the claim's own few lines
        a = ns.get("a"); signal = ns.get("signal")
        event = bool(a.iloc[-1]) if isinstance(a, pd.Series) and len(a) else False
        if self._remaining > 0:
            self._remaining -= 1
        elif event and isinstance(signal, pd.Series):
            s = float(signal.iloc[-1])
            if s != 0 and np.isfinite(s):
                self._active, self._remaining = float(np.sign(s)), self.horizon
        self._raw_value = self._active * self.scaling_factor if self._remaining > 0 else 0.0
        self.confidence = 1.0
        self.debug_info = {"event": event, "remaining": self._remaining, "active": self._active}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.min_bars

    def get_required_periods(self) -> int:
        return self.min_bars
