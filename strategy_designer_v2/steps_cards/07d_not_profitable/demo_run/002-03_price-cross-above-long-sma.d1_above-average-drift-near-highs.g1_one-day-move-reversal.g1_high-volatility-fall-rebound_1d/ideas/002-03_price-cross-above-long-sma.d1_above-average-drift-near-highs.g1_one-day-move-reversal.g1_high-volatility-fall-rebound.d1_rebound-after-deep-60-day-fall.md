---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high compared with its own past levels, the larger its one-day fall relative to its usual daily move over the past 20 days, the larger its rise over the next day, and the further the coin has fallen over its past 60 days, the stronger that rebound.
Consequence: A trader would buy sharp falls in turbulent stretches mostly in coins already well down over the past two months, and stay small in coins near their highs, where the falls kept going.
Why:
- F1: The book's gain comes almost entirely from its largest forecasts. The top forecast tercile (mean forecast 13.6, n 613) earned 0.00699 per active bar, while the lower two terciles earned 0.00004 (n 1226) and 0.00041 (n 613). With the book active on only 14.0 % of bars at a mean allocation of 0.247, its mean daily return is only 0.000209, against 0.00118 for holding.
- F2: Most signal bars are small falls that do not rebound. Of 1408 signal bars with a measured fall, 1153 had a vol-scaled fall between -1 and 0, with a next-day excess of 0.00196 (t 1.17) and a gain of 0.00042. Falls between -1.5 and -1 gave 0.01655 (t 3.07, n 163), and falls below -3 gave 0.201 (t 7.74, n 8).
- F3: The rebound sits in coins already deep in a 60-day fall. Signal bars in the lowest 60-day-return quartile (mean -36.6 %, n 215) had a next-day excess of 0.01703 (t 4.60) and a 5-day excess of 0.02186. The other three quartiles had next-day excesses of 0.00002, 0.00315 and 0.00367, all with t below 1.
- F4: The same holds for the 20-day trend. Among the largest forecasts, signal bars after a 20-day fall had a next-day excess of 0.01412 (t 3.80, n 389), against 0.00841 (t 2.04, n 181) after a 20-day rise.
- F6: The Calmar failure comes from one stretch. The deepest fall, -20.7 %, is in w16, with w17 at -14.1 % and w15 at -10.0 %. In w15–w17 the active bars earned 0.000388 each (n 486), against 0.002235 in the other windows (n 1966). The coins there were on average up 5.0 % over 60 days, and the 50 worst bars were held at a mean allocation of 0.66 and forecast 13.5.
