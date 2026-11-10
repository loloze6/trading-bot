---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin up move -> kept: BTC's own recent return can be measured from BTC bars.
- Comparison: altcoin response against the earlier bitcoin move -> replaced: the altcoin bars are not in the BTC config, which sees only its own coin.
- Outcome: altcoins drift up in the following bars -> replaced: only BTC's own next return can be traded on BTC/USDT.
- Verdict transfer: no: a test on BTC alone only checks BTC momentum, which says nothing about altcoins catching up.
Reason: The idea's outcome is the later return of other coins (altcoins) after a bitcoin move. A config sees only one coin's own bars and feeds and cannot read bitcoin while trading an altcoin, and the run is BTC/USDT only.
