---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp up move on unusually low volume -> adapted: low volume becomes an on/off regime (bar volume below its 20-bar mean), and the up-move size is graded.
- Comparison: volume against its usual level -> adapted: "unusually low" becomes "below the 20-bar mean", the only volume cut the config allows.
- Outcome: price falls back, giving up part of the rise -> adapted: the short is held while the situation lasts and measured on the next bar, so no holding period.
- Verdict transfer: yes: a confirm or reject of next-bar returns after low-volume up days, graded by the size of the move, answers the idea directly.
Forecast: The forecast is active only on bars whose volume is below its 20-bar mean. The regime comes from a veto: volume_filter applied to a constant reads 0 there. On those bars the forecast takes the current 1-day percent move, standardises it over its past 60 values and negates it. It then keeps only the short side, so it is negative after an up day and zero after a down day. Last, signed_power with exponent 2 grows the short faster for sharp moves and damps small ones. It is 0 on normal or high-volume bars and on down days. It is never positive.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars where the forecast is non-zero, regress the coin's next-bar return, minus its mean daily return in the same window, on the forecast. Pool all 6 windows and compute the t-stat of the slope. A positive slope means larger shorts are followed by larger excess falls.
- Supporting check: The mean excess next-bar return after the most negative quartile of forecasts (the sharpest thin-volume up days) is below zero.
- Confirm: The slope is positive with t >= 2.0. This is the same as a positive mean of strategy return in excess of the forecast-weighted hold.
- Reject: The slope is negative with t <= -2.0, meaning thin-volume up days are followed by continued rises that grow with the move's size.
- Inconclusive: A t between -2.0 and 2.0 is inconclusive. Fewer than 40 active bars (non-zero forecast) pooled across windows, or fewer than 10 in the top quartile, is also inconclusive whatever the t.
