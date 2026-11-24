---
idea: 032-02_choppy-agitated-weekly-fall-reverts
brief: 032_choppy-agitated-weekly-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's fall over the past 7 days, larger or smaller -> adapted: the 7-day fall is graded, and the position is zero when the coin did not fall.
- Comparison: none -> kept
- Outcome: a rise over the next 7 days that grows with the fall -> kept
- Verdict transfer: yes: the forecast is the 7-day fall itself and the book holds 7 days, so a forward rise that grows with it confirms the idea, and a forward fall that grows with it rejects it.
Forecast: The forecast is the coin's 7-bar return in percent (PriceEvolutionComponent, period 7). It is standardised against its own last 60 values, so a usual-sized move reads about 10. It is negated so that a fall reads positive, then clipped at 0 so it is long only. On a bar where the coin fell over the past 7 days the forecast is positive and grows smoothly with the size of the fall. On a bar where the coin rose or was flat over 7 days it is zero. The code adds the choppy agitated profile, so the book is flat outside that profile.
Config: 032-02_choppy-agitated-weekly-fall-reverts_1d_config.json
Profile: choppy agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 7 bars
- Main measure: Use grid cells every 7 bars within each window, keeping only cells with forecast > 0. For each cell, take the coin's 7-bar forward return minus its normal 7-bar drift (the mean over all its windows). Regress that excess return on the forecast and read the slope's t. Cases on the same day are summed into one piece of evidence.
- Supporting check: The mean excess 7-bar return over those cells (the unusual move in the long direction) is above 0.
- Confirm: Slope t ≥ 2 and a positive mean excess return.
- Reject: Slope t ≤ -2, meaning larger falls are followed by weaker or more negative next-week returns.
- Inconclusive: A slope t between -2 and 2, or t ≥ 2 with a mean excess return of 0 or below. Fewer than 30 independent positive-forecast grid cells (day-clustered) is always inconclusive.
