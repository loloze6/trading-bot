---
line: 7.g patterns
backtest: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h
idea tested: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4025 USD
---
## Findings
- **F1:** Across all bars, not only panics, the coin's excess 3-day return rises steadily with the 24-hour mean bar range over its 30-day mean. It goes from −0.78 % (t −3.5, n 1389) when the ratio is at most 0.7, to −0.12 % for 0.7–1, +1.06 % for 1.5–2 (t 2.2, n 446) and +3.31 % for 2–3 (t 3.7, n 168). Regressing the 3-day excess on the log of the ratio gives a slope of 0.0148 (t 5.7, n 5436) while the scaled 24-hour return adds nothing (t −0.49).
- **F2:** The range gradient holds in every coin (slopes 0.005 to 0.026, t 0.8 to 3.7, strongest in XRP at t 3.7 and ZEC at t 3.3) and in both halves of the windows (early t 3.1, late t 4.8). It also shows over 1 day (+1.26 % above 3×, t 2.0) and over 7 days (+3.3 % for 1.5–2, t 2.2).
- **F3:** Among wide-range stretches (ratio at least 1.5), those with a 24-hour fall are followed by +2.72 % excess over 3 days (t 4.9, n 264), against +0.87 % (t 1.2, n 245) after a rise and +0.97 % (t 1.1, n 160) after a flat stretch.
- **F4:** The plan's panic level of at least 3× is past the sweet spot. For falls of at least 2 usual moves, the excess 3-day return is +1.68 % for ratio 1.5–2 (t 1.8, n 103), +4.31 % for 2–3 (t 3.5, n 38) and only +1.20 % above 3 (t 1.1, n 36), which fits the failed supporting check (−2.77 %).
- **F5:** Without any range condition, 24-hour falls of at least 2 usual moves are followed by +0.97 % excess over the next day (t 5.3, n 1038) and +1.31 % over 3 days (t 2.9, n 340). Mild moves between −1 and +1 are followed by −0.49 % and −0.58 % (t −2.2 and −3.2).
- **F6:** The book is almost never in the market, so its small earnings come from exposure, not from the move. It holds a position on 15.6 % of bars at a mean allocation of 0.14 and is flat on 56 % of days, earning 0.0069 % a day against 0.118 % for holding, while each case moves 21 times the cost of a trade.
- **F7:** Time of day also stands out. The 4h bar opening at 16:00 UTC returns +0.077 % above usual (t 5.1, n 17506) and the bar opening at 20:00 returns −0.072 % (t −4.6). Fridays show +0.40 % excess over the day (t 4.3, n 2478), but that is not positive in 2021, 2022 or 2025 (t 0.5, −1.9, −0.7), and these calendar effects cannot be written as graded ideas.

## Ideas
- `027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.g1_range-expansion-predicts-rebound` (from F1, F2, F6): The wider the coin's mean bar range over the last 24 hours relative to its 30-day average, the higher its return over the next 3 days. Unusually quiet stretches are followed by below-usual returns and unusually wide ones by above-usual returns, all along the scale.
- `027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.g2_wide-range-falls-rebound-graded` (from F3, F4, F1): When the coin's 24-hour range is wider than its 30-day average, the larger its 24-hour fall measured in usual 24-hour moves, the higher its return over the next 3 days.
- `027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.g3_next-day-rebound-after-falls` (from F5, F6): The larger the coin's 24-hour fall measured in usual 24-hour moves, the higher its return over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
