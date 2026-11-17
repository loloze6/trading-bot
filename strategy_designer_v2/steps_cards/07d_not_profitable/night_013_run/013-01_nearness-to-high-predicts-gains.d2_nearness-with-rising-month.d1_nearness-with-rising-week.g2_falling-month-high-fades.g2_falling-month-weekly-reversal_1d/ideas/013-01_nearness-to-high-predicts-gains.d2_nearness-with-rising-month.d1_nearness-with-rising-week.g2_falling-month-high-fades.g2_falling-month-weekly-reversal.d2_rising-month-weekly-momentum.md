---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its 7-day return, the higher its return over the next 7 days.
Consequence: In a rising month, a strong week is a reason to add long rather than stay out, scaled to the strength of that week.
Why:
- F1: The book is flat on the bars where coins rise most and active where they barely move. Flat bars (n=8112) had a mean next-bar coin return of +0.216%, against +0.016% on long bars (n=5896) and +0.071% on short bars (n=3516), so the book leaves the market's rise behind (Sharpe -0.16, Sharpe minus holding's -0.71).
- F2: In a rising month (30-day return > 0, non-overlapping 7-day grid), the 7-day return grades the next 7 days in the trend's direction. The mean forward return goes from -0.27% in the lowest 7-day-return quintile to +1.08%, +0.89%, +2.86% and +5.12% in the highest (179 cases per quintile). The book holds about 0 position there (mean position about 0.00).
- F6: Losses are spread across periods, not concentrated in one. Twelve of 24 windows have a negative mean daily book return. The book lost even in rising windows, for example w11 (book -0.043% a day against coins +1.26%) and w16 (-0.044% against +0.45%). This matches F1 and F3: it sat out rises and shorted bounces that kept going.
