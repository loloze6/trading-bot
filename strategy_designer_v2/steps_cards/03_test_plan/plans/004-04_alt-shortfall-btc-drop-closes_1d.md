---
idea: 004-04_alt-shortfall-btc-drop-closes
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: an altcoin falls less than bitcoin's sharp down move implies in the same bar -> replaced: the config sees only one coin's bars, so bitcoin's move cannot be read while trading an altcoin, and the only coin in this run is BTC/USDT itself.
- Comparison: the altcoin's move against the move bitcoin's drop implies -> replaced: comparing two coins is outside the config.
- Outcome: the altcoin falls over the following bars and closes the gap -> replaced: there is no altcoin in this run to measure.
- Verdict transfer: no: no config on one coin's bars can measure a gap between an altcoin and bitcoin, so no result would confirm or reject the idea.
Reason: The idea's situation and comparison are an altcoin's same-bar return set against bitcoin's sharp down move. That needs a second coin's prices, and the guide says a component sees only its own symbol's bars and feed columns. The run also covers only BTC/USDT, so the lagging altcoin whose drift is predicted is not in the data.
