# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiDivergence: from closes, takes the RSI(14) at the bar of the previous highest close in the lookback and subtracts the RSI at the current close when the current close exceeds that prior high; it is positive and grows as the current RSI falls further below the prior high's RSI, and is 0 when there is no divergence | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiBullishDivergence: on closes, finds the lowest close in a lookback (e.g. 5 to 60 bars ago) as the previous low; when the current close is below it, outputs RSI(14) now minus RSI(14) at that prior low, positive and growing with the RSI gap (optionally times the depth of the price undercut), and 0 when there is no new low or no higher RSI low | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RsiHighGap: RSI(14) of the closes on the current bar minus the highest RSI(14) over the previous `period` bars, current bar excluded; signed and continuous, more negative the further the current RSI sits below its prior high (divergence), positive when RSI makes a new high too (confirmation) | measures: comparison

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RsiRangePositionComponent: from closes, compute Wilder RSI(`period` 14), then output (2 x pos - 1) x `sf`, where pos = (RSI - lowest RSI) / (highest RSI - lowest RSI) over the last `lookback` bars (for example 20 on 1d bars, current bar included). The value is -`sf` when RSI is at a new low and grows continuously toward +`sf` the further RSI sits above its recent low; read alongside price at a new low, a higher value means a stronger bullish divergence. | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RsiRangePositionComponent: where the current RSI(14) sits between its own lowest and highest values over the last `period` bars, computed from closes, as (2 x (RSI - min RSI) / (max RSI - min RSI) - 1) x sf; it rises from -sf at the RSI low to +sf at the RSI high | measures: situation
- Component: PriceRsiDivergenceComponent: the close's Donchian range position (closes, `period` bars) minus the RSI's range position over the same bars, both on -1 to +1; it grows towards +2 as price nears its high while RSI stays below its own high, and turns negative for the mirror case at lows | measures: situation

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiDivergenceComponent: from closes over the last `period` bars (for example 14 for the RSI and 20 for the lookback), computes the current RSI minus the RSI at the bar of the previous lowest close in the lookback window, when the current close is at or below that previous low; 0 when price is not at a new low; grows with the size of the RSI's higher low (signed negative for the mirror case at new highs) | measures: situation
- Component: NewLowDepthComponent: from closes, the percent by which the current close sits below the lowest close of the prior `period` bars (excluding the current bar), 0 when it is not below; grows as the new low is deeper | measures: comparison
