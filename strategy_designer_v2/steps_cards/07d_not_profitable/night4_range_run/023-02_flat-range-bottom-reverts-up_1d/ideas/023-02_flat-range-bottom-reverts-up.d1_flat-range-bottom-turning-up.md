---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the larger its rise over the past 10 days, the more it rises over the next 5 days.
Consequence: In a flat market, buy a dip below the middle only once it has already turned up, and size the trade by the strength of that turn, not by the depth of the dip.
Why:
- F1: The tested effect is not in the data: in flat coins (30-day net move ≤ 0.3 of the range) with the close below the middle, the 5-day excess return is -0.61 % per case (926 cases, strength -0.057), with a total move of -0.02 % against a 0.19 % trade cost; the step-5 mean is -0.50 % (t -1.25, 628 cases).
- F2: Distance below the middle does not grade the rebound: across flat-regime distance sextiles the excess return runs -0.22 %, -0.73 %, -0.20 %, +0.97 %, -0.79 %, -1.20 % (n 62 to 220, all |t| < 1.5); trending coins show the same lack of order, so reversion is no larger in flat coins.
- F3: Within flat-below-middle cases, the coin's recent path decides the next 5 days. By 10-day return tercile the excess is -1.47 % (t -1.91, n 147), then -0.88 % (t -1.46), then +1.48 % (t 1.80), with total moves of -0.85 %, -0.26 % and +2.09 %. By 5-day return quintile it is -1.25 %, -1.74 % (t -2.19), -0.13 %, +1.65 % and +0.03 % (n 88 each).
- F4: Cases still falling into the bottom keep falling: a negative 5-day return gives -0.74 % excess at both depths (deep n 172, shallow n 128). A positive 5-day return gives +1.11 % when shallow (n 92) and -0.13 % when deep (n 48).
- F6: The loss is concentrated in years of falling-into-the-bottom cases: flat-below excess was -1.5 % to -1.8 % per case in each of 2018 to 2021 (n 40 to 54), against +0.7 %, +1.9 % and +2.2 % in 2022 to 2024 (t up to 1.97).
