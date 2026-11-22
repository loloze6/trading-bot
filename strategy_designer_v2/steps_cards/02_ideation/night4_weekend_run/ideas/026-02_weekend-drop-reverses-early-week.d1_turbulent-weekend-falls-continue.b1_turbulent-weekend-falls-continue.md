---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue
line: 7.b inconclusive
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin falls over the weekend (Saturday 00:00 to Monday 00:00 UTC), it keeps falling over Monday and Tuesday. The fall is larger the more volatile the weekend's hours were compared with the coin's previous week, graded by that volatility comparison alone and not by the size of the weekend's fall.
Consequence: A trader should refuse to buy a weekend dip the more turbulent the weekend's hourly trading was against the prior week, and may lean short for the next two days in proportion to that turbulence.
Why:
- F1: The test's main measure is on the side the idea predicts, with t 2.28 over 759 cases. It stays inconclusive only because the supporting check fails: the upper |forecast| half earns 0.11 % less short excess than the lower half. My quartiles of the cases show no grading either: 0.97 % (t 1.66), 0.00 %, 0.66 %, 0.20 % from smallest to largest |forecast|.
- F2: The forecast multiplies two parts that grade in opposite directions. The weekend's fall size grades against continuation:
- F3: The other part, the weekend's hourly volatility against the prior week, grades the way the idea predicts:
- F4: The vol-ratio grading holds in both halves of the data, with the top-quartile short excess at +0.91 % (t 1.28) in 2018–2021 and +1.64 % (t 2.35) in 2022–2025. It is positive in all six coins (0.29 % for ZEC to 2.10 % for XRP). It is not stable by year: 2019 −0.54 %, 2020 −0.35 % and 2025 −1.56 % against 2022 +4.14 % and 2024 +3.76 % (t 4.73).
- F6: The 48-hour horizon is where the effect shows. On the cases, the short excess is 0.09 % (t 0.39) at 24 hours, 0.46 % (t 1.51) at 48 hours and 0.36 % (t 0.94) at 72 hours. The plan's own size, an unusual move of 0.68 % per case, is 3.5 times the 0.19 % cost of a trade.
