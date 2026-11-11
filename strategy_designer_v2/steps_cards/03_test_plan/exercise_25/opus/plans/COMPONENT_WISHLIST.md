# Component wish list

One block per idea that needs components the catalogue does not have.

## 003-07_quiet-hours-moves-revert_1d
- Component: RelativeVolumeRegimeComponent: the bar's volume divided by the mean volume of the last N bars (for example 20), current bar excluded, from the `volume` column; it falls below 1 as volume thins and rises above 1 as it swells | measures: situation
- Component: DayOfWeekRegimeComponent: the UTC weekday of the bar's `timestamp` (0 = Monday to 6 = Sunday), so a rule can select weekend bars; on 1d bars this is the only form of "quiet time" the bars carry | measures: situation

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiAtPriorPriceHigh: from closes, finds the previous highest close in a lookback (excluding the current swing) and outputs the Wilder RSI on that bar, a 0 to 100 value | measures: comparison
- Component: RsiBearishDivergence: from closes, on each bar outputs (RSI at the previous price high − current RSI) × max(0, close position at the top of its N-bar range); it is 0 with no new high or no RSI shortfall, and it grows with both the RSI shortfall and how close the close is to a new high (negated for a short forecast) | measures: situation

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiDivergenceComponent: from closes, Wilder RSI(14) at the current bar minus RSI at the lowest close of the prior N bars (excluding the last few), scaled by how close the current close is to or below that prior low; positive and growing as price sits further below the prior low while RSI sits further above its value there, 0 when there is no new low | measures: situation
- Component: RsiRangePositionComponent: from closes, where the current Wilder RSI(14) sits in its own N-bar min-max range, -1 at the bottom to +1 at the top; combined with the Donchian position (RSI position minus price position) it gives a graded "price at its low, RSI not at its low" reading | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RsiRangePositionComponent: where the current RSI (Wilder, from closes) sits within its own range over the last N bars, as (RSI - max RSI) / (max RSI - min RSI); 0 when RSI makes a new high, more negative the further RSI is below its prior high | measures: situation
- Component: PriceRsiDivergenceComponent: the gap between the close's position in its N-bar close range and RSI's position in its own N-bar range (price position minus RSI position), from closes; 0 when both make new highs together, larger when price is at its high but RSI is below its own high | measures: comparison

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RsiRangePositionComponent: where the current RSI(14) of the closes sits between its lowest and highest values over the last N bars, scaled from -1 to +1. It grows towards +1 as RSI rises further above its window low, and is -1 when RSI makes a new low | measures: comparison
- Component: PriceRsiDivergenceComponent: from the closes, close range position minus RSI range position over N bars (graded). It is most positive when price is at its N-bar low while RSI stays above its own N-bar low, and most negative in the mirror case at highs | measures: situation

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RSIRangeGapComponent: from closes, Wilder RSI(14) and the close's position in its 14-bar range. Output is the close's range position (0 to 1) minus RSI's position in its own 14-bar range (0 to 1). It grows from 0 towards +1 as the close sits at its high while RSI sits further below its own recent peak, and is negative for the reverse. | measures: comparison

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiRangePositionComponent: where the current Wilder RSI(period) sits inside its own min..max over the last N bars, from closes, as (2 x pos - 1); it grows from -1 when RSI is at its N-bar low to +1 at its N-bar high | measures: comparison
