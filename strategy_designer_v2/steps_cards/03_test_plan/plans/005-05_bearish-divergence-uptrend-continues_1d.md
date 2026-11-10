---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Active only while the close is at or near a new 20-day closing high, meaning DonchianBreakoutComponent(period 20) is at least 15. That value puts the close in the top 12.5% of its 20-bar closing range. On those bars, forecast = (D + R) / 2, where both parts are standardised over the previous 60 bars: - D is the range position. It is near +15 to +20 at a new high and grows as the close sits closer to the top of the range. - R is 50 − RSI(14, Wilder). It is negative when RSI is strong and rises toward 0 and above as RSI weakens. The forecast is largest and positive (long) when price is at its high while RSI is comparatively weak, which is the divergence. It shrinks toward 0 as RSI strengthens. It turns negative when RSI is very strong at the high, meaning momentum confirms the high and there is no divergence. Off the high it is 0 (flat).
Config: 005-05_bearish-divergence-uptrend-continues_1d_config.json
Confirm: Take the active bars pooled over all coins and windows, and keep the top third by forecast (strongest divergence). Their mean forward 10-bar return must exceed the same coin and window's unconditional mean 10-bar return (buy-and-hold drift) by at least 1 percentage point. The t-stat must be at least 2, computed on non-overlapping 10-bar blocks so overlapping returns count once. As a supporting check, the Spearman correlation between forecast and forward 10-bar return on active bars must be positive.
Reject: The top-third forecast bars' forward 10-bar excess return over buy-and-hold is zero or negative. A t-stat of −2 or lower on non-overlapping blocks also rejects, and it would favour the reversal view instead.
Inconclusive: Either of two results: an excess return that is positive but below 1 percentage point or with a t-stat under 2, or fewer than 30 non-overlapping 10-bar blocks with top-third bars.
Deviation: The idea compares the RSI peak at the new high with the RSI peak at the earlier high ("lower high"). The config cannot compare peaks, so it measures RSI's level relative to its own recent scale while price is at or near a 20-day closing high. "New high" becomes "close in the top 12.5% of its 20-day closing range". The forecast also goes negative when RSI is strong at the high, which is a no-divergence reading the idea makes no claim about. For that reason the criterion is judged on the top third of the forecast.
