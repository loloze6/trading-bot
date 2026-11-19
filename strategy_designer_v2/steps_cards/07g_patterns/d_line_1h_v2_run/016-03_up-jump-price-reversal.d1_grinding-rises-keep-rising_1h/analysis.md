---
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
idea tested: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3561 USD
---
## Findings
- **F1:** Each coin's hourly returns in the 21:00 and 22:00 UTC bars are positive on their own: BTC +4.3bp (t 4.5), ETH +5.6bp (t 4.6), LTC +4.9bp (t 3.7), XMR +4.9bp (t 3.6), XRP +4.8bp (t 3.0) and ZEC +5.4bp (t 3.3), with about 5,600 to 5,800 non-overlapping hourly cases per coin; pooled, hour 21 gives +5.5bp (t 6.9) and hour 22 gives +4.4bp (t 5.8), against roughly 0 to 1bp in most other hours.
- **F2:** The 21:00–22:00 UTC rise grows with the coin's trailing 72-hour mean absolute hourly return: +2.1bp (t 3.2) in the lowest volatility quintile, then +2.0, +4.2, +4.7 and +11.4bp (t 5.5) in the highest, with about 6,800 hours per quintile.
- **F3:** The 21:00–22:00 UTC rise is positive in 7 of 8 years (2018 +5.1bp t 2.3, 2019 +5.9bp t 4.5, 2020 +8.6bp t 5.3, 2021 +9.8bp t 5.4, 2023 +2.0bp t 1.9, 2024 +6.9bp t 5.7, 2025 +3.6bp t 2.4; only 2022 is −2.2bp t −1.5) and on every weekday (+2.8 to +5.6bp); the other hours average −1.7 to +1.2bp in the same years.
- **F4:** Among 3-day rises on the non-overlapping 72-bar grid, the next-3-day excess return rises with path efficiency (net log move over the summed absolute hourly log moves): −38bp, −27bp, +16bp, +23bp and +111bp (t 2.8, n 597) from the lowest to the highest efficiency quintile; efficiency also correlates with the next-3-day excess return over all moves (rho 0.044, t 3.3, n 5,539), while the 3-day return alone does not (rho 0.015, t 1.1).
- **F5:** The efficiency effect is not stable across years: the correlation of signed efficiency with the next-3-day excess return is positive and significant in 2018 (t 2.3), 2020 (t 2.2) and 2024 (t 2.8), but negative in 2019, 2021 and 2025 (t −1.1 to −1.3); across coins it is positive for 5 of 6 (t 1.0 to 1.4 each).
- **F6:** Coin daily returns pooled over coins and windows are highest on Saturday (+45bp, t 5.5) and Friday (+33bp, t 3.5); the book's best weekdays are Saturday (+19bp, t 4.7) and Monday (+17bp, t 3.0); these pooled t's overstate the evidence because the coins move together.
- **F7:** The tested grind measure (one minus the top-3 hourly gains' share of a 3-day rise) correlates with the next-3-day excess return (rho 0.058, t 3.1, n 2,865) only before the rise's size is accounted for; the plan's regression with the 3-day return included gives t 1.5.

## Ideas
- `016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.g1_late-utc-volatility-scaled-drift` (from F1, F2, F3): In each coin, the price rises over the 21:00–23:00 UTC hours, and the rise is larger the higher the coin's average absolute hourly return over the past 3 days.
- `016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.g2_efficient-rises-keep-rising` (from F4, F5, F7): When a coin has risen over the past 3 days, the more efficient the path of that rise (a larger net move relative to the sum of its absolute hourly moves), the more the coin rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
