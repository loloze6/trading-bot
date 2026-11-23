---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday move is reversed over Monday and Tuesday. The reversal over the next 2 days is larger the lighter the weekend's hourly volume is against its mean over the preceding five weekdays, and the larger the weekend move.
Consequence: A large weekend move made on thin volume is a reason to trade against it into Tuesday, and a reason to refuse a trade that follows it.
Why:
- F1: On Sundays with the thinnest weekend volume against the five weekdays before (lowest quartile of the 48h over prior-120h volume ratio), the Saturday-Sunday move reverses over the next 48 hours: mean signed return −0.80 % (t −2.91, 473 non-overlapping cases). The reversal is negative in 5 of 6 coins (ETH −1.13 %, LTC −1.18 %, XMR −1.35 %, XRP −1.02 %, BTC −0.43 %) and in 6 of 8 years. Its size is about four times the 0.19 % cost of a trade.
- F2: The reversal is graded by thinness and by move size. Over all 1,890 Sundays, the volume ratio's rank correlates with the signed 48-hour return at rho +0.078 (p 0.0007): heavy weekends continue, thin ones reverse. Among the 1,563 light weekends, a larger move is followed by a lower signed 48-hour return (rho −0.10, p 0.00006). Even inside light weekends, the thinnest quartile reverses (−0.79 %, t −2.54) while the least-thin quartile does not (+0.54 %, t 1.48).
- F6: The book's losses are concentrated in its exposure on Monday, where it holds its positions. 77 of its 116 worst 5 % days are Mondays. Its mean return on days in a position is negative in 2018 (−0.041 %, t −1.49, 594 days) and in 2023 (−0.116 %, t −1.23), which explains the weak Calmar.
