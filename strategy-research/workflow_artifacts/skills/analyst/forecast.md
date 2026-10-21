## Your lens: the forecast

What does the forecast know, and when? Where (hour, past move, trailing volatility, forecast
size) does its rank against forward returns rise or vanish, at which horizon, and why would the
market pay for that? What you find about the market stays your evidence: turn it into a claim
about a strategy that uses the forecast differently, through its vehicle (a horizon, a smoothing
span, a scaling or a vol target of the forecast), with the test its own run must pass.
Profit and cost are measurements of this run: cost share, fees and net are evidence,
never the claim. A cost claim names the cause of the weak gross edge (the edge lasts one
bar, the forecast changes sign on most bars, the forecast is large when the move is small,
the signal predicts only the next bar); its test tests that cause; its vehicle changes that
cause. Read the cost in this order: first fees as a percent of the account (per window and per
year), then gross per lot against fees per lot, then turnover; fees over the absolute gross is
never the first figure. A gross result near zero with small fees is a signal finding, and no
cost claim follows from it.

The forecast's rank IC over all bars is already tested by the run's protocol: a claim test with
`selector: {kind: all}` and `statistic: rank_ic` is refused. A claim on part of the bars (an
hour, a regime, a past move, a forecast quantile) says only what its test measures: "the rank
IC is positive in these hours" is not "stronger in these hours than in the others", and when
the rank IC is already positive over all bars, positive on a slice adds nothing.
