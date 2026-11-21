---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a calm period, the lower a coin's 30-day volatility is next to its usual level, the more its 3-day return, scaled by that volatility, carries into its return over the next 5 days in the same direction.
Consequence: A trader should lean on short-term continuation mostly when the coin is calmer than usual, and trust it less when volatility is high.
Why:
- F1: The coin's 3-day return divided by its 30-day volatility predicts its next 5-day return in the same direction, the opposite of the reversal this idea assumes. The product with the coin's standardised unusual 5-day move is positive on all five non-overlapping grid offsets, with t of 2.40, 3.22, 5.04, 1.39 and 1.37 on about 2,450 to 2,555 cases each. Lookbacks of 2, 5 and 7 days give similar t values, from 2.2 to 5.0 on offsets 0 to 2.
- F4: The continuation is larger per case than a trade costs. Cases with a 3-day |z| above 1 on the offset-0 grid have an unusual move of +0.90 % and a total move of +0.98 % over 5 days (676 cases), with a strength of 0.080. That is about 4.7 times the 0.19 % round-trip cost.
- F5: The continuation is concentrated in calm periods. On offset 0, the 3-day z product has t 2.67 when the coin's 30-day volatility is below its median (1,278 cases) and t 0.82 above it (1,277 cases). The 1-day z product shows the same split: t 3.34 against 0.13.
- F7: The continuation is not stable from year to year. On offset 0 the 3-day z product has t 2.87 in 2018 and 3.69 in 2021, but -1.82 in 2022 and -1.99 in 2025. The tested combined forecast swings the same way: t 3.30 in 2020, -3.05 in 2023.
