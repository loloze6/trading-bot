---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coin rose over the weekend (its Saturday-to-Sunday close-to-close return) -> kept: the Sunday bar's 1-bar return, selected by a weekday regime (the coming bar is Monday).
- Comparison: the larger the weekend rise, the larger the fall -> kept: the short grows with the size of the weekend rise.
- Outcome: the price falls over the next 2 days (Monday and Tuesday) -> adapted: holding period dropped; the position is held over Monday only, and the record's 2-bar return (Sunday close to Tuesday close) is what gets measured.
- Verdict transfer: yes: the Sunday-close forecast is sized by the weekend rise and judged on the following Monday-plus-Tuesday return.
Forecast: The forecast is computed only on the Sunday bar, the bar whose next bar is Monday. It uses the Sunday bar's 1-bar return in percent, from Saturday's close to Sunday's close. That return is standardised against its own past 60 values (20 at minimum) and negated. It is then clipped at 0 from above. The forecast is negative (short) when the weekend rose, and its size grows in proportion to the rise. It is 0 when the weekend fell or was flat, and 0 on every other weekday (the regime is flat there).
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are all Sunday bars (regime mean_reversion) with forecast < 0, pooled over coins and windows. Sundays are 7 bars apart, so the cases do not overlap. For each case, x = (-forecast/10) × -(r2 - m), where: - r2 = close[t+2]/close[t] - 1, taken inside the same window; - m = the coin's mean non-overlapping 2-bar return over all its windows. The measure is the ordinary t of the mean of x.
- Supporting check: Split the cases into thirds by |forecast|. The mean of (r2 - m) in the top third, minus the same mean in the bottom third, must be below 0.
- Confirm: The idea is confirmed when both hold: - the main measure has t ≥ 2; - the supporting check is below 0.
- Reject: The idea is rejected when the main measure has t ≤ -2, meaning weekend rises are followed by above-average Monday-Tuesday returns.
- Inconclusive: Any t strictly between -2 and 2 is inconclusive. A t of 2 or more with the check at or above 0 is also inconclusive. Fewer than 100 cases is inconclusive whatever the t.
