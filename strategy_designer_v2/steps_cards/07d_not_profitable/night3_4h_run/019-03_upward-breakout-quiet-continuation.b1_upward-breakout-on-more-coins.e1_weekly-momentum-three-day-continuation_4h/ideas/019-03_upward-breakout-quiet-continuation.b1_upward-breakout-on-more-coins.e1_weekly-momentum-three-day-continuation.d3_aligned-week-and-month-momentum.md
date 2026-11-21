---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The more a coin's 7-day and 30-day returns, each measured against its 30-day volatility, both point up, the more the coin rises over the next three days, by more than its normal drift.
Consequence: A trader should size a three-day long by how strongly the week and the month agree in rising, so that each trade carries a move several times its cost.
Why:
- F3: On the 18-bar grid, the idea's move depends on whether the forecast agrees with the coin's 30-day return. Where they agree, the move beyond the drift is +73.7 bps for longs in a 30-day rise (t 3.58, 2968 cases) and +58.0 bps for shorts in a 30-day fall (t 3.65, 2902 cases). Where they disagree, it is −34.0 bps for longs in a 30-day fall (t −1.68, 1661 cases) and +20.7 bps for shorts in a 30-day rise (t 1.03, 1564 cases).
- F4: The agreement effect is graded. Ranked by how far the 30-day volatility-scaled return agrees with the forecast's side, the move beyond the drift by quintile is −25, 0.3, 96.5, 55.5 and 70.9 bps (t −1.33, 0.01, 3.98, 2.47, 2.89; about 1820 cases each).
- F5: The size explains why the gain is thin. Over all cases the move is 18 bps against a 22 bps round trip (0.8 times the cost). The agreeing cases carry 58 to 74 bps beyond the drift, about 2.6 to 3.3 times the cost, and 126 bps of total move for longs in a 30-day rise.
- F6: The book's bars show the same split. Longs in a 30-day rise earn 4.39 bps net per bar (55535 bars), while longs in a 30-day fall lose 0.37 bps (29644 bars). Shorts in a 30-day rise lose 1.60 bps (27445 bars) and shorts in a 30-day fall earn only 0.03 bps (55313 bars). Across all shorts the net is −0.89 bps per bar, against +2.52 bps for longs.
