---
idea: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the coin's 20-day volatility is high relative to its 120-day volatility, and the last day moved -> kept: a regime on the rank of 20-day volatility within its last 120 days, set at or above the median; the last day's return is divided by its 20-day volatility.
- Comparison: the reversal is stronger after down days than after up days -> kept: a criterion check comparing down-day bars with up-day bars.
- Outcome: the move reverses over the next 1 day, and more so the larger the vol-scaled move -> kept: the position is opposite and proportional to the vol-scaled move, held for 1 bar.
- Verdict transfer: yes: the forecast fades the vol-scaled daily move only in elevated volatility, and the check tests whether down days reverse more than up days, so both results carry over to the idea.
Forecast: The regime detector computes the volatility percentile (20-day volatility ranked in its last 120 days, smoothed over 5). When it is 0.5 or higher, the regime is mean_reversion and the forecast is active; otherwise the forecast is 0. When active, the forecast is the coin's 1-day return divided by its 20-day return volatility (VolatilityScaledReturn, period 1, vol_period 20). This is standardised over 60 past values (min 20) and negated. The forecast is long after a down day and short after an up day. Its size grows in proportion to how large the day's move was in usual moves, capped at ±20.
Config: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Measured on bars where regime is mean_reversion. Per bar: postRebalance_current_allocation × (close[t+1]/close[t] − 1 − the coin's mean daily return over all windows). Report the ordinary t of the mean, pooled over coins and windows, with each bar as one independent case.
- Supporting check: On the same bars, take the reversal return −sign(close[t]/close[t−1] − 1) × (close[t+1]/close[t] − 1 − the coin's mean daily return). Compute the down-day mean minus the up-day mean, with Welch t.
- Confirm: Main-measure t ≥ 2 with a positive mean, and the down-minus-up difference > 0 with Welch t ≥ 2.
- Reject: Main-measure t ≤ −2. Or the main measure confirms but the down-minus-up difference has Welch t ≤ −2, meaning up days reverse more than down days.
- Inconclusive: Any main t between −2 and 2, or a confirmed main measure with a check t between −2 and 2. Minimum: 200 active bars in total and 50 in each of the down-day and up-day groups; below that, inconclusive.
