---
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4a01343a8148
---
Fidelity:
- Situation: a large one-day move, in a coin whose 20-day volatility is high relative to its last 100 days -> adapted: "large" becomes graded through the strongest signed_power dead zone; the volatility condition is kept as a regime rule (20-day volatility rank over 100 days of at least 0.8).
- Comparison: the day's move against its 60-day mean absolute daily move -> kept: standardise over a 60-bar window divides the one-day return by the mean absolute value of the 60 prior one-day returns.
- Outcome: an opposite move over the next 3 days, larger after a larger move -> adapted: the 3-day hold is dropped, so the fade is held while the move reads large, and the 3-day give-back is judged in the criterion.
- Verdict transfer: yes: the test measures the same move ratio, the same volatility condition and the same 3-day opposite return, so a confirm or a reject here carries over to the idea.
Forecast: The forecast is active only while the 20-day volatility rank over 100 days (unsmoothed) is at least 0.8; on all other bars it is flat. When active, it takes today's one-day percent return and divides it by the mean absolute one-day return of the prior 60 days, times 10, capped at ±20. The sign is flipped so the position fades the move: short after an up day, long after a down day. A cubic dead zone with pivot 20 is then applied. A move of 1 times the usual size gives about 1.25, 1.5 times gives about 4.2, and 2 times or more gives 20. The position grows smoothly with the move's size relative to its usual size, and it is near zero on ordinary days.
Config: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Use the non-overlapping 3-bar grid of each window, keeping grid bars with |forecast| ≥ 5. On each, take sign(forecast) × (close[t+3]/close[t] − 1), minus sign(forecast) × the coin's mean 3-bar return over all windows. Report the mean of these values and its t.
- Supporting check: On the same cases, regress the signed excess 3-bar return on |forecast|. The slope must be positive with t ≥ 1.
- Confirm: The mean signed excess 3-bar return is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The mean signed excess 3-bar return has t ≤ −2, meaning the price continues in the direction of the large move.
- Inconclusive: Any t between −2 and 2 is inconclusive. A confirming main measure with a failed supporting check is also inconclusive. Fewer than 30 qualifying cases across all coins and windows is inconclusive.
