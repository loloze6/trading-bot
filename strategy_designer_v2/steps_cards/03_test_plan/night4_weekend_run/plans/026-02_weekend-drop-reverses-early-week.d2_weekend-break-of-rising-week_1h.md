---
idea: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2a96c3272007
---
Fidelity:
- Situation: a coin falls over the weekend after rising over the previous five days -> kept: a regime fires at Sunday's last close, when the 48-bar weekend return is below 0 and the 120-bar return ending at Friday's close is above 0.
- Comparison: the fall is larger the larger the preceding five-day rise -> kept: the short grows with the five-day rise, measured in the coin's usual moves.
- Outcome: it keeps falling over Monday and Tuesday (short) -> kept: a short opened at Sunday's last close and held 48 bars.
- Verdict transfer: yes: the test bets only at the end of the weekend, short, sized by the prior rise, over Monday and Tuesday.
Forecast: The forecast is computed once a week, at the close of Sunday's 23:00 UTC bar, when the coming bar is Monday 00:00. It is non-zero only when two conditions hold: the coin's 48-bar return (Saturday and Sunday) is below 0, and its 120-bar return ending 48 bars earlier (Monday to Friday) is above 0. On that bar the forecast is short. Its size is the five-day rise in the coin's usual moves (`VolatilityScaledReturnComponent`, period 120, lag 48, vol_period 720). That value is standardised over its past 500 values, negated, and clipped at 0 from above, so a larger prior rise gives a larger short. On every other bar the forecast is 0, and the bet is held for the 48-bar horizon.
Config: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The unusual move per case, on the short side. A case is a Sunday-close bet (forecast at or below -2). The move is the coin's return over the next 48 bars from the signal bar's close, minus the coin's normal 48-bar drift over all windows, signed short. The measure is its mean over all coins and windows, with the t of that mean.
- Supporting check: Across cases, regress the short-side unusual move on the absolute forecast. The slope must be above 0, because a larger prior rise should give a larger fall.
- Confirm: The mean short-side unusual move is above 0 with t ≥ 2, and the supporting slope is above 0.
- Reject: The mean short-side unusual move has t ≤ -2: after such weekends the coin rises more than its normal drift.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t ≥ 2 with a slope at or below 0. Fewer than 100 cases across all coins and windows is also inconclusive. Cases are a week apart, so each one is independent.
