---
idea: 061-01_choppy-agitated-strong-close-fade
brief: 061_choppy-agitated-high-close-fades
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a choppy, agitated market, the daily close sits near the top of the day's high-low range -> adapted: the profile is added by code, and "near the top" becomes a regime where the close is in the top 20% of the range (the conventional IBS of 0.8).
- Comparison: the nearer the close is to the high, the larger the fall -> kept: inside the regime, the short grows with the close's location in the range.
- Outcome: the price falls over the next two days -> kept: the book holds a 2-bar short.
- Verdict transfer: yes: the test measures the same bars, side and horizon as the idea, so its result carries over in both directions.
Forecast: One detector component, CloseLocationInRangeComponent (reference "low", which gives (close − low)/(high − low) for the day), sets the regime. When it is at least 0.8, the bar is `mean_reversion`; otherwise the bar is `unknown`, which is flat. Code adds the choppy-agitated profile on top, as vetoes to flat. Inside the regime, the same close location is standardised over its last 60 values (about 0.5 on average, so about +16 at 0.8 and about +20 at the high). It is then negated and clipped at 0. The forecast is therefore short only: about −16 at a close at 80% of the range, growing to about −20 as the close reaches the day's high. Outside the regime it is 0.
Config: 061-01_choppy-agitated-strong-close-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: choppy agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 2 bars
- Main measure: The cases are short signals: bars where the forecast drops below 0 by at least the band, read once per 2-bar grid cell. For each case, take the coin's 2-bar return from the signal's close minus the coin's normal 2-bar drift over all windows, counted in the short direction. Report its mean and its t, with the cases of one day pooled.
- Supporting check: The mean unusual move of cases with close location ≥ 0.9 is at least that of cases with close location from 0.8 to 0.9. The close location is recomputed from that bar's high, low and close.
- Confirm: The idea is confirmed when both hold: - the mean unusual move in the short direction is positive, with t ≥ 2 over at least 30 cases; - the supporting check passes.
- Reject: The idea is rejected when the mean unusual move in the short direction has t ≤ −2 over at least 30 cases, meaning prices rose beyond their drift after high closes.
- Inconclusive: The result is inconclusive in any of these cases: - t is between −2 and 2; - the main measure confirms but the supporting check fails; - there are fewer than 30 cases.
