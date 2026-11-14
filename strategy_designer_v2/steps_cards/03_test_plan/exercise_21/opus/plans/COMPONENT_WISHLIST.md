# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiRangePositionComponent: from closes, computes the Wilder RSI(14), then (2 x pos - 1) x sf, where pos is where the current RSI sits between the min and max of its last N values (same window as Donchian). It is +sf when RSI is at its window high; subtracted from the Donchian price position, the gap grows as price makes a new high with RSI further below its earlier peak | measures: comparison
- Component: RsiBearishDivergenceComponent: from closes, Donchian price position over N bars minus the RSI range position over the same N bars. It is positive and larger when the close is at its range top while RSI sits further below its window high, and negative for the mirror (bullish) case | measures: situation

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiAtPriorLow: over the last N closes, finds the previous swing low of the close (the lowest close before the current lookback segment) and returns the Wilder RSI value on that bar; graded in RSI points | measures: comparison
- Component: RsiBullishDivergence: from closes, when the current close is at or below the prior swing low, returns (RSI now - RSI at prior swing low) x (depth of the new low in percent); 0 when there is no new low or RSI is not higher; grows with the RSI gap and with the depth of the new low | measures: situation

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RsiDistanceFromHigh: RSI(14) from closes minus the highest RSI(14) over the last N bars (same window as the price high); 0 when RSI makes a new high, more negative the further RSI lags its prior peak | measures: situation

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RSIRangePosition: where the current Wilder RSI(14) of closes sits within its own min-max over the last N bars, (2 x (RSI - minRSI) / (maxRSI - minRSI) - 1) x sf; it grows from -sf when RSI is at its N-bar low to +sf at its high | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RsiRangePositionComponent: RSI(period) from closes, placed in its own range over the last N bars, as (2 x (RSI - min RSI) / (max RSI - min RSI) - 1); it falls toward -1 as the current RSI sits further below its recent peak, so negated it grows with the size of the lower high | measures: comparison

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiDivergenceComponent: over the last N closes (e.g. 14-bar Wilder RSI, N = 20), computes price range position from closes (0 at the N-bar low) and RSI range position (where current RSI sits between its N-bar min and max); outputs (1 - price position) x RSI position, graded from 0 to 1, growing as price is nearer its low while RSI is further above its own low (signed mirror for highs) | measures: situation
