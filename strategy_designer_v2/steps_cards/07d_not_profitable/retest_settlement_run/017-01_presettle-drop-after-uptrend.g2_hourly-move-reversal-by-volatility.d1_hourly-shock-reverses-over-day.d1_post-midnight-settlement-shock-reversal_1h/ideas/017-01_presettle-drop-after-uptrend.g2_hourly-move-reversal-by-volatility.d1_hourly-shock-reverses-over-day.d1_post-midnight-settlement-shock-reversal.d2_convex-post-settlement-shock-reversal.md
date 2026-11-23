---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-hour return in the first hour after the 00:00 UTC funding settlement relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way, and the reversal grows faster than the move itself, so that moves of several usual hourly moves reverse far more per unit of move than small ones.
Consequence: A trader would size the daily post-settlement fade convexly in the move, near nothing for ordinary hours and large for big shocks, so that the book is not exposed every day to cases whose move does not cover a trade's cost.
Why:
- F2: The effect grows with the size of the post-settlement hour's move. The drift-adjusted 24-hour reversal is +0.16 % (t 2.1, 4820 cases) for |forecast| 0–5, +0.18 % (t 2.5) for 5–10, +0.39 % (t 4.5) for 10–15 and +0.50 % (t 6.7, 4872 cases) for 15–20. The small signals carry little: even holding only the signals with |forecast| ≥ 10, at full weight, lifts a simulated book's Calmar from 0.26 to 0.61, with the deepest fall going from -75 % to -63 % and Sharpe from 0.60 to 0.93.
- F8: The book trades at 1.65 trades a day and is in a position on 98 % of days, though its signal comes once a day. Its small signals still get a mean |allocation| of 0.25, against 0.77 for large ones. With a trade cost of 0.19 %, the small signals' +0.16–0.18 % reversal per case does not cover the cost.
- F1: The check failed on the falls. The book's deepest fall was -47.0 % over 140 days in w12–w13, against a yearly return of +22.2 % (Calmar 0.47 against the 0.75 required). During that fall the coins barely drifted (-2.8 bp a day) but moved hard (346 bp mean absolute daily move), while the book lost 40 bp a day. In w12 the large signals (|forecast| ≥ 10) lost 0.49 % per case (t -2.04, 410 cases), and w12 alone fell 42 %.
- F6: The book's losses come on the coins' big days. Its worst tenth of days lost 3.16 % with a mean absolute coin move of 6.6 %, against 1.4 % on middle days. The mean worst excursion inside a 24-hour case is -2.6 %, about eight times the +0.33 % mean case.
