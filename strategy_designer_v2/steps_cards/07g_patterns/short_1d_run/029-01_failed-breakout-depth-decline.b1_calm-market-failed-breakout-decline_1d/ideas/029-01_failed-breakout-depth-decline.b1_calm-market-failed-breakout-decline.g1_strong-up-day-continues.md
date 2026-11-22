---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline
line: 7.g patterns
backtest: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's daily return measured in units of its 20-day volatility of daily returns, the more the coin rises over the next 5 days.
Consequence: A short trader should refuse shorts in the days after a strong up close, since such closes are followed by further gains rather than a reversal.
Why:
- F1: The tested situation shows no fall. On a 5-day grid, the 245 failed-breakout cells were followed by a 5-day return +0.263 % above the coin's mean (t 0.36), against −0.020 % (t −0.10, 3174 cells) for all other cells. The step-5 cases gave −0.11 % per case in the short direction (t −0.27, 615 cases). The book earned less than holding in every coin, from +0.0016 % to −0.048 % a day, while active on 15 % to 26 % of days.
- F2: A large up day was followed by a further rise. Cells in the top quintile of the day's return divided by its 20-day volatility gained +1.63 % above the coin's mean over the next 5 days (t 3.24, 570 cases), the only quintile clearly away from zero. The bottom quintile was −0.28 % (t −0.73).
- F3: The rise after a large up day is graded and widespread. The 5-day excess return in volatility units rises with the day's return in all six coins, significantly in XMR (t 2.12), XRP (t 2.86) and ZEC (t 2.51). Top-quintile cells were positive in 5 of 6 coins (BTC +1.61 % t 1.94, ZEC +3.91 % t 2.09; LTC −0.21 % the exception) and in 6 of 8 years (2021 +5.15 % t 3.19, 2024 +2.47 % t 2.06; 2022 −0.90 % t −0.93).
