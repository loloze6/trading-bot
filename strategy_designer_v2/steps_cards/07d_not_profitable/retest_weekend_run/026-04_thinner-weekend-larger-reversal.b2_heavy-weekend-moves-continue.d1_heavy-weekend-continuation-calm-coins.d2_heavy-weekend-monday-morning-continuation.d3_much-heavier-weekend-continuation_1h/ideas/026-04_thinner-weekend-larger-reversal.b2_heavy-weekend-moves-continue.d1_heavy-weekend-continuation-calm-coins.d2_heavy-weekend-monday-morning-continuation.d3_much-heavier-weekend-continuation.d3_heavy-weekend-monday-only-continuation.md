---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation
line: 7.d confirmed, not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday move made on weekend volume a multiple of its mean over the preceding five weekdays continues in the same direction over the first 12 hours of Monday only as far as the weekend volume ranks high among the coin's own past weekends, the continuation fading entirely by Monday afternoon.
Consequence: Put the whole position on the heaviest weekends and close it after Monday's first 12 hours, instead of carrying small leftover positions for days, where they lose after fees.
Why:
- F1: The continuation lives only in the heaviest-volume weekends. Ranking Sunday 23:00 cases by the weekend-to-weekday volume ratio, the top decile's signed 12-hour excess return is +0.93 % (t 3.03, 229 cases) and the ninth decile's is +0.45 % (t 1.67, 228 cases), while deciles 0–7 lie between −0.20 % and +0.17 % with every |t| below 0.9; across all Sundays the signed 12-hour continuation is only +0.09 % (t 1.22, 2286 cases).
- F3: The book loses its gain in positions it keeps long after Monday morning. The quarter of trades with the smallest entry |forecast| (mean 3.1) is held 230 hours on average and nets −0.21 % per trade (171 trades), while the two largest quarters are held about 8 hours and net +0.38 % and +0.37 %; this lingering exposure, about 10–18 % of cases still held 12 to 48 hours later, dilutes the mean daily return on days in a position to 0.047 %, under the 0.05 % rule.
- F5: Within the heaviest-volume fifth, the largest move tercile continues by +1.13 % over 12 hours (t 2.91, 153 cases) against +0.43 % and +0.49 % (t ≈ 1.4) for the smaller two, so the move's size grades the effect only at its top.
- F7: The book's falls are concentrated in the Monday trade. 32 of the 40 worst coin-days fall on Monday (sum −115.7 %), mostly XMR and ZEC (11 each). Monday carries the whole gain (sum of daily returns +1.42), Tuesday to Sunday together sum −0.27, and the maximum drawdown reaches 6.4 % against a yearly return of +2.3 % (Calmar 0.36). The heavy-volume effect is uneven by year: 12-hour excess of +3.16 % in 2022, −0.38 % in 2018 and −0.26 % in 2023.
