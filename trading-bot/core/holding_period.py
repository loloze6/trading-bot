"""The holding period: strategies.min_holding_bars (operator's option 2, 2026-11-20; topics/30 and 34;
strategy_designer_v2/steps_cards/common/forecast.md 7). All of its logic is here; core/trading_bot.py makes one call.

An idea claims a move over its horizon, so each bet it makes is held for that horizon (N bars):
- A bet is a rise of the forecast on its own side (long: up; short: down) of at least the band, measured from the
  forecast's lowest level on that side since its last bet (a start from 0, or a change of side, starts from 0). A
  smaller rise is noise, not a bet. The band is the risk layer's min_allocation_change, on the signal scale
  (forecast / 10), the same threshold that decides a trade.
- A bet's size is the share of this bar's sized target that the rise accounts for: target x rise / |forecast|.
  The sizing alone (volatility) never makes a bet.
- The floor: a long book does not go below the sum of its long bets still within their N bars (at most its
  position); a short book, symmetrically. With no bet held on the book's side, nothing is held.
Rises and new positions are bought at once. The risk gate and the gap tiers act after this and are never held. A NaN
forecast makes no bet and leaves the state as it was.

Why this can't leak: it reads only this bar's forecast and target and the earlier bars' (its own state).
"""
import math
from collections import deque
from typing import Dict


class HoldingPeriod:
    def __init__(self, bars: int, band: float):
        self.bars = int(bars)
        self.band = float(band)
        self._bets: Dict[str, deque] = {}       # per symbol: the last N bars' bets (signed sizes, 0.0 for none)
        self._prev: Dict[str, float] = {}       # per symbol: the previous bar's signal (forecast / 10)
        self._low: Dict[str, float] = {}        # per symbol: the lowest signal on its side since its last bet

    def _bet(self, symbol: str, signal: float, target: float) -> float:
        """The bet made on this bar (a signed size; 0.0 for none), and the state updated."""
        side = (signal > 0) - (signal < 0)
        prev = self._prev.get(symbol, 0.0)
        if side == 0 or (prev > 0) != (signal > 0) or (prev < 0) != (signal < 0):
            self._low[symbol] = 0.0                       # flat, or a change of side: measured from 0
        low = self._low.get(symbol, 0.0)
        self._prev[symbol] = signal
        size = side * signal                              # the signal's size on its side
        if side == 0:
            return 0.0
        if size - low >= self.band - 1e-9 and size > 0:
            self._low[symbol] = size
            return target * (size - low) / size
        self._low[symbol] = min(low, size) if low > 0 else low
        return 0.0

    def apply(self, symbol: str, forecast: float, target: float, position: float) -> float:
        """The target after the hold: records this bar's bet, then keeps the book at the bets still held."""
        bets = self._bets.get(symbol)
        if bets is None:
            bets = self._bets[symbol] = deque(maxlen=self.bars)
        if forecast is None or not math.isfinite(forecast):
            bets.append(0.0)
        else:
            bets.append(self._bet(symbol, forecast / 10.0, target))
        if position > 0.0 and target < position:
            held = sum(b for b in bets if b > 0.0)
            if held > 0.0:
                return max(target, min(position, held))
        elif position < 0.0 and target > position:
            held = sum(-b for b in bets if b < 0.0)
            if held > 0.0:
                return min(target, max(position, -held))
        return target
