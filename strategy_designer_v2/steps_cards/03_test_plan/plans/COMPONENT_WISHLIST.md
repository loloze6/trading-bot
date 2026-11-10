# Component wish list

One block per idea that needs components the catalogue does not have.

## 003-01_low-volume-up-move-reverts_1h
- Component: RelativeVolumeComponent: the latest bar's volume divided by the mean volume of the prior N bars (for example 24), from the volume column. It is 1 at normal volume and falls toward 0 as volume thins; with a log or a negated form it grows as volume gets thinner, so it can be thresholded in a regime rule or used as a graded weight. | measures: situation
- Component: VolumeWeightedMoveComponent: the return over the last k bars (from close) multiplied by (1 - relative volume over the same k bars), clipped at 0 on the volume side. It grows with both the size of the up move and how thin its volume was, signed by the move's direction. | measures: situation

## 003-04_high-volume-down-move-continues_1h
- Component: RelativeVolumeComponent: the current bar's `volume` divided by the mean `volume` of the previous N bars (e.g. 24 on 1h); 1 is normal, and it rises as volume grows heavier (2 means twice the usual), 0 or above, from the volume column. | measures: situation

## 003-06_down-move-retrace-by-volume_1h
- Component: RelativeVolumeComponent: the mean volume over the last `period` bars divided by the mean volume over a longer `baseline` window (`volume` column), centred at 0 by subtracting 1 (or its log); grows above 0 as the move's volume gets heavier and falls below 0 as it gets thinner | measures: comparison
- Component: VolumeWeightedDrawdownComponent: the percent close change over `period` bars (`close` column), negated so drops are positive, times (1 minus relative volume over those same bars, from the `volume` column), clipped at 0 below; grows with the size of the drop and with how thin its volume was | measures: situation

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiDivergence: from closes, takes the RSI(14) at the bar of the previous highest close in the lookback and subtracts the RSI at the current close when the current close exceeds that prior high; it is positive and grows as the current RSI falls further below the prior high's RSI, and is 0 when there is no divergence | measures: comparison

## 005-01_bearish-rsi-divergence-reversal_1h
- Component: RsiBearishDivergence: from closes, finds the highest close in the prior N bars and the RSI(14) on that bar. When the current close is at or above that prior high, it outputs (RSI at prior high − current RSI) x (percent by which the close exceeds the prior high), or 0 otherwise. The value grows as momentum fades more behind a larger new high. | measures: comparison
- Component: RsiBullishDivergence: the mirror case from closes, for a new low with a higher RSI low than at the prior price low. It outputs (current RSI − RSI at prior low) x (percent below the prior low), or 0 otherwise. Needed for the brief's lows side and as the non-divergence contrast. | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiBullishDivergence: on closes, finds the lowest close in a lookback (e.g. 5 to 60 bars ago) as the previous low; when the current close is below it, outputs RSI(14) now minus RSI(14) at that prior low, positive and growing with the RSI gap (optionally times the depth of the price undercut), and 0 when there is no new low or no higher RSI low | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1h
- Component: RsiPriceLowDivergence: over the last N closes (period 48, RSI 14), RSI's position in its own N-bar range minus the close's position in its N-bar range. Positive and growing as the close sits at or below its range low while RSI stays further above its own range low. Signed, graded; the mirror case gives negative values. | measures: situation
- Component: RsiAtPriorLow: the RSI(14) value at the bar of the lowest close in the N bars before the latest swing, subtracted from the current RSI when the current close is below that prior low. Grows with the RSI's higher-low margin, 0 when price has not made a new low. | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RsiHighGap: RSI(14) of the closes on the current bar minus the highest RSI(14) over the previous `period` bars, current bar excluded; signed and continuous, more negative the further the current RSI sits below its prior high (divergence), positive when RSI makes a new high too (confirmation) | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1h
- Component: RsiRangePositionComponent: Wilder RSI(period) from closes, then (2 x pos - 1) x sf with pos = (RSI - min RSI) / (max RSI - min RSI) over the last `period` bars, current included; it grows from -sf to +sf as RSI rises toward its own recent high | measures: comparison
- Component: PriceRsiDivergenceComponent: from closes, Donchian position of the close minus RSI range position over the same window (each scaled -1..+1), times sf; it is positive and grows when price is near its range high while RSI is below its own high (bearish divergence), and negative for the mirror case at lows | measures: situation

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RsiRangePositionComponent: from closes, compute Wilder RSI(`period` 14), then output (2 x pos - 1) x `sf`, where pos = (RSI - lowest RSI) / (highest RSI - lowest RSI) over the last `lookback` bars (for example 20 on 1d bars, current bar included). The value is -`sf` when RSI is at a new low and grows continuously toward +`sf` the further RSI sits above its recent low; read alongside price at a new low, a higher value means a stronger bullish divergence. | measures: comparison

