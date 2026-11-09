---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Config: 005-01_bearish-rsi-divergence-reversal_config.json
Confirm: The idea is confirmed if, across the bars where price sits in the top quarter of its 20-day range, the size of the short predicts the fall that follows, on at least two of the three coins and before costs. Concretely, the mean 10-day forward return after bars with forecast ≤ -5 (new high with weak RSI) must be negative. It must also be lower than both the forward return after near-high bars with forecast above -2 (new high with strong RSI) and the coin's unconditional 10-day return, so that the strategy's equity on active bars rises while buy-and-hold over the same bars falls.
Reject: The idea is rejected if forward returns after the strongest shorts are no lower than after near-high bars with strong RSI, or no lower than the coin's unconditional drift. That means pre-cost P&L on active bars is flat or negative, or does not grow with the size of the short.
Deviation: The config never finds the previous price peak or compares RSI with its value there; the catalogue has no swing-point detection. "New high with RSI lower than at the prior high" becomes "while the close is in the top quarter of its 20-day closing range (a regime), short more the weaker 14-day RSI is relative to its own recent scale". The short is zero when RSI is at its cap of strength and about -13 when RSI is below 50. The short is held only while price stays near the high, so a retrace deeper than the top quarter of the range is not captured. Only bearish divergence at highs is tested: the brief's mirror case at lows is excluded, and the forecast is never positive.
