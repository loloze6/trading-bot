---
idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: aaeaf3675030
---
Fidelity:
- Situation: a coin has just risen in an unbroken streak of 4h bars -> adapted: "just after the streak" becomes "while the streak is running at bar t" (up-streak through the current bar).
- Comparison: the streak's gain against the coin's typical 4h move over the past 30 days -> kept: summed gain divided by the mean absolute one-bar return over 180 bars.
- Outcome: the coin keeps rising over the next three days, more after a larger relative gain -> kept: the long position grows with the ratio and each bet is held 18 bars.
- Verdict transfer: yes: the forecast is the idea's own ratio, held over the idea's own three days, so a confirm or a reject carries straight to the idea.
Forecast: One component, DownStreakLossInUsualMovesComponent with side "up", window 180 (30 days of 4h bars), max_bars 180 and base "start". On each bar it gives the current up-streak's gain, as a share of the streak's starting close, divided by the coin's mean absolute 4h return over the last 180 bars. This is the streak's gain counted in usual 4h moves. It is standardised over its own past 181 values (min_periods 45), so a typical streak reads about +10, and it is capped at +20. The forecast is positive and grows with the streak's gain in usual moves. It is 0 on any bar that did not close up, and it never goes short. A rise of the forecast is a bet, and each bet is held for 18 bars (three days).
Config: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The unusual move per case. A case is a bet, read once per 18-bar grid cell of each window, all coins pooled. Its value is the coin's 18-bar return from the signal bar's close, minus the coin's normal 18-bar drift over all windows. The measure is the mean of these values over the cases, with its t of the mean.
- Supporting check: The mean unusual move of the cases in the top half of forecast size, minus that of the bottom half, is above 0.
- Confirm: The mean unusual move has t >= 2 and the top-half minus bottom-half difference is above 0.
- Reject: The mean unusual move has t <= -2 (the up-runs are followed by a give-back larger than the coin's drift).
- Inconclusive: A t between -2 and 2, or t >= 2 with a top-minus-bottom difference at or below 0. Fewer than 100 cases is inconclusive whatever the result.
