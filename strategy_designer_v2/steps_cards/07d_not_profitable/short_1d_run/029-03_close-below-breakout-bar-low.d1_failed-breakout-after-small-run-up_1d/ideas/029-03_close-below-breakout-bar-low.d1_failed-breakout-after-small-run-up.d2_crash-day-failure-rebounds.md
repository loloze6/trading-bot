---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up
line: 7.d not profitable
backtest: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes back below the low of a breakout day above its prior 20-day high through a one-day fall far larger than its usual daily move, it rises over the next 5 days. The larger that day's fall against its usual daily move, the larger the rise.
Consequence: A trader would refuse, or close, a short on a failed breakout whose failure came as a crash day, since the late buyers' forced selling is already spent.
Why:
- F5: Failures that arrive on a crash day bounce instead of falling, and the depth grading points the wrong way. The quintile with the largest one-day fall on the signal day (−10.8 % on average) is followed by a short-side move of −4.25 % (t −2.21, 73 cases), meaning the coin rose. The deepest-depth quintile (8.3 % under the breakout low) moved −2.71 % (t −1.51). The next fall quintiles (−6.2 % and −2.6 % that day) do continue: +0.91 % (t 1.12) and +1.11 % (t 1.16) over 5 days, and +3.27 % (t 2.45) and +2.72 % (t 1.94) over 10 days.
- F6: The losses cluster in one year. In 2020 the failures moved −2.94 % (t −2.33, 49 cases), the only year whose t lies beyond ±2. In 2025 they moved −2.73 % (t −0.93).
- F2: The forecast fires on a small, unrepresentative share of failures, and even those carry little. It is nonzero on only 31 of the 361 recomputed failures (8.6 %), and those gained just +0.86 % (t 0.55). The 330 failures left at zero moved −0.74 % (t −1.27). The book held a position on 256 of about 17,524 coin-bars (1.5 %) and made 89 trades, or 0.00485 trades a day.
