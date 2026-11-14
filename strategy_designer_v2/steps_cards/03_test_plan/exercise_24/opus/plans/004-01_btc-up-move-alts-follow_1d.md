---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: bitcoin makes a sharp up move -> kept: BTC's own past return is in its own bars.
- Comparison: altcoins catch up to the bitcoin move later, not right away -> replaced: no altcoin bars exist in a one-coin config, so it cannot be measured.
- Outcome: smaller altcoins keep rising over the following bars -> replaced: only BTC's own next return could be traded, which is a different quantity.
- Verdict transfer: no: a test that trades BTC after BTC up moves measures BTC's own momentum, not altcoins' lagged response.
Reason: The idea pairs a signal on one coin (bitcoin) with an outcome on other coins (altcoins). The config sees only one symbol's bars, and the run holds only BTC/USDT, so the cross-coin lead-lag cannot be expressed.
