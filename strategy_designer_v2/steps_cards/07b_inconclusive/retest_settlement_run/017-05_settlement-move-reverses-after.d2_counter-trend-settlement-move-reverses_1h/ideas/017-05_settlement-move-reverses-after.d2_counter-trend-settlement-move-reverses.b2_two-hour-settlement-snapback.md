---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses
line: 7.b inconclusive
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 2 hours after each funding settlement time runs opposite to the return over the 2 hours before it when that pre-move runs against the coin's 24-hour trend, and the stronger the 24-hour trend, the larger the move back.
Consequence: A trader expecting a counter-trend dip or rally into settlement to be retraced should expect it within about 2 hours, sized by the 24-hour trend, rather than over the full 8 hours to the next settlement.
Why:
- F1: The tested move is clear over the first 2 hours after settlement and fades by 8 hours: on the settlement cases signed by the 24-hour trend, the raw return has t 4.03 at 1 hour, 5.67 at 2 hours, 3.04 at 4 hours and only 1.41 at 8 hours (the plan's horizon), then turns to t -2.69 at 16 hours (21,059 cases). The plan's 8-hour test measured the idea where most of the move has already been given back.
- F2: Over 2 hours the counter-trend pre-move reverses at the settlements, with a strength of 0.039 of a usual 2-hour move against 0.017 at other hours (excess +0.056 % against +0.025 %). At the 8-hour horizon the strength is 0.0078 against 0.0021, near the 0.007 the verdict gives.
- F3: Over 2 hours the move grows with the 24-hour trend, as the idea says, but over 8 hours it does not. By quintile of the trend's size the 2-hour excess rises from -0.003 % (t -0.19) to +0.080 % (t 3.66) and +0.139 % (t 4.33), with a slope of 0.0079. The 8-hour quintiles are flat and noisy: +0.005 %, +0.042 %, -0.013 %, +0.031 %, +0.065 %, all with |t| ≤ 1.24.
- F5: Even at 2 hours the effect is not specific to the settlement clock times, and it is missing at one of them. The 08:00 settlement shows -0.017 % (t -1.04), while the hours without settlement next to the other two are as strong or stronger: 22:00 +0.103 % (t 6.64), 15:00 +0.093 % (t 4.63), 01:00 +0.093 % (t 5.83).
- F6: The 2-hour reversal is broad across coins and years but not uniform. It is positive in all six coins, with t from 0.65 (XMR) to 3.44 (ZEC), and in seven of eight years. It is absent in 2022 (-0.030 %, t -1.26) and 2023 (-0.004 %, t -0.26).
- F8: The size is far below the cost of a trade at either horizon. The 8-hour total move is +0.02 % per case and the 2-hour excess about +0.056 %, against 0.19 % for a buy and a sell. Neither horizon could make the book pay as it is; the book's Sharpe was -0.83.
