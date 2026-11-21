---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 24 hours, only while the coin rose over the preceding 3 days.
Consequence: A deep evening dip inside a 3-day rise is a reason to go long for a day rather than for two hours, and a dip inside a 3-day fall is a reason to stay out.
Why:
- F1: Fees, not the forecast, sink the book: across the 11,085 trades (all long, median 120 minutes) the mean gross gain per coin is 0.01–0.15 % and the mean net is -0.09 to +0.05 %; the fee runs 0.107 % per unit of turnover, and the summed bar gains of 4.84 sit against costs of 9.38, giving a Sharpe of -1.08 and a mean daily return of -0.026 %.
- F2: The 2-hour effect is real but smaller than a round trip: decision bars with a positive forecast earn a 2-hour excess return of 0.095 % (t 5.31, n 8,596), and the best forecast fifth (the fourth) earns only 0.22 %, against about 0.21 % of round-trip fee; the shallowest-fall fifth earns 0.010 % (t 0.31) while still paying full fees.
- F3: The second active hour adds trades that lose before fees: the 2,081 trades entered at 20:00 have a gross mean of -0.021 % and a net of -0.12 %, while the 8,960 entered at 19:00 have a gross of 0.098 % and a net of -0.002 %.
- F6: Active cases that come after a 3-day rise keep paying past 2 hours (excess 0.098 % at 6 h, t 2.44; 0.15 % at 24 h, t 1.77; n 2,805), while those after a 3-day fall fade to -0.025 % at 24 h (t -0.35, n 5,680).
