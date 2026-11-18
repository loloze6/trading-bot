---
line: 7.g patterns
backtest: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d
idea tested: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5487 USD
---
## Findings
- **F1:** After a sharp one-day drop (scaled return below -1 against the 20-day volatility), the next 3 days' excess return rises with the day's volume against its 30-day average. On non-overlapping 3-day samples, the quartiles of volume ratio give -0.95% (t -1.18), -0.53% (t -0.74), -0.21% (t -0.32) and +4.09% (t 3.90, n=133); the Spearman correlation of volume ratio with the 3-day return is 0.14. The brief predicts the opposite: heavy-volume drops should carry on.
- **F2:** The heavy-volume drop rebound starts the very next day. After drops below -1, the next-day excess return is +0.71% (t 3.90, n=1020) in the heavy-volume tercile against +0.01% (t 0.03, n=148) in the thin tercile. For drops on volume above average, the 3-day rebound is positive in 7 of 8 years (all but 2018). It is positive in LTC, XMR, XRP and ZEC (+2.1% to +3.1%, t 1.6 to 2.1) but near zero in BTC and ETH.
- **F3:** After sharp heavy-volume rises (scaled return above 1.5, top volume tercile), the gain does not come on the next day but over the days that follow. The next day's excess return is -0.11% (t -0.55, n=712), days 2 to 5 give +1.78% (t 4.57, n=682), and days 6 to 10 add another +1.40% (t 2.74, n=660), for +3.43% (t 4.34) over 10 days.
- **F4:** The same lag shows in the strategy's own forecast. For bars with forecast above 5, the next day's excess return is -0.02%, against +1.09% over days 2 to 5 (t 4.26, n=1459) and +1.01% over days 6 to 10. Yet trades last only about 3.4 days on average and the book earns 4.9e-05 a day (Sharpe 0.10, below holding). The book is paid for day 1, which carries nothing, and exits before much of the drift.
- **F5:** The book's worst 2% of days come right after the coin's sharp rise: the previous day's coin return averages +8.6%, and the day itself is -7.6% for the coin and -7.7% for the book. Buying at the close of the rise day exposes the book to a next-day give-back before any continuation.
- **F6:** Among sharp rises (scaled return above 1), the volume ratio does not grade the days 2 to 5 drift. The volume quartiles give +1.04%, +3.84%, -0.35% and +3.36% (Spearman 0.018). The grading lies in the rise's size instead: the 5-day excess return is +1.77% (t 2.36, n=240) for scaled rises of 1 to 2 and +2.63% (t 2.08, n=109) above 2.
- **F7:** The day after a Wednesday close has a lower excess return (-0.30%, t -2.70, n=2489). This is negative in all 6 coins, in both halves of the period and in 7 of 8 years. The day after a Friday close is higher (+0.30%, t 3.76) and positive in 5 of 6 coins. These are calendar effects with no graded situation, so I give them no idea.

## Ideas
- `003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue.g1_heavy-volume-drops-rebound` (from F1, F2): When a coin falls sharply over one day relative to its 20-day volatility on heavy volume against its 30-day average, it rebounds over the next 3 days, and the heavier that day's volume against its average, the larger the rebound.
- `003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue.g2_delayed-continuation-after-surges` (from F3, F4, F5, F6): When a coin rises sharply over one day relative to its 20-day volatility on heavy volume against its 30-day average, it keeps rising from the second to the tenth day after the rise, and the larger the volatility-scaled rise, the larger that later gain.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
