# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiPeakDivergence: from closes, on a bar whose close is the highest close of the last `period` bars, outputs RSI(14) at the previous swing high (the earlier local maximum of the close within the window) minus the current RSI(14). It is positive when RSI makes a lower high and grows with the size of that gap. A mirrored negative value covers new lows with a higher RSI low. It is 0 when there is no new extreme, or when RSI confirms the new extreme. | measures: situation
- Component: RsiAtPriorPeak: from closes, the RSI(14) value recorded at the most recent swing high of the close before the current bar, carried forward. It lets a config compare the current RSI with the RSI at the prior peak, and its value is that earlier RSI reading. | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiBullishDivergence: from closes, computes Wilder RSI(`period`, 14). On each bar where the close is at or below the lowest close of the prior `lookback` bars (a new low, excluding the last `gap` bars, e.g. lookback 30, gap 5), it finds the bar of that previous lowest close and outputs max(0, RSI now − RSI at that previous-low bar) × (depth of the new low below the previous low, in percent, floored at a small positive value so a close exactly at the prior low still reads). It outputs 0 when there is no new low or RSI is not higher. The value grows with the RSI gap and the depth of the new low (one-sided, long; a mirrored output, negative for bearish divergence at new highs, optional) | measures: situation
- Component: RsiAtPriorPriceLow: from closes, the Wilder RSI(`period`) value on the bar of the lowest close within the prior `lookback` bars (excluding the last `gap` bars). It is continuous and rises as momentum at that earlier low was stronger. It would let "RSI now minus RSI at the prior low" be built with a negative weight next to an RSI-level component | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RSIRangePositionComponent: from closes, the Wilder RSI(`period`, 14) on each bar, then (2 x pos - 1) x sf, where pos = (RSI_now - min RSI over the last `lookback` bars) / (max RSI - min RSI over those bars), current bar included. It is continuous from -sf (RSI at its lowest of the window) to +sf (RSI at its highest). Subtracted from `DonchianBreakoutComponent` over the same lookback, it gives a graded divergence: largest when price is at its range top while RSI sits well below its own top. | measures: comparison

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RsiRangePositionComponent: from closes, compute Wilder RSI(`rsi_period`, 14), then output (2 x (RSI - min RSI over the last `period` bars) / (max RSI - min RSI over the same bars) - 1) x sf, 0 when max = min. It is continuous, -sf when RSI is at its window low and grows toward +sf as RSI rises further above that low, so at a new price low a higher value means a stronger bullish divergence. | measures: situation

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: RsiBelowPeak: max(RSI(14) over the last N bars, e.g. N = 20, including the current bar) minus the current RSI(14), with Wilder RSI computed from closes. It is 0 when the current RSI is its own window high (no divergence) and grows, never negative, as the current RSI sits further below its earlier peak (a larger lower-high divergence when the close is at a new high). | measures: comparison

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RsiBullishDivergenceComponent: from closes over a `lookback` of N bars (convention 14-bar Wilder RSI, N = 20), it computes the close's position in its N-bar close range, p = (close - min) / (max - min), and RSI's position in its own N-bar range, r = (RSI - min RSI) / (max RSI - min RSI). It outputs max(0, r - p) x (1 - p): 0 when price is not near its range low or RSI is no higher than price within its range, and a continuum up to 1 when the close sits at its N-bar low while RSI sits well above its own N-bar low. The value grows as the price low gets deeper and the RSI low gets relatively higher (one-sided; standardise, then negate for the continuation-short reading). | measures: situation
