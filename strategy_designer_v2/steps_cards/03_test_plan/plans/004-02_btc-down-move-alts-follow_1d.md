---
idea: 004-02_btc-down-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin down move -> kept: the BTC/USDT bars can measure it, for example with a short PriceEvolutionComponent.
- Comparison: altcoins against the move bitcoin already made -> replaced: a config sees only one coin, so it cannot set altcoin prices against bitcoin's.
- Outcome: smaller altcoins keep falling over the next bars -> replaced: the only coin in the test is BTC/USDT, so the config can trade only bitcoin's own next move, not the altcoins'.
- Verdict transfer: no: whether bitcoin itself keeps falling after a sharp drop says nothing about whether altcoins lag bitcoin.
Reason: The signal comes from bitcoin and the outcome happens in other coins, but a config sees only one coin's bars and trades only that coin. The test runs on BTC/USDT alone, so no altcoin price is available at all.
