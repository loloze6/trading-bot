---
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation_1h
idea tested: 016-05_up-even-volume-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3299 USD
---
## Findings
- **F1:** The book's fees exceed its gross gain: per bar, the position earns 0.000025 before costs and pays 0.000031 in fees, so it loses money net (book Sharpe -0.32, mean daily return -0.00018, against a holding Sharpe 0.87 higher), over 16,107 trades lasting 23.6 hours on average.
- **F2:** The fees come from the regime switching on and off around a 3-day return of zero: bars with a 72-bar return between -0.5% and +0.5% carry 51% of all fees (25.7% + 25.5%), with turnover of 0.19 per bar against 0.003–0.009 on rises above 2%, yet they hold only 6% of the bars and earn -6% of the gross gain.
- **F3:** The gross gain sits in the larger rises: rises above 2% carry 93% of it (36.6% + 56.1%) and only 7.5% of the fees, while the top 40% of trending rises earn 4.64 gross against 0.32 in fees, and the rest earn 4.51 against 6.32 in fees, plus 6.24 in fees paid on non-trending bars.
- **F4:** Only the largest 3-day rises are followed by excess continuation: on the non-overlapping 72-bar grid, the top rise quintile's next-72-bar excess return is +0.0157 (t 3.37, n 573), while the other four quintiles range from -0.0056 to +0.0026 (|t| ≤ 1.74).
- **F5:** Volume evenness adds nothing to the rise: its Spearman correlation with the 72-bar excess return is 0.008 (0.004 standardised), the evenness terciles differ by under 0.004 (|t| ≤ 1.02), and the top-minus-bottom forecast tercile gives t 0.68; inside the top rise tercile, the middle-evenness cell (+0.0130, t 2.24) beats the most even (+0.0043, t 0.70).
- **F6:** The sizing leans against the gain: from the low to the high forecast tercile, mean allocation rises (0.43, 0.49, 0.59) while gross gain per bar falls (0.000065, 0.000048, 0.000031), and fees rise (0.000028 to 0.000039).
- **F7:** Large 3-day falls are followed by further falls: on non-trending grid bars, the deepest-fall tercile has a next-72-bar excess return of -0.0083 (t -3.51, n 892), against +0.0049 (t 1.51) for the mildest tercile.

## Ideas
- `016-05_up-even-volume-continuation.d1_large-rise-even-volume-continuation` (from F1, F2, F3, F4, F6): When a coin has risen over the past 3 days, the more evenly its hourly volume was spread across those hours, the more the coin keeps rising over the next 3 days, only while its 3-day rise is large, and the larger that rise, the more it keeps rising.
- `016-05_up-even-volume-continuation.d2_3-day-rise-size-continuation` (from F3, F4, F5): The larger a coin's 3-day return, the more the coin rises over the next 3 days in excess of its usual return.
- `016-05_up-even-volume-continuation.d3_3-day-fall-continuation` (from F7): The deeper a coin's 3-day fall, the more the coin falls over the next 3 days in excess of its usual return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
