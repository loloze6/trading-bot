# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-giveback_1d
- Component: RsiDivergenceComponent: from closes, RSI(14) on the bar of the previous highest close in the prior 30 bars minus RSI(14) on the current bar; it is 0 when the current close is not a 30-bar high or RSI is not lower, and grows as the current RSI falls further below the earlier peak's reading | measures: comparison

## 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation_1d
- Component: RankWeightedScaledMoveComponent: (close[t]/close[t-1] − 1) / mean(abs one-bar returns over the last 60 bars) × (1 − share of the last 100 values of the 20-bar return standard deviation that are <= today's), from closes. Signed like the day's move; its size grows with the move against the 60-day mean absolute move and as the 20-day volatility rank falls, and it tends to 0 when volatility ranks high. | measures: situation
