---
idea: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: aaeaf3675030
---
Fidelity:
- Situation: an unbroken streak of rising 4h bars whose gain is large against the coin's typical 4h move over the past 30 days -> adapted: "after the streak" becomes "while the streak lasts", and "large" is graded as the streak's gain in usual one-bar moves over 180 bars.
- Comparison: the more volume declined from the streak's start to its end, the larger the fall -> adapted: graded as ln(first-bar volume / last-bar volume) of the streak, added to the short's size rather than a threshold.
- Outcome: the coin falls over the next three days -> kept: a short held for 18 bars.
- Verdict transfer: yes: both the streak gain and the volume fade are measured as stated, and the 18-bar fall after them is tested directly.
Forecast: Two parts, both computed on 4h bars. - Streak gain: the gain of the current run of consecutive up-closes, counted in mean absolute one-bar moves over the last 180 bars (30 days). It is standardised over 180 bars and put through signed_power with exponent 3, so only large runs count, then negated. - Volume fade: ln(volume of the run's first bar / volume of its last bar). It is standardised over 180 bars, put through signed_power with exponent 3, negated, and clipped at 0, so rising volume adds nothing. The forecast is their weighted mean, with weights 2 for the gain and 1 for the fade. It is zero when the current bar did not close up. It grows more negative (short) as the run gets larger against the usual move and as its volume fades. It is never positive.
Config: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The unusual move of the cases, in the short direction. Each case is a short bet: the forecast falls at least 2 points from its last level, read once per 18-bar grid cell. For each case, take the coin's return over the next 18 bars, minus its normal 18-bar drift (holding the coin), with the sign flipped for the short. The test is the mean over all coins and windows, with the t of that mean.
- Supporting check: Over the same cases, fit a least-squares regression of the drift-adjusted 18-bar return on the recorded raw run_gain and vol_fade values (last_history_value). The vol_fade coefficient must be negative: more fade, larger fall for the same run size.
- Confirm: The main mean is above 0 with t ≥ 2, and the vol_fade coefficient has t ≤ -2.
- Reject: The main mean is below 0 with t ≤ -2, or the vol_fade coefficient has t ≥ +2.
- Inconclusive: Any result in between, including t near 0 on either measure. Any result with fewer than 30 cases overall is also inconclusive.
