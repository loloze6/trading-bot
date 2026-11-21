---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift
line: 7.d not profitable
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises over the two hours after 21:00 UTC, and the larger its fall over the past 24 hours measured in units of its 7-day hourly volatility, the larger that rise.
Consequence: A trader would buy a coin at the 21:00 close after a steep, volatility-adjusted 24-hour drop, holding it for about two hours, and would refuse the trade when the coin has not fallen.
Why:
- F2: The slot effect itself is real but too small for its cost. The return from the 21:00 to the 23:00 close averages 0.101 % (t 9.07, 16,256 independent days), and every coin is positive with t between 3.1 and 4.7. Yet the fee per unit of turnover is 0.075 % to 0.125 %, so a daily in-and-out round trip costs 0.15 % to 0.25 % of the position, more than the 0.10 % it earns.
- F3: Holding longer does not grow the gain to pay the fee. The mean return from the 21:00 close is 0.108 % over 4 hours (t 6.6), falls to 0.038 % over 8 hours (t 1.8) and is 0.118 % over 24 hours (t 3.1), so nearly all of the drift sits in the first 2 to 4 hours.
- F5: The slot gain is largest after a fall. When the coin's 24-hour return into 21:00 is in its lowest quintile (mean -5.95 %), the slot return is 0.229 %, against 0.071 % to 0.074 % in the middle quintiles. The lowest quintile of the 7-day return (mean -15.3 %) also gives 0.132 %, against 0.076 % in the middle.
