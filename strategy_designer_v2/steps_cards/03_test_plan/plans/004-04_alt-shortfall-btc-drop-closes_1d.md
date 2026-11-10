---
idea: 004-04_alt-shortfall-btc-drop-closes
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: altcoin falls less than bitcoin's sharp down move implies -> replaced: the config sees only one coin's bars, so it has no bitcoin return to compare against.
- Comparison: the altcoin's move against the bitcoin-implied move -> replaced: the bitcoin move needs another coin's data, which the config cannot read.
- Outcome: the altcoin falls over the following bars to close the gap -> kept: the forward return of the traded coin can be measured.
- Verdict transfer: no: without bitcoin's move, a confirm or a reject says nothing about the gap closing.
Reason: The idea needs bitcoin's return next to the altcoin's on the same bar, but the config sees only one coin's own bars and feeds. The test also runs only on BTC/USDT, so there is no altcoin whose lagged response could be measured.
