---
idea: 044-02_agitated-down-day-range-rebound
brief: 044_agitated-wide-range-fall-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 0e977cd77240
---
Fidelity:
- Situation: in an agitated market, a day the coin closes lower -> kept: the down close is a regime (close below the prior close), and the agitated profile is added by code.
- Comparison: that day's high-to-low range against its average daily range over the past 30 days -> kept: the day's range over the 30-bar mean bar range, which includes that day.
- Outcome: the coin rises over the next day, more the wider the range -> kept: a long position held one bar, sized by the range multiple.
- Verdict transfer: yes: the forecast is long only on agitated down days, in proportion to the day's range multiple, and is judged on the next day's return.
Forecast: On a bar whose close is below the prior close (the regime `mean_reversion`), the forecast is long. Its size is the bar's high-to-low range divided by the mean high-to-low range of the last 30 bars (`RangeCompressionRatioComponent`, `short_period` 1, `long_period` 30, `base` "mean_bar_range", `form` "width"). It is standardised against its own past 60 values, so a day of usual width gives about +10, a day twice as wide gives about +20 (the cap), and a narrow day gives a small long. On bars that close flat or up the forecast is 0. Outside the agitated profile it is also 0, a rule the code adds. It is never negative.
Config: 044-02_agitated-down-day-range-rebound_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Over the cases (bars with forecast > 0), the mean of forecast/10 x (the coin's next-bar return minus its mean daily return over all its windows). This is tested with a t that takes the cases of one day together.
- Supporting check: The mean next-bar excess return of the wider-range half of cases minus that of the narrower half, split at the median range multiple of each coin. It must be above 0.
- Confirm: The main measure has a t of 2 or more and the wide-minus-narrow difference is above 0.
- Reject: The main measure has a t of -2 or less, or the wide-minus-narrow difference has a Welch t of -2 or less.
- Inconclusive: Any other result is inconclusive, including a main t between -2 and 2, or a main t of 2 or more with the difference at or below 0. At least 200 cases on at least 100 distinct days are needed; with fewer, the result is inconclusive.
