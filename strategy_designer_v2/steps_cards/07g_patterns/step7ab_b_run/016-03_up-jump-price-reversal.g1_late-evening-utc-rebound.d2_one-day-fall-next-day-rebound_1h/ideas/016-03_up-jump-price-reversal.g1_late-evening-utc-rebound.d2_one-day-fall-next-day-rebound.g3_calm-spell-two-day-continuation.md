---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over its last 7 days stands low within its own last 3 months, the larger its 24-hour move, the further it continues in the same direction over the next 2 days.
Consequence: A trader in a calm spell follows the last day's move for two days rather than fading it.
Why:
- F1: The 24-hour reversal sits almost entirely in the coin's high-volatility regime. On the non-overlapping daily grid, cases were split by where each coin's 7-day hourly volatility stood within its own trailing ~3 months. In the top fifth, the move against the last 24 hours was +62 bps (strength 0.13, t 5.8, 2,788 cases). In the bottom fifth it was −17 bps (t −2.6, 3,563 cases), a continuation. Per case, the top fifth's move is about 3.3 times the 19 bps round-trip cost, while the tested idea over all cases makes only 12 bps.
- F5: In a regression of the next 24-hour excess return on the 24-hour move scaled by 7-day volatility, the sign flips with the volatility rank. The scaled move has a coefficient of +0.107 (t 5.9), a continuation at low volatility. Its product with the coin's volatility rank has −0.281 (t −9.0), so the coin reverses at high volatility.
- F6: In the coin's lowest trailing-volatility fifth, 24-hour moves continue rather than reverse. The move against them is −17 bps over 24 hours (t −2.6) and −33 bps over 48 hours (t −3.6, 3,563 cases); the 48-hour move is above the round-trip cost.
