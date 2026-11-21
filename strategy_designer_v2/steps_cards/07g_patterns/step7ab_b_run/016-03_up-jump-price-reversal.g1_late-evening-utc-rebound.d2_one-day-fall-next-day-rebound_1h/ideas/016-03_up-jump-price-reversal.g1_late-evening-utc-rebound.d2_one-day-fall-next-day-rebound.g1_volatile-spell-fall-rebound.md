---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over its last 7 days stands high within its own last 3 months, the more it has fallen over its last 24 hours, the more it rises over the next 24 hours.
Consequence: A trader buys deep one-day falls only when the coin is in a volatile spell, where the rebound is several times a round-trip cost, and refuses them in calm spells.
Why:
- F1: The 24-hour reversal sits almost entirely in the coin's high-volatility regime. On the non-overlapping daily grid, cases were split by where each coin's 7-day hourly volatility stood within its own trailing ~3 months. In the top fifth, the move against the last 24 hours was +62 bps (strength 0.13, t 5.8, 2,788 cases). In the bottom fifth it was −17 bps (t −2.6, 3,563 cases), a continuation. Per case, the top fifth's move is about 3.3 times the 19 bps round-trip cost, while the tested idea over all cases makes only 12 bps.
- F2: Inside that high-volatility regime the rebound is graded by the depth of the fall. For falls, the smallest, middle and largest thirds of the 24-hour move were followed by +11 bps (t 0.3, n 437), +56 bps (t 2.4, n 434) and +216 bps (strength 0.43, t 6.4, n 441) of unusual move over the next 24 hours. After rises the reversal was much weaker: +31, +26 and +44 bps, the largest third at t 1.9.
- F3: The high-volatility reversal is broad and stable across coins, years and windows. With a trailing rank of volatility, it is positive on all 6 coins (31 to 90 bps; t above 2 on BTC, ETH, LTC and XMR) and positive in every year from 2018 to 2025 (20 to 189 bps). With the volatility fifth taken over the whole sample, it is positive in 87.5 % of windows, and its t stays between 4.64 and 6.17 when any one window is left out.
- F4: The effect outlasts the day. In the top trailing-volatility fifth the move against the last 24 hours is +30 bps over 12 hours (t 4.3) and +51 bps over 48 hours (t 3.9).
- F5: In a regression of the next 24-hour excess return on the 24-hour move scaled by 7-day volatility, the sign flips with the volatility rank. The scaled move has a coefficient of +0.107 (t 5.9), a continuation at low volatility. Its product with the coin's volatility rank has −0.281 (t −9.0), so the coin reverses at high volatility.
