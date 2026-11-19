---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1h
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3914 USD
---
## Findings
- **F1:** The coins' average next-hour return is clearly positive in two hours of the day, 20:00 UTC (+4.8 bp, t 2.93, n 2917 timestamps after averaging the coins at each hour) and 21:00 UTC (+3.7 bp, t 2.44, n 2920), and the 20–21 UTC pair is positive in all 6 coins (+3.7 to +4.8 bp) and in 7 of 8 years (only 2022 is negative, at −2.7 bp); with 24 hours tested this would be borderline on its own, but it holds in every coin and in nearly every year.
- **F2:** The 20–21 UTC drift grows with the coin's 14-day volatility: +2.1 bp (t 2.69) in the calmest quintile against +11.2 bp (t 5.51) in the most volatile quintile, n ≈ 6560 per quintile pooled across coins, so these t's are overstated by the coins moving together.
- **F3:** The 20–21 UTC drift is largest after a 1-day fall: +11.2 bp (t 6.27) when the coin's prior 24-hour return is in its lowest quintile, falling to +3.8, +1.8 and +0.2 bp through the next three quintiles, with a smaller rebound to +5.1 bp in the top quintile (n ≈ 6560 each, pooled).
- **F4:** The hours 00–02 UTC are weak: next-hour return of −1.8, −2.4 and −3.4 bp (hour 02 t −2.45 after averaging the coins), negative in all 6 coins (−0.4 to −5.0 bp), but positive in 2024 and 2025, so the effect is fading.
- **F5:** Within the trending regime, the tested 14-day-rise effect sits almost entirely in the top quintile, +3.45 % demeaned 7-day return (t 2.55, n 217), while quintiles 1–4 are all at or below zero (−1.7 % to −0.05 %); in the non-trending regime the top 14-day-rise quintile is also positive, +1.46 % (t 1.95, n 212).
- **F6:** The book earns far less than holding in strong up years (2020: 16 bp a day against 42 bp; 2021: 7 against 41) and loses less in down years (2018: −4.7 against −34.9 bp; 2022: −4 against −18.6 bp), which fits a long-only book that is in the market only part of the time.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends.g1_late-us-session-volatility-drift` (from F1, F2): A coin's return over the two hours from 20:00 to 22:00 UTC is positive, and larger the higher its 14-day volatility.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends.g2_evening-rebound-after-daily-fall` (from F1, F3): The more a coin fell over its last 1 day, the higher its return over the two hours from 20:00 to 22:00 UTC.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
