# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RSIDivergence: on each bar, from closes, compute RSI(14). Find the previous swing-high close in a lookback (e.g. 48 bars), excluding the current run. Output -(RSI at that prior high minus current RSI) times how far the close is at or above that prior high (0 when below it). It is more negative when price is further above the old high while RSI falls further short of the RSI at that high, so the short grows with the divergence. The mirror case (new low with a higher RSI) gives a positive value. | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: SwingLowFinder: from closes (or lows) over a lookback such as 60 bars, finds the latest swing low and the one before it. It outputs how far the new low sits below the prior one, as a percent: 0 when there is no lower low, larger the deeper the new low | measures: situation
- Component: RsiBullishDivergence: from closes, takes the Wilder RSI(14) at the latest and prior swing lows found by SwingLowFinder. When price made a lower low, it outputs RSI at the new low minus RSI at the prior low, floored at 0. The value grows with how much higher RSI's low is, and is 0 without a lower low or a higher RSI low | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RsiRangePositionComponent: where the current RSI(14), computed from closes, sits between its lowest and highest value over the last `period` bars, mapped to -sf..+sf; it grows toward +sf as RSI nears its recent peak | measures: situation
- Component: PriceRsiDivergenceComponent: price range position (closes, `period` bars) minus RSI range position over the same window, signed and continuous; it grows as price sits nearer its high while RSI sits further below its own high, negated for the bearish reading (and mirrored at lows) | measures: comparison

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RSIRangePosition: where the current RSI (Wilder, period 14, from closes) sits within its own lowest-to-highest range over the last N bars, scaled from -1 at a new RSI low to +1 at a new RSI high; the value rises as RSI holds further above its prior low while price is at a new low | measures: situation
- Component: RSIChangeOverPeriod: RSI now minus RSI N bars ago (from closes), signed; it grows as RSI rises over a stretch in which price fell to a new low, so it grades the divergence's strength | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RSIRangePosition: the RSI (Wilder, from closes) placed in its own range over the last N bars, as (2 x (RSI - min RSI) / (max RSI - min RSI) - 1) x sf; it is +sf when RSI is at its N-bar high and falls as RSI sits further below its prior peak | measures: situation
- Component: PriceRsiDivergence: the close's range position over N bars minus the RSI's range position over N bars, from closes; it is largest when the close is at its N-bar high while RSI is well below its own N-bar high, and grows with that gap | measures: situation

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RSIRangeDivergence: from closes over `period` bars (e.g. 14-bar RSI, 48-bar window), computes RSI's position in its own window range minus the close's position in its range (each 0 to 1, as Donchian does for price). It grows positive as the close nears its window low while RSI stays above its window low (bullish divergence), and negative for the mirror case at highs; signed and graded | measures: situation
- Component: RSIRollingMin: from closes, the lowest RSI(`period`) value over the last `window` bars, so the current RSI can be set against its prior trough; its gap from current RSI grows with the strength of the RSI higher low | measures: comparison
