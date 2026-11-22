---
idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: aaeaf3675030
---
Fidelity:
- Situation: an unbroken down-streak of 4h bars with volume declining across it -> kept: the down-streak's loss component, gated by a regime rule on the streak's volume slope above 0.
- Comparison: the streak's loss is several times the typical 4h move over the past 30 days -> adapted: the loss is measured in mean absolute 4h moves over 180 bars, and "several times" becomes a cubic graded dead zone.
- Outcome: the coin rises over the next three days, more after larger relative losses -> kept: an 18-bar long hold, sized by the relative loss.
- Verdict transfer: yes: the measured quantities are those of the idea, and only the threshold is made graded.
Forecast: The forecast is the size of the current down-streak's loss, counted in the coin's mean absolute 4h move over the last 180 bars (DownStreakLossInUsualMovesComponent, window 180, side down, base start). It is standardised over 180 past values and then raised to the power 3 (pivot 10), so ordinary streaks stay near zero and only losses of several usual moves give a real position. It is active only while the streak's volume is fading: a regime rule needs the least-squares volume slope over the streak (DownStreakVolumeFadeComponent, slope) to be above 0. On all other bars the forecast is flat. The forecast is never negative, so the strategy is long only. It is 0 when the last bar did not close down, and it grows steeply with the relative loss.
Config: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: A case is a bet (a rise of the forecast of at least 2 points), read once per cell of a non-overlapping 18-bar grid in each window. For each case, take the coin's 18-bar return from the bet's bar minus the coin's normal 18-bar drift over all its windows. The measure is the mean of this excess return over all cases, with its t.
- Supporting check: Across the cases, the slope of the excess 18-bar return on the bet bar's forecast is positive.
- Confirm: The mean excess 18-bar return is positive with t >= 2, over at least 30 cases, and the supporting slope is above 0.
- Reject: The mean excess 18-bar return is negative with t <= -2, over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a slope at or below 0 is also inconclusive. Fewer than 30 cases across all coins and windows is inconclusive.
