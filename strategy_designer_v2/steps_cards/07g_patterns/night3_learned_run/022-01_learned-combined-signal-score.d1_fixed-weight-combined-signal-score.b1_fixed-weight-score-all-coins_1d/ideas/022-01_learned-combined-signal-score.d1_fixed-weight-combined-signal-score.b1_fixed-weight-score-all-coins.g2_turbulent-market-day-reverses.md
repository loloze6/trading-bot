---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 30-day volatility is high compared with its own usual level, the larger its last 1-day return in units of that volatility, the more its return over the next 1 day goes the opposite way.
Consequence: In a turbulent coin, a large day is a reason to expect a next-day pullback, and a reason to refuse chasing it.
Why:
- F1: The 1-day move's effect on the next 5 days changes direction with the coin's volatility level. In the coin's calmest third of 30-day volatility, the negated 1-day component ranks against the 5-day excess return with a t of -5.1, so a rise continues. In its most volatile third the t is +4.8, so a rise reverses. In the middle third it is +1.3. On the full sample the component's t is only 1.7.
- F2: The split holds coin by coin. The rank correlation of the 1-day return with the next 5-day excess return is positive in the calm third for 15 of 19 coins (up to +0.25 on AVAX, +0.24 on ADA, +0.19 on ETH). It is negative in the volatile third for 15 of 19 coins (down to -0.27 on ADA, -0.30 on TRX, -0.68 on TAO over 59 cases).
- F5: In the volatile third, the reversal shows mostly on the next day: date-clustered t of -2.34 over 2029 dates at 1 day, against -0.22 at 5 days. A 1-day move is unlikely to cover the 0.22 % round trip.
