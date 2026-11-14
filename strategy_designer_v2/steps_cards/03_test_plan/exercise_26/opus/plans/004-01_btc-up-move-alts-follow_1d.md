---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: bitcoin makes a sharp up move -> replaced: an altcoin config cannot see bitcoin's bars, and only BTC/USDT is in the test.
- Comparison: altcoins have not yet taken on the bitcoin move -> replaced: needs bitcoin's and an altcoin's returns side by side.
- Outcome: smaller altcoins keep rising over the following bars -> replaced: the test only trades BTC, so altcoin prices are never measured.
- Verdict transfer: no: a test on BTC's own bars cannot show whether altcoins follow bitcoin.
Reason: The idea uses bitcoin's move as the signal and an altcoin's later return as the outcome, so it needs two coins at once. The guide says a component sees only its own symbol's bars and feeds, and the test runs only on BTC/USDT, so neither the signal nor the outcome can be measured together.
