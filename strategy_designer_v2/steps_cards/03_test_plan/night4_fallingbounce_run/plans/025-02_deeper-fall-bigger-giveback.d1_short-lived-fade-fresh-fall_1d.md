---
idea: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: 90-day return negative, 30-day return also negative, and a one-day rise of several usual daily moves -> adapted: both negative returns are a regime condition, and "several usual daily moves" becomes a graded rise in usual moves with a strong dead zone
- Comparison: none -> kept
- Outcome: a larger fall over the next 2 days, the larger the one-day rise -> kept
- Verdict transfer: yes: the test shorts in proportion to the rise only inside the double-fall condition and judges the 2-day move that follows.
Forecast: The regime is active only while both the 90-day and the 30-day percent returns are below zero. On every other bar the forecast is 0. Inside the regime, the forecast is built from today's one-day return divided by the standard deviation of the last 20 daily returns, in four steps: - It is standardised against its last 60 values. - Falls are clipped to 0, so only rises count. - It goes through signed_power with exponent 3 and pivot 20, the strongest graded dead zone allowed. A rise of about one usual move gives a forecast of about 5. A rise of about 1.6 moves or more reaches the full 20. - It is negated. So the forecast is never positive. It is zero on down days and outside the regime, and the short grows steeply with the size of the bounce.
Config: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are short bets: a fall of the forecast of at least 2 points, read once per non-overlapping 2-bar grid cell of each window. For each case, take the coin's 2-bar return from the close of the signal's bar, minus the coin's mean 2-bar return over all windows, with its sign flipped so a fall counts as a gain. The measure is the mean of these values weighted by abs(forecast), with its t-statistic. All coins are pooled, before costs.
- Supporting check: Split the cases at the median abs(forecast). The mean short-direction unusual move of the larger half, minus that of the smaller half, must be above 0.
- Confirm: The main measure has a t of 2 or more over at least 30 cases, and the supporting check passes.
- Reject: The main measure has a t of -2 or less over at least 30 cases, meaning the bounces kept rising beyond the coin's drift.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming t whose supporting check fails, and so is any result from fewer than 30 cases.
