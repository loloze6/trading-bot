---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: The forecast is active only on bars where the close is at or very near its 20-day closing high, meaning the close sits in the top 2.5% of the range of the last 20 closes. On every other bar it is 0. On an active bar it is short, sized by how weak the 14-day Wilder RSI is. R is RSI strength (RSI − 50), divided by its own mean absolute value over the previous 60 bars, times 10, then held between 0 and 10. The forecast is (R − 10) / 2. It is 0 when RSI is at or above its usual strength, and it grows toward −5 (50% short) as RSI falls toward 50 while price is at the high. It is never positive.
Config: 005-01_bearish-rsi-divergence-reversal_config.json
Confirm: Pool all coins and windows. Take the new-high bars (recorded Donchian value ≥ 19) and keep one bar per cluster, with clusters at least 10 bars apart so overlapping returns count once. On these bars, the mean 10-bar forward close-to-close return after divergence bars (forecast < 0) is negative and at least 2 percentage points below the mean after non-divergence new-high bars (forecast = 0). This needs at least 20 divergence episodes and a one-sided permutation p < 0.05. Supporting check: across the divergence bars, the Spearman correlation between forecast and the 10-bar forward return is positive, so larger shorts are followed by weaker returns.
Reject: With at least 20 divergence episodes, the 10-bar forward return after divergence new highs is not below the return after non-divergence new highs (difference ≥ 0). Or it is lower by less than 0.5 percentage points with permutation p > 0.3.
Inconclusive: Fewer than 20 independent divergence episodes. Or a difference between −0.5 and −2 points, or below −2 points with p ≥ 0.05. Or results that point in opposite directions on different coins with no pooled significance.
Deviation: "RSI makes a lower high than at the previous price high" becomes "RSI is weaker than its usual absolute deviation from 50 while the close is at its 20-day high". No comparison with RSI at the previous peak is made, because the catalogue has no rolling RSI maximum. "New high" means the close is in the top 2.5% of the 20-day close range, not a new swing high. The short is held only while price stays at the high. The retracement that follows is measured from the recorded price over 10 bars, not earned by the position. Only the bearish side is tested.
