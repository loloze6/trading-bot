# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiBearishDivergence: from closes, finds the latest price high (the close at its N-bar maximum) and the prior swing high within a lookback, computes Wilder RSI at both, and outputs the signed RSI shortfall (RSI at the prior high minus RSI now, in RSI points). It is positive and grows as momentum fades more behind a higher price high, and is 0 when the close is not at a new high above the prior swing high; a mirrored bullish form covers new lows | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiBullishDivergence: over a lookback of N closes, finds the previous swing low of the close and reads the RSI(14) value on that bar. When the current close is below that previous low, it outputs (RSI now − RSI at the previous low) times the percent the close undercut the previous low. The value grows as the RSI gap and the new low both widen. The output is 0 when price makes no new low, and negative when RSI also makes a lower low. | measures: comparison
- Component: RsiRangePosition: where the current RSI(14) sits inside its own min-max range over the last N bars, scaled to −1..+1 like the Donchian position. It is computed from closes and grows as RSI rises above its recent low. Combined with a negated Donchian position, it would give a graded "price at its low, RSI above its low" reading. | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RsiDivergence: (RSI(14) on the current bar) minus (highest RSI(14) over the prior N bars, e.g. 20), computed from closes; signed: negative and growing in size as a new price high comes on weaker momentum (a bearish divergence), positive when RSI confirms with a new high | measures: situation

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RSIRangePosition: computes RSI(period) from closes, then (2 x pos - 1) x sf, where pos = (RSI - lowest RSI) / (highest RSI - lowest RSI) over the last N bars including the current one; it rises from -sf when RSI is at its N-bar low to +sf when RSI is at its N-bar high. Combined with weight against the negated DonchianBreakoutComponent on closes, it grows with how far above its own low RSI stays while price sits at its low. | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RSIPeakDeficit: from closes, RSI(14) minus the highest RSI(14) over the previous `period` bars (e.g. 14), excluding the current bar; never positive, and it grows more negative the further the current RSI sits below its recent peak, so a lower RSI high gives a larger deficit | measures: comparison
- Component: PriceRSIDivergence: from closes, the product of the close's range position (0 to 1, as in Donchian over `period` bars) and the RSI peak deficit above, sign flipped; graded, near 0 unless price is at the top of its range and RSI is below its recent peak, and it grows with both (a mirrored version for new lows) | measures: situation

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RSIRangePosition: (2 x (RSI - lowest RSI) / (highest RSI - lowest RSI) - 1) x sf over the last `period` bars, using Wilder RSI(14) from closes. It runs from -sf when RSI is at its window low to +sf at its window high, so it rises the further RSI sits above its earlier lows. | measures: comparison
