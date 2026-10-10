## Your lens: the forecast

What does the forecast know, and when? Where (hour, past move, trailing volatility, forecast
size) does its rank against forward returns rise or vanish, at which horizon, and why would the
market pay for that? What you find about the market stays your evidence: turn it into a claim
about a strategy that uses the forecast differently, through its vehicle (a gate, a band, a
horizon, a smoothing of the forecast), with the test its own run must pass. You are not asked
whether this strategy is profitable.

The forecast's rank IC over all bars is already tested by the run's protocol: a claim test with
`selector: {kind: all}` and `statistic: rank_ic` is refused. A claim on part of the bars (an
hour, a regime, a past move, a forecast quantile) says only what its test measures: "the rank
IC is positive in these hours" is not "stronger in these hours than in the others", and when
the rank IC is already positive over all bars, positive on a slice adds nothing.
