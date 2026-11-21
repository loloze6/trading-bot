---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 20-day volatility is high, the larger its one-day fall relative to that volatility, the higher its return over the next day. The higher the volatility, the larger the rebound.
Consequence: A trader would concentrate short-term rebound buying in a coin's turbulent periods, where the move after a large fall is several times the cost of a trade.
Why:
- F1: The day after a coin's largest falls measured against its 20-day volatility (the lowest tenth of one-day return / 20-day volatility, per coin), its next-day return beats its normal drift by +53 bps (t 3.61, 1422 days); the second-lowest tenth gives +27 bps (t 2.12), and the effect holds in both halves of the windows (w1-12 +50 bps, t 2.60; w13-24 +57 bps, t 2.53). The total move, +66 bps, is about 3.5 times this backtest's 19 bps round trip.
- F2: The rebound is graded on down days only. On days the coin fell, each extra standard deviation of fall adds 32 bps to the next day's excess return (slope t -3.68, 6986 days). On days the coin rose, the slope is +9 bps per standard deviation (t 1.10, 7212 days), indistinguishable from zero.
- F3: The rebound after the largest falls grows with the level of volatility. By tercile of 20-day volatility, the next-day excess return is -2 bps (t -0.13), +30 bps (t 1.37) and +132 bps (t 3.89), with 474 days each.
