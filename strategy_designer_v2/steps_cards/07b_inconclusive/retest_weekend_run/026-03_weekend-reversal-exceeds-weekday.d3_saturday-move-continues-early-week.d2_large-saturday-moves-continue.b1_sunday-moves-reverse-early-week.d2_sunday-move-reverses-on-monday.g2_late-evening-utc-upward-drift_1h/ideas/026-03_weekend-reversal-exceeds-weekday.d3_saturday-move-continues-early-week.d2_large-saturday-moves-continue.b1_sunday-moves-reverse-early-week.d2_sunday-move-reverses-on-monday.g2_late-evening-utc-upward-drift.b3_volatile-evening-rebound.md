---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift
line: 7.b inconclusive
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the two hours from 21:00 to 23:00 UTC is above its normal hourly drift, and the excess is larger the more the coin fell over the three hours before 21:00 and the higher its 30-day hourly volatility.
Consequence: A trader would buy at 21:00 UTC mainly when a volatile coin has just fallen, and hold it until 23:00 UTC, where the move per case is large next to the cost of a trade.
Why:
- F3: Graded by the idea's own variable, the effect grows with volatility. Within each coin, the 2-bar excess from the 20:00 close rises from +0.042 % (t 2.69) in the lowest 30-day volatility quintile to +0.201 % (t 5.64) in the highest. On the standardised volatility the forecast uses, it rises from +0.003 % (t 0.12) in the lowest quintile to +0.154 % (t 4.56) in the highest.
- F5: Volatility and the prior fall compound each other. In the top volatility tercile, a prior 3-hour fall (mean −2.05 %) is followed by +0.411 % (t 8.39, 1,688 cases), against +0.085 % after a fall in the bottom volatility tercile and −0.055 % after a rise in the top one. That +0.41 % is about 2.2 times the 0.19 % cost of a trade, while the tested idea's total move is +0.10 % (0.5 times the cost).
- F4: The evening rise is mostly a rebound after a fall over the preceding three hours. With that fall scaled by volatility, the 2-bar excess from the 20:00 close falls from +0.369 % (t 7.55) in the decile with the largest prior fall (mean prior 3-hour return −2.98 %) through +0.10 % to +0.16 % in deciles 2 to 5, to about 0 or slightly negative (−0.04 % to +0.02 %) in the five deciles with prior rises. The slope of excess on the scaled prior move is −0.0011 per unit.
