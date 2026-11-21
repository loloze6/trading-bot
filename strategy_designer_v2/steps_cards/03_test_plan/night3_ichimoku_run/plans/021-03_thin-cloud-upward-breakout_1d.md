---
idea: 021-03_thin-cloud-upward-breakout
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bf6ee48001bb
---
Fidelity:
- Situation: a daily close crosses up from below the Ichimoku cloud to above it -> kept: a regime rule selects the bar where the cross age reads +1, the first close above the cloud after a stay below it.
- Comparison: thinner cloud at the cross, as width relative to price, means a larger rise -> kept: the forecast grows with the cloud's proximity, 1/(1+width%) at the cross, against that measure's own past.
- Outcome: the coin rises over the next 26 days -> kept: the long bet made at the cross is held 26 bars.
- Verdict transfer: yes: the test bets long only at upward crosses, sized by cloud thinness, and holds for the idea's 26 days, so both claims are measured as stated.
Forecast: The forecast is zero on every bar except the bar where the daily close first sits above the Ichimoku cloud (9/26/52/26) after its last stay below it. On that bar the forecast is long. Its size is the cloud's proximity, 1/(1 + cloud width in % of close), standardised against its own past 78 bars: about +10 for a usual cloud, more for a thinner one and less for a thicker one, capped at 20. It is never negative. The 26-bar holding period keeps the bet after the cross bar.
Config: 021-03_thin-cloud-upward-breakout_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: Each upward cross bar (regime "trending") is one case. The case's value is the coin's 26-bar return from that close minus the coin's mean 26-bar return over all windows, and the measure is the mean of these values with its t.
- Supporting check: Compare cases above and below the median thin_cloud post_pipeline_value (thinner against thicker clouds). Take the mean unusual 26-bar return of each group, the thin group minus the thick group, with Welch's t.
- Confirm: The idea is confirmed only if both hold, with at least 30 cases: - the mean unusual return is above 0 with t ≥ 2; - the thin-minus-thick difference is above 0 with t ≥ 2.
- Reject: The idea is rejected if either holds, with at least 30 cases: - the mean unusual return has t ≤ -2; - the thin-minus-thick difference has t ≤ -2.
- Inconclusive: Any other result is inconclusive, including t between -2 and 2 on either measure. Fewer than 30 cross cases in total, or fewer than 15 per group for the check, is also inconclusive.
