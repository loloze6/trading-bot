---
idea: 004-06_btc-lead-larger-wide-range
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin move, seen from an altcoin's bars -> replaced: a config sees only its own coin, so on another coin it cannot read bitcoin's move.
- Comparison: altcoins with wide ranges against altcoins with narrow ranges -> replaced: this is a comparison across coins, and the config runs on each coin separately.
- Outcome: the altcoin follows bitcoin's direction over the next bars -> replaced: the test runs on BTC/USDT only, so no altcoin's return is measured.
- Verdict transfer: no: a test on bitcoin's own bars cannot confirm or reject a lagged link between bitcoin and altcoins.
Reason: The idea's situation is bitcoin's move, and its outcome is a different coin's later return, ranked across coins by bar range. The config sees only one symbol's bars and feeds, has no cross-coin comparison, and the run covers only BTC/USDT.
