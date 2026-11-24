# Component wish list

One block per idea that needs components the catalogue does not have.

## 031-03.g1.b1.d2.e2.g1.g2_fade-during-volatility-bursts_1d
- Component: VolatilityRatioWeightedScaledReturn: (close[t]/close[t-1] − 1) / s30 x s5 / s30, where s5 and s30 are the std (ddof 1) of the last 5 and 30 one-bar close returns ending at bar t. It is signed like the day's move, and its size grows with the move in usual 30-day moves and with the 5-day volatility against the 30-day one. | measures: situation
