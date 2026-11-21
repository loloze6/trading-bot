---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day rise compared with its 30-day volatility, the higher its return over the next 5 days.
Consequence: A trader would hold a coin for several days after an unusually large daily rise rather than sell into it.
Why:
- F5: Large daily rises continue over the following days rather than reverting. Over 5 days, the excess return after rises has a slope of +106 bps per usual move (t 2.5, n 1,365). By quartile of the rise it is -42, +19, +54 and +174 bps (strength -0.06, 0.02, 0.06, 0.14). Rises above 1.5 usual moves are followed by +214 bps excess and +275 bps total over 5 days (n 175), 11 to 14 times the cost of a trade.
- F6: That continuation is not stable, and with many angles examined it is only marginal. Over 10 days its slope has t 1.96. Rises above 1.5 usual moves lose -187 bps over 5 days in 2022 and -168 bps in 2025, and no single coin reaches t 2 (XRP +635 bps, t 1.57).
