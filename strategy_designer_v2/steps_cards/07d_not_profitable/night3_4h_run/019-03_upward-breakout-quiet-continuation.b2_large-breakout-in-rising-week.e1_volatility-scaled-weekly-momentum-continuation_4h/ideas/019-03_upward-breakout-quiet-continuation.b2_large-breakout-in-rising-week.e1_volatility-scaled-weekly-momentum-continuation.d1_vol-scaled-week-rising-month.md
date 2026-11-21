---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 7-day return, measured in units of its own 4h volatility, the more the coin rises over the next twelve days, only while its 30-day return is positive.
Consequence: A trader would buy coins after weeks that are strong for their volatility within a rising month and hold them about twelve days, so that each trade captures a move several times its cost instead of shorting against the drift.
Why:
- F1: The book fails on size. Per case over 3 days, the total move is +0.18 % and the unusual move +0.17 % (strength 0.017 against a usual move of 8.17 %, 5544 cases), while a buy and a sell cost 0.19 %. That is 0.9 times the cost, so the mean daily return is 0.00045 against the 0.0005 required, and the Sharpe of 0.41 trails holding's by 0.14.
- F3: The move outlasts the 3-day horizon. Strong-week cases (forecast above 10) gain +0.67 % net of drift over 3 days, +0.73 % over 6 days and +1.67 % over 12 days. For the top positive bucket alone the excess rise is +0.72 %, +0.94 % and +2.30 %. Holding 3 days captures under half of the move and pays the cost on each re-entry.
- F4: The effect exists only when the 30-day return points the same way as the 7-day signal. With agreement, the gain net of drift is +0.65 % over 3 days and +1.51 % over 12 days (n 2503). With disagreement, it is +0.05 % and -0.21 % (n 1349).
- F5: The short side earns nothing once the coins' drift is counted. Shorts have a total move of -0.13 % per case over 3 days, against +0.77 % for longs (about 2640 cases each). Summed short gains before costs are negative on BTC (-0.70), XMR (-0.94) and XRP (-0.84).
- F6: The deepest fall of the chained book is 63 %. It deepened steadily from w2 (-29 %) to w10 (-63 %), and in w4, w6 and w10 the coins rose (+0.28 %, +0.23 %, +0.40 % per day) while the book lost (-0.02 % to -0.06 % per day). Calmar is 0.14.
