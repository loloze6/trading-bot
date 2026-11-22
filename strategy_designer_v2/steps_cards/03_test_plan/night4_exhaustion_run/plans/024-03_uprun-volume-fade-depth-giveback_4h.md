---
idea: 024-03_uprun-volume-fade-depth-giveback
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: aaeaf3675030
---
Fidelity:
- Situation: an unbroken streak of rising 4h bars with a large gain, while volume declined from the streak's start to its end -> adapted: "after the streak" made "while the streak lasts", and "large" and "declined" made graded.
- Comparison: the gain against the coin's typical 4h move over the past 30 days (180 bars) -> kept.
- Outcome: the coin falls over the next three days, more so the more the volume faded -> kept: a short held 18 bars and graded by the fade.
- Verdict transfer: yes: the forecast is the streak's gain in usual 4h moves plus its volume fade, shorted for three days, so a confirm or a reject of its falls is a confirm or a reject of the idea.
Forecast: Two components, each scaled by `standardise` over 180 bars (min_periods 45). - Gain: the current up-streak's summed gain over the mean absolute 4h move of the last 180 bars (`DownStreakLossInUsualMovesComponent`, side "up", window 180). - Fade: ln(first streak bar's volume / last streak bar's volume) (`DownStreakVolumeFadeComponent`, side "up", log_ratio), clipped at 0 so that only a fade adds. How they combine: - Each passes through `signed_power` exponent 3, the strongest graded dead zone, because big runs are rare extremes. - Each is then negated, and the two are averaged with equal weights. What the forecast does: - It is 0 when the last bar did not close up. It is never positive. - It grows more negative, in a convex way, as the run grows larger against usual moves and as volume fades more across it.
Config: 024-03_uprun-volume-fade-depth-giveback_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The cases are the short bets (a fall of the forecast of at least 2 points), read once per 18-bar grid cell in each window. For each case, take the coin's 18-bar return from the signal bar, subtract the coin's normal 18-bar drift over all windows, and count it in the short direction. The measure is the mean of that unusual move over all coins and windows, with the t of that mean.
- Supporting check: Split the cases at the median of `vol_fade` `last_history_value`. The mean unusual fall of the high-fade half, minus that of the low-fade half, must be above 0.
- Confirm: The main mean unusual fall is positive with t >= 2 over at least 30 cases, and the supporting check's difference is above 0.
- Reject: The main mean unusual move in the short direction has t <= -2 over at least 30 cases, meaning the coin rises more than its drift after such runs.
- Inconclusive: Any t between -2 and 2, fewer than 30 cases, or a confirming main measure with a high-fade minus low-fade difference at or below 0.
