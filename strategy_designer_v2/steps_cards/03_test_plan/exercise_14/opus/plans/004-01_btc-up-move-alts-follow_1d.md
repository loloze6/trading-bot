---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: bitcoin has just made a sharp up move -> replaced: the config runs on one coin's own bars, and a component sees only its own symbol. A bitcoin move would have to come from bitcoin's bars while the position is held in an altcoin, and no component can read another coin's prices. The run's only coin is BTC/USDT, so bitcoin's move could be measured only as BTC's own past return.
- Comparison: the altcoin's response to the bitcoin move, beyond the altcoin's own past returns -> replaced: this needs the altcoin's and bitcoin's returns side by side, two coins in one forecast, which the config cannot express.
- Outcome: smaller altcoins drift up over the following bars -> replaced: the only price traded is BTC/USDT, so the test would measure bitcoin following its own move (time-series momentum), not altcoins catching up.
- Verdict transfer: no: a test of BTC following its own up moves says nothing about whether altcoins lag bitcoin, so neither a confirmation nor a rejection would carry over to the idea.
Reason: The idea links two coins: the signal is bitcoin's move and the traded price is a smaller altcoin. The config sees only one symbol's own bars and feeds, and has no key for another coin's prices. The run also contains only BTC/USDT, so there is no altcoin to observe drifting.
