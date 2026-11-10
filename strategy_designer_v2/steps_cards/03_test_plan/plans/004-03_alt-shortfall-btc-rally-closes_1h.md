---
idea: 004-03_alt-shortfall-btc-rally-closes
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: altcoin rises less than bitcoin's sharp up move in the same bar -> replaced: needs bitcoin's bars alongside the altcoin's, which one-coin config cannot see
- Comparison: altcoin move against the move bitcoin's return implies -> replaced: needs a cross-coin relation outside the coin's own bars
- Outcome: altcoin rises over following bars, closing the shortfall -> kept
- Verdict transfer: no: no single-coin forecast measures the altcoin's shortfall versus bitcoin, so neither result would bear on the idea
Reason: The idea's situation and comparison need bitcoin's return and an altcoin's return on the same bar. A config sees only one symbol's own bars and feeds, and the guide says another coin's prices are data it cannot express. The run also covers only BTC/USDT, so there is no altcoin to test.
