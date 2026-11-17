---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3962 USD
---
## Findings
- **F1:** The tested relation is real and stands out. In rising months (30-day return above 0), the slope of the demeaned next-7-day return on the 7-day return is 0.142 with t 4.35 over 893 grid cases. The top r7 quintile earns +3.5% over the coin's average (t 3.21, n 252) and the bottom quintile earns −0.9%. In falling months the slope turns negative (−0.057, t −1.49, n 830).
- **F2:** Nearness to the 30-day high carries no information beyond the 7-day return. In rising months, with r7 and the distance to the 30-day high in one regression, r7 keeps t 3.91 and the distance to the high falls to t 0.11 (n 893). The anchoring-to-the-high reading adds nothing over plain one-week momentum.
- **F3:** In falling months the 30-day return reverses. The slope of the demeaned next-7-day return on r30 is −0.074 (t −2.35, n 830), so a deeper monthly fall is followed by a higher next week. The slope is negative in 5 of 6 coins (BTC t −2.85, n 126). It is stronger in 2018–2021 (t −2.35, n 425) than in 2022–2025 (t −0.88, n 405).
- **F4:** A one-day fall large relative to the coin's 20-day daily volatility is followed by a higher next-day return. The pooled slope of the demeaned next-day return on the volatility-scaled down move is −0.0031 (t −3.61, n 7151). The slope is negative in all 6 coins (XMR t −3.21, XRP t −2.08). Day-averaged across coins, falls of 1 to 2 volatilities are followed by +0.63% (t 1.82) in 2018–2021 and +0.12% (t 0.53) in 2022–2025, so the effect has weakened lately.
- **F5:** A 3-day rise continues and a 3-day fall does not reverse. On the non-overlapping 3-day grid, the slope of the demeaned next-3-day return on the volatility-scaled 3-day rise is 0.0070 (t 2.89, n 2356). For 3-day falls it is −0.0013 (t −0.46, n 2359).
- **F6:** The rising-month momentum holds at every volatility level. The r7 slope is t 2.48 in the low tercile, t 1.43 in the middle and t 3.18 in the high tercile (about 297 cases each). Scaling r7 by volatility gives t 3.61, so the effect is not a volatility artefact.
- **F7:** Weekday effects do not stand out once coins are averaged per day. The best day is Friday, at +0.32% with t 2.17 across 414 days, out of 7 weekdays tested. Its t is 1.70 in 2018–2021 and 1.37 in 2022–2025. I count this as chance.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum.g1_falling-month-depth-rebound` (from F3, F1): While a coin's 30-day return is negative, the deeper its 30-day fall, the higher its return over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum.g2_volatility-scaled-down-day-bounce` (from F4): The larger a coin's one-day fall relative to its own 20-day daily volatility, the higher its return over the next day.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum.g3_short-horizon-rise-continuation` (from F5, F6): The larger a coin's 3-day rise relative to its own 20-day daily volatility, the higher its return over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
