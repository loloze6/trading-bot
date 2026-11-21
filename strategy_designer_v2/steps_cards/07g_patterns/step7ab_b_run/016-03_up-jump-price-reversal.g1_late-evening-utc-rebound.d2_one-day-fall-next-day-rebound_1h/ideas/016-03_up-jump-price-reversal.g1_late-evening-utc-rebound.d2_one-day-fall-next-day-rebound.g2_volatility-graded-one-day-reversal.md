---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 7-day hourly volatility stands within its own last 3 months, the more its 24-hour move, measured in units of that volatility, is reversed over the next 24 hours.
Consequence: A trader scales a fade of the last day's move by how volatile the coin is next to its own recent history.
Why:
- F1: The 24-hour reversal sits almost entirely in the coin's high-volatility regime. On the non-overlapping daily grid, cases were split by where each coin's 7-day hourly volatility stood within its own trailing ~3 months. In the top fifth, the move against the last 24 hours was +62 bps (strength 0.13, t 5.8, 2,788 cases). In the bottom fifth it was −17 bps (t −2.6, 3,563 cases), a continuation. Per case, the top fifth's move is about 3.3 times the 19 bps round-trip cost, while the tested idea over all cases makes only 12 bps.
- F3: The high-volatility reversal is broad and stable across coins, years and windows. With a trailing rank of volatility, it is positive on all 6 coins (31 to 90 bps; t above 2 on BTC, ETH, LTC and XMR) and positive in every year from 2018 to 2025 (20 to 189 bps). With the volatility fifth taken over the whole sample, it is positive in 87.5 % of windows, and its t stays between 4.64 and 6.17 when any one window is left out.
- F5: In a regression of the next 24-hour excess return on the 24-hour move scaled by 7-day volatility, the sign flips with the volatility rank. The scaled move has a coefficient of +0.107 (t 5.9), a continuation at low volatility. Its product with the coin's volatility rank has −0.281 (t −9.0), so the coin reverses at high volatility.
