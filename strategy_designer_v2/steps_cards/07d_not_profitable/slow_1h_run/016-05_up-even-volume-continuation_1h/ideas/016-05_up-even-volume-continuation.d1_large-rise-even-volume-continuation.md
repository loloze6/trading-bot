---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the more evenly its hourly volume was spread across those hours, the more the coin keeps rising over the next 3 days, only while its 3-day rise is large, and the larger that rise, the more it keeps rising.
Consequence: A trader would stay out of small, barely positive 3-day rises, where entries and exits churn the fees, and would weight the long by the size of the rise rather than by volume evenness.
Why:
- F1: The book's fees exceed its gross gain: per bar, the position earns 0.000025 before costs and pays 0.000031 in fees, so it loses money net (book Sharpe -0.32, mean daily return -0.00018, against a holding Sharpe 0.87 higher), over 16,107 trades lasting 23.6 hours on average.
- F2: The fees come from the regime switching on and off around a 3-day return of zero: bars with a 72-bar return between -0.5% and +0.5% carry 51% of all fees (25.7% + 25.5%), with turnover of 0.19 per bar against 0.003–0.009 on rises above 2%, yet they hold only 6% of the bars and earn -6% of the gross gain.
- F3: The gross gain sits in the larger rises: rises above 2% carry 93% of it (36.6% + 56.1%) and only 7.5% of the fees, while the top 40% of trending rises earn 4.64 gross against 0.32 in fees, and the rest earn 4.51 against 6.32 in fees, plus 6.24 in fees paid on non-trending bars.
- F4: Only the largest 3-day rises are followed by excess continuation: on the non-overlapping 72-bar grid, the top rise quintile's next-72-bar excess return is +0.0157 (t 3.37, n 573), while the other four quintiles range from -0.0056 to +0.0026 (|t| ≤ 1.74).
- F6: The sizing leans against the gain: from the low to the high forecast tercile, mean allocation rises (0.43, 0.49, 0.59) while gross gain per bar falls (0.000065, 0.000048, 0.000031), and fees rise (0.000028 to 0.000039).
