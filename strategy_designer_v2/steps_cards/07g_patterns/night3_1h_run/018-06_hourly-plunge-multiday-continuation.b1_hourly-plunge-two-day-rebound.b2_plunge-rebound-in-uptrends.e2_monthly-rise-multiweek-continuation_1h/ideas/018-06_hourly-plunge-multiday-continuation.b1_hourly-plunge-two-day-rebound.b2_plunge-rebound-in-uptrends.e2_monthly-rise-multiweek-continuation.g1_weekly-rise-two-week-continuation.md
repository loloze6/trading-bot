---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 7-day return predicts its next 2 weeks: the larger the rise over its past 7 days, measured against its usual 7-day move, the further it rises over the next 2 weeks above its usual 2-week drift.
Consequence: A strong week is a reason to be long for the following two weeks, more strongly as the week's rise is larger, rather than waiting for a month-long rise to show.
Why:
- F1: Over a coin's past 7 days, the larger its return, the larger its unusual move over the next 2 weeks. Pooled slope of 2-week excess return on 7-day return is 0.179 (t 3.71, 1004 independent cells). For the 7-day move in units of usual volatility the slope is 0.023 (t 3.58). Over the next 7 days the slope is 0.087 (t 2.83). The slope is positive on all 6 coins (0.04 to 0.29) but strong only on ZEC (t 2.20), and in years it is positive in 5 of 8 (t 2.01 in 2020, 2.65 in 2025) and negative in 2021 to 2023.
- F2: Sorted into quintiles per coin, the 7-day return separates the next 2 weeks much more than the tested 30-day return does. By 7-day quintile, the 2-week excess runs from −3.17 % (t −2.87, 203 cells) at the bottom to +5.29 % (t 2.14, 203 cells) at the top, a total move of +6.87 % against a cost of 0.19 %. By 30-day quintile, no quintile's excess goes past ±1.6 % (all |t| ≤ 1.13). The 30-day slope over 2 weeks is weaker than the 7-day one (14-day return slope t 1.64).
- F5: The tested forecast is almost always saturated, so it barely grades. Of 568 positive grid cells, 502 have a forecast above 2.5. Their 2-week excess is +1.38 % (t 1.28). Trades entered in the top forecast quartile have a median net gain of +3.6 %, against −0.55 % in the bottom quartile, but their means are equal (12.7 % each).
