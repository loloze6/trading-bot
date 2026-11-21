---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds
line: 7.b inconclusive
backtest: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes far below a price where it turned up several times in the past 90 days, it tends to rise over the next 3 days, and the rise grows with the close's depth under that level times the number of times the level held, so that the deepest breaks of the most-touched levels rise the most.
Consequence: A very deep break of a much-defended support is a reason to buy the coin for about three days, with a move per case several times a trade's cost, while a shallow break is a reason not to buy it.
Why:
- F2: Ranked on the raw depth × touches value instead, the 5-day unusual move rises with the situation. Decile 0 is -0.21 %, deciles 1–4 are -0.78 % to -1.38 % (decile 2: t -2.34), decile 8 is -0.01 %, and the top decile is +1.97 % (t 2.32, 235 cases), with a total move of +2.57 % and a strength of 0.17. The top raw fifth is +0.98 % (t 1.81, 470 cases), total +1.58 %, strength 0.09.
- F3: Shallow breaks of support keep falling rather than rebounding. In raw quintile 1 (median 5.2) the 5-day unusual move is -1.12 % (t -2.67, 465 cases) and the 10-day one is -1.60 % (t -2.50, 443 cases). Over all positive-forecast cases the 5-day unusual move is -0.30 % (t -1.42, 2346 cases).
- F5: The rebound shows most clearly over about 3 days. For the top raw fifth it is +0.96 % at 3 days (t 2.35, 473 cases, strength 0.12), +0.98 % at 5 days (t 1.81) and +1.21 % at 10 days (t 1.59, 443 cases). The tested forecast-top fifth gives only t 0.92, 0.44 and 0.86 at the same horizons.
- F6: Against the backtest's 0.19 % cost per buy and sell, the deepest breaks clear it and the whole set does not. The top raw fifth's total move (+1.58 %) is about 8 times the cost and its unusual move (+0.98 %) about 5 times. The tested idea's whole set has an unusual move of -0.19 % per case (-1.0 times the cost), consistent with the earlier finding that no idea below cost pays.
