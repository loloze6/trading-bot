---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin's daily move, with its 20-day volatility high -> adapted: the on/off "high volatility, not in calm stretches" becomes graded. The raw one-day percent move over its long-run mean absolute move equals (the move in 20-day-vol units) x (the 20-day vol relative to its long run).
- Comparison: larger move and higher 20-day volatility mean a larger move back -> kept: the forecast is the product of move size and volatility, so it grows with both.
- Outcome: the price moves the other way over the next day -> kept: the position fades the move and is judged over 1 bar.
- Verdict transfer: yes: the forecast is the idea's sizing rule, so its next-day timing gain confirms or rejects the idea directly.
Forecast: Start from the one-day percent change of the close (PriceEvolutionComponent, period 1). Divide it by the mean absolute one-day change of the previous 500 stored bars (standardise window 500, min_periods 120), then negate it. The result is the move in units of the coin's usual 20-day move, times the 20-day volatility relative to its long-run level. This is the product the idea names. A short window of 60 would divide the volatility away, so the window is 500. The forecast is positive after a down day and negative after an up day, and zero when there was no move. Its size grows with the move and with the volatility. In calm stretches the moves are small against the long-run average, so the forecast stays near zero. It is capped at ±20.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Pooled over all bars of all coins and windows: postRebalance_current_allocation[t] x (close[t+1]/close[t] - 1 - the coin's mean daily return over all its windows). This is the position's next-day timing gain, beyond holding the coin. Measure its mean and the ordinary t of that mean, before costs.
- Supporting check: Rank the bars by |position|. The mean timing gain per unit of |position| on the top third must exceed that of the bottom third (top minus bottom > 0), showing that the gain grows with the size of the position.
- Confirm: The main mean is positive with t ≥ 2, and the supporting check passes.
- Reject: The main mean is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with the supporting check failing. At least 1000 non-zero-position bars are needed, else the result is inconclusive.
