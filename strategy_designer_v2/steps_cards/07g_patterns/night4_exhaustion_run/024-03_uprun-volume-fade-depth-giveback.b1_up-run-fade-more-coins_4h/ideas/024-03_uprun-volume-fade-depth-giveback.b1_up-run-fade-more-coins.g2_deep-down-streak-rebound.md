---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins
line: 7.g patterns
backtest: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: After an unbroken streak of falling four-hour periods, the coin rises over the next 3 days, and the rise grows with the streak's loss measured in the coin's typical four-hour moves over the past 30 days.
Consequence: A trader buys the coin after a long, deep unbroken four-hour sell-off, sized by how many usual moves it lost, rather than shorting it.
Why:
- F3: The largest down-streak losses are followed by a 3-day rise. The largest quintile of down streaks (mean −4.85 usual 4h moves) gives +1.28 % drift-adjusted (t +4.04, 1050 cases), against −0.50 % to −0.87 % in the three smallest quintiles. The joint regression keeps the slope (−0.0029 per usual move of loss, t −4.33), and the mean is positive on every coin (share 1.0). It is uneven by year: +4.98 % in 2020 (t 5.52), +4.15 % in 2024 (t 4.69), and negative in 2018 and 2021.
- F4: The past 1-day move on its own adds nothing once volume and the down-streak loss are in the regression. Alone, its lowest quintile gives +0.94 % (t +4.88), but its joint coefficient is −0.0001 (t −0.41).
