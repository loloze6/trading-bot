---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Config: 001-01_rsi-high-extreme-reversal_config.json
Confirm: For each coin, take the bars with the largest short positions (forecast at -10 or lower, meaning RSI is well above its usual reading). Over the next 1 to 10 days, the before-cost close-to-close return after those bars is lower than the coin's average return over all bars. This should hold in at least two of BTC, ETH and BNB. Across bins of forecast size, the short's before-cost gain relative to holding the coin should grow as the position gets larger.
Reject: In at least two of the three coins, returns after the largest short positions are equal to or higher than the coin's average return over all bars (no difference or continuation), or the gain relative to holding does not grow with position size.
Deviation: The idea says "after RSI reaches a high extreme, price falls back over the following bars." The config tests something different: while RSI(14) is above 50, it holds a short sized by how far RSI is above 50. The signed_power step makes that short small near 50 and large at the extremes. The position shrinks as RSI falls, and nothing holds it for a fixed number of bars after the extreme reading. Only the high-RSI (reversal-down) side is tested; low-RSI readings give a flat position.
