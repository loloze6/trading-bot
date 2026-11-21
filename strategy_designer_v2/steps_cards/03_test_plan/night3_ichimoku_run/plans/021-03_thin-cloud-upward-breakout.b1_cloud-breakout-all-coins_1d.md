---
idea: 021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bf6ee48001bb
---
Fidelity:
- Situation: a daily close crossing up from below the cloud to above it -> adapted: "after the cross" becomes "while above the cloud within 26 bars of an up-cross from below" (regime on `IchimokuCloudCrossAgeComponent` between 1 and 26).
- Comparison: thin versus thick cloud, as width relative to price, at the cross -> kept: `IchimokuCloudWidthComponent` "proximity" is 1/(1+width% of close), and it grows as the cloud thins.
- Outcome: the coin rises over the next 26 days, more after a thinner cloud -> kept: long only, each bet held 26 daily bars.
- Verdict transfer: yes: the bet is opened at the cross, sized by the cloud's thinness then, and held 26 days, so both claims are measured as stated.
Forecast: The regime is active only while the close is above the cloud, within 26 bars of an up-cross from below; on every other bar the forecast is 0. On active bars the forecast is the cloud proximity (Ichimoku 9/26/52, displacement 26), standardised over its own past 78 values. It is always positive, so the forecast is long only. It is near +10 for a cloud of usual thickness, larger for a thinner cloud and smaller for a thicker one, capped at 20. The bet opened on the cross bar carries the cloud's thinness at the cross, and it is held for 26 bars.
Config: 021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: Over the cases (a forecast rise of at least 2 points from 0 on entering the regime, one per 26-bar grid cell, inside one window), take the 26-bar return from the signal bar's close minus the coin's normal 26-bar drift. Compare thin-cloud cases (recorded `thin_cloud` raw proximity above the median of all cases) with thick-cloud cases, as thin minus thick, by Welch's t.
- Supporting check: The mean unusual 26-bar return over all cases is above 0, with an ordinary t of 2 or more.
- Confirm: The idea is confirmed only when both hold. The thin-minus-thick difference must be above 0 with Welch t of 2 or more. The supporting check must also pass.
- Reject: The idea is rejected if the thin-minus-thick Welch t is -2 or less. It is also rejected if the all-case mean unusual return has t of -2 or less.
- Inconclusive: Any other result is inconclusive, including differences near zero. It is also inconclusive with fewer than 40 cases in total, or fewer than 20 in either half.
