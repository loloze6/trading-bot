---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin's 14-day fall, graded by its size -> kept: the 14-day return, falls only.
- Comparison: moderate falls against the deepest falls, and against the coin's usual return -> adapted: the "deepest falls" cut-off made a graded hump, short to long.
- Outcome: lower 7-day return after larger falls, a rebound after the deepest -> kept: 7-bar forward return against holding the coin.
- Verdict transfer: yes: the forecast is short in proportion to moderate falls and long at the deepest, so its 7-bar results judge both claims.
Forecast: The forecast uses the 14-bar price change (PriceEvolutionComponent, period 14), standardised over 60 bars with min_periods 20, and clipped at 0 from above, so only falls count. Write s for the size of the standardised fall (0 to 20). Two copies are combined. The first has weight 3 and gives -s, a short position. The second has weight 1 and gives +10 x (s/10)^3, a long position, through signed_power with exponent 3 and pivot 10, then negate. The forecast is (-3s + 10(s/10)^3) / 4: - It is 0 when the coin is up over 14 days. - It is negative for moderate falls, most negative (-5) at a fall of usual size (s = 10). - It crosses 0 at s ≈ 17. - It is positive (+5 at s = 20) for the deepest falls, about twice the usual size. The change is graded everywhere and never jumps.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: The sample is the non-overlapping 7-bar grid points of each window with forecast ≠ 0, pooled over coins. On it, take the slope of the excess 7-bar return on the forecast, with its t. The excess return is close[t+7]/close[t] - 1 minus the coin's mean 7-bar return over all windows.
- Supporting check: Compare the mean excess 7-bar return at grid points with forecast > 0 (deepest falls) against the mean at points with forecast < 0 (moderate falls). The difference must be above 0.
- Confirm: The slope has t ≥ +2 and the supporting difference is positive.
- Reject: The slope has t ≤ -2.
- Inconclusive: Any slope t between -2 and +2 is inconclusive. A slope with t ≥ 2 whose supporting difference is not positive is also inconclusive. So is any test with fewer than 200 non-zero grid points, or fewer than 30 grid points with forecast > 0.
