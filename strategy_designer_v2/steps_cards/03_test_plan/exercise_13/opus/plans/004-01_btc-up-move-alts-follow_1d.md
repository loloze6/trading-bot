---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: bitcoin makes a sharp up move over recent bars -> kept (the BTC/USDT bars hold bitcoin's own returns, e.g. `PriceEvolutionComponent`)
- Comparison: altcoin returns judged against bitcoin's earlier move, with the altcoin's own past returns accounted for -> replaced: no config can hold an altcoin's returns next to bitcoin's, because a component sees only its own symbol's bars
- Outcome: smaller altcoins drift up over the following bars -> replaced: the only price the test can trade and score is BTC/USDT itself, so the outcome would become bitcoin's own continuation, a different claim
- Verdict transfer: no: a test on BTC/USDT alone would only measure bitcoin's own momentum after a sharp up move, which says nothing about whether altcoins lag bitcoin.
Reason: The idea links one coin's move (bitcoin) to the later returns of other coins (altcoins). The config sees only one symbol's bars and feeds, and the guide says other coins' prices cannot be expressed. The test runs only on BTC/USDT, so the altcoin outcome cannot be measured or traded.
