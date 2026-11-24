---
idea: 031-02_extreme-fall-partly-rebounds
brief: 031_medium-term-overreaction-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: a coin's 90-day return stands below its own usual 90-day move -> adapted: a regime holds the position only while the 90-day return is at or below minus one usual 90-day move, and the size grows with the depth of the fall.
- Comparison: against its own usual 90-day move, from its own past volatility -> kept: the usual move is the mean absolute 90-day return over the past 365 days.
- Outcome: price rebounds over the next 30 days -> kept: long, held 30 daily bars, judged against holding the coin.
- Verdict transfer: yes: the test bets long only in the idea's situation and sizes by the idea's own scaled fall, so its result answers the idea both ways.
Forecast: The indicator is the 90-day return divided by the mean absolute 90-day return over the last 365 days, which is the fall counted in usual 90-day moves. The regime detector selects `mean_reversion` only while this value is -1 or lower. On all other bars the forecast is 0 (flat). Inside the regime, the same value is standardised over its past 455 values and negated, so the forecast is positive and grows with the depth of the fall. It is then clipped at 0 so it can never go short, and squared through `signed_power` (exponent 2, pivot 10) so that falls only just past the edge are damped and the deepest falls are amplified, up to the cap of 20.
Config: 031-02_extreme-fall-partly-rebounds_1d_config.json
Criterion:
- Horizon: 30 bars
- Main measure: Use grid cells at bars 0, 30, 60, 90 of each window where the forecast is above 0. For each, take the coin's 30-day return from that close minus the coin's mean 30-day return over all its windows. Report the mean, with a t that clusters cases from the same day.
- Supporting check: Split the in-regime cases at the median forecast. The cases above the median must have a higher mean excess 30-day return than those below it (larger minus smaller above 0).
- Confirm: The mean excess return is above 0 with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean excess return is below 0 with t ≤ -2 over at least 30 cases: deep falls keep falling more than usual.
- Inconclusive: Any t between -2 and 2, a confirm without the supporting check, or fewer than 30 in-regime cases.
