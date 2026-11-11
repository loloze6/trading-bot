---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
---
Fidelity:
- Situation: bitcoin makes a sharp up move -> replaced: the config sees only its own coin's bars, so bitcoin's move would have to be stood in for by the altcoin's own move.
- Comparison: altcoin's response judged relative to bitcoin's earlier move -> replaced: no bitcoin data per coin; the lag relative to bitcoin cannot be measured.
- Outcome: smaller altcoins keep rising over the following bars -> kept: the altcoin's own forward return is in its bars.
- Verdict transfer: no: a test on one coin's own bars measures the coin's own momentum, not a lagged response to bitcoin.
Reason: The situation is bitcoin's move and the outcome is another coin's later return. The config runs on one coin at a time and sees only that coin's bars and feeds. The guide says it cannot read another symbol's prices, so the bitcoin lead cannot be computed.
