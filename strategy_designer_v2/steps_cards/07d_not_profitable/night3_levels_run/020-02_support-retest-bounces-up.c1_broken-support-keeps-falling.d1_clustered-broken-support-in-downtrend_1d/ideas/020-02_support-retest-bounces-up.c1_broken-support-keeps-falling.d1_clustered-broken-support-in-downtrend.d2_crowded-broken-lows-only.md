---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits below its 50-day average price, it tends to fall over the next 5 days by more the more of its past-90-day turning-up lows are clustered within a few percent above the close. The fall grows with the count of such lows faster than in proportion, so that a single distant low above the close is followed by a rise over the next 5 days.
Consequence: A trader below the 50-day average should be short in proportion to the crowding of broken lows overhead, and should lean long when only one far low sits above the close.
Why:
- F1: The fall is graded by the cluster and the book loses on the weak end of it. On active bars, split into quintiles of the raw cluster reading, the unusual long-side 5-day move runs +0.81 % (351 cases, t 1.12), -0.33 %, -0.38 %, -0.78 %, -0.89 % (351 cases, t -2.13). The book was still short in the lowest quintile, at a mean allocation of -0.22, so it bet on a fall where the coin rose more than usual.
- F2: Only the largest clusters cover a trade, and only narrowly. The top quintile's unusual fall of 0.89 % per case is about 0.08 of the coin's usual 5-day move (10.6 %) and 4.7 times the 0.19 % cost. Against the coins' rising drift of about +0.59 % per 5 days, its total short move is only about +0.30 %, 1.6 times the cost. Over all 1355 cases the total move is -0.40 %, -2.1 times the cost.
- F6: Most trades lose and a few large wins carry the mean. The book made 3269 short trades, with a median holding of 5 days and a mean of 11.3. The mean gross gain per trade was +0.23 % and the mean net gain +0.13 % after about 0.24 % commission, but the median trade lost 1.55 % net.
- F7: Step 5's supporting check had no cases in its larger half. 41 % of active forecasts sit at the cap (|forecast| ≥ 19, median -7.2). This leaves the graded half-split of the verdict empty, while the raw reading itself is graded (F1).
