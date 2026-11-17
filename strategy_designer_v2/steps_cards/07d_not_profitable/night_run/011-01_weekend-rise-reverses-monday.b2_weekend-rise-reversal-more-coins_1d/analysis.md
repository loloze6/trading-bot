---
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3945 USD
---
## Findings
- **F1:** The book's whole gross gain is spent on fees: the per-bar gain summed over all bars is 2.45 against summed fees of 2.41. The active Mondays earn 0.00114 per bar while each trade bar costs 0.00056, and every one-day short is two trade bars (4316 fee bars for 2156 active bars), so the mean daily return is only 3.9e-05.
- **F2:** Most of the reversal comes after the bar the book holds. In the top quintile of Sunday returns (mean +6.1%), Monday's next-day return is -0.59% and Tuesday adds another -0.51%. The pooled short-on-rise measure grows from mean 0.0020 (t 2.20) for Monday alone to 0.0037 (t 3.58) for Monday plus Tuesday, over 4382 Sunday cases.
- **F3:** Weekend falls also reverse, and the book leaves that side out. The long-on-fall measure over Monday plus Tuesday is 0.0017 (t 2.55). Both sides together give 0.0054 (t 4.40, n 4382). The bottom Sunday quintile (-5.5%) is followed by +0.99% over the next two days, against -1.08% after the top quintile.
- **F4:** The reversal belongs to the weekend. The slope of the next 2-day excess return on the day's standardised return is -0.0068 (t -5.15) for the Sunday bar and -0.0020 (t -1.98) for Monday. It is positive for Friday (+0.0031, t 3.60) and Saturday (+0.0017, t 1.33).
- **F5:** The book is short only, so it pays the coins' upward drift. The drift costs -0.00073 per active bar against the coins' mean daily return of +0.0015. That is why it trails holding (Sharpe 0.16 minus holding's, -0.45) and loses in rising years: book -0.00017 in 2020 and -0.00016 in 2024, while the coins made +0.0046 and +0.0029.
- **F6:** For the largest weekend rises, low weekend volume deepens the reversal. In the top third by size, the 2-day excess return is -1.63% when Sunday volume is below its 28-day median and -0.89% when it is above. In the smaller thirds volume makes no difference (-1.65% vs -1.59%, -0.61% vs -0.77%).

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.d1_weekend-move-reverses-two-days` (from F1, F2, F3, F4, F5): A coin that rose over the weekend (its Saturday-to-Sunday close-to-close return) falls over the next 2 days (Monday and Tuesday), and a coin that fell over the weekend rises over the next 2 days, the move running against the weekend move and growing with its size.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.d2_thin-weekend-rise-reverses` (from F1, F2, F6): A coin that rose over the weekend (its Saturday-to-Sunday close-to-close return) falls over the next 2 days (Monday and Tuesday), and the larger the weekend rise, the larger the fall, more so the lower Sunday's volume relative to the coin's average daily volume over the past 28 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
