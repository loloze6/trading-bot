---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks
line: 7.b inconclusive
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days (Monday and Tuesday), only while the coin's 30-day hourly volatility is high against its own last 6 months. The larger the weekend gain, the larger the fall.
Consequence: A trader would fade a weekend rise only in turbulent weeks, and stand aside from the fade in calm ones, where the move tends to carry on instead.
Why:
- F1: The main measure is on the predicted side, with a weighted mean unusual 48-hour fall of +1.15 % and t 2.80 over 557 cases. It is inconclusive only because the grading fails: the larger half of abs(forecast) minus the smaller half is -0.08 %. My recomputation agrees, with a mean unusual fall of +0.89 %, t 2.77, n 547.
- F2: Inside the cases the size of the weekend gain does not grade the fall. The Spearman correlation of the weekend gain with the fall is 0.053 (p 0.22), and 0.030 (p 0.50) once the gain is scaled by volatility. Across raw-gain quintiles the fall runs +0.67 %, +0.52 %, +0.66 %, +1.72 %, +0.85 %. Across forecast quintiles it runs +1.24 %, +0.49 %, +0.63 %, -0.04 %, +2.09 %, with no order.
- F3: The effect sits in two years. The fall is +4.91 % (t 3.21, n 51) in 2018 and +2.95 % (t 3.90, n 81) in 2025. Over the six other years it is -0.01 % (t -0.04, n 415), and the per-window means range from -2.45 % to +8.14 %, with a median of +0.63 % over 23 windows.
- F4: The effect is spread unevenly over the coins. LTC (+1.33 %, t 2.01), XMR (+1.06 %, t 1.76), ETH (+1.10 %, t 1.47) and ZEC (+1.47 %, t 1.45) lean the predicted way. BTC goes against it (-0.35 %, t -0.60).
