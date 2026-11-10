---
idea: 004-02_btc-down-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin down move -> kept: the move is in BTC/USDT's own bars, which is the coin the test runs on.
- Comparison: none -> kept
- Outcome: altcoins keep falling over the following bars -> replaced: a config sees only one coin's bars, so on BTC/USDT it could only measure bitcoin's own next return.
- Verdict transfer: no: bitcoin's own drift after its drops says nothing about whether altcoins catch up later.
Reason: The idea links one coin's move (bitcoin) to another coin's later returns (altcoins), but each config sees only one coin's own bars and feeds. The test also runs on BTC/USDT alone, so no altcoin outcome can be observed, and a config cannot read bitcoin's bars while trading an altcoin.
