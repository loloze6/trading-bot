# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_trend-conditioned-one-day-reversal_1d
- Component: VolScaledMoveTimesTrend: from closes, (close[t]/close[t-1]-1) / std(last 20 one-bar returns) x (close[t]/close[t-50]-1) x 100. It is signed and grows in size with both the day's move in usual moves and the 50-day return. | measures: situation

## 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_extended-fall-daily-rebound_1h
- Component: StackedFallProductComponent: from closes, max(0, -(close[t]/close[t-24] - 1)) x 100 x max(0, -(close[t-24]/close[t-72] - 1)) x 100; 0 unless both windows fell, and it grows with the depth of each fall | measures: comparison
