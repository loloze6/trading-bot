---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days
line: 7.d not profitable
backtest: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour range is several times its 30-day average, the smaller its 24-hour fall relative to that range, the higher its return over the next 1 day.
Consequence: A trader should favour wide-range days that closed only moderately lower, where forced selling has been absorbed, over the deepest crashes.
Why:
- F5: For a given range excess, the premium is largest when the 24-hour fall is small relative to the range, not when it is deepest:
- F1: The idea's premium is paid within the first day and is gone by a week: after a broad panic (24-hour fall of at least 1 usual move while the 24-hour mean bar range is at least 1.5 times its 30-day mean), the mean excess return is +1.18 % over 1 day (t 7.21, 1798 cases, strength 0.233), +1.41 % over 3 days (t 4.63, 1206 cases, strength 0.155), +0.27 % over 7 days (t 0.52, 879 cases, strength 0.003) and +0.31 % over 14 days (t 0.37, 645 cases).
- F3: The book is far too small and too rare to reach the required mean daily return (6.9e-05 against 5e-04). Panics as the plan defines them occur on only 60 to 102 bars per coin in about 17500. When in, the allocation averages only 0.15 to 0.29, because the vol-target sizing (target 0.38) meets realised vols of 0.59 to 1.07 during panics. Per-window book returns are mostly within ±3 % while the coins moved -50 % to +268 %.
