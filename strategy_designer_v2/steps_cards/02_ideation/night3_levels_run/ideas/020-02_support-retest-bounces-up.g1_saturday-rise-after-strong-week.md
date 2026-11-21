---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up
line: 7.g patterns
backtest: 020-02_support-retest-bounces-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Over the day that starts at Friday's close (UTC), a coin tends to rise, and the larger its own 5-day return up to Friday's close, the larger that rise.
Consequence: A trader would hold the coin over Saturday, and hold more of it after a strong week; a rejection is a reason not to give weekend long exposure any special weight.
Why:
- F1: Saturday (UTC) is the coin's best day, and it holds across coins, windows and years. Averaged over the 6 coins, the mean Saturday return is +0.454 % (t 3.04, 414 days) against +0.062 % on the other days (Welch t 2.29). Every coin's Saturday mean is above its other days' mean (t from 0.34 on BTC to 2.67 on LTC), and the share of up Saturdays is 53 to 57 % against 49 to 52 % on other days. The Saturday-minus-other difference is positive in 19 of 24 windows (t 2.30 over windows) and in 7 of 8 years, 2023 being the exception (t -1.24).
- F2: The Saturday rise is graded. Across coins pooled, a coin's return over Saturday rises with its own return over the 5 days before it (Spearman 0.078, p 0.0001, 2382 Saturdays). I did not measure the same correlation on other weekdays, so this may be ordinary short-term continuation rather than something specific to Saturday.
- F3: The Saturday move is large against this backtest's cost of a trade. The mean Saturday total move (+0.45 %) is 2.4 times the 0.19 % round trip, and its excess over the other days (+0.39 %) is about 2 times it. I looked at 7 weekdays and about 10 bar features, so the pooled t of 3.04 only just survives a correction for that many looks.
- F4: Saturday is also the quietest day. Its mean absolute return is 2.46 % against 3.26 to 3.71 % from Monday to Friday, and 2.78 % on Sunday, so the rise comes with low risk per day.
