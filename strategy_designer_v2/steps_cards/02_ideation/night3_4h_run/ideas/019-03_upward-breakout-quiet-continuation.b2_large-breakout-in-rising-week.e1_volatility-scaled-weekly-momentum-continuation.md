---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week
line: 7.e profitable but not proven
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 7-day return, measured in units of its own 4h volatility, the more the coin rises over the next three days.
Consequence: A trader would buy coins after weeks that are strong for their volatility, and the book's gain is a reason to hold such positions rather than wait for a breakout bar.
Why:
- F1: The book's gain is mostly timing, not the market's own rise. Summed over bars, the position's gain is 22.3 against 9.7 from the coins' mean drift, so timing is about 12.6. Timing is positive on all 6 coins: XRP +3.61, ETH +3.43, ZEC +2.82, BTC +1.86, LTC +0.52, XMR +0.37.
- F3: The break itself adds nothing over the regime. On non-overlapping 3-day grid bars with a positive 7-day return, bars in an upward break show +0.49 % unusual move (n 292, t 0.79). Bars not in a break show +0.19 % (n 2394, t 1.10).
- F4: The 7-day return carries the effect, graded at its top end. Among grid bars with a positive 7-day return, the 3-day unusual move by quartile of that return (mean 1.4 %, 4.4 %, 9.3 %, 24 %) is -0.40 %, -0.01 %, +0.27 % and +1.05 % (t 2.33, n 672). Among the idea's own entries the same quartiles give +0.03 %, +0.45 %, +0.35 % and +1.06 % (t 1.99).
- F5: The 7-day return measured in units of the coin's 4h volatility predicts both ways in its tails. Over 3 days the top sextile gives +0.91 % (t 2.67, strength 0.10, n 882). Over 12 days the top sextile gives +3.02 % (t 2.21, strength 0.15, n 210) and the bottom sextile -2.59 % (t -2.59, strength -0.15). Rank correlation over all bars is weak (0.009 at 3 days, 0.047 at 12 days).
