---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback_1h
idea tested: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4139 USD
---
## Findings
- **F1:** The 24-hour move reverses over the next 24 hours, and more so the larger it is against the coin's own volatility. On a non-overlapping 24-hour grid, with the 24-hour return z-scored by the coin's 30-day hourly volatility, the reversal by |z| quintile is −15, −2, −3, +23 and +52 bp. The top quintile has t 5.09 over 3260 cases and a strength of 0.104. That move is about 2.7 times the 0.19 % cost of a trade. The same holds on the grid that starts at 00 UTC, where continuation in the top quintile is −45.9 bp, t −4.25, over 3416 cases.
- **F2:** The 24-hour reversal comes mostly after falls. After the largest falls, the next 24 hours rise 92.7 bp (t 5.80, 1554 cases). After the largest rises, the next 24 hours fall only 15.7 bp (t 1.19, 1706 cases).
- **F3:** The 24-hour reversal is uneven across years and coins. In the top quintile it is +178, +51, +171 and +42 bp in 2018, 2019, 2021 and 2023 (t 5.2, 2.0, 4.6, 2.9). It is −9, −34 and −7 bp in 2020, 2024 and 2025, none significant. It is positive in all six coins, weakest in BTC (+9.7 bp, t 0.60) and strongest in XMR (+79.6 bp, t 3.24).
- **F4:** The tested 2-hour snapback is part of a general 2-hour reversal that is not tied to settlement. Across all even hours, the reversal of the 2-hour move rises with its size: +12.3 bp in the top decile of |z| (t 7.76, 19625 cases). It also rises with volatility: 1.5, 2.7 and 8.9 bp by volatility tercile (t 4.2, 5.6, 11.0). Even the largest of these 2-hour moves is below the 19 bp cost, consistent with the backtest's gross trade means of −0.21 % to +0.06 % against net means of −0.31 % to −0.05 %.
- **F5:** The counter-trend snapback is not specific to settlement times, which breaks the brief's own falsification clause:
- **F6:** The hour of day carries a drift. The 1-hour return after the close at hour 21 UTC is +5.45 bp (t 6.75), and after hour 22 it is +4.36 bp (t 5.66). The 2-hour return after the hour-21 close is positive in 7 of 8 years (t 2.0 to 5.9; 2022: −4.3 bp, t −1.43). At about 10 bp per 2 hours, this is half the cost of a trade.
- **F7:** Large 3-day moves continue over the next 3 days rather than reversing: −90.6 bp of reversal in the top |z| quintile (t −2.99, 1050 cases). The lower quintiles are not monotone (−50.8, +10.8, +29.4, +28.7), so this does not stand out from chance given the number of angles looked at.

## Ideas
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback.g1_one-day-oversold-rebound` (from F1, F2, F3): After a coin's 24-hour fall, the larger that fall relative to the coin's own recent hourly volatility, the more the coin rises over the next 24 hours.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback.g2_volatility-scaled-daily-reversal` (from F1, F4): After a coin's 24-hour move in either direction, the larger that move relative to the coin's own recent hourly volatility, the more the coin moves back against it over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
