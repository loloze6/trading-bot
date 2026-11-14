# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiBearishDivergence: from closes over N bars (e.g. 20 on 1d, RSI 14), price's position in its N-bar close range minus RSI's position in its own N-bar range, or RSI at the previous swing high minus RSI now when the close sets a new N-bar high; it grows as price nears the top of its range while RSI falls further below its earlier peak, near 0 when they agree | measures: situation
- Component: RsiAtPriorPriceHigh: from closes, the RSI value on the bar of the previous N-bar closing high before the current one, stored as a graded level for comparison with RSI now; a higher prior RSI gives a larger gap | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiBullishDivergence: finds the latest and the previous swing low of the closes in a lookback window and takes RSI (Wilder, 14) at each; outputs (RSI at current low − RSI at previous low) when the current price low is below the previous one, else 0; the value grows with the RSI gap, and could be weighted by how deep the new price low is | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RsiRangePosition: where the current RSI (Wilder, period 14, from closes) sits within its own highs and lows over the last N bars, from -1 at the window's lowest RSI to +1 at its highest; it grows as RSI nears a new high | measures: comparison
- Component: PriceRsiDivergence: Donchian range position of the closes minus RsiRangePosition over the same N bars, from closes; it grows as price nears a new high while RSI stays below its prior high, and is near 0 when both confirm | measures: situation

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RsiLowDivergence: when the close is at or near its N-bar lowest close, it outputs RSI(14) now minus RSI at the earlier lowest close of that window (from closes). It is positive and grows with the gap when RSI makes a higher low, negative when RSI also makes a lower low, and near 0 away from new lows. | measures: situation
- Component: RsiLowConfirmation: the signed counterpart that gives a size to new lows confirmed by a new RSI low (RSI now below its N-bar minimum, from closes). It grows as RSI falls further below its earlier low, so returns after confirmed lows can be compared with returns after divergent lows. | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RsiPeakGap: the highest RSI over the prior N bars minus the current RSI, using the Wilder RSI from closes; grows as the current RSI falls further below its recent peak | measures: comparison
- Component: RsiBearishDivergence: the Donchian position of the close in its N-bar range of closes (0 to 1, 1 at a new high) times RsiPeakGap, signed positive; grows when the close is nearer its N-bar high and the RSI is further below its prior peak | measures: situation
