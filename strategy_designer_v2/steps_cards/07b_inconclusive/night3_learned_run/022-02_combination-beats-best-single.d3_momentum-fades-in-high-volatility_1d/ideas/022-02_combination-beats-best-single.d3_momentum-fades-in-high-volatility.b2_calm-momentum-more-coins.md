---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return, the higher its return over the next 20 days, the more so the lower its 30-day volatility is against its own past.
Consequence: Momentum bets held for weeks should be sized up in calm or ordinary volatility and cut back when the coin is at its most volatile.
Why:
- F4: The effect is mixed over time. It is negative in w1-6 at every horizon (t -2.3 at 20 days, -1.7 at 5 and at 10 days) and positive in later windows: w13-18 at 5 days t 2.7, w19-24 at 10 days t 2.7 and at 20 days t 1.7.
- F6: The 20-day result is positive but weak (mean 0.0066, t 0.57) on 827 cases from 6 coins. The rise in t at shorter horizons comes from more independent cases and a cleaner move, which points to too little data at 20 days rather than no effect.
