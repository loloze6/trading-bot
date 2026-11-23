---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Sunday 24-hour return, measured in its usual 30-day move, is reversed over Monday and Tuesday by more the higher the coin's current 30-day usual move stands against its own usual level of the past three months.
Consequence: A trader would size the Monday bet against Sunday's move by how volatile the coin is against its own recent norm, and refuse it when volatility is low.
Why:
- F3: The tested Monday effect sits almost wholly in high volatility. The Monday 48h slope is -0.0119 (t -4.8, 598 cases) in the high vol tercile, -0.0021 (t -0.9) in the middle and +0.0033 (t 1.3) in the low tercile. By coin it is only t -0.7 to -2.0 (about 375 cases each), and by year only 2019, 2020 and 2025 have t below -2.
- F2: That reversal grows with volatility. When the coin's 30-day usual move is measured against its own median over about 83 days, the daily-grid slope is +0.0004 (t 0.9) in the low tercile, -0.0023 (t -4.5) in the middle and -0.0032 (t -6.3) in the high tercile. The z × vol-ratio interaction is -0.0029 (t -3.6). In the high-vol tercile the next-24h return is +0.66 % after the lowest third of 24h moves and -0.25 % after the highest third, a spread of about 0.9 %. That spread is 4.8 times the 0.19 % cost of a trade. The high-vol slope is negative in all 8 years (t from -0.9 to -4.7) and in every coin, with t below -2 everywhere except XRP (t -1.1).
- F5: The book earns on Mondays only. Its mean daily return is +0.095 % on Mondays, +0.022 % on Tuesdays and between -0.039 % and +0.003 % on the other five days (about 2480 coin-days each). This fits a position opened at Monday 00:00 that carries little after its first day.
