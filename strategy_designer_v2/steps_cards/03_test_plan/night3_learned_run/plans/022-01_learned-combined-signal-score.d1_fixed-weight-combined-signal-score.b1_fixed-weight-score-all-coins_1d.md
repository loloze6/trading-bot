---
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: four signals combined into one equally weighted score: 28-day return, minus 1-day return, closeness to 90-day high, minus 30-day volatility -> kept
- Comparison: fixed known directions instead of weights learned over the past 365 days; the score is judged against the coin's normal drift -> kept
- Outcome: the next 5-day return is higher the higher the score -> kept
- Verdict transfer: yes: the forecast is the fixed, equal-weight, sign-fixed score itself, so its link to 5-day returns is the idea's claim.
Forecast: The forecast is computed on every bar, with no regime condition. It averages four standardised parts, each scaled against its own past absolute size. - Momentum: the 28-day percent return. - Reversal: the 1-day percent return, negated. - Nearness to the high: the percent distance of the close below its 90-day closing high, always 0 or negative. - Calm: the 30-return standard deviation of daily returns, negated, so always negative. The last two never change sign, so a constant +10 (weight 2) centres them both. Nearness then reads positive when the close is nearer its high than usual, and calm reads positive when volatility is below its usual level. The forecast is (momentum + reversal + nearness + calm + 20) / 6, with weights 1, 1, 1, 1 and 2 for the offset. It is long when the combined score is positive and short when it is negative. Its size grows continuously with the score, and it sits near 0 when the four parts cancel.
Config: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are non-overlapping 5-bar grid bars, pooled over all coins and windows. On each, take forecast/10 × (the coin's 5-day return − its normal 5-day drift over all its windows). The measure is the mean of this product and its t-statistic, judged before costs.
- Supporting check: On the same grid, cases with forecast > 0 have a higher mean excess 5-day return than cases with forecast < 0 (Welch difference, positive minus negative, above 0).
- Confirm: The main measure's t is 2 or more, and the supporting difference is above 0.
- Reject: The main measure's t is −2 or less, meaning a higher score is followed by lower excess returns.
- Inconclusive: A t between −2 and 2, or a t of 2 or more with a supporting difference at or below 0, is inconclusive. So is any test with fewer than 300 non-overlapping cases with a non-zero forecast.
