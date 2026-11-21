---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average
line: 7.b inconclusive
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, only while its 60-day return is positive and its close is above its 50-day average, and the further its close stands above that average, the larger the rise.
Consequence: A break of a repeatedly held level is a reason to buy only when the coin already trades well above its 50-day average; a break made from below or near that average, as in the bear phases that carry the book's deepest falls, is a reason to stay out.
Why:
- F1: Step 5's result is on the side the idea predicts but short of the bar: a mean unusual move of +0.70 % over 5 days, t 1.79 on 990 cases. My own recount of the cases, the first positive-forecast bar in each 5-day cell, gives +0.79 % with t 2.05 on 1009 cases. The verdict therefore sits right at the threshold, and how the cases are counted is enough to move it across.
- F2: The mean comes from a few large rises, not from the typical break. The median unusual move over 5 days is -0.95 % and only 44.9 % of cases rise more than the drift. Skew is 1.59 and excess kurtosis 10.1. Trimming 5 % from each tail cuts the mean to +0.24 %, and winsorising at 1 %/99 % gives t 1.94.
- F3: The effect is uneven across coins. ZEC carries most of it, at +4.1 % over 5 days (t 2.65, 141 cases). BTC gives +1.1 % (t 1.84) and ETH +0.7 % (t 0.90). LTC is flat at +0.2 %, and XMR (-0.6 %) and XRP (-0.2 %) are below their drift.
- F6: A longer horizon makes the move larger but not clearer. Strength grows from 0.067 at 5 days to 0.12 at 20 days and 0.14 at 30 days. But the t on each horizon's own non-overlapping grid stays about 2: 2.05 at 5 days (1009 cases), 2.00 at 10 days (675), 2.01 at 20 days (411) and 1.87 at 30 days (304). Changing the horizon gives no clearer answer than adding cases.
- F7: The size easily covers the cost of a trade. The total move of +1.27 % per case is 6.6 times the 0.19 % round trip, and the unusual move alone is 3.6 times it. The book passed every profitability check (Sharpe 1.00 against holding's 0.55). Size is not the problem; the problem is too few independent cases for a fat-tailed move, and the 13 coins outside the default data are available on daily bars.
