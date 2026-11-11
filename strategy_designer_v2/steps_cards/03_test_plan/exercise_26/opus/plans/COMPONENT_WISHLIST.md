# Component wish list

One block per idea that needs components the catalogue does not have.

## 003-07_quiet-hours-moves-revert_1d
- Component: thin-move score: the one-bar return (close vs previous close, percent) times (1 - volume / its 20-bar mean volume), floored at 0 for the volume factor; signed like the move, and larger as the move is bigger and the volume thinner | measures: situation
- Component: volume ratio: volume / its n-bar mean, from the `volume` column, continuous and non-negative; it falls as volume gets thinner, for regime rules or as a graded input | measures: comparison
- Component: weekend share: the share of the bar's time that falls on Saturday or Sunday UTC, from `timestamp`; 1 on weekend daily bars and 0 on weekdays, a fraction on intraday bars that span a boundary | measures: situation

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiBearishDivergence: from closes, finds the previous swing high within a lookback (e.g. 14-bar RSI, 48-bar window). When the current close is at or above that high, it outputs the negative of (RSI at the previous high minus current RSI), floored at 0 in the shortfall, and scales it by how far the close sits above the old high. It is 0 with no new high and grows more negative as the RSI shortfall widens. | measures: situation
- Component: RsiAtPriorPriceHigh: from closes, the RSI value on the bar of the highest close in the last N bars excluding the current bar. It is a level from 0 to 100 that a weighted mean could subtract from current RSI. | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiBullishDivergence: from closes, finds the previous price low (lowest close in a past window, e.g. 48 bars, excluding the last few bars). When the current close is at or below that low, it outputs RSI(14) now minus RSI at that low, scaled by how far price undercut it; otherwise it outputs 0. The value grows with the RSI gap and the depth of the new low, and is graded. | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RSIRangePositionComponent: from closes, compute Wilder RSI(14), then output (2 x (RSI - min RSI over the last N bars) / (max - min) - 1) x sf; it rises continuously to +sf when the current RSI is at its N-bar high and falls to -sf at its N-bar low. Paired with `DonchianBreakoutComponent` on price at the same N, the difference (price position minus RSI position) grows with the divergence | measures: situation

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RsiRangePosition: (2 x pos - 1) x sf, where pos = (RSI - lowest RSI) / (highest RSI - lowest RSI) over the last `period` bars of a Wilder RSI(14) computed from closes. It is -sf when RSI is at its lowest in the window and grows continuously toward +sf as RSI rises above its earlier low. Paired with Donchian price position, RSI position minus price position grows with the size of the divergence. | measures: situation

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RsiPriceDivergence: from closes, the close's position in its N-bar range minus RSI(14)'s position in its own N-bar range (each 0 to 1); grows as price nears its high while RSI stays further below its own high | measures: comparison

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiLowDivergence: from closes, computes the Wilder RSI, finds the prior swing low of the close within a lookback window, and on bars where the close is at or below that prior low outputs (RSI now - RSI at the prior low) x (percent undercut of the prior low), else 0; grows with both the RSI rise and the depth of the new low | measures: comparison
