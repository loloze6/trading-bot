---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour volatility is high relative to its 30-day volatility, the larger its 1-hour fall relative to its 24-hour volatility, the more its return over the next 24 hours rises, at any hour of the day; this holds for sharp down-hours, the side that carries the reversal, and not for sharp up-hours.
Consequence: A trader would buy sharp hourly drops while volatility is elevated against its monthly norm and hold for a day, and would not short sharp hourly rises, whose fade loses.
Why:
- F1: The two sides of the book diverge sharply. Before costs, the short positions lost a summed −1513 % over 120 283 bars (−1.26 bp a bar), while the long positions gained +669 % over 118 325 bars (+0.57 bp a bar). Short trades averaged −3.53 % gross and −3.63 % net over 5182 trades; long trades averaged +0.92 % gross and +0.82 % net over 6255 trades, held a median of 42 hours. The negative Sharpe (−0.87) and Calmar (−0.34) come from the short side.
- F2: On the non-overlapping 24-bar grid with the 24/720-bar volatility ratio above 1, only the long side carries the effect. After a 1-hour return between −1 and −0.5 of its 24-hour volatility, the excess 24-hour return is +0.77 % (t 3.43, 717 cases). Between −1.5 and −1 it is +0.83 % (t 2.58, 341 cases), and between −3 and −2 it is +1.36 % (t 2.34, 119 cases). The pooled fade after a down-hour beyond 1.5 is +0.75 % (t 2.14, 323 cases). The same fade after an up-hour beyond 1.5 is +0.07 % (t 0.20, 339 cases), and no short bucket reaches t 1.2.
- F3: The volatility condition and the down-hour are each needed; neither earns on its own. With the ratio above 1 but no down-hour (z above −0.5), the excess 24-hour return is +0.07 % (t 0.75, 3612 cases). A down-hour beyond 1 with the ratio at or below 1 earns +0.03 % (t 0.27, 1704 cases). The long effect sits where the tested idea's situation says it should.
- F4: The long move per case (+0.77 % excess over 24 hours after a down-hour between −1 and −0.5, F2) is about 4 times the 0.19 % cost of a trade. The idea's size over both sides (+0.07 %, 0.4 times the cost) is small because it mixes this long move with a short side that earns nothing.
- F5: The long side of the idea holds across years. Among grid cases with the ratio above 1 and z below −0.5, the excess 24-hour return is positive in 7 of 8 years (for example 2021 +2.14 %, t 3.02; 2023 +0.56 %, t 2.56; 2025 +0.72 %, t 2.19). Only 2022 is negative (−0.15 %, t −0.30).
- F6: Trading costs are almost as large as the long side's gain. The book's turnover sums to 7217 units of allocation, which at 0.095 % a side costs about 686 %, close to the long side's +669 % gross gain. Removing the short side (F1) removes about half of this turnover and all of its −1513 % loss.
