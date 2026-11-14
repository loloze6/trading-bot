# Component wish list (hourly plans)

## 003-01_low-volume-up-move-reverts_1h
- Component: RelativeVolumeComponent: the latest bar's volume divided by the mean volume of the prior N bars (for example 24), from the volume column. It is 1 at normal volume and falls toward 0 as volume thins; with a log or a negated form it grows as volume gets thinner, so it can be thresholded in a regime rule or used as a graded weight. | measures: situation
- Component: VolumeWeightedMoveComponent: the return over the last k bars (from close) multiplied by (1 - relative volume over the same k bars), clipped at 0 on the volume side. It grows with both the size of the up move and how thin its volume was, signed by the move's direction. | measures: situation

## 003-04_high-volume-down-move-continues_1h
- Component: RelativeVolumeComponent: the current bar's `volume` divided by the mean `volume` of the previous N bars (e.g. 24 on 1h); 1 is normal, and it rises as volume grows heavier (2 means twice the usual), 0 or above, from the volume column. | measures: situation

## 003-06_down-move-retrace-by-volume_1h
- Component: RelativeVolumeComponent: the mean volume over the last `period` bars divided by the mean volume over a longer `baseline` window (`volume` column), centred at 0 by subtracting 1 (or its log); grows above 0 as the move's volume gets heavier and falls below 0 as it gets thinner | measures: comparison
- Component: VolumeWeightedDrawdownComponent: the percent close change over `period` bars (`close` column), negated so drops are positive, times (1 minus relative volume over those same bars, from the `volume` column), clipped at 0 below; grows with the size of the drop and with how thin its volume was | measures: situation

## 005-01_bearish-rsi-divergence-reversal_1h
- Component: RsiBearishDivergence: from closes, finds the highest close in the prior N bars and the RSI(14) on that bar. When the current close is at or above that prior high, it outputs (RSI at prior high − current RSI) x (percent by which the close exceeds the prior high), or 0 otherwise. The value grows as momentum fades more behind a larger new high. | measures: comparison
- Component: RsiBullishDivergence: the mirror case from closes, for a new low with a higher RSI low than at the prior price low. It outputs (current RSI − RSI at prior low) x (percent below the prior low), or 0 otherwise. Needed for the brief's lows side and as the non-divergence contrast. | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1h
- Component: RsiPriceLowDivergence: over the last N closes (period 48, RSI 14), RSI's position in its own N-bar range minus the close's position in its N-bar range. Positive and growing as the close sits at or below its range low while RSI stays further above its own range low. Signed, graded; the mirror case gives negative values. | measures: situation
- Component: RsiAtPriorLow: the RSI(14) value at the bar of the lowest close in the N bars before the latest swing, subtracted from the current RSI when the current close is below that prior low. Grows with the RSI's higher-low margin, 0 when price has not made a new low. | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1h
- Component: RsiRangePositionComponent: Wilder RSI(period) from closes, then (2 x pos - 1) x sf with pos = (RSI - min RSI) / (max RSI - min RSI) over the last `period` bars, current included; it grows from -sf to +sf as RSI rises toward its own recent high | measures: comparison
- Component: PriceRsiDivergenceComponent: from closes, Donchian position of the close minus RSI range position over the same window (each scaled -1..+1), times sf; it is positive and grows when price is near its range high while RSI is below its own high (bearish divergence), and negative for the mirror case at lows | measures: situation

## 005-04_divergent-low-stronger-than-confirmed_1h
- Component: RsiLowDivergence: from closes, over the last N bars, takes (RSI_t minus the lowest RSI in the window) times the closeness of close_t to its N-bar lowest close, (1 - Donchian pos). It is near 0 away from lows, near 0 or negative when RSI also makes a new low, and grows as price sits at its low while RSI holds further above its earlier low. | measures: situation
- Component: RsiLowConfirmation: from closes, it is the same window and closeness weight, multiplied by (lowest RSI in the window minus RSI_t, floored at 0) plus a small closeness term. It is positive and grows when a new price low comes with RSI at or below its own window low, so it gives the non-divergent comparison group. | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1h
- Component: RsiBearishDivergence: from closes, computes how far the close sits in its N-bar range (as Donchian does) times the gap between RSI at the previous N-bar closing high and the current RSI, clipped at 0 when RSI is not lower; grows as price gets nearer a new high and as the RSI shortfall widens | measures: situation
- Component: RsiAtPriorHighGap: from closes, computes the RSI on the bar of the highest close of the last N bars (excluding the current bar) minus the current RSI; positive and growing as the current RSI falls further below that earlier peak | measures: comparison

## 005-06_bullish-divergence-downtrend-continues_1h
- Component: RsiRangePositionComponent: from closes, compute RSI(period, Wilder), then (2 x pos - 1) with pos = (RSI - lowest RSI) / (highest RSI - lowest RSI) over the last `period` bars, current bar included; -1 at the RSI's own low, rising continuously to +1 at its high | measures: comparison
- Component: PriceRsiDivergenceComponent: from closes, the RSI range position minus the close's range position (as in Donchian) over the same window; grows continuously as the close sits nearer its low while RSI sits further above its own low (positive = bullish divergence), negative for the mirror case | measures: situation
