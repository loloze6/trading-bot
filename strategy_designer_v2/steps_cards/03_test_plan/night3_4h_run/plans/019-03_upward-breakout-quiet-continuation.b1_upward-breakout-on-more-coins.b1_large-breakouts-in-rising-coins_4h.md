---
idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: ad5059559106
---
Fidelity:
- Situation: a 4h close above the highest high of the preceding two-day stretch -> adapted: the on/off break becomes graded, as the percent clearance over the prior 12-bar high, and is zero at or below that high.
- Comparison: only while the 30-day return is positive, and the further the close clears the high, the larger the rise -> kept: a regime rule on the 180-bar return above 0, with the position growing with the clearance.
- Outcome: the coin rises over the next three days -> kept: a long held for 18 bars.
- Verdict transfer: yes: the test measures the graded breakout, gated by the positive 30-day trend, against the 3-day rise that follows.
Forecast: The regime is `trending` while the 180-bar (30-day) close-to-close return is above 0, and flat (`unknown`, null) otherwise. In `trending`, the forecast is the percent distance of the close from the highest high of the prior 12 bars, with bar t excluded. It is standardised over the 60 values before the bar and then clipped at 0, so it stays long-only. It is 0 whenever the close is at or below the stretch's high or the 30-day return is not positive. It is positive on a breakout and grows linearly with how far the close clears that high, up to the cap of 20.
Config: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Each case is a bet (a forecast rise of at least 2 points), read once per cell of the 18-bar grid of each window. For each case, take the coin's 18-bar return from the bet's bar, minus the coin's normal 18-bar drift over all windows. Test the mean of this excess return over all cases, before costs, with the ordinary t of the mean.
- Supporting check: Split the cases at the median forecast. The mean excess return of the upper half minus that of the lower half must be above 0.
- Confirm: The mean excess return is positive with t >= 2, and the supporting check passes.
- Reject: The mean excess return is negative with t <= -2.
- Inconclusive: Any t between -2 and 2, or t >= 2 with the supporting check failing. Fewer than 30 cases over all coins and windows is inconclusive whatever the t.
