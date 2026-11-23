---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday
line: 7.d confirmed, not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday, measured against the coin's usual 30-day move, is followed over Monday and Tuesday (the next 48 hours) by a move in the opposite direction whose size as a share of price grows with the coin's 30-day hourly volatility, so the reversal is largest in the coin's most volatile months and near nothing in its calmest.
Consequence: A trader would lean against Sunday's move with a stake that rises with the coin's hourly volatility, not falls with it, hold it through Tuesday, and refuse it when the coin is calm and the move cannot cover the fee.
Why:
- F1: The book sizes against its own effect: the vol-target sizing holds a mean position of 0.56 on Mondays in the lowest pooled tercile of 30-day hourly volatility, where the reversal is nil (-0.004 %, t -0.03, n 604; position-weighted -0.17 %), but only 0.21 on the highest tercile, where the reversal is +0.98 % per case (t 3.27, n 604); the middle tercile gives +0.56 % (t 3.06) at a position of 0.36.
- F2: Fees take all of what the book captures: its 3746 trades gain +0.098 % on average before fees and -0.003 % after; one trade costs 0.19 %, more than the whole low-volatility Monday move (≈0 %) but a fifth of the high-volatility one (0.98 %). That is why the mean daily return on days in a position is 0.0099 % against the 0.05 % required.
- F3: Its losses sit in the low-volatility years: the book lost in 2023 (-6.8 % summed daily returns), 2024 (-4.1 %) and 2025 (-5.6 %). In 2023, 166 of 224 Mondays fell in the lowest volatility tercile, and only 10 in the highest. The deepest fall (-16.8 %, 310 days) sits in those stretches, so a 0.7 % yearly return gives a Calmar of 0.04.
- F4: High volatility is not an effect of its own. On other days of the week, a day's 24-hour move is reversed over the next 24 hours by only +0.12 % (t 1.75, n 7281) in the highest volatility tercile, against +0.98 % after a Sunday at the same volatility. Monday's reversal at high volatility is not a general drift either: Monday's unsigned excess move is -0.23 % (t -0.77). The volatility grading is the idea's own stated condition.
- F5: It is the level of hourly volatility that grades the reversal, not volatility relative to the coin's own past six months: across terciles of that ratio the reversal is -0.35 %, +0.14 % and +0.01 % (all |t| < 1.1, n ≈ 200 each).
- F6: The reversal keeps going into Tuesday. Over 48 hours it is +0.58 % per case (t 3.82, n 2404) against +0.39 % over 24 hours (t 3.61), with hours 24–48 alone adding +0.21 % (t 2.19). In the highest volatility tercile it grows from +0.98 % to +1.37 % (t 3.49), and in the middle one from +0.56 % to +0.99 % (t 4.09).
