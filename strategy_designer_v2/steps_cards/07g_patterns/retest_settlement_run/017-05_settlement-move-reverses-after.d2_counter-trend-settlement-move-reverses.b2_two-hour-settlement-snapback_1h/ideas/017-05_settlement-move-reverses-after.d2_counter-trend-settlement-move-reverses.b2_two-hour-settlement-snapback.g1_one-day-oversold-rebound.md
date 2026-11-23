---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a coin's 24-hour fall, the larger that fall relative to the coin's own recent hourly volatility, the more the coin rises over the next 24 hours.
Consequence: A trader can buy a coin after an unusually sharp one-day fall and expect a rebound over the following day that is large enough to cover trading costs, and should refuse to short into it.
Why:
- F1: The 24-hour move reverses over the next 24 hours, and more so the larger it is against the coin's own volatility. On a non-overlapping 24-hour grid, with the 24-hour return z-scored by the coin's 30-day hourly volatility, the reversal by |z| quintile is −15, −2, −3, +23 and +52 bp. The top quintile has t 5.09 over 3260 cases and a strength of 0.104. That move is about 2.7 times the 0.19 % cost of a trade. The same holds on the grid that starts at 00 UTC, where continuation in the top quintile is −45.9 bp, t −4.25, over 3416 cases.
- F2: The 24-hour reversal comes mostly after falls. After the largest falls, the next 24 hours rise 92.7 bp (t 5.80, 1554 cases). After the largest rises, the next 24 hours fall only 15.7 bp (t 1.19, 1706 cases).
- F3: The 24-hour reversal is uneven across years and coins. In the top quintile it is +178, +51, +171 and +42 bp in 2018, 2019, 2021 and 2023 (t 5.2, 2.0, 4.6, 2.9). It is −9, −34 and −7 bp in 2020, 2024 and 2025, none significant. It is positive in all six coins, weakest in BTC (+9.7 bp, t 0.60) and strongest in XMR (+79.6 bp, t 3.24).
