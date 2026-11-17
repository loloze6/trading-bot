# Component wish list

One block per idea that needs components the catalogue does not have.

## 005-01_bearish-rsi-divergence-giveback_1d
- Component: RsiDivergenceComponent: from closes, RSI(14) on the bar of the previous highest close in the prior 30 bars minus RSI(14) on the current bar; it is 0 when the current close is not a 30-bar high or RSI is not lower, and grows as the current RSI falls further below the earlier peak's reading | measures: comparison

## 005-02_bullish-rsi-divergence-rebound_1d
- Component: RsiLowDivergence: at the current close, finds the lowest close in the prior 30 closes (excluding the last few bars), then outputs current RSI(14) minus RSI(14) at that earlier low, from closes only; it is signed, and grows as the current RSI sits further above the earlier trough while price is at or below that low | measures: comparison
