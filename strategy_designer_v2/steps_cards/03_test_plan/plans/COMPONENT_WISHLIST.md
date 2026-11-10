# Component wish list

One block per idea that needs components the catalogue does not have.

## 003-06_down-move-retrace-by-volume_1d
- Component: RelativeVolumeComponent: the current bar's volume divided by the mean volume of the previous N bars (from the `volume` column), optionally in log form, and continuous: above 1 and growing as volume becomes unusually heavy, below 1 and shrinking toward 0 as it becomes unusually thin | measures: comparison

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RSIBearishDivergenceComponent: from closes, it computes Wilder RSI(14) and the close's position in its N-bar range. The output is (RSI at the highest prior close in the window minus current RSI) times how near the current close is to that high. It is zero when the close is far from the high or RSI is not lower, and it grows as price nears or exceeds the prior high while RSI falls further below its earlier peak value | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiBullishDivergence: from the closes, find the most recent prior swing low (lowest close in a lookback window, before a minimum gap). When the current close is below that swing low's close, output (RSI now - RSI at that swing low) x (percent by which the close undercuts the swing low). Otherwise output 0. The value is graded and positive, and grows as RSI holds higher and the new low goes deeper. | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RSIRangePositionComponent: from closes, RSI(period) minus the highest RSI over the last `lookback` bars, so 0 when RSI is at a new high and more negative the further it lags. Signed variant: (RSI - max RSI) when the close is at its `lookback` high, mirrored for lows | measures: situation

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RSIRangePosition: from closes, the Wilder RSI over `rsi_period` (14). Output is (2 x (RSI - min RSI) / (max RSI - min RSI) - 1) x sf over the last `period` (14) bars, current bar included. It is -sf when RSI is at its lowest of the window and grows toward +sf as RSI sits further above its recent low. | measures: comparison

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiDivergenceComponent: from closes, over a window of `period` bars, computes (RSI now minus the lowest RSI in the window) when the close is at or near the window's lowest close, scaled by how close the close is to that low; it grows as RSI sits further above its prior low while price is at a new low (bullish divergence), and its mirror at highs gives a negative value | measures: situation
- Component: RsiRangePositionComponent: from closes, where the current RSI sits inside its own `period`-bar range, -1 at its lowest to +1 at its highest; combined with `DonchianBreakoutComponent` it gives price range position minus RSI range position, which grows with the size of the divergence | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RsiPriceDivergence: position of the close in its N-bar close range minus the position of the Wilder RSI(14) in its own N-bar range, both from closes, signed; grows from 0 to +1 as price sits at its range top while RSI sits further below its range top (and to -1 for the mirror case at lows) | measures: situation
- Component: RsiRangePosition: (RSI - min RSI) / (max RSI - min RSI) over the last N bars, from closes, 0 to 1; falls as the current RSI sits further below its recent peak | measures: comparison
