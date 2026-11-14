---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin up move -> kept: bitcoin's recent return is in BTC/USDT's own bars.
- Comparison: the altcoin's response against the bitcoin move -> replaced: the config sees only one coin's bars, so it cannot compare one coin's move with another's.
- Outcome: smaller altcoins drift up over the following bars -> replaced: the only tradable price is bitcoin's, not an altcoin's.
- Verdict transfer: no: a test on BTC/USDT alone can only show bitcoin following its own move, which says nothing about altcoins catching up.
Reason: The situation is measured on bitcoin, but the outcome is an altcoin's later return. A config sees only its own symbol's bars and cannot read another coin's prices, so it cannot link one coin's move to another's. The run also covers only BTC/USDT, so no altcoin is ever traded.
