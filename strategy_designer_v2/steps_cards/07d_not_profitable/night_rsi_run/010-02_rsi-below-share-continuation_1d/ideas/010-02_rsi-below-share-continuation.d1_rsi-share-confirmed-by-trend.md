---
brief: 010_rsi-midline-regime-direction
source-idea: 010-02_rsi-below-share-continuation
line: 7.d not profitable
backtest: 010-02_rsi-below-share-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 30 days that a coin's 14-day RSI has spent below its midpoint of 50, the lower the coin's return over the next 14 days, and the more so the further the coin's own 30-day return lies on the same side as that RSI share (falling for a large share below, rising for a small one).
Consequence: Size a short on RSI time-below-50 up only as the coin's 30-day price move confirms the decline, and size it down when the coin has been rising; this cuts the shorts held into rallies that dug the deepest falls.
Why:
- F1: The Calmar fails (0.577 = a 30.6% yearly return over a 53.0% deepest fall) because of one 413-day fall across w2–w5 (2022), during which the coins' summed daily moves were +0.77 while the book was short on 54% of days with a mean position of only 0.04; the next falls, -44.2% (w19–w20) and -43.4% (w16–17), also had the book short on about half their days (48% and 60%).
- F2: The short side carries almost none of the book's gain: short coin-days earn a mean of 0.000189 per day (n=2866) against 0.001857 for long coin-days (n=2793), with similar spread (std 0.0245 against 0.0270).
- F3: Shorts held while the coin's 30-day return is in its highest third lose 0.0011 per day (n=182) and earn 0.0011 per day in its lowest third (n=1242); longs earn 0.0024 per day in the highest third (n=1251) against 0.0011 in the lowest (n=180), so the book pays when the RSI side and the 30-day move agree.
- F5: Shorts held after the highest third of the 7-day return lose 0.00115 per day (n=780) and earn 0.00053 after the lowest third (n=992).
- F6: The short side lost in five of eight years, worst in 2020 (-0.00375 per day, n=205); it gained only in the falling years 2018, 2022 and 2025, while the long side lost only in 2018 and 2022 (-0.00237 per day, n=131).
