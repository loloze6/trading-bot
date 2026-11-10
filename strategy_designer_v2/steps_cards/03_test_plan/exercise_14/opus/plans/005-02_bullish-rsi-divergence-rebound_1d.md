---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price closes at a new low below its previous swing low, while RSI(14) at this low is higher than RSI was at that previous low (bullish divergence) -> adapted: the new-low part can be read graded with `DonchianBreakoutComponent` (close at the bottom of its range), held "while" rather than "at" the low. The RSI-higher-low part cannot be built (see comparison).
- Comparison: RSI at the current price low judged against RSI at the previous price low -> replaced: the catalogue can only give the current RSI level (`RSIPullbackComponent`) or that level against RSI's own past distribution. Neither reads RSI on the bar of the previous price low, so this part would have to be swapped for "price low while RSI is not oversold", which is a different quantity.
- Outcome: price rebounds afterwards and recovers part of the decline into the low (long, up) -> kept: a long forecast while the divergence is present, with forward returns judged against holding the coin.
- Verdict transfer: no: with the comparison replaced, a test of "low price, non-extreme RSI" could confirm or reject without saying anything about RSI making a higher low than at the previous price low.
Reason: A bullish divergence needs RSI's value on the bar of the previous swing low in price, compared with RSI now. Both come from the coin's own closes and a per-bar forecast could hold the result. But no catalogue component, alone or combined through weights, negation, offsets or history ops, finds the previous price low and reads RSI there. The only compositions available, such as Donchian position combined with RSI level, or RSI against its own history, measure something else.
