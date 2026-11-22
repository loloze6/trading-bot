---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next six hours. The higher that hour's volume against its 30-day average, the larger the further rise.
Consequence: A sharp hourly rise on a volume surge is a reason to go long for six hours and never to fade it, while a rise on ordinary volume gives no edge either way.
Why:
- F5: Hours that rise more than 2.5 usual moves continue over 6 hours only on surging volume, and the continuation grows with volume:
- F2: The fade the book bets on is not in the data, and no change of holding or sizing can make it pay. The unusual move is +0.02 % per case over 6 hours (strength 0.011, 12,052 cases), and the total move is -0.01 %, against a cost of 0.11 % per trade. Up-hours of 2.5 to 4 usual moves on volume 0.5 to 1.5 times average end 0.06 % lower than drift, not higher (t -0.47, n 209). Those of 1.5 to 2.5 usual moves end +0.01 % (t 0.17, n 704). Trades entered on the larger forecasts lose more (-0.38 % against -0.18 % before fees), and the step-5 size check difference is -0.0018 %.
- F1: The book loses before any fee. Its gross bar returns sum to -3.17 against 7.72 in fees over 140,090 bars. All 19,983 trades are short and lose a mean of 0.33 % before fees and 0.43 % after. The book's mean daily return is -0.18 % (standard deviation 2.44 %), while holding the coins earned +0.13 % a day, so the always-short book also pays the coins' rise.
