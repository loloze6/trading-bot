---
brief: 013_anchoring-to-recent-high
source-idea: 013-04_heavy-volume-below-high-breakout
line: 7.d not profitable
backtest: 013-04_heavy-volume-below-high-breakout_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 52-week high, the heavier its volume over the preceding 10 days, relative to its own 90-day average, the larger its return over the next 30 days, and this return keeps building on the days when its close has slipped back below that prior high within those 30 days.
Consequence: A trader keeps a break position for the 30 days after the close above the 52-week high instead of letting a dip back under the high end it, which multiplies the time in the market and the share of the move captured.
Why:
- F1: The book is almost never in the market: it holds a position on only 1.38% of bars, across 152 entries with a median spell of 1 day (mean 1.56, max 5). Trades per bar are 0.0095 and the mean daily return is 5.9e-05, which explains why the size, trades and Calmar measures fail even though the bars it does hold gain 0.99% a day against 0.13% for all bars.
- F2: The book drops the break far too early: its position is lost as soon as the close slips back under the prior high, so it holds only 11.3% of the 30 days after each break. Over those 30 days the idea's own horizon pays, with a 30-day excess of +9.5% on 49 non-overlapping break cases (t 1.33) and a 6.4% excess on trending bars against -0.08% on the others.
- F3: The 30 days after a break pay as a whole. A unit position held on every one of those 1,531 days earns a mean 0.49% a day with an annualised Sharpe of 1.64, on 8.9% of all bars. The book's in-position days in that span earn 0.86% excess (t 2.03, n 237), and the days it sits out still earn 0.14% excess (t 1.01, n 1,869).
- F6: Holding the coin's 30 days after a break pays even when the price has fallen from its post-break peak. Daily excess is +0.47% on days 1–30 in the deepest drawdown quartile (mean -28% from the peak, t 1.26) and +0.47% near the peak (t 1.85). Falling back below the high therefore does not mark the move as over.
