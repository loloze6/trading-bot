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
- Situation: RSI reaches a high extreme -> adapted: the 14-bar RSI's upper excess is graded, with a cubic dead zone instead of a threshold, and "after" becomes "while".
- Comparison: more than after neutral readings -> kept: neutral readings give a forecast near zero, so bars with large positions are compared with bars with near-zero ones.
- Outcome: price keeps rising over the following bars -> adapted: the holding period is dropped, and the rise is measured over a fixed forward horizon from each bar.
- Verdict transfer: yes: high RSI drives the long size, and neutral RSI drives near-flat, so higher returns after extremes than after neutral bars confirm the idea and lower ones reject it.
Forecast: The forecast starts from the 14-bar Wilder RSI on daily bars, read as RSI minus 50. It is scaled by the mean absolute value of its own past 60 readings, so an average reading is 10, capped at 20. Readings below 50 are clipped to 0, so the forecast is long or flat, never short. It then passes through a cubic graded dead zone with pivot 20. A typical reading of 10 gives 2.5 (25 percent long), while 20 (RSI far above its usual range) gives 20 (200 percent long). The forecast is zero whenever RSI is at or below 50 and grows smoothly as RSI climbs further into its upper extreme.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The 5-bar forward close-to-close return of the coin, before costs. It is compared between "extreme" bars (the top decile of forecast, pooled across coins and windows) and "neutral" bars (forecast 0, i.e. RSI at or below 50, or the bottom half of positive forecasts). The difference is tested with a t-statistic on non-overlapping 5-bar blocks, so overlapping returns are counted once.
- Supporting check: The portfolio's per-bar return minus the per-bar return of holding the coin, scaled to the same average exposure, is regressed on the prior bar's forecast. The slope should share the sign of the main measure.
- Confirm: Forward 5-bar returns after extreme bars exceed those after neutral bars, with t >= 2, and the difference is positive on at least 2 of the 3 coins.
- Reject: Forward 5-bar returns after extreme bars fall short of those after neutral bars, with t <= -2 (that is reversal, or less rise than after neutral readings).
- Inconclusive: Any t between -2 and 2, including a difference near zero. A result is also inconclusive if there are fewer than 30 non-overlapping extreme-bar cases pooled, or fewer than 30 neutral ones.
