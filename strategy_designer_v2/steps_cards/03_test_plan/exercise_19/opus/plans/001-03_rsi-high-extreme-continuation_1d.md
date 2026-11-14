---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a high extreme -> adapted: graded RSI(14) above 50 with a cubic dead zone, and "after" made "while".
- Comparison: versus neutral readings -> adapted: neutral RSI gives a position near zero, so returns after large positions are compared with returns after near-zero positions.
- Outcome: price keeps rising over the following bars -> kept.
- Verdict transfer: yes: the forecast takes its largest longs exactly at high RSI extremes and is near flat at neutral readings, so the measured difference is the idea's difference.
Forecast: Wilder RSI(14) on daily closes, read as (50 - RSI) and standardised over its past 60 values. It is then negated, so it is positive when RSI is above 50. It is clipped at 0, because the idea concerns only high extremes. A signed_power with exponent 3 and pivot 10 then makes the long position stay close to zero near neutral RSI and grow steeply as RSI moves to its high extreme. The forecast is never negative. It is 0 when RSI is 50 or below, and its size can reach the +20 cap.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward return after "extreme" bars (forecast >= 10) minus its 5-bar forward return after "neutral" bars (forecast < 1). This is pooled over 3 coins and 6 windows, before costs. Overlap is handled with non-overlapping 5-bar blocks or a Newey-West t with lag 4. Because it is a difference against neutral bars, the market's own rise is not credited to the idea.
- Supporting check: Inside each coin, the strategy's excess return over buy-and-hold, on bars where forecast >= 10. The difference should be positive for at least 2 of the 3 coins.
- Confirm: The pooled difference is > 0 with t >= 2.
- Reject: Either the pooled difference has t <= -2, or the whole 90% confidence interval of the difference lies inside ±1.0% per 5 bars (no difference, as the brief allows).
- Inconclusive: Any other result, including an estimate on the wrong side of zero with t between -2 and 2. The test needs at least 30 non-overlapping extreme cases pooled across coins; with fewer it is inconclusive.
