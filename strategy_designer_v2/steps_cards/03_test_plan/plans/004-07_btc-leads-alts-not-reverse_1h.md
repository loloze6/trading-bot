---
idea: 004-07_btc-leads-alts-not-reverse
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a bitcoin return at a bar -> replaced: the config sees only one coin's own bars, so a BTC/USDT run cannot pair bitcoin's return with altcoin returns.
- Comparison: BTC-to-alt lead against alt-to-BTC lead -> replaced: both directions need altcoin bars, and the config cannot see another coin.
- Outcome: later altcoin returns in bitcoin's direction -> replaced: altcoin prices are not in the bitcoin coin's bars or data feeds.
- Verdict transfer: no: any single-coin forecast on BTC alone measures bitcoin's own autocorrelation, not a cross-coin lead-lag.
Reason: The idea relates one coin's returns to another coin's later returns, in both directions. A config sees only its own symbol's bars and feeds and has no cross-symbol input, so it cannot measure either the lead or the comparison.
