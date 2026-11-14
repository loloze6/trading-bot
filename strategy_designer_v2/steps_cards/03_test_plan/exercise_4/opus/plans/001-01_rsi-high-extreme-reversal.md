---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Use a 14-bar Wilder RSI (RSIPullbackComponent, period 14), whose raw value is (50 - RSI) x 0.4. It is negative when RSI is above 50. Each bar, divide it by the mean absolute raw value of the previous 60 bars and multiply by 10 (standardise, window 60, min_periods 20, cap +/-20). Then clip it at a maximum of 0, so only readings above 50 count. Then apply signed_power with exponent 2 and pivot 10. Moderate readings shrink smoothly toward 0, and high readings grow quickly; for example, a standardised -5 becomes -2.5 and -15 becomes -22.5. The combined forecast is then clipped at -20. - When RSI is at or below 50 the forecast is exactly 0, and the position is flat. - When RSI is above 50 the forecast is negative, a short. Its size grows with the square of how far RSI sits above 50, measured against the coin's own recent RSI deviations. The largest shorts come at the high extremes. - The forecast is never positive. It is ungated: it runs on every bar.
Config: 001-01_rsi-high-extreme-reversal_config.json
Confirm: Horizon is 5 bars. Use the "large" bars, where the recorded forecast is -10 or lower, and sample them non-overlapping: after a sampled bar, skip the next 4 bars. Pool these across all 3 coins and 6 windows. For each sampled bar, take the coin's 5-bar forward return minus that window's average 5-bar return (so the coin's own drift is not credited). The idea is confirmed if the mean of these excess returns is negative with t ≤ -2, and (supporting check) the mean is negative in at least 2 of the 3 coins.
Reject: The idea is rejected if, on the same non-overlapping large bars, the mean 5-bar excess forward return is zero or positive. A mean with t ≥ +2 is also rejected, and points to continuation rather than reversal.
Inconclusive: Three cases: the mean is negative but with -2 < t < 0; the pooled t is ≤ -2 but fewer than 2 of the 3 coins are negative; or fewer than 20 non-overlapping large bars exist across all coins and windows.
Deviation: - "After RSI reaches a high extreme" becomes "while RSI is above 50". The short is held and sized only while RSI stays high, so it shrinks as RSI falls back, and part of any retrace that comes after RSI normalises is not held. - "Extreme" is not a fixed level such as 70. It is a deviation that is large relative to the coin's last 60 bars, softened by the squared power. - Low-RSI extremes, the mirror case, are not tested.
