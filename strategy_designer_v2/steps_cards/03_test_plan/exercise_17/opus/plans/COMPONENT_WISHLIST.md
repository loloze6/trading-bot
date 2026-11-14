# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RSIBearishDivergence: from closes, finds the highest close of the earlier part of a lookback (e.g. 48 bars) and its Wilder RSI (14). When the current close is at or above that earlier high, it outputs the earlier RSI minus the current RSI (0 otherwise, negative values clipped to 0). It grows the further RSI's peak has fallen behind the new price high, and is meant to be negated into a graded short forecast. | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiPriceDivergence: from closes, finds the lowest close in the last N bars before the current low and the RSI(14) at that bar; when the current close is at or below that low, outputs RSI now minus RSI at the prior low (positive when RSI makes a higher low), 0 otherwise; grows with the RSI gap and with how far price undercuts the prior low | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RSIRangePositionComponent: where the current Wilder RSI(14), from closes, sits within its own min and max over the last `period` bars (default 20), (2 x pos - 1) x sf, continuous from -sf at its range low to +sf at its range high; read beside DonchianBreakoutComponent(20) as price position minus RSI position, which grows as the price high outruns the RSI high | measures: comparison

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RsiPriceDivergence: computes over the last `period` bars, from closes only, price position minus RSI position. Price position is (close - lowest close) / (highest - lowest). RSI position is the same with Wilder RSI(14) and its lowest and highest values in that window. Each is mapped to -1..+1, then multiplied by -sf. It is positive and grows when price sits at its range low while RSI sits well above its own low (bullish divergence). It is near 0 when both make new lows together, and negative in the mirror case at highs | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RsiRangePosition: where the current RSI(14) sits inside its own min and max over the last `period` bars, computed from closes, from -1 at the window's lowest RSI to +1 at its highest, growing as RSI nears its recent peak | measures: comparison
- Component: PriceRsiDivergence: the close's position in its `period`-bar close range minus RSI(14)'s position in its own `period`-bar range, computed from closes, signed, and growing as price nears its high while RSI stays further below its prior high | measures: situation

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiLowDivergence: from closes, compute Wilder RSI(14) and the close's position in its N-bar range. When the close is at or near its N-bar lowest close, output (RSI now − lowest RSI over the prior N bars), else 0. The value grows as RSI's low rises further above its earlier low, signed positive for a bullish divergence | measures: situation
- Component: RsiRangePosition: from closes, give where the current Wilder RSI sits within its own min–max over the last N bars, from −1 at its low to +1 at its high, continuous on every bar | measures: comparison
