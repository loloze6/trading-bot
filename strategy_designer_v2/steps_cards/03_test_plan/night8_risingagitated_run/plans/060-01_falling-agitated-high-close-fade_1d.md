---
idea: 060-01_falling-agitated-high-close-fade
brief: 060_falling-agitated-high-close-fades
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: a falling, agitated market and a daily close near the top of the day's high-low range -> kept: the profile is added by code, and the close's location in the day's range is graded.
- Comparison: the nearer the close is to the high, the larger the fall -> kept: the short position grows with the close's location in the range.
- Outcome: the price falls over the next day -> kept: a short held for 1 bar.
- Verdict transfer: yes: the test bets short in proportion to the same close location, inside the same profile, over the same next day.
Forecast: One component, `CloseLocationInRangeComponent` with `reference` "low". It reads (close − low) / (high − low) for the day: 0 when the close is at the low, 1 when it is at the high. It is standardised against its last 60 values (min_periods 20) and then negated. The forecast is therefore never positive. It is 0 for a close at the day's low, about −10 for a close at the usual location, and down to −20 for a close at the high. The short grows continuously as the close nears the day's high. The book is flat outside the falling agitated profile, which code adds.
Config: 060-01_falling-agitated-high-close-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On bars inside the profile (where `close_loc` is recorded), sort bars by the raw close location (`last_history_value`) into a top group (at least 2/3) and a middle group (1/3 to 2/3). Take each bar's next-day return, close[t+1]/close[t] − 1, within its window, minus the coin's mean daily return over all windows. The measure is the Welch t of the top group's mean minus the middle group's mean.
- Supporting check: Compute the position's mean per-bar gain before costs, minus the position x the coin's mean daily return (the timing part), on bars in a position. It must be above 0.
- Confirm: The top-minus-middle difference has a Welch t of −2 or less, and the supporting check is above 0.
- Reject: The top-minus-middle difference has a Welch t of +2 or more.
- Inconclusive: Any t between −2 and +2 is inconclusive. A t of −2 or less with a timing gain of 0 or below is also inconclusive. The test needs at least 30 bars in each of the two groups; with fewer it is inconclusive.
