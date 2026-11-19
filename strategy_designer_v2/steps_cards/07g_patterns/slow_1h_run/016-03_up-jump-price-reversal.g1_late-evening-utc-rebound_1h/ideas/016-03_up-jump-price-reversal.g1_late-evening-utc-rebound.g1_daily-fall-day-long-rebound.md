---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over its last 24 hours, the more it rises over the next 24 hours.
Consequence: A dip-buying long held for a day collects the reversal with one round trip instead of twelve 2-hour round trips, so it has a chance to clear its cost.
Why:
- F3: The 24-hour reversal behind the idea holds over a full day, not only 2 hours. On a non-overlapping 24-bar grid, the slope of the next 24-hour return on the past 24-hour return is negative in every coin (−0.064 to −0.129, t −3.4 to −6.9, about 2,800 cases each) and in seven of eight years. The deepest-fall fifth gains +58.5 bps over the next 24 hours (t 5.69, n 3,423), while the 72-hour version is not significant (slope +0.016, t 1.16, n 5,539).
- F1: The book loses because of fees, not because the forecast is wrong: the position's gain averages 0.116 bps per bar against 0.225 bps per bar of fees. The fee hits 2.39 bps on the 19:00 bar and 2.38 bps on the 21:00 bar, and each of the roughly 1,800–1,900 two-hour trades per coin nets −0.09 % to +0.05 % after costs, with four of six coins negative.
- F5: How the 24-hour move was built changes nothing, which goes against the brief's grind-versus-jump split. Sorted into terciles by the largest hourly move's share of the day's total movement, the reversal slopes are −0.072, −0.097 and −0.081 (t −4.7, −7.0, −7.3, about 5,700 cases each).
- F6: The evening makes the reversal steeper. At the 20:00 close, the slope of the 2-hour return on the 24-hour return is −0.0189 (t −8.12, n 17,261), against −0.0062 (t −4.75, n 52,412) at the other odd hours. At 20:00 the deepest-fall fifth gains +21.3 bps over 2 hours (t 5.70), while the top fifth gains only +1.3 bps.
