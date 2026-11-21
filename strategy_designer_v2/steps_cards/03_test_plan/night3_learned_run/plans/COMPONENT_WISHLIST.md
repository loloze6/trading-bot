# Component wish list

One block per idea that needs components the catalogue does not have.

## 022-04_signal-weights-carry-forward_1d
- Component: PastPredictivePowerWeightedSignal: from closes, computes a chosen signal s (momentum over weeks, short reversal after large days, nearness to the high, or volatility level) at bar t, multiplied by the correlation, over bars i from t-365 to t-5, of s(i) with close[i+5]/close[i]-1; it is signed and grows with both the signal and its past predictive power | measures: situation
- Component: TrailingPredictivePower: from closes, the same trailing 365-bar correlation of a chosen signal with its later 5-day return, alone; signed, -1 to +1, larger as the signal predicted better | measures: comparison
