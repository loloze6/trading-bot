---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its 7-day return, the higher its return over the next 7 days.
Consequence: In a rising month, a strong week is a reason to add to the coin rather than fade it.
Why:
- F1: When a coin's 30-day return was zero or positive, a larger 7-day return came before a larger excess return over the next 7 days (slope 0.142, t 4.35, 894 non-overlapping grid cases). The effect was much stronger in windows w13–w24 (t 4.35, n 399) than in w1–w12 (t 1.12, n 495). It was strongest in XRP (t 2.51) and ZEC (t 2.72), and not stable by year: 2023 went the other way (t −2.54) while 2025 was strongest (t 5.00).
- F5: The tested relation in falling months was only weakly in the idea's direction (7-day return slope −0.057, t −1.49, n 829). The book lost money on average in every coin (for example ETH −0.031% a day against the coin's +0.137%), with a book-to-coin daily correlation of 0.32.
