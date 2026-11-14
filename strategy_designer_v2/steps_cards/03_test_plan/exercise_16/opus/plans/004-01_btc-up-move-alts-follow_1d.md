---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: bitcoin makes a sharp up move -> kept
- Comparison: altcoin's later move against bitcoin's earlier move -> replaced: the config sees only one coin's bars, so no second coin is available to compare
- Outcome: smaller altcoins keep rising over the following bars -> replaced: the test runs on BTC/USDT only, and a config cannot read another coin's prices
- Verdict transfer: no: a forecast on BTC's own bars only tests BTC's own momentum, not whether altcoins lag bitcoin.
Reason: The situation is measured on bitcoin and the outcome on other coins, so the idea needs two coins' prices at once. The config sees only one symbol's own bars and feeds, which the guide lists as something it cannot express ("another coin's prices"), and the run covers BTC/USDT alone.
