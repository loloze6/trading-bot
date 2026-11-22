---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong
line: 7.b inconclusive
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume above its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The larger that hour's rise measured in typical 30-day hourly moves, the larger the further rise.
Consequence: A trader would buy after an hourly rise of several typical moves and hold for about a day, leaning more on the larger rises, and refuse to short such hours.
Why:
- F1: The test's cases are diluted by modest hours. Its forecast ≥ 2 cases give +0.05 % unusual over 24 hours (t 0.82, 5014 cases), and their forecast quartiles are flat (+0.04 %, +0.17 %, −0.07 %, +0.05 %). The first hour in each 24-hour cell that rises at least 2 typical 30-day hourly moves gives +0.30 % (t 2.97, 1988 cases; total +0.45 %), and 1975 of those 1988 hours carry a forecast ≥ 2. The roughly 3000 other test cases are therefore smaller rises that contribute about nothing.
- F2: Among those large rises, the 24-hour unusual move grows with the size of the rise. Rises of 2–3 typical moves give +0.12 % (t 1.02, n 1315), 3–5 give +0.69 % (t 3.34, n 526) and above 5 give +0.54 % (t 1.12, n 147). The top quartile of rise × relative volume gives +0.64 % (t 2.66) against +0.08 % (t 0.45) for the bottom quartile.
- F3: Volume adds only a weak, unclean grading. By relative volume the 24-hour unusual move is +0.20 % below 1× (n 204), +0.12 % at 1–2× (n 592), +0.40 % at 2–4× (t 2.31, n 713) and +0.43 % above 4× (t 1.81, n 479). The top half of rise × volume minus the bottom half is +0.18 % (Welch t 0.87).
- F4: The brief's 2–6 hour horizon shows no continuation, and the move appears only at a day.
- F6: The large-rise continuation over 24 hours is positive in every year from 2018 to 2025, between +0.02 % and +0.58 % (best t 1.96 in 2023, 1.73 in 2020). It is stronger in ETH (+0.48 %, t 2.95, n 1005) than in BTC (+0.13 %, t 1.01, n 983).
- F7: The test's cases do not cover the cost of a trade beyond holding, but the large rises do.
