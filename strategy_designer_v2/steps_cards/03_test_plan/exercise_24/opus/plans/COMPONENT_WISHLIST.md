# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-reversal_1d
- Component: RsiBearishDivergence: on bars where the close is the highest close of the last N bars, RSI at the previous price swing high minus the current RSI (from closes); 0 elsewhere; it grows as the current RSI peak falls further below the prior one | measures: situation

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiDivergenceComponent: from closes over a lookback (e.g. 48 bars), finds the previous swing-low close and the RSI(14) at that bar. When the current close is below that prior low, it outputs (current RSI minus RSI at the prior low), positive for a bullish divergence. The value grows with the RSI gap and is 0 when no new low is made. | measures: comparison

## 005-03_divergent-high-weaker-than-confirmed_1d
- Component: RsiRangePosition: the position of the current 14-bar Wilder RSI, from closes, inside the range of its last N values (current included), (2 x pos - 1) x sf, so -sf at the lowest RSI of the window and +sf at its highest | measures: situation
- Component: RsiPriceDivergence: the close's position in its N-bar range of closes minus RSI's position in its own N-bar range, both on 0 to 1, computed from closes; it grows toward +1 when price is at a new high while RSI sits below its high, and toward -1 for the mirror case at lows | measures: comparison

## 005-04_divergent-low-stronger-than-confirmed_1d
- Component: RSI range position: (RSI_t - min RSI over the last N bars) / (max RSI - min RSI over the last N bars), with a Wilder RSI of the closes. It is 0 when RSI is at its own N-bar low and rises toward 1 as RSI sits further above that low. Combined with the price range position, it separates new price lows with a higher RSI low from new price lows with a confirming RSI low. | measures: comparison

## 005-05_bearish-divergence-uptrend-continues_1d
- Component: rsi_bearish_divergence: from closes, computes the price range position over N bars (0 at the low, 1 at the N-bar closing high) times the shortfall of the current RSI below the highest RSI of the previous N bars (0 if RSI is at a new high). It grows as price nears a new high while RSI falls further below its earlier peak, and is near 0 otherwise | measures: comparison

## 005-06_bullish-divergence-downtrend-continues_1d
- Component: RSIRangePosition: computes Wilder RSI(14) from closes, then where the current RSI sits within the min–max of its last N RSI values (-1 at its low, +1 at its high), which grows as RSI holds further above its recent low | measures: situation
