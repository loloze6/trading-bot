---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its 20-day volatility, the higher its return over the next 1 to 2 days.
Consequence: A trader would buy a coin after an unusually large daily fall for a short rebound, sized by how large the fall is against the coin's recent volatility, and refuse to sell into such a fall.
Why:
- F1: The day after a coin's largest falls measured against its 20-day volatility (the lowest tenth of one-day return / 20-day volatility, per coin), its next-day return beats its normal drift by +53 bps (t 3.61, 1422 days); the second-lowest tenth gives +27 bps (t 2.12), and the effect holds in both halves of the windows (w1-12 +50 bps, t 2.60; w13-24 +57 bps, t 2.53). The total move, +66 bps, is about 3.5 times this backtest's 19 bps round trip.
- F2: The rebound is graded on down days only. On days the coin fell, each extra standard deviation of fall adds 32 bps to the next day's excess return (slope t -3.68, 6986 days). On days the coin rose, the slope is +9 bps per standard deviation (t 1.10, 7212 days), indistinguishable from zero.
- F5: The rebound lasts about two days, then fades. Over the next 2 days the largest falls are followed by +54 bps excess (t 2.13, 730 non-overlapping cases); over 3 days, by +60 bps (t 1.57, 446 cases).
