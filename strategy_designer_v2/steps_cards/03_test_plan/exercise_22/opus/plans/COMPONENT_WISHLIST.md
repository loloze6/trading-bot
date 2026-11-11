# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiRangeDivergence: computes RSI(14, Wilder) from closes, then its position in its own range over the last N bars (2 x pos - 1); outputs the close's Donchian position over the same N bars minus that RSI position, signed (bearish when price is near its high and RSI is well below its high), and grows as the gap widens | measures: comparison
- Component: RsiAtPriorHighGap: finds the previous swing high of the closes within the last N bars and records RSI there; outputs (RSI at that prior high - current RSI) scaled by how far the current close exceeds that prior high, positive and growing for a new price high with a lower RSI high, and signed for the low side | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiBullishDivergence: from closes, using RSI(14) and a lookback window (for example 20 bars); when the current close is the lowest close of the window, outputs RSI now minus RSI at the previous swing low of the close in that window, times how far the new low undercuts the old one in percent; 0 when there is no new low; grows as the RSI low rises further above the earlier RSI low | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RSIRangePosition: where the current RSI(14) sits in its own last-N-bar range, (RSI - min RSI) / (max RSI - min RSI) x 2 - 1, from closes. It runs from -1 at the RSI low of the window to +1 at a new RSI high. Taking price range position minus this value gives a graded divergence that grows as price makes a new high while RSI stays below its earlier peak. | measures: situation

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RSIDivergence: from closes, over a lookback (e.g. 14-period RSI, 20-bar window), when the close is at or below the lowest prior close of the window, outputs RSI now minus RSI at the bar of that prior lowest close (and the mirror for highs, sign flipped); 0 when no new extreme; grows with how much higher the RSI low is than the price low implies | measures: situation
- Component: RSIRollingLowDistance: from closes, the current RSI minus the lowest RSI over the prior N bars; positive when RSI stays above its prior low, negative when RSI makes a new low; grows with the gap | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RsiBearishDivergence: from closes, on bars where the close is at or near the highest close of the last N bars (e.g. 14), the RSI(14) maximum over those N bars minus the current RSI(14), graded by how close the close is to the high; 0 when the close is not near its high, and it grows as RSI falls further below its earlier peak while price sets the new high | measures: situation

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RSIRangePosition: where the current Wilder RSI (from closes) sits between its lowest and highest value over the last N bars, as (2 x pos - 1) scaled to forecast units. It is -1 when RSI is at its N-bar low and grows toward +1 as RSI sits higher above that low while price is at its own range low. | measures: situation
