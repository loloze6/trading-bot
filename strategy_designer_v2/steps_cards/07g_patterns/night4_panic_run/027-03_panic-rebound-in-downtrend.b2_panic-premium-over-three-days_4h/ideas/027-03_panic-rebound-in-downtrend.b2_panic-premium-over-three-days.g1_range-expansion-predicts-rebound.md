---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days
line: 7.g patterns
backtest: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The wider the coin's mean bar range over the last 24 hours relative to its 30-day average, the higher its return over the next 3 days. Unusually quiet stretches are followed by below-usual returns and unusually wide ones by above-usual returns, all along the scale.
Consequence: A trader should lean long a coin as its 24-hour range widens against its 30-day norm, and refuse longs after its quietest stretches.
Why:
- F1: Across all bars, not only panics, the coin's excess 3-day return rises steadily with the 24-hour mean bar range over its 30-day mean. It goes from −0.78 % (t −3.5, n 1389) when the ratio is at most 0.7, to −0.12 % for 0.7–1, +1.06 % for 1.5–2 (t 2.2, n 446) and +3.31 % for 2–3 (t 3.7, n 168). Regressing the 3-day excess on the log of the ratio gives a slope of 0.0148 (t 5.7, n 5436) while the scaled 24-hour return adds nothing (t −0.49).
- F2: The range gradient holds in every coin (slopes 0.005 to 0.026, t 0.8 to 3.7, strongest in XRP at t 3.7 and ZEC at t 3.3) and in both halves of the windows (early t 3.1, late t 4.8). It also shows over 1 day (+1.26 % above 3×, t 2.0) and over 7 days (+3.3 % for 1.5–2, t 2.2).
- F6: The book is almost never in the market, so its small earnings come from exposure, not from the move. It holds a position on 15.6 % of bars at a mean allocation of 0.14 and is flat on 56 % of days, earning 0.0069 % a day against 0.118 % for holding, while each case moves 21 times the cost of a trade.
