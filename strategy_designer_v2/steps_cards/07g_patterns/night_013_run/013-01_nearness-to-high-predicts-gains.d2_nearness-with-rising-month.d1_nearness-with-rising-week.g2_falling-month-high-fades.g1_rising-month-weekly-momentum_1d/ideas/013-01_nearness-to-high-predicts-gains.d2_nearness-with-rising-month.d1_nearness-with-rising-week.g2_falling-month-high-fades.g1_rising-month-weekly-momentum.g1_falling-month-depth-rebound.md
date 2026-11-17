---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, the deeper its 30-day fall, the higher its return over the next 7 days.
Consequence: In a falling month, a coin's steepest monthly declines are a reason to look for a long rebound rather than to stay out, which the current strategy does.
Why:
- F3: In falling months the 30-day return reverses. The slope of the demeaned next-7-day return on r30 is −0.074 (t −2.35, n 830), so a deeper monthly fall is followed by a higher next week. The slope is negative in 5 of 6 coins (BTC t −2.85, n 126). It is stronger in 2018–2021 (t −2.35, n 425) than in 2022–2025 (t −0.88, n 405).
- F1: The tested relation is real and stands out. In rising months (30-day return above 0), the slope of the demeaned next-7-day return on the 7-day return is 0.142 with t 4.35 over 893 grid cases. The top r7 quintile earns +3.5% over the coin's average (t 3.21, n 252) and the bottom quintile earns −0.9%. In falling months the slope turns negative (−0.057, t −1.49, n 830).
