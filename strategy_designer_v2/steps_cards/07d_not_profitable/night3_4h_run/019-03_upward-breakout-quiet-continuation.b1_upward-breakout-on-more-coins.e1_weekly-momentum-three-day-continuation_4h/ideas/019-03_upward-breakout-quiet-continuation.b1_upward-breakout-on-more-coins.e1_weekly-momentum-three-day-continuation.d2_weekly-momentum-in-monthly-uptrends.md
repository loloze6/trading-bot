---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's return over the past 7 days, measured against its 30-day volatility, the more the coin rises over the next three days, by more than its normal drift, only while its 30-day return is positive.
Consequence: A trader should lean long after strong weeks in coins rising over the month, and not use falls as a reason to go short.
Why:
- F2: In each of the four deepest falls, both the long and the short bars lost money. In the deepest fall the longs lost 4.0 bps per bar over 10797 bars and the shorts 1.7 bps per bar over 12643 bars. The book is caught on both sides when the market turns.
- F3: On the 18-bar grid, the idea's move depends on whether the forecast agrees with the coin's 30-day return. Where they agree, the move beyond the drift is +73.7 bps for longs in a 30-day rise (t 3.58, 2968 cases) and +58.0 bps for shorts in a 30-day fall (t 3.65, 2902 cases). Where they disagree, it is −34.0 bps for longs in a 30-day fall (t −1.68, 1661 cases) and +20.7 bps for shorts in a 30-day rise (t 1.03, 1564 cases).
- F5: The size explains why the gain is thin. Over all cases the move is 18 bps against a 22 bps round trip (0.8 times the cost). The agreeing cases carry 58 to 74 bps beyond the drift, about 2.6 to 3.3 times the cost, and 126 bps of total move for longs in a 30-day rise.
- F6: The book's bars show the same split. Longs in a 30-day rise earn 4.39 bps net per bar (55535 bars), while longs in a 30-day fall lose 0.37 bps (29644 bars). Shorts in a 30-day rise lose 1.60 bps (27445 bars) and shorts in a 30-day fall earn only 0.03 bps (55313 bars). Across all shorts the net is −0.89 bps per bar, against +2.52 bps for longs.
- F7: The gain sits in the top forecast quintile, at 5.40 bps net per bar. Quintiles 0 to 2 lose 0.33 to 0.71 bps per bar, after fees of 0.18 to 0.48 bps per bar.
