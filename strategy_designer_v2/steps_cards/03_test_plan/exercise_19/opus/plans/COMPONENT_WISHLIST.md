# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiAtPriorHighGap: over the last N closes, find the highest close before the current bar and output RSI(14) at that bar minus the current RSI; it grows as current RSI falls further below RSI at the prior high. Weighted with the Donchian position, it would form the graded bearish divergence. | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: PriceNewLowDepth: from closes, the percent by which the current close is below the lowest close of the prior swing low within a lookback (for example 20 bars, swing found by a local-minimum rule); 0 when the close is not below it, and it grows as the new low goes deeper | measures: situation
- Component: RsiDivergenceAtLow: from closes, Wilder RSI(14) on the current bar minus RSI(14) on the bar of the prior swing low in price, output only while the current close is below that prior low; positive and growing as RSI sits higher above its earlier low (bullish divergence strength), 0 or negative otherwise | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RSIRangePositionComponent: (2 x (RSI - min RSI) / (max RSI - min RSI) - 1) x sf over the last `period` bars, from Wilder RSI(14) of the closes; it grows toward +sf as RSI nears a new high of its own, so a low value at a price high marks a divergence | measures: comparison
- Component: PriceRsiDivergenceComponent: the Donchian price position (closes, `period`) minus the RSI range position above, signed and graded; it grows as price sits higher in its range than RSI does in its own (a bearish divergence), and goes negative for the mirror case at lows | measures: comparison

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RsiPriceLowDivergence: over the last N closes (e.g. N = 20 on 1d), compare price's low with RSI's low. Price's distance from its N-bar low is (close - min close) / (max - min). RSI's distance from its N-bar low is the same formula on RSI(14) from closes. The output is (RSI position - price position) x sf, scaled up by how near price is to its low. It is graded and signed: larger and positive when price is at a new low while RSI sits well above its own low (bullish divergence), near 0 when RSI confirms the low, negative when RSI is weaker than price. | measures: situation
- Component: RsiConfirmedLowFlag-free contrast (same component, sign read): the negative-to-zero side of RsiPriceLowDivergence at new price lows supplies the "RSI also makes a new low" group, so that group's forward returns can be compared with those after positive readings. | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RsiDivergenceComponent: over the last N closes (default 14), the close's position in its range (0 to 1) minus Wilder RSI(14)'s position in its own range over the same N bars. Both come from closes only. The value grows from 0 toward +1 as price sits at its high while RSI sits further below its own recent peak, and is negative for the bearish mirror case. | measures: situation
- Component: RsiRangePositionComponent: where the latest Wilder RSI(14) sits between its lowest and highest value over the last N bars, scaled to -1 to +1, from closes. It falls as RSI moves away from its recent peak, so it can be combined with `DonchianBreakoutComponent` using a negative weight. | measures: comparison

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiRangePositionComponent: where the current Wilder RSI(14) of the closes sits between its lowest and highest value over the last N bars, mapped to -sf at the low and +sf at the high. It grows as RSI rises above its recent low. With a negative weight on `DonchianBreakoutComponent` over the same N, it gives a graded divergence spread (RSI position minus price position) | measures: comparison
- Component: RsiPriceDivergenceComponent: over the last N closes, the price's range position (low = -1) times how far the current RSI(14) sits above its window minimum, in RSI points. It is signed negative when price is at its range low and RSI is above its earlier low, and grows with both the price extreme and the RSI gap | measures: situation
