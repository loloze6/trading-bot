---
line: 7.d confirmed, not profitable
backtest: 061-01.d1_calm-big-up-day-long-only_1d
idea tested: 061-01.d1_calm-big-up-day-long-only
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3442 USD
---
## Findings
- **F1:** The Calmar fails because of the book's falls. Its deepest fall is −47 % (in w14, with −46.7 % in w15 and −37 % in w13 and w16). On the 2,526 coin-bars in a position, almost all of the gain comes from bars where the coin's 60-day return is above +10 %: those bars gained +6.81 in summed position returns (mean +0.72 % per bar, 951 bars). Choppy bars added +1.09 (493 bars), and falling bars lost −1.04 (mean −0.10 % per bar, 1,082 bars).
- **F2:** The falls come from being long calm up days inside a falling 60-day trend. In w14, the window of the −47 % fall, positions held in falling trends lost −1.16 in summed returns, against −0.12 in rising trends. On the 5-day grid, calm up days in a falling trend are followed by only +0.51 % excess (t 0.33, 103 cases on 41 days).
- **F3:** In a rising 60-day trend, the same calm up days are followed by +4.25 % excess over 5 days (t 2.07, 93 cases on 42 days). The rising trend alone, on calm grid bars without an up day, gives −0.24 % (t −0.17, 85 cases). So the trend is not an effect of its own; it is where the idea's follow-through shows.
- **F4:** A rebuilt book that is in a position only while the 60-day trend is rising raises the Calmar from 0.65 to 1.79. Its deepest fall shrinks from −47 % to −16.5 %, its Sharpe rises from 0.89 to 1.35, and its yearly return stays near 30 % (29.6 % against 30.4 %). These figures use my own rebuild (half the 0.19 % cost per side on each change of position); the official Calmar is 0.31, not the 0.65 of my baseline.
- **F5:** The same holds with the coin's own 20-day return as the condition.
- **F6:** Inside the rising trend, the follow-through is not clearly graded by the day's size.

## Ideas
- `061-01.d1.d1_rising-calm-big-day-follow-through` (from F1, F2, F3, F4, F6): In a rising, calm market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger its rise over the next 5 days.
- `061-01.d1.d2_calm-big-day-in-uptrend` (from F2, F5, F6): In a calm market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger its rise over the next 5 days, and the more so the higher its 20-day return before that day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
