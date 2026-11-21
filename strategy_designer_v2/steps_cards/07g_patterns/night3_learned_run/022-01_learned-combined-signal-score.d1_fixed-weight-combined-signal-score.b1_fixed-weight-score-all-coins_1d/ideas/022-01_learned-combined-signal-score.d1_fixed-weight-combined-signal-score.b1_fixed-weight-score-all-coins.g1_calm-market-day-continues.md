---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 30-day volatility is low compared with its own usual level, the larger its last 1-day return in units of that volatility, the higher its return over the next 5 days, in the same direction as that day's move.
Consequence: In a calm coin, a large up or down day should be followed rather than faded, and a short-reversal bet should be refused there.
Why:
- F1: The 1-day move's effect on the next 5 days changes direction with the coin's volatility level. In the coin's calmest third of 30-day volatility, the negated 1-day component ranks against the 5-day excess return with a t of -5.1, so a rise continues. In its most volatile third the t is +4.8, so a rise reverses. In the middle third it is +1.3. On the full sample the component's t is only 1.7.
- F2: The split holds coin by coin. The rank correlation of the 1-day return with the next 5-day excess return is positive in the calm third for 15 of 19 coins (up to +0.25 on AVAX, +0.24 on ADA, +0.19 on ETH). It is negative in the volatile third for 15 of 19 coins (down to -0.27 on ADA, -0.30 on TRX, -0.68 on TAO over 59 cases).
- F3: The split also holds year by year. The calm-third correlation is positive in 7 of 8 years (+0.05 to +0.33, one year at -0.00). The volatile-third correlation is negative in 5 of 8 years (-0.01 to -0.24, every year from 2020 on except a flat 2024).
- F4: Averaged across coins on each date, the calm continuation keeps a t of 2.69 over 315 independent 5-day dates (1-day move scaled by volatility, times the next 5-day z). At 10 days it fades to t 1.34, and over 3-day moves it is weaker (t 1.84). The graded interaction with the volatility rank has t -1.94 over 414 dates. This is suggestive but marginal after the many angles looked at.
