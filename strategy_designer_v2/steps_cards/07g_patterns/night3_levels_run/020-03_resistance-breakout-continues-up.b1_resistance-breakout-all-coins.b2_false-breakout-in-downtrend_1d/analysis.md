---
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend_1d
idea tested: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4836 USD
---
## Findings
- **F1:** The coin's 30-day return predicts the next 10 days in its own direction, except at the extreme low end. Per coin, by 30-day return quintile, the drift-adjusted next-10-day move on non-overlapping grid bars is −0.96 % (t −0.87, n 530), −2.13 % (t −3.87, n 524), −1.35 % (t −1.93, n 522), +0.61 % (t 1.10, n 524) and +3.18 % (t 3.19, n 528). By decile, the lowest one is flat (+0.05 %, t 0.53, n 268), and deciles 1 to 3 fall by about 2 % each (t −1.9 to −2.8).
- **F2:** Scaling the 30-day return by the coin's 30-day volatility sharpens the top end. Its highest quintile is followed by +3.53 % drift-adjusted over 10 days (strength 0.19, t 3.66, n 528). That is about 16 times the 0.22 % cost of a round trip.
- **F3:** The rise after the strongest 30-day returns holds across coins but not in bear years. In the top two deciles, 16 of 19 coins have a positive mean. By year it is positive in 2020 (+3.1 %, t 1.8), 2021 (+11.2 %, t 2.9), 2023 (+3.6 %, t 2.1) and 2024 (+3.6 %, t 2.3). It is negative in 2018 (−17.7 %, n 7) and 2022 (−4.9 %, t −2.0).
- **F4:** Closeness to the 30-day high gives the same pattern as the 30-day return. Its top quintile is followed by +2.95 % drift-adjusted over 10 days (t 3.21, n 528), and its second-lowest by −2.42 % (t −3.33). This matches the earlier nearness-to-highs result.
- **F5:** The resistance break adds nothing inside a falling month, so the tested idea's edge comes from the regime, not from the break. On grid bars with a negative 30-day return, the next 10 days are −1.32 % with a fresh break (n 166) and −1.38 % without one (n 1147). Across break cases, the quartiles of the break's strength show no grading (−1.86, −0.28, −2.42, −2.26 %).
- **F6:** The book loses because it shorts a coin whose own drift is up, which costs more than the timing earns. All 2229 trades are shorts, with a mean net of −3.49 % and 34 % winners. The book earns only in the years the coins fell: 2018 +7.1 bps a day against coins at −34.9, 2022 +5.2 against −24.7, and 2025 +5.8 against −2.6. It loses in rising years, for example 2023 −15.0 bps a day against coins at +31.7.

## Ideas
- `020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.g1_volatility-scaled-monthly-momentum-continues` (from F1, F2, F3): The more a coin has risen over the past 30 days relative to its own 30-day volatility, the more it rises over the next 10 days.
- `020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.g2_closes-near-monthly-high-continue` (from F4, F1, F3): The closer a coin's close is to its highest close of the past 30 days, the larger its rise over the next 10 days.
- `020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.g3_moderate-monthly-decline-continues` (from F1, F5, F6): The more a coin has fallen over the past 30 days, up to a moderate decline measured against its volatility, the more it falls over the next 10 days, whether or not it has just crossed a past turning price.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