## 005-04_divergent-low-stronger-than-confirmed_1h
- Component: RsiLowDivergence: from closes, over the last N bars, takes (RSI_t minus the lowest RSI in the window) times the closeness of close_t to its N-bar lowest close, (1 - Donchian pos). It is near 0 away from lows, near 0 or negative when RSI also makes a new low, and grows as price sits at its low while RSI holds further above its earlier low. | measures: situation
- Component: RsiLowConfirmation: from closes, it is the same window and closeness weight, multiplied by (lowest RSI in the window minus RSI_t, floored at 0) plus a small closeness term. It is positive and grows when a new price low comes with RSI at or below its own window low, so it gives the non-divergent comparison group. | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RsiRangePositionComponent: where the current RSI(14) sits between its own lowest and highest values over the last `period` bars, computed from closes, as (2 x (RSI - min RSI) / (max RSI - min RSI) - 1) x sf; it rises from -sf at the RSI low to +sf at the RSI high | measures: situation
- Component: PriceRsiDivergenceComponent: the close's Donchian range position (closes, `period` bars) minus the RSI's range position over the same bars, both on -1 to +1; it grows towards +2 as price nears its high while RSI stays below its own high, and turns negative for the mirror case at lows | measures: situation

## 005-05_bearish-divergence-uptrend-continues_1h
- Component: RsiBearishDivergence: from closes, computes how far the close sits in its N-bar range (as Donchian does) times the gap between RSI at the previous N-bar closing high and the current RSI, clipped at 0 when RSI is not lower; grows as price gets nearer a new high and as the RSI shortfall widens | measures: situation
- Component: RsiAtPriorHighGap: from closes, computes the RSI on the bar of the highest close of the last N bars (excluding the current bar) minus the current RSI; positive and growing as the current RSI falls further below that earlier peak | measures: comparison

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiDivergenceComponent: from closes over the last `period` bars (for example 14 for the RSI and 20 for the lookback), computes the current RSI minus the RSI at the bar of the previous lowest close in the lookback window, when the current close is at or below that previous low; 0 when price is not at a new low; grows with the size of the RSI's higher low (signed negative for the mirror case at new highs) | measures: situation
- Component: NewLowDepthComponent: from closes, the percent by which the current close sits below the lowest close of the prior `period` bars (excluding the current bar), 0 when it is not below; grows as the new low is deeper | measures: comparison

## 005-06_bullish-divergence-downtrend-continues_1h
- Component: RsiRangePositionComponent: from closes, compute RSI(period, Wilder), then (2 x pos - 1) with pos = (RSI - lowest RSI) / (highest RSI - lowest RSI) over the last `period` bars, current bar included; -1 at the RSI's own low, rising continuously to +1 at its high | measures: comparison
- Component: PriceRsiDivergenceComponent: from closes, the RSI range position minus the close's range position (as in Donchian) over the same window; grows continuously as the close sits nearer its low while RSI sits further above its own low (positive = bullish divergence), negative for the mirror case | measures: situation
