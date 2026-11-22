---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the past 7 days is high, its 24-hour return is followed by a move in the opposite direction over the next 24 hours, larger the larger the past 24-hour move and the higher that volatility, and largest after falls.
Consequence: In turbulent stretches, a trader would fade a coin's large one-day moves, sell-offs above all, for a day, and refuse that trade when markets are calm.
Why:
- F1: Volatility sets the sign of the daily reversal. In each coin's highest third of 7-day hourly volatility, a 24-hour return to 00:00 UTC is followed by an opposite unusual move over the next 24 hours, on a non-overlapping daily grid. The strength is 0.133 for BTC (t 3.13, 948 cases), 0.133 for ETH (t 3.23), 0.150 for LTC (t 3.71) and 0.189 for XMR (t 4.32), with XRP 0.083 (t 1.92) and ZEC 0.052 (t 1.20). The unusual move is 0.31 % to 0.88 % per case, 1.6 to 4.6 times the 0.19 % trade cost. In the lowest third the strength is about zero or slightly negative (BTC −0.053, t −2.38).
- F2: Inside the high-volatility third the reversal grows with the size of the past move, most strongly after falls. By quintile of the past 24-hour return, the next 24 hours' unusual move is +1.01 % after a mean past move of −7.2 % (t 6.02, n 1654) and −0.47 % after +7.7 % (t −2.81, n 1603). The middle quintiles are near zero.
- F3: The high-volatility 24-hour reversal holds in 7 of 8 years. Its strength is 0.168 in 2018, 0.092 in 2019, 0.162 in 2020, 0.124 in 2021, 0.165 in 2022, 0.172 in 2023 and 0.081 in 2024 (t 1.6 to 4.6). 2025 is the exception at −0.031 (t −0.57, n 501).
- F4: The weekend gets no special reversal. The 48-hour reversal score ending Monday 00:00 is 0.013 (t 0.47, n 2387), against 0.037 (t 1.13) for Wednesday and −0.067 (t −2.13) for Friday. The 24-hour score ending Monday, 0.082 (t 2.77), is no larger than on Wednesday (0.102), Thursday (0.135) or Friday (0.148).
