---
idea: 027-03_panic-rebound-in-downtrend
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a 24h stretch (6 bars) with range several times its 30-day (180-bar) average and a hard fall, in a coin whose prior 30-day return was negative -> adapted: the prior return is lagged past the stretch and kept as a rule, the range is kept as a rule (mean bar range at least 3x its average), and the hard fall is made graded.
- Comparison: higher than usual returns -> kept: the forward return is judged against the coin's normal drift (holding it).
- Outcome: price rises over the next 14 days (84 bars), more so the more extreme the panic -> kept.
- Verdict transfer: yes: the rules select exactly the idea's panics in falling coins, and the long size grows with the depth of the fall, so the test's verdict is the idea's.
Forecast: The forecast is live only on bars where two conditions hold together. First, the 30-day return ending just before the 24h stretch (close[t-6] / close[t-186] - 1) is negative. Second, the mean 4h bar range over the last 6 bars is at least 3 times its 180-bar mean (180-bar mean / 6-bar mean <= 0.333). On every other bar the forecast is 0. On live bars the forecast measures the 24h fall: the 6-bar return divided by the coin's mean absolute 6-bar return over 180 bars. That value is standardised over 186 past values, negated, clipped at 0 so only falls count, and passed through signed_power with exponent 3 as a strong graded dead zone. The forecast is therefore 0 on rises, small on mild falls, and grows steeply (capped at 20) with the depth of the fall. It is never negative.
Config: 027-03_panic-rebound-in-downtrend_4h_config.json
Criterion:
- Horizon: 84 bars
- Main measure: The unusual move per case: the coin's 84-bar return from the close of each bet's bar, minus the coin's normal 84-bar drift over all its windows. Cases are read once per 84-bar grid cell, inside windows only. The measure is the mean over cases and its t.
- Supporting check: The case mean weighted by the forecast at the bet must be at least the unweighted mean (more extreme panics earn more).
- Confirm: The mean unusual move is above 0 with t >= 2 on at least 20 independent cases, and the supporting check passes.
- Reject: The mean unusual move is below 0 with t <= -2 on at least 20 independent cases.
- Inconclusive: Any t between -2 and 2, or a confirming t whose supporting check fails, or fewer than 20 independent cases.
