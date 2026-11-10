---
idea: 004-05_btc-lead-larger-low-volume
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin move -> replaced: the config sees only one coin's bars, so the altcoin's own bars cannot hold bitcoin's move.
- Comparison: low-volume vs high-volume altcoins' follow-through -> replaced: it needs several altcoins ranked by volume, and the config runs on one coin at a time.
- Outcome: altcoin follow-through in bitcoin's direction -> replaced: the test runs on BTC/USDT only, so there is no altcoin price to measure.
- Verdict transfer: no: no config built from one coin's bars can measure the lead from bitcoin to altcoins or how it changes with altcoin volume.
Reason: The idea needs bitcoin's past returns and the forward returns of several altcoins, ranked against each other by volume. The config sees only its own symbol's bars and feeds, and the run covers BTC/USDT alone. The guide says another coin's prices are data a config cannot read.
