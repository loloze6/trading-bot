# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: rsi_swing_divergence: from closes over a lookback (e.g. 48 bars), find the previous swing high of the close and the RSI(14) at that bar. Output (RSI at previous swing high minus current RSI) times max(0, current close / previous swing-high close minus 1), so it grows as the new high extends further and RSI lags further. Mirror it for lows with the opposite sign: negative for bearish divergence, positive for bullish. | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: rsi_at_swing_lows: from closes, finds the most recent and the previous swing low (lowest close in two consecutive N-bar windows) and returns RSI at each and the price change between them; output is RSI(current low) minus RSI(prior low), which grows as the second low's momentum improves | measures: comparison
- Component: bullish_rsi_divergence: from closes, graded signal that is positive while the current close is at or below the prior swing-low close and RSI is above its value at that prior low; equals (RSI gap in points) × (percent undercut of the prior low), 0 when there is no new low or no higher RSI, and grows with both | measures: situation

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RsiRangePosition: Wilder RSI(14) from the closes, then (2 x (RSI - min RSI) / (max RSI - min RSI) - 1) x sf over the last N bars including the current one. It is +sf when RSI makes a new high in the window, -sf at a new low, and grows continuously as RSI nears its recent high | measures: situation

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RsiRangePosition: where the current RSI (Wilder, from closes) sits inside its own range over the last `period` bars, from -1 at the RSI's period low to +1 at its period high. Paired with the Donchian price position, a price at its range bottom with an RSI well above its own low grows the divergence reading continuously. | measures: situation

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RSIBearishDivergence: from closes, the close's position in its N-bar range (0 to 1, 1 at the N-bar high) times RSI's shortfall below its N-bar maximum ((max RSI_N - RSI) / max RSI_N); zero when price is off its high or RSI is at its own high, and larger as price sits nearer its high while RSI sits further below its prior peak | measures: situation

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiPriceDivergence: from closes over N bars, the close's position in its N-bar close range minus RSI's position in its own N-bar RSI range (each from -1 to +1); graded and signed. It becomes more negative as the close nears its range low while RSI stays above its own low, and more positive in the mirrored case at highs. | measures: situation
- Component: RsiRangePosition: where the latest RSI sits between its lowest and highest value over the last N bars (-1 at its low, +1 at its high), from closes; it grows as RSI moves above its recent low. | measures: comparison
