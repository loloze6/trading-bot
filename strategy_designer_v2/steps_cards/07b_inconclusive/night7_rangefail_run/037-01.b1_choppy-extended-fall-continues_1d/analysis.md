---
line: 7.b inconclusive
backtest: 037-01.b1_choppy-extended-fall-continues_1d
idea tested: 037-01.b1_choppy-extended-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3528 USD
---
## Findings
- **F1:** The main measure is on the predicted side but small: the unusual 5-day move per short case is +0.63 % (t 1.36, 994 cases on 567 days, strength 0.044). On the folds B and C shown here, the step-5 cases give +2.0 % (t 2.09, 258 cases, 185 days), but one window carries it: w16 alone gives +27.4 % (t 6.9, 9 cases), and without w16 the mean drops to +1.08 % (t 1.30, 249 cases).
- **F2:** The effect varies widely across windows and coins. Five of 12 windows are negative (w8 -1.4 %, w11 -6.3 % with t -2.81, w13 -5.8 %, w17 -2.1 %), and ZEC (-3.3 %) and TRX (-2.9 %) run against it while DOGE (+14.9 %, t 4.27) and BTC (+3.8 %, t 2.39) carry it. This mixture is why the overall t stays between -2 and 2.
- **F3:** The grading the idea claims is not in the data. By terciles of the 5-day fall in swing units, the unusual 5-day move is +1.5 %, +2.0 % and +2.5 %, each with t under 1.5. By forecast terciles it is +0.5 %, +4.2 % and +1.3 %. The slope on the forecast's size is +0.0004 here and -0.0004 in step 5, so the supporting check fails.
- **F4:** The effect sits in agitated markets.
- **F5:** The continuation builds past the plan's 5-day horizon. On the step-5 cases, the unusual move is +0.5 % at 1 day, +1.2 % at 3, +2.0 % at 5, +2.5 % at 10 and +4.6 % at 20 days (t 0.80, 1.63, 2.09, 1.87, 2.18).
- **F6:** The coins' own falls in these periods absorb the unusual move. The normal drift in the short direction is -0.79 % per 5 days, so the total move is -0.16 % per case, below the 0.22 % cost of a trade. The total 5-day move on the B and C cases is +0.7 % (t 0.76). Only a larger unusual move, like the +6.6 % to +9.2 % of the agitated cases, clears that cost.

## Ideas
- `037-01.b1.b1_agitated-chop-falls-continue` (from F4, F5, F1, F2, F6): In a choppy, agitated market, the more of its own 20-day daily swings a coin's 5-day fall spans, the more the coin falls over the next 10 days, only while its 20-day return is also a fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
