---
idea: 041-02_wide-down-day-next-day-rebound
brief: 041_wide-range-days-reverse-next-day
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: f9d41455da54
---
Fidelity:
- Situation: a down-closing day, graded by its high-to-low range in units of its 30-day daily-return swing -> kept: the down close is a regime condition, and the range over the 30-day return std grades the position inside it.
- Comparison: the range measured against the coin's 30-day daily-return swing -> kept
- Outcome: the coin rises over the next day, more the wider the range -> kept: long for 1 bar, sized by the range in swing units.
- Verdict transfer: yes: the book is long only after down closes, sized by the range in swing units, and is judged on the next day's return.
Forecast: The forecast is non-zero only on bars whose close is below the prior close; the regime detector reads the 1-bar return in percent and requires it to be below 0. On those bars the forecast is long and equals that day's (high − low) / close divided by the std of the last 30 daily returns (`RangeInReturnStdComponent`, vol_period 30), standardised against its own last 60 values. A day of usual width gives about +10. A wider day gives more, up to +20, and a narrow day gives less. On up or flat closes the forecast is 0. It is never negative.
Config: 041-02_wide-down-day-next-day-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Use the bars with forecast > 0, every such bar being one 1-bar case. Regress the next day's return minus the coin's mean daily return over all its windows on the forecast (post_pipeline_value of range_swing). The measure is the slope's t.
- Supporting check: The mean of that next-day excess return over the same cases is above 0.
- Confirm: The slope's t is ≥ +2 and the mean next-day excess return over the cases is > 0.
- Reject: The slope's t is ≤ −2, so the rebound shrinks or reverses as the range widens.
- Inconclusive: A slope t between −2 and +2 is inconclusive, and so is a t ≥ 2 with a mean excess return ≤ 0. At least 300 cases are needed across coins and windows; with fewer, the result is inconclusive.
