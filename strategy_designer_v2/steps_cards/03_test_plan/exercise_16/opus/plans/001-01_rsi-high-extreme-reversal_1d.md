---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a high extreme -> adapted: graded RSI excess above 50 ("after" becomes "while"), with extremes amplified and no fixed 70 cut.
- Comparison: behaviour after high readings vs after neutral readings -> kept: forward returns after the largest shorts are compared with forward returns on flat (neutral) bars.
- Outcome: price falls back, giving back part of the run -> kept: the short gains when the next 5 bars' return is negative.
- Verdict transfer: yes: the short-only RSI forecast bets exactly that high readings come before falls, sized by how extreme the reading is.
Forecast: The forecast uses one indicator, RSIPullbackComponent with period 14 (the daily convention). Its raw value is (50 - RSI) x 0.4. - Scaling. standardise (window 60, min_periods 20) puts the raw value on the scale of its own past 60 values, about 10 on average. - Short side only. clip with max 0 keeps only the short side, so the forecast is zero whenever RSI is 50 or below. - Extremes weigh more. signed_power with exponent 2 and pivot 10 shrinks mild readings smoothly toward 0 and enlarges extreme ones. RSI near 55 gives a tiny short. RSI near 70 or higher gives a short of 10 to 20. - Sign and size. The forecast is never positive. It grows more negative, and the position larger, as RSI climbs further above 50.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's mean 5-bar forward return after bars with forecast ≤ -10 (the largest shorts, RSI roughly 70 or above), minus its mean 5-bar forward return after flat bars (forecast 0). This is pooled over coins and windows, using non-overlapping 5-bar returns only (a new case starts at least 5 bars after the previous one).
- Supporting check: The same difference has the reversal sign (negative) in at least 2 of the 3 coins.
- Confirm: The difference is negative with a t-stat ≤ -2 on non-overlapping cases, and the supporting check holds.
- Reject: The difference is ≥ 0, or its t-stat is above -1 (high readings are followed by flat or continuing prices, not by a fall).
- Inconclusive: A t-stat between -2 and -1, or a confirming t-stat where the coins disagree. The result is also inconclusive with fewer than 30 non-overlapping extreme cases in total, or fewer than 30 flat-bar cases.
