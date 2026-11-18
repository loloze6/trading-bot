---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue
line: 7.g patterns
backtest: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day relative to its 20-day volatility on heavy volume against its 30-day average, it keeps rising from the second to the tenth day after the rise, and the larger the volatility-scaled rise, the larger that later gain.
Consequence: A large heavy-volume up day is a reason to be long the coin from the day after it through the following week and a half, rather than only over the next few days.
Why:
- F3: After sharp heavy-volume rises (scaled return above 1.5, top volume tercile), the gain does not come on the next day but over the days that follow. The next day's excess return is -0.11% (t -0.55, n=712), days 2 to 5 give +1.78% (t 4.57, n=682), and days 6 to 10 add another +1.40% (t 2.74, n=660), for +3.43% (t 4.34) over 10 days.
- F4: The same lag shows in the strategy's own forecast. For bars with forecast above 5, the next day's excess return is -0.02%, against +1.09% over days 2 to 5 (t 4.26, n=1459) and +1.01% over days 6 to 10. Yet trades last only about 3.4 days on average and the book earns 4.9e-05 a day (Sharpe 0.10, below holding). The book is paid for day 1, which carries nothing, and exits before much of the drift.
- F5: The book's worst 2% of days come right after the coin's sharp rise: the previous day's coin return averages +8.6%, and the day itself is -7.6% for the coin and -7.7% for the book. Buying at the close of the rise day exposes the book to a next-day give-back before any continuation.
- F6: Among sharp rises (scaled return above 1), the volume ratio does not grade the days 2 to 5 drift. The volume quartiles give +1.04%, +3.84%, -0.35% and +3.36% (Spearman 0.018). The grading lies in the rise's size instead: the 5-day excess return is +1.77% (t 2.36, n=240) for scaled rises of 1 to 2 and +2.63% (t 2.08, n=109) above 2.
