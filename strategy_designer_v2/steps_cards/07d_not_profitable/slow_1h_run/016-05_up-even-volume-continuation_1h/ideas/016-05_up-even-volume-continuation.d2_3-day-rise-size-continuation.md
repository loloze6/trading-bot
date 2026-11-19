---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day return, the more the coin rises over the next 3 days in excess of its usual return.
Consequence: A trader would hold a coin long in proportion to the strength of its 3-day rise and cut the position as the rise fades toward zero.
Why:
- F3: The gross gain sits in the larger rises: rises above 2% carry 93% of it (36.6% + 56.1%) and only 7.5% of the fees, while the top 40% of trending rises earn 4.64 gross against 0.32 in fees, and the rest earn 4.51 against 6.32 in fees, plus 6.24 in fees paid on non-trending bars.
- F4: Only the largest 3-day rises are followed by excess continuation: on the non-overlapping 72-bar grid, the top rise quintile's next-72-bar excess return is +0.0157 (t 3.37, n 573), while the other four quintiles range from -0.0056 to +0.0026 (|t| ≤ 1.74).
- F5: Volume evenness adds nothing to the rise: its Spearman correlation with the 72-bar excess return is 0.008 (0.004 standardised), the evenness terciles differ by under 0.004 (|t| ≤ 1.02), and the top-minus-bottom forecast tercile gives t 0.68; inside the top rise tercile, the middle-evenness cell (+0.0130, t 2.24) beats the most even (+0.0043, t 0.70).
