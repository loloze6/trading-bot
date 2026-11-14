---
idea: 004-03_alt-shortfall-btc-rally-closes
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: an altcoin rises less than bitcoin's sharp up move in the same bar -> replaced: the config sees only the coin's own bars, and the test coin is BTC itself, so no bitcoin move exists in an altcoin's data.
- Comparison: the altcoin's move against the move bitcoin's rise implies -> replaced: this needs another coin's prices, which no component or feed carries.
- Outcome: the altcoin rises later and closes the gap -> adapted: it would be the coin's forward return while a gap is open, but the only coin here is BTC.
- Verdict transfer: no: a config on BTC alone cannot measure an altcoin's shortfall against BTC, so no result would confirm or reject the idea.
Reason: The idea's situation and comparison are the gap between an altcoin's return and bitcoin's return in the same bar. That needs a second coin's prices, and the guide says a component sees only its own symbol's bars and feed columns. The run is also on BTC/USDT only, so the altcoin whose lag is the subject is not tested at all.
