# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiPriceDivergence: over the last N closes, (price's position in its N-bar range) minus (RSI(14)'s position in its own N-bar range), computed from closes and signed negative for a bearish divergence. It grows as price sits nearer its high while RSI sits further below its earlier high, with the mirror case at lows | measures: situation
- Component: RsiAtPriorPeak: from the closes, the RSI(14) value on the bar of the previous swing high (and swing low) within the last N bars, so the current RSI can be compared with it | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: SwingLowDetector: from closes over a lookback (e.g. 48 bars), finds the previous swing low and outputs how far the current close is below it, in percent; 0 when the close is not below it, and it grows as the new low is made deeper | measures: situation
- Component: RsiBullishDivergence: from closes, computes RSI(14) on the current bar and at the previous swing low of the close; when the current close is below that low, it outputs current RSI minus RSI at the previous low (0 otherwise); the value grows as the RSI higher low widens | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: rsi_divergence: on each bar, from closes, takes the RSI(14) value minus the highest RSI of the prior N bars, multiplied by the close's position in its N-bar close range (pos from 0 to 1, as in Donchian). It is graded and signed: most negative when price is at its N-bar high and RSI is far below its prior high (divergence), positive when RSI also makes a new high (confirmation), and near 0 away from price highs. | measures: situation

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RSIRangePosition: (2 x pos - 1) x sf, where pos = (RSI - lowest RSI) / (highest RSI - lowest RSI) over the last `period` bars, RSI being Wilder RSI(14) of the closes. It is -sf when RSI is at a new low and rises continuously as RSI sits further above its prior low. | measures: comparison
- Component: RsiPriceLowDivergence: graded bullish-divergence score, max(0, -price_pos) x max(0, rsi_pos - price_pos), with price_pos the close's position in its `period`-bar close range (-1 to +1) and rsi_pos the same for RSI(14). It is zero away from new lows and grows as price sits at its range low while RSI stays above its own low. | measures: situation

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RsiRangePositionComponent: where the current RSI (Wilder, period 14, from closes) sits within the range of its own last N values, -1 at the lowest and +1 at the highest; it falls as RSI drops below its recent peak | measures: situation
- Component: PriceRsiDivergenceComponent: the close's N-bar range position (as in Donchian) minus RSI(14)'s N-bar range position, both from closes; it is positive and grows when price is at the top of its range while RSI is below the top of its own | measures: situation

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiRangePosition: where the current RSI(14) sits between its lowest and highest value over the last N closes, scaled -sf at the RSI low to +sf at the RSI high; it rises as RSI moves further above its prior low | measures: situation
- Component: PriceRsiDivergence: RSI range position minus the close's range position over the same N closes (from closes); near 0 when the two move together, and growing positive when the close is near its N-bar low while RSI stays well above its own N-bar low | measures: comparison
