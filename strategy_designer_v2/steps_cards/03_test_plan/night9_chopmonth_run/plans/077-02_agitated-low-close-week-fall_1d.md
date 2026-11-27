---
idea: 077-02_agitated-low-close-week-fall
brief: 077_agitated-close-location-week-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in an agitated market, a daily close near the bottom of that day's range -> kept: the code adds the agitated profile, and a regime rule selects bars whose close sits in the bottom quarter of the day's range (the most common convention for "near the low").
- Comparison: larger the nearer the close sits to the day's low -> kept: inside the regime the short grows as (high − close)/(high − low) nears 1.
- Outcome: a fall over the next 7 days -> kept: a short held for 7 daily bars.
- Verdict transfer: yes: the test measures the idea's own situation, grading and 7-day fall, so a confirm or a reject carries over to the idea.
Forecast: The regime detector reads `CloseLocationInRangeComponent` (`reference` "high"). This is (high − close)/(high − low): 0 when the close is at the day's high and 1 when it is at the day's low. A bar is `mean_reversion` when this value is 0.75 or more. Every other bar is `unknown`, which is flat. The code's agitated veto also keeps the book flat outside the agitated profile. Inside the regime, the same component is standardised over the 60 bars before it. Its average there is about 0.5, so regime bars read about 15 to 20. It is then negated and passed through `signed_power` (exponent 3, pivot 20). This gives a short of about −8 at the 0.75 edge, growing smoothly to −20 with the close at the low. The forecast is never positive and is zero outside the situation.
Config: 077-02_agitated-low-close-week-fall_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 7 bars
- Main measure: The unusual move of the cases. A case is a short bet (a fall of the forecast of at least 2 points), read once per cell of the non-overlapping 7-bar grid in each window. For each case, take the coin's 7-bar return minus its normal 7-bar drift (holding the coin, all windows together), in the short direction. Report the mean and its t, with cases on the same day summed into one piece of evidence.
- Supporting check: Among the cases, the mean unusual move of the half with the larger |forecast| (closes nearer the low) exceeds that of the smaller half.
- Confirm: The mean unusual move is positive (a fall beyond drift) with t ≥ 2, and the supporting check passes.
- Reject: The mean unusual move is negative (the coin does better than its drift after low closes) with t ≤ −2.
- Inconclusive: Any t between −2 and 2, or a confirming t with a failed supporting check. Fewer than 30 distinct case days is also inconclusive, whatever the t.
