---
idea: 060-01_falling-agitated-high-close-fade
brief: 060_falling-agitated-high-close-fades
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a falling, agitated market, a close near the top of the day's high-low range -> adapted: a regime holds only closes in the upper half of the day's range (conventional level), and the profile is added by code.
- Comparison: the nearer the close sits to the day's high, the larger the fall -> kept: the short grows from 0 at mid-range to its largest at the day's high.
- Outcome: the price falls over the next day -> kept: a short held for 1 daily bar.
- Verdict transfer: yes: the test measures next-day falls after high closes in the named profile, sized by how near the close is to the high.
Forecast: The forecast uses the day's signed close location, (2 x (close − low) / (high − low) − 1), from DonchianBreakoutComponent with period 1, source high_low and exclude_current 0. This value is 0 at mid-range and +20 at the high. The regime detector selects a regime only when this location is 0 or above, so the close is in the upper half of the range. Inside that regime the location is standardised over 60 bars, clipped at 0 and negated. The forecast is therefore 0 at mid-range and becomes a larger short as the close nears the day's high, capped at -20. It is never positive. It is 0 on lower-half closes and outside the falling-agitated profile, which code adds.
Config: 060-01_falling-agitated-high-close-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: A case is a bar with a forecast below 0. For each case, take the coin's next-day return minus its mean daily return over all windows, with the sign flipped for the short. Report the mean of this excess and its t, with cases on the same day summed into one piece of evidence.
- Supporting check: Split the cases at the median of the absolute forecast. The mean short-side excess of the larger half minus that of the smaller half must be above 0.
- Confirm: The idea is confirmed when the mean short-side excess is above 0 with t of 2 or more, and the supporting check is also above 0.
- Reject: The idea is rejected when the mean short-side excess is below 0 with t of -2 or less.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming main measure whose supporting check is not above 0. The test needs at least 100 cases on at least 100 distinct days; fewer is inconclusive.
