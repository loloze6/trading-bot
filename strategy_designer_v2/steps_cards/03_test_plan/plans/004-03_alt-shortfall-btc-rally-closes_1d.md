---
idea: 004-03_alt-shortfall-btc-rally-closes
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: an altcoin rises less than bitcoin's sharp up move implies in the same bar -> replaced: the run's only coin is BTC/USDT, so there is no altcoin, and a config cannot read another coin's bars.
- Comparison: the altcoin's move against the move the bitcoin move implies -> replaced: this needs bitcoin's and the altcoin's returns side by side, and a config sees only one symbol.
- Outcome: the altcoin rises over the following bars, closing the shortfall -> replaced: the only price traded is BTC, not the lagging altcoin.
- Verdict transfer: no: a BTC-only forecast cannot measure an altcoin's shortfall against bitcoin, so its result says nothing about the idea.
Reason: The idea needs two coins at once: bitcoin's move as the driver and an altcoin's return measured against it. A config sees only its own symbol's bars and feeds (the guide lists "another coin's prices" as data the config cannot hold), and the run's only coin is BTC/USDT.
