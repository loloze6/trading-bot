---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall measured in units of its own 30-day daily volatility, the larger its rebound over the next 3 days.
Consequence: A trader would buy a coin's sharp volatility-scaled sell-off, sized up with the depth of the fall, rather than treat a collapse as the start of further decline.
Why:
- F1: The 3-day return after a sharp one-day fall rises with the fall's size measured against the coin's own volatility. On the non-overlapping 3-day grid, a daily return below −2 of its trailing 30-day standard deviation is followed by +1.60% over holding (t 2.37, n 124). A return between −2 and −1 standard deviations is followed by +0.87% (t 1.47, n 337). A return between −1 and 0 is followed by −0.06% (n 1423). On all days the same ordering holds: +2.19% (t 4.04, n 370), then +0.71% (t 2.85, n 1389), then +0.24% after ordinary days.
- F2: That rebound after falls beyond 1 standard deviation is carried by the smaller coins. It is +1.12% to +2.26% in LTC, XMR, XRP and ZEC (71 to 82 cases each) and slightly negative in BTC (−0.39%) and ETH (−0.69%). It is positive in 5 of 8 years, with 2021 the largest at +6.01%.
- F7: Strength alone did not follow through. Daily moves above 2 standard deviations were followed by only +0.49% over 3 days (t 0.86, n 473), against +2.19% after falls of the same size.
