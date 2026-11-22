---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, and the larger the streak's loss relative to the coin's typical four-hour move over the past 30 days, the larger the rise, only while the coin's 7-day return is positive, the rise growing the higher that 7-day return.
Consequence: A fading-volume sell-off is a reason to buy only as a dip inside a rising week, and a reason to stay out when the week is already falling, which is where the book's falls carry no gain.
Why:
- F1: The book's deepest fall was -57.1 % over 83 days across w16–w17, deeper than holding the coins over the same days (-43.9 %). The book's daily returns move with holding's (correlation 0.86), and on its worst 5 % of days the book lost -6.6 % while the coins lost -8.5 %. Its falls are the market's falls, which gives the failing Calmar of 0.33.
- F3: Bars held after a low 30-day return pay nothing but carry full risk. The book's mean bar gain in the lowest 30-day-return quintile is +0.000009 (t 0.06, n 12279, sd 0.0160) and in the second -0.00020 (t -1.56). In the highest quintile it is +0.00065 (t 4.08, n 12400), and the 7-day return shows the same pattern (lowest quintile +0.00014, t 0.88; highest +0.00062, t 4.07).
- F4: The rebound shows only after a strong prior week. Cases in the highest 7-day-return quintile have an unusual 18-bar move of +1.63 % (t 1.58, n 102) and the second-lowest -0.89 % (t -1.34, n 124). By 30-day return, the highest quintile is +1.60 % (t 1.19, n 75) and the middle ones are about -0.27 %.
