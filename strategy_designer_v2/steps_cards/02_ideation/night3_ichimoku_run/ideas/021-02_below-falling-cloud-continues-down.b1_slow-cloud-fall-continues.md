---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down
line: 7.b inconclusive
backtest: 021-02_below-falling-cloud-continues-down_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the more slowly the cloud has fallen over the past 26 days.
Consequence: A coin drifting below a gently falling cloud is a reason to short it, while a coin below a cloud that has collapsed fast is a reason to refuse the short.
Why:
- F2: The grading runs the opposite way to the idea. Against the cloud's 26-day fall speed, the coin's long-side excess 26-day return has a regression slope of +0.0069 (t 2.66, n 156), so the faster the cloud fell, the more the coin rose afterwards. The supporting check's slope on |forecast| is likewise -0.0092.
- F3: The fall the idea predicts shows only where the cloud falls slowly. In the gentlest-fall quartile the long excess is -7.8 % (t -2.36, n 39) and in the next quartile -6.8 % (t -1.95, n 39), versus +7.5 % (t 1.36) and +1.1 % (t 0.24) in the two steepest quartiles. By |forecast| quartile the short excess is +12.3 % (t 4.24, 84 % hits, n 37) in the smallest quartile and -4.0 % (t -1.21, n 41) in the largest.
- F1: The tested result is close to zero and is not a near miss. The short-signed 26-day excess return is +1.51 % per case with t 0.69 over 156 cases, and only 59 % of cases are on the short side. The idea's size is not the problem: the unusual move is 0.071 of the coin's usual move (25.48 %) and 7.8 times the 0.19 % cost of a trade. The effect is simply not consistently one-sided.
