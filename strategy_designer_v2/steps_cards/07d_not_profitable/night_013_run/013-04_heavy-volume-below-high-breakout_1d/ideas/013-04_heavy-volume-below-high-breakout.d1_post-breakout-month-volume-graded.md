---
brief: 013_anchoring-to-recent-high
source-idea: 013-04_heavy-volume-below-high-breakout
line: 7.d not profitable
backtest: 013-04_heavy-volume-below-high-breakout_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin has closed above its prior 52-week high at any time within the past 30 days, the heavier its volume over the 10 days before that break, relative to its own 90-day average, the larger its return over the next 30 days.
Consequence: The breakout's follow-through runs for weeks, so the long should be carried through the month after the break, sized by the pre-break volume, rather than taken only on the breakout day.
Why:
- F1: The book is almost never in the market, and this is why it fails on size, trades and Calmar. It is long on only 1.4% of bars, from 0.7% for XRP to 2.4% for ETH. Its 165 trades last a mean of 1.52 days and a median of 1 day. As a result it trades 0.0095 per bar, earns a mean daily return of 5.9e-05 against the coins' 0.00129, and has a daily return SD of 0.0052 against holding's 0.048.
- F2: The gain the idea predicts is real but spread over a month, and the book exits after about a day. On breakout bars (the first day of a run) the mean 30-day return is 0.107 (107 cases) against 0.050 over all bars, and the mean 1-day return is only 0.011. Across the 50 de-duplicated events the mean 30-day return is 0.128, with t 1.79 and 52% positive.
- F3: The extra rise continues for weeks after the break. On the non-overlapping 30-day grid, bars 1 to 10 days after a break return 0.082 (14 cases) and bars 10 to 30 days after return 0.068 (31 cases). Bars in windows with no break return 0.028 (457 cases). The 30 days after breaks cover 12.3% of bars against the book's 1.4%.
- F4: The volume grading works on the 30-day horizon. Breakout events sorted into tertiles of 10-day over 90-day volume return 0.019, then 0.199, then 0.438 over 30 days (11 events each). The verdict's top-minus-bottom difference is 0.273 with Welch t 1.99 on 50 events, but the book captures almost none of it.
- F6: Because of this, the book's risk-adjusted result trails holding. Its Sharpe is 0.505 against holding's (difference −0.064) and its Calmar is 0.32. The trades' mean gain of 1.42% is too small and too rare to lift either measure.
