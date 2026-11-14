---
idea: N2-06_rebound-in-high-volatility
brief: 002_moving-average-cross-trend-persistence
data-instruments: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ
data-bar: 1d
data-period: folds A, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a large one-day drop in a coin -> adapted: graded, so the long position grows with the size of the one-day fall and is damped near zero for small falls.
- Comparison: recent volatility in the upper part of the coin's own history, against the coin being quiet -> kept: the 20-day volatility percentile over 100 days, at 0.5 or above versus below, labels each bar.
- Outcome: next close higher (rebound, long) -> kept: the next bar's return, after drops, in high-volatility bars against quiet bars.
- Verdict transfer: yes: a higher rebound rate after drops in high-volatility bars than in quiet bars confirms the idea, and a lower one rejects it.
Forecast: A one-bar price change (PriceEvolution, period 1) is standardised over its past 60 values and negated, so a fall gives a positive value. It is clipped at 0, so the forecast is long only. It then goes through signed_power (exponent 3, pivot 20), the strongest graded dead zone the guide allows. The forecast is near zero on ordinary days and grows steeply with the size of the drop. It is zero on up days. The same forecast runs in both volatility states, so the position never jumps. The detector labels each bar "trending" when the volatility percentile (20-day returns std ranked over 100 days, smoothed 5) is 0.5 or above, and "unknown" otherwise. The test compares the two labels.
Config: N2-06_rebound-in-high-volatility_1d_oos_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Take the bars whose forecast is in the top 10 percent, pooled over all coins and windows. For each, record whether the next close is higher. Compare the share of higher next closes in high-volatility bars (volp ≥ 0.5) with the share in quiet bars, using a two-proportion z-test. Each share is first taken net of the coin's share of up days over all windows together.
- Supporting check: The mean next-bar return on top-decile high-volatility drop bars minus the coin's mean daily return over all windows together, with a t-test.
- Confirm: The high-volatility share of higher next closes exceeds the quiet share with z ≥ 2.
- Reject: The high-volatility share is below the quiet share with z ≤ -2.
- Inconclusive: Any z between -2 and 2 is inconclusive, including a difference near zero. Fewer than 30 top-decile drop bars in either volatility group is also inconclusive.
