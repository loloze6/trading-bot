# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiPriceDivergence: on each bar, finds the previous swing high of the closes within N bars (14-bar RSI by default). It outputs (RSI at that prior high minus current RSI) times the close's position in its N-bar range (0 to 1). It is graded and grows as price nears or exceeds the prior high while RSI falls further below its earlier peak, mirrored for lows, from closes only | measures: comparison
- Component: RsiRangePosition: where the current RSI sits inside its own range over the last N bars, from closes. It runs from -1 at the RSI's N-bar low to +1 at its high, so subtracting it from `DonchianBreakoutComponent` gives a graded price-minus-RSI divergence | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiLowDivergence: finds the last two swing lows of the close, then outputs (RSI at the latest low minus RSI at the prior low) when the latest close low is below the prior one, else 0, all from closes; it grows with the RSI improvement and with how recent the new low is | measures: comparison
- Component: SwingLowDepth: the percent by which the latest swing-low close sits below the prior swing-low close, from closes; it grows with how far the new low undercuts the old one | measures: situation

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RsiRangePosition: RSI(14) from closes, placed in its min-max range over the last N bars (default 48), -1 at the lowest RSI of the window, +1 at the highest; it rises as RSI nears its recent high, so price range position minus this value grows with the divergence | measures: situation

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RsiRangePositionComponent: from closes, computes Wilder RSI(14) over the bar window, then (2 x pos - 1) x sf, where pos = (RSI - min RSI) / (max RSI - min RSI) over the last `period` bars; it is -sf when RSI makes a new low and rises continuously as RSI sits higher above its range low (a higher RSI low) | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RsiHighDivergence: over the last N closes (e.g. 14-bar Wilder RSI, N 48), it outputs pos_price x (max RSI over the window - current RSI), where pos_price is the close's place in its N-bar close range (0 to 1). It grows as price nears its high while RSI falls further below its own high, and is 0 when RSI is at its high or price is at its low | measures: situation
- Component: RsiDistanceFromHigh: (rolling N-bar max of RSI(14) - current RSI), from closes, never negative; it grows as RSI falls further below its recent peak | measures: comparison

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiRangePositionComponent: Wilder RSI(14) from closes, then (2 × (RSI − min RSI over the last N bars) / (max − min) − 1) × sf over the same N as the price Donchian window. It rises from −sf when RSI is at its own N-bar low to +sf at its high, so with price at its N-bar low a higher value means a stronger bullish divergence | measures: situation
- Component: RsiPriceDivergenceComponent: from closes, (RSI range position − price range position) / 2 over the same N bars, both on −1..+1 and scaled by sf. It is graded and signed: positive when price sits lower in its range than RSI does (bullish divergence), negative for a bearish one, near zero when they agree | measures: situation
