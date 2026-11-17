---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's day volume relative to its own 30-day average volume, the higher its return over the next 3 days, only on days when the coin closed lower than the day before.
Consequence: A heavy-volume down day is a reason to favour a long over the next few days, more firmly the heavier the volume, while a heavy-volume up day gives no such reason.
Why:
- F1: The book is short on 58% of bars (long 34%, flat 8%, mean position −0.007), so it gives up the coins' rise. Its mean daily return is 0.000105 against 0.00118 for holding, its Sharpe is 0.50 against 0.55, and its Calmar is 0.27, from a 3.6% yearly return over a 13.5% deepest fall.
- F2: The short side earns nothing. Short bars (n=10120) have a mean gain of −0.000003 because the coin's next-day return there is only −0.0002. Long bars (n=6018) carry all of the book's gain, at 0.00057 per bar on a next-day coin return of 0.0034.
- F3: Forecast quintiles 0–3 all show a negative 3-day excess return (−0.0024, −0.0028, −0.0026, −0.0009) and only the top quintile is positive (+0.0087, n=1145). The pooled slope of t=4.1 (n=5723) comes from heavy days alone, while light volume carries no graded fall to short.
- F4: Heavy volume pays only on days the coin closed lower. On down days the top volume-ratio quintile (mean ratio 2.25) has a 3-day excess return of +0.0242 (t=4.5, n=397), and quintiles 0–3 sit between −0.001 and −0.005 with |t|<1.4. On up days the top quintile has −0.0033 (t=−0.8, n=460).
- F5: The heavy-volume down-day gain is positive in 7 of 8 years, at +0.016 to +0.061, with t up to 3.9 in 2020. It is positive whatever the 30-day trend: +0.022 (t=3.5, n=206) when the 30-day return is negative and +0.026 (t=3.0, n=191) when it is positive.
- F7: The gain is not linear in the product of the down move and the volume ratio (slope t=0.27, n=4283), but it is graded at the extreme quintile (+0.0070, t=2.1). The effect sits in the heaviest-volume falling days, not across all days.
