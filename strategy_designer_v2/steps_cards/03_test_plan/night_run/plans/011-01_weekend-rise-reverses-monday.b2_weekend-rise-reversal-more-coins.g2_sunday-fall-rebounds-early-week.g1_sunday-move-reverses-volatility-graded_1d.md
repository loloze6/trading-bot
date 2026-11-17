---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin's Sunday return in units of its own 20-day daily volatility -> adapted: the on/off "Sunday" condition is a regime that is active only on Sunday's bar (the coming bar is a Monday), and the vol-scaled Sunday return is graded within it.
- Comparison: the reversal is larger for larger Sunday moves and larger still when recent volatility is high -> kept: the position grows with the vol-scaled move, plus a raw-return term that grows with recent volatility.
- Outcome: the price moves the opposite way over the next 2 days -> adapted: the 2-day holding period is dropped, so the position is held Sunday close to Monday close and the 2-day reversal is measured on the record.
- Verdict transfer: yes: the forecast fades exactly the Sunday move, sized by the idea's two strengths, and is judged on the next 2 days' return.
Forecast: The forecast is computed only at Sunday's close and is flat on every other bar. A WeekdayComponent rule selects `mean_reversion` when the coming bar is Monday (0). In that regime the forecast is the equal-weight mean of two terms, both negated so they fade the move: - Sunday's return divided by the 20-day standard deviation of daily returns (VolatilityScaledReturnComponent, period 1, vol_period 20), standardised over 60 bars. - Sunday's raw percent return (PriceEvolutionComponent, period 1), standardised over 60 bars. This equals the vol-scaled move times the ratio of recent to 60-day volatility, so it adds size when recent volatility is high. A Sunday rise gives a negative forecast and a Sunday fall a positive one. The size grows smoothly with the move and with volatility, and is 0 when Sunday is flat.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Use Sunday bars only (regime `mean_reversion`, forecast not 0); each is its own case, 7 days apart so they do not overlap. For each, take (forecast/10) × (the coin's 2-bar return close[t+2]/close[t]−1 within the window, minus that coin's mean 2-bar return over all windows). Report the t-statistic of the mean of these values, pooled over coins and windows, before costs.
- Supporting check: On the top third of Sunday bars by |forecast|, the mean of sign(forecast) × excess 2-bar return is positive.
- Confirm: The main measure's t is ≥ 2 and the supporting check passes.
- Reject: The main measure's t is ≤ −2, meaning Sunday moves continue rather than reverse.
- Inconclusive: Any t between −2 and 2, or t ≥ 2 with the supporting check failing. At least 300 Sunday cases are required; with fewer, the result is inconclusive.
