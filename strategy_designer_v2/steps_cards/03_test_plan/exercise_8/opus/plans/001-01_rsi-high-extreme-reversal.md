---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Use the 14-period Wilder RSI on daily bars, taken as (50 - RSI) through RSIPullbackComponent. Divide it by the mean absolute value of its previous 60 readings and multiply by 10 (standardise, capped at ±20). Apply signed_power with exponent 2 and pivot 10, so moderate readings shrink smoothly toward 0 and large ones grow. Then clip at a maximum of 0, so only the short side remains. The forecast is zero whenever RSI is at or below 50. It turns negative (short) when RSI is above 50, and the short grows roughly with the square of how far RSI sits above 50 relative to its own recent typical distance. A reading about as far from 50 as usual gives -10, which is 100% short. Readings near RSI 70 or higher reach the -20 cap, which is 200% short. The forecast is never positive.
Config: 001-01_rsi-high-extreme-reversal_config.json
Confirm: The test uses a 5-bar horizon and pools 3 coins × 6 windows. Take the bars where the forecast is ≤ -10, keep only non-overlapping ones (at least 5 bars apart, giving at least 20 such observations), and measure the coin's mean forward 5-bar return after them. The idea is confirmed if that mean is negative and at least 1 percentage point below the mean of all non-overlapping 5-bar returns on the same windows (the hold-the-coin baseline), before costs. Supporting check: the same sign of difference holds in at least 2 of the 3 coins.
Reject: The idea is rejected if the pooled mean forward 5-bar return after forecast ≤ -10 is at or above the unconditional 5-bar mean. It is also rejected if it is higher than the unconditional mean in at least 2 of the 3 coins, meaning price continues or behaves as usual after high RSI.
Inconclusive: The result is inconclusive in three cases: the conditional mean is below the baseline by less than 1 percentage point; it is below the baseline by more but in fewer than 2 of 3 coins; or there are fewer than 20 non-overlapping observations with forecast ≤ -10.
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, short sized by the square of its standardised distance from 50". The position closes as soon as RSI falls back to 50, not over a fixed set of following bars. "Extreme" is judged against RSI's own recent typical distance from 50 rather than a fixed level such as 70. The low-extreme (long) side of the brief is not tested.
