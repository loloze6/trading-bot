---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back
line: 7.b inconclusive
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise measured in units of its 20-day standard deviation of daily returns is followed by a fall over the next 5 days. The fall grows steeply with that raw number of usual daily moves: rises of one usual move or less are followed by almost nothing, and the rare rises of several usual moves are given back by several percent.
Consequence: A trader would fade a falling coin's bounce in proportion to its raw size in usual daily moves, so that only the rare outsized bounces carry a meaningful short.
Why:
- F1: Step 5's main measure is on the predicted side (+0.62 % unusual 5-day fall per case, t 2.81, 2312 cases). It is inconclusive only because the grading ran backwards. Cases at forecast −10 or below faded 0.63 % less than cases between −2 and −10. In my recount the −5..−2 bucket faded +1.19 % (t 3.33, n 702), against +0.20 % (t 0.43, n 666) for the full −20 bucket.
- F2: The grading inverts because the forecast does not track the bounce's size in raw usual moves. It restandardises the move against its own past 60 values and saturates near 1.6 usual moves. Measured on the raw size (the day's return over its 20-day standard deviation), the cases do follow the idea at the top end. Bounces above 3 usual moves faded +4.77 % over 5 days (t 3.02, n 33), against +0.11 % at 1 to 1.5 moves (t 0.26, n 673) and +1.01 % at 2 to 3 moves (t 1.13, n 224).
- F3: On the full 5-day grid of falling coins, rises above 2 usual moves were followed by an unusual fall of 3.90 % (t 2.79, n 78). On the event study (rises deduplicated per 5-day cell) the fall was 4.60 % (t 3.17, n 58). By contrast, rises of 0 to 1 usual moves were followed by only 0.27 % (t 0.80, n 990), and the correlation of bounce size with the later fade among rises is only 0.086.
