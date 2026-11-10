# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiBearishDivergence: from closes, finds the most recent prior swing high within a lookback (e.g. 48 bars). While the current close is above that swing high, it outputs (RSI at that swing high − current RSI(14)), else 0. The output is positive and grows as RSI's shortfall widens; used negated, it gives a short. | measures: comparison
- Component: PriorSwingHighExcess: from closes, gives the percent by which the current close exceeds the most recent prior swing high within the lookback (0 if not above). It grows with the size of the new high. | measures: situation

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: rsi_low_divergence: over a lookback of closes, find the previous swing low before the current bar and output RSI(now) minus RSI(at that low), signed, from closes. It is positive and grows as RSI's low rises further above its earlier low, negative for a lower RSI low. It is weighted by how far the current close sits below that earlier low, so it is near 0 when no new low is made. | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RsiHighGapComponent: on closes, the Wilder RSI(14) minus the highest RSI of the last `period` bars before the current one (and, for lows, minus the lowest); graded, 0 when RSI confirms the price extreme, growing more negative the further RSI falls short of its prior high | measures: situation

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RSIDivergence: from closes, compute Wilder RSI(14) and the price range position over the last N (e.g. 20) bars. Output (RSI now − lowest RSI of the prior N bars) × (1 − range position of the close), and the mirror for highs with the sign flipped. It is near 0 when price is mid-range or RSI confirms the extreme, and grows with how far RSI sits above its prior low while price is at its low | measures: situation
- Component: RollingExtremeRSI: from closes, the lowest (and highest) RSI(14) value over the prior N bars, excluding the current bar, so the current RSI can be compared with its earlier low; graded in RSI points | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RSIRangePosition: the Wilder RSI(14) from closes, placed in its own range over the last `period` bars as (2 x (RSI - min RSI) / (max RSI - min RSI) - 1); it is +1 when RSI is at its window high and falls as RSI sits further below its earlier peak | measures: situation
- Component: PriceRsiDivergence: the Donchian position of the close over `period` bars minus the RSIRangePosition over the same `period`, from closes; it is graded, and grows when price is at the top of its range while RSI sits below its own earlier high | measures: situation

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiRangePosition: where the current RSI(14), from closes, sits between its lowest and highest values over the last N bars; graded from -1 at its low to +1 at its high, so it rises as RSI holds above its own recent low | measures: situation
- Component: PriceRsiLowDivergence: from closes, the RSI(14) now minus the RSI at the bar of the lowest close of the prior N bars, multiplied by how far the current close is below that prior lowest close (0 when it is not below); grows as price undercuts its earlier low by more while RSI stays further above its earlier reading | measures: comparison
