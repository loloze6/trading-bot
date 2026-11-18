---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation
line: 7.b inconclusive
backtest: 006-04_upside-squeeze-break-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above the high of its prior 20 days, the wider its 20-day range was against its 100-day range, the further price rises over the next 10 days.
Consequence: A trader would favour upside breaks that come out of already-wide, active ranges and treat breaks out of tight squeezes as no better than ordinary.
Why:
- F1: The tested slope is on the side the idea does not predict: on the 299 break-bar 3-day cases, excess return falls as the forecast rises (slope -0.00204, t -1.46). Using the raw narrowness ratio instead of the forecast gives the same sign (slope -0.051, t -1.83). So the result is not a true effect too small to show; there is no sign at all that narrower bands lead to further rises.
- F2: The forecast quartiles show where the slope comes from. The least-compressed quartile (raw ratio 0.26) has the largest mean 3-day excess return, +0.033 (n 75). The three narrower quartiles have +0.005, -0.002 and +0.009. Narrowness adds nothing, and the widest bands carry the gain.
- F3: The negative tilt holds at every horizon and is strongest at 10 days. Raw-ratio slopes are -0.012 (t -1.20) at 1 day, -0.051 (t -1.83) at 3 days, -0.063 (t -1.08) at 5 days and -0.271 (t -2.16) at 10 days (n 107). So the plan's 3-day horizon caught the tilt before it became clear.
- F4: Closing above the prior 20-day high is itself followed by an excess rise, and the rise grows with horizon. Mean excess is +0.0114 at 3 days (t 2.12, n 299) and +0.066 at 10 days (t 2.84, n 107). Against non-break grid bars the gap is Welch t 2.19 at 3 days and 2.99 at 10 days. Mean absolute 10-day moves are 0.160 after breaks against 0.104 otherwise.
