---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3284 USD
---
## Findings
- **F1:** Saturday (UTC) is the one weekday whose coin return stands out: averaged across the six coins it is +0.46% on 414 days (t 3.07), against between −0.17% and +0.32% on the other six weekdays, and it holds after the top 1% of days are removed (+0.23%, t 3.48, while Monday, Tuesday and Thursday turn negative).
- **F2:** The Saturday excess is broad rather than a few outliers: Saturday minus other days is positive in all six coins (LTC t 2.67, XMR 1.82, ZEC 1.77, ETH 1.59, XRP 1.42, BTC 0.34), in 7 of 8 years (only 2023 negative, t −0.67) and in all four window groups (w7–12 t 2.66, w19–24 t 1.78); Saturday's median return is +0.19% against 0.00% on other days, and its hit rate is 55.0% against 50.0%.
- **F3:** The book's own daily return peaks on Saturday (+0.20%, t 2.78 over 414 days), the largest of any weekday. The strategy has no calendar input, so this gain comes from being long on the day the coins rise most.
- **F4:** The idea's own forecast does not grade the 20-day excess return: forecast buckets 0–5, 5–10, 10–15 and 15–20 give −2.9%, −1.1%, +0.2% and +5.5% (t −1.63 to 1.17), and every bucket's hit rate is below 50% (37–42%). The only positive mean comes from a few large gains, not from frequent drift.
- **F5:** Most of the book's mean daily gain of 0.0535% comes from holding the market rather than from timing: the position times the coins' mean return gives about 0.0342%, leaving about 0.019% for timing.
- **F6:** Other angles showed nothing beyond chance given how many I looked at: 20-day excess return by 200-day distance sextile (|t| ≤ 1.21), by volatility tercile (|t| ≤ 0.92) and by past 20-day return quintile (|t| ≤ 1.56); 5-day return after one-day moves was not graded (only the second quintile stood out, t −3.70, with the extremes +0.4% and +1.0%); and no weekday dominates the book's 40 largest gains or losses.

## Ideas
- `002-03_price-cross-above-long-sma.g1_saturday-crypto-drift` (from F1, F2, F3): In each coin, the close-to-close return over the UTC Saturday is higher than its return over the other days of the week, so the coin's next 1-day return is larger when the coming day is a Saturday.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
