---
idea: 024-04_downrun-volume-fade-depth-rebound.d1_rebound-in-expanding-volatility
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 9111077ea370
---
Fidelity:
- Situation: an unbroken streak of falling 4h bars whose loss is large against the coin's typical 4h move over 30 days -> adapted: graded as the streak's loss in usual one-bar moves (DownStreakLossInUsualMovesComponent, window 180), with no fixed "large" threshold.
- Comparison: only while 7-day volatility is high against 30-day volatility, the higher that ratio the larger the rise -> replaced: no component gives a 42-bar to 180-bar return-volatility ratio, and the forecast's weighted mean cannot multiply the streak loss by any ratio.
- Outcome: the coin rises over the next three days (18 bars) -> kept.
- Verdict transfer: no: without the volatility ratio scaling the bet, a result would test plain down-streak reversal, not reversal that grows with volatility expansion.
Reason: The idea's bet is the down-streak loss scaled by the ratio of 7-day to 30-day volatility. The config can only add components, not multiply them, and no catalogue component computes that product or even the plain 42/180-bar volatility ratio. VolatilityRatioToAverageComponent compares 7-day volatility with its own 30-day average, and MeanBarRangeRatioComponent uses bar ranges, inverted. A regime gate on such a ratio would drop "the higher the ratio, the larger the rise".
