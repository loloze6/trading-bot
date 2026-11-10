---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Use the 14-bar Wilder RSI on daily closes, through RSIPullbackComponent (period 14), whose raw value is (50 − RSI) × 0.4. Then apply these steps in order: 1. Standardise it against its own past 60 values (min_periods 20). An average deviation from 50 maps to about 10 forecast points, capped at ±20. 2. Clip at a maximum of 0, so only RSI above 50 counts and gives a short. RSI at or below 50 gives a forecast of exactly 0. 3. Apply signed_power with exponent 2 and pivot 10. Mild readings just above 50 then give near-zero shorts. Readings far above 50 give shorts that grow with the square of the standardised distance, up to the −20 cap (200% short). The forecast is never positive. It is zero when RSI ≤ 50 and grows more negative the higher RSI is pushed.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Confirm: Take the bars whose forecast is in the most negative 20% of all non-zero forecasts, pooled over 3 coins × 6 windows. Over the next 5 bars, their mean close-to-close return must be below the unconditional mean 5-bar return of all bars by a t-statistic of −2 or lower. Overlap is removed by counting each run of consecutive qualifying bars once, using its first bar. The same sign must hold in at least 2 of the 3 coins. Supporting check: the Spearman correlation between the forecast and the next 5-bar return, sampled every 5th bar, is positive.
Reject: The 5-bar forward return after the most negative 20% of forecasts is at or above the unconditional mean 5-bar return, which would mean continuation or no effect. Or it is below that mean in fewer than 2 of the 3 coins.
Inconclusive: The difference is negative but its t-statistic is between −2 and 0. Or the result is significant in the pooled sample but not in at least 2 coins. Or there are fewer than 30 non-overlapping extreme episodes in the pooled sample.
Deviation: The idea says the reversal comes "after RSI reaches a high extreme". The config tests "while RSI is above 50, short in proportion to the squared standardised distance above 50". The position is held during the elevated reading and shrinks as RSI falls, rather than starting at the extreme and being held for a fixed number of bars afterwards. Moderate readings above 50 carry small shorts instead of none. "Extreme" is relative to each coin's last 60 RSI readings, not a fixed level such as 70.
