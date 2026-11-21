---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 90-day return is negative, the higher its 20-day volatility, the higher its return over the next 5 days; quiet stretches inside a fall keep falling and turbulent ones do not.
Consequence: Inside a coin's 90-day fall, a trader refuses longs while the coin is calm and refuses shorts while its daily moves are large.
Why:
- F1: Inside 90-day falls (the `unknown` regime, flat in this book), the coin's 20-day volatility is graded against its next 5-day return net of drift: slope +0.063 of a usual move per standard deviation of volatility, t 2.54, on 1304 non-overlapping cases. By quintile of each coin's volatility the 5-day unusual move rises steadily: -1.00 %, -0.44 %, -0.35 %, +0.09 %, +0.19 %. That is a 1.2 % spread against a 0.19 % round trip. The slope is positive on all 6 coins (0.02 to 0.11, none with t above 1.6 alone) but carried by windows w13-24 (t 2.84, n 586); on w1-12 it is -0.47. Given the more than 20 angles looked at, this sits at the edge of chance.
- F4: Inside 90-day falls, every momentum measure turns to a weak reversal: 1-day return slope -0.047 (t -2.01), 20-day return -0.039 (t -1.65). The 20-day reversal holds only on w1-12 (t -2.97, n 718) and not on w13-24 (t +0.46). It does not carry forward.
