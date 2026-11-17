---
idea: 013-01_nearness-to-high-predicts-gains.d1_gain-concentrated-at-the-high
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: close near its 52-week (365-bar) high, with the gain rising faster in the last stretch below the high, and larger after a stronger 30-day return -> replaced: no catalogue component or composition gives closeness that steepens near the high and scales with the 30-day return; the config can only add a separate 30-day momentum term.
- Comparison: closes nearer the high against closes farther below it, and stronger months against weaker ones -> kept: a graded forecast ordering bars by closeness and momentum would carry this comparison.
- Outcome: higher coin return over the next 7 days -> kept: 7 bars on daily bars.
- Verdict transfer: no: adding a momentum term and a closeness term in a weighted mean tests neither the steepening near the high nor the claim that closeness pays more after a strong month, so neither a confirm nor a reject would carry to the idea.
Reason: All the idea needs is in each coin's own daily closes, and a component could compute it. The catalogue's DistanceFromHighComponent is linear in depth below the high. signed_power (exponent 1 to 3) can only damp values near zero, so it flattens the response near the high instead of steepening it. Strategies also combine components only by weighted sums, so no composition can make the closeness effect grow with the 30-day return.
