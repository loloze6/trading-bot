---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Config: 005-01_bearish-rsi-divergence-reversal_config.json
Confirm: On bars where the forecast is negative (close in the top 5% of its 20-day range with RSI below 50), the largest short positions should be followed by 5 to 10 day returns clearly below that coin's unconditional average return. Short-side gains should also grow with position size across position-size buckets, and be positive before costs on BTC, ETH and BNB.
Reject: Returns after the largest short positions are equal to or above the coin's unconditional average, or the short side loses money before costs, so that bars at new highs with weak RSI do no worse than other bars. Gains that do not grow with position size also reject it.
Deviation: The config does not compare the RSI at the new high with the RSI at the previous price high. It tests "close in the top 5% of its 20-day range while RSI sits below 50, shorting more as RSI weakens". A new high is approximated by the range position, and divergence by absolute RSI weakness. The position is held only while the condition lasts and is flat otherwise, and it is short-only (only the bearish divergence is tested). The reversal is measured as forward returns and the position, not as a retracement of the run-up.
