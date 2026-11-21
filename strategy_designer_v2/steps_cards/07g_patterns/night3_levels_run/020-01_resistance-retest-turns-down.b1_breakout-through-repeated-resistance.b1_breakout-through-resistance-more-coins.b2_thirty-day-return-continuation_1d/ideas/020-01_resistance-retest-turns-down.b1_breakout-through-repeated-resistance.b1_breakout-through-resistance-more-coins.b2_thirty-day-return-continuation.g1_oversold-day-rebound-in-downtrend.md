---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation
line: 7.g patterns
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is negative, the larger its fall over the last day relative to its usual daily move, the larger its rise over the next 3 days.
Consequence: A sharp one-day drop inside a month-long decline is a reason to buy the coin for the following few days, more so the sharper the drop, and a reason not to short it.
Why:
- F1: A coin's large down day is followed by a rebound, graded by the size of the fall. On the daily grid (30522 one-day cases), the 1-day excess return has a slope of -0.00331 per usual daily move of the day's fall (t -6.37), and up days have no slope (t 0.16). Over 3 days the down-day slope is -0.00707 (t -4.73, 10024 cases). Over 10 days it is -0.01245 (t -2.24, 2680 cases).
- F2: The rebound after a fall shows in almost every coin and is large enough to trade. The down-day slope is negative in 15 of 19 coins over 1 day and 16 of 19 over 3 days. After falls beyond one usual daily move, the next 3 days give an unusual move of +0.61 % and a total move of +1.08 % per case (strength 0.061, t 2.05, 1193 cases), against a round-trip cost of 0.22 %, so 2.8 to 4.9 times the cost. Over the next day the unusual move is +0.33 % (strength 0.064, t 3.43, 3702 cases).
- F3: The rebound after a fall sits mainly where the 30-day forecast is negative, and mainly in the later windows. Over 3 days the down-day slope is -0.00683 (t -3.85, 2610 cases) when the forecast is negative and -0.00026 (t -0.06, 2195 cases) when it is positive. Over 1 day it is -0.00338 (t -5.17) against -0.00209 (t -1.43). By half, the slope is t -5.40 in windows w13 to w24 and t -1.05 in w1 to w12 (1 day), so it is not stable through time.
- F5: The short side does not pay, because the deepest 30-day falls do not continue. Short trades earn -2.01 % gross on average, with a win share of 0.375 over 6331 trades, against +14.36 % for long trades (median -0.58 %). Among negative forecasts, the deepest quartile (-20 to -13) has a 10-day excess return of +0.64 % (t 0.91), while the two middle quartiles have -2.99 % (t -3.76) and -2.64 % (t -3.39).
