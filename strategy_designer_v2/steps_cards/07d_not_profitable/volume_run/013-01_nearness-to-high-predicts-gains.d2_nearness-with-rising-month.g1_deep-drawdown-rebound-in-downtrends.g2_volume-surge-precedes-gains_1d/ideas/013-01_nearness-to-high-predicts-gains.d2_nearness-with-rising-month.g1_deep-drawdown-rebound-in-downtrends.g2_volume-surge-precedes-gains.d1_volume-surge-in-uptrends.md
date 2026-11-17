---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's traded volume over the past day relative to its average over the past 20 days, the higher its return over the next 7 days, only while the coin's own 20-day return is positive.
Consequence: A volume surge would justify a larger long position over the next week while the coin is rising over the past 20 days, and no position while it is falling, which is when the book's deep falls happen.
Why:
- F1: The book fails on its falls, not its gain: it makes 21.0% a year but its deepest fall is −50.6%, so Calmar is 0.42. Its deepest fall episode lasts 426 days across w1–w5 (−46.8%), and the second lasts 440 days across w12–w16 (−40.8%).
- F2: The book barely steps aside in its falls. On bars inside its three deepest falls, the coins' 20-day return averaged −1.5% (against +4.9% outside) and the close sat 26.7% below its 60-day high (against 18.7%). The book still held 0.46 of capital (against 0.52) and earned only 0.00018 a bar (against 0.00139).
- F3: Volume carries both the gain and the losses. The top volume-ratio quintile has the largest position (0.93) and gain (0.0041 a bar), but also the largest summed losses (−45.6 against −7.4 in the bottom quintile). Inside that quintile the gain is 0.00289 when the 20-day return is negative and 0.00493 when it is positive. The middle quintiles lose in downtrends (−0.00034, −0.00016) and earn in uptrends (0.00072, 0.00102).
