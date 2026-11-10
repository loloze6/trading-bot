---
idea: 004-04_alt-shortfall-btc-drop-closes
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: altcoin fell less than BTC's sharp down bar implies -> replaced: the config sees only one coin's bars, so it cannot see the BTC move and the altcoin's together.
- Comparison: altcoin move vs the move implied by BTC -> replaced: no BTC series sits beside the altcoin bars, and the run's only coin is BTC/USDT.
- Outcome: altcoin falls over the next bars, closing the gap -> kept: this is the altcoin's own later return, which its bars hold.
- Verdict transfer: no: no single-coin forecast can measure the gap between BTC and an altcoin, so no result here would speak to the idea.
Reason: The idea's situation and comparison need bitcoin's same-bar return next to an altcoin's return, which means a second coin's prices. The config sees only one symbol's bars and feeds, and the guide names "another coin's prices" as data it cannot use. The run is also on BTC/USDT alone, so there is no altcoin to test.
