# Component wish list

One block per idea that needs components the catalogue does not have.

## 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d1_nearness-reversal-in-uptrends_1d
- Component: TrendScaledExcessPowerReversal: max(0, −(w(t) − wbar(t)) × z(t)) × max(0, (close[t] − SMA100) / SMA100 × 100), from closes only. Here w is the 365-day correlation of nearness to the 90-day high with 5-day returns, wbar is its 365-day mean, and z is today's nearness z-score over 365 days. The value is 0 unless the reading implies a fall and the price is above its 100-day mean; otherwise it grows with both factors. | measures: situation
- Component: TrendScaledExcessPowerReversal (the 100-day-mean factor, inside the same product): it supplies the scaling of the rise by the uptrend, the (close − SMA100) / SMA100 term above | measures: outcome
