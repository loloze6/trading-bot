---
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6082 USD
---
## Findings
- **F1:** The 24-hour reversal sits almost entirely in the coin's high-volatility regime. On the non-overlapping daily grid, cases were split by where each coin's 7-day hourly volatility stood within its own trailing ~3 months. In the top fifth, the move against the last 24 hours was +62 bps (strength 0.13, t 5.8, 2,788 cases). In the bottom fifth it was −17 bps (t −2.6, 3,563 cases), a continuation. Per case, the top fifth's move is about 3.3 times the 19 bps round-trip cost, while the tested idea over all cases makes only 12 bps.
- **F2:** Inside that high-volatility regime the rebound is graded by the depth of the fall. For falls, the smallest, middle and largest thirds of the 24-hour move were followed by +11 bps (t 0.3, n 437), +56 bps (t 2.4, n 434) and +216 bps (strength 0.43, t 6.4, n 441) of unusual move over the next 24 hours. After rises the reversal was much weaker: +31, +26 and +44 bps, the largest third at t 1.9.
- **F3:** The high-volatility reversal is broad and stable across coins, years and windows. With a trailing rank of volatility, it is positive on all 6 coins (31 to 90 bps; t above 2 on BTC, ETH, LTC and XMR) and positive in every year from 2018 to 2025 (20 to 189 bps). With the volatility fifth taken over the whole sample, it is positive in 87.5 % of windows, and its t stays between 4.64 and 6.17 when any one window is left out.
- **F4:** The effect outlasts the day. In the top trailing-volatility fifth the move against the last 24 hours is +30 bps over 12 hours (t 4.3) and +51 bps over 48 hours (t 3.9).
- **F5:** In a regression of the next 24-hour excess return on the 24-hour move scaled by 7-day volatility, the sign flips with the volatility rank. The scaled move has a coefficient of +0.107 (t 5.9), a continuation at low volatility. Its product with the coin's volatility rank has −0.281 (t −9.0), so the coin reverses at high volatility.
- **F6:** In the coin's lowest trailing-volatility fifth, 24-hour moves continue rather than reverse. The move against them is −17 bps over 24 hours (t −2.6) and −33 bps over 48 hours (t −3.6, 3,563 cases); the 48-hour move is above the round-trip cost.
- **F7:** The brief's grind-versus-jump distinction is weak and inconsistent in these bars:
- **F8:** The hourly pattern by hour of day is strong but small. The coin's hourly return is high at 20 and 21 UTC (t 6.1 and 5.1) and low at 2 and 13 UTC (t −4.8 and −4.6). These are single-hour moves of a few hundredths of a standard deviation, below a round trip by F2 of the findings file.

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound.g1_volatile-spell-fall-rebound` (from F1, F2, F3, F4, F5): When a coin's hourly volatility over its last 7 days stands high within its own last 3 months, the more it has fallen over its last 24 hours, the more it rises over the next 24 hours.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound.g2_volatility-graded-one-day-reversal` (from F1, F3, F5): The higher a coin's 7-day hourly volatility stands within its own last 3 months, the more its 24-hour move, measured in units of that volatility, is reversed over the next 24 hours.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound.g3_calm-spell-two-day-continuation` (from F1, F5, F6): When a coin's hourly volatility over its last 7 days stands low within its own last 3 months, the larger its 24-hour move, the further it continues in the same direction over the next 2 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
