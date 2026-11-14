---
line: 7.d not profitable
backtest: N1-08_twenty-day-momentum_1d
idea tested: N1-08_twenty-day-momentum
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3207 USD
---
## Findings
- **F1:** Only the long side pays: 4,507 long trades made +4.71% mean before fees (+21,229% summed), while 4,864 short trades lost −0.66% mean (−3,191% summed), and on non-overlapping 20-bar cases the short signal's signed forward return was −2.3% (t −2.20, n 427) against +2.7% for the long signal (t 1.67, n 400).
- **F2:** The size of the forecast earns nothing: the pooled non-overlapping slope has t 0.06 (n 827), the bottom forecast fifth has a higher forward 20-bar excess return (+4.0%) than the top fifth (+2.3%) with the middle fifths negative (−1.7% to −2.6%), and trade gain by entry |forecast| quartile is flat (1.79%, 2.18%, 1.33%, 2.40%).
- **F3:** The book churns on the fast part of the signal: the forecast changes sign 1.87 times per 20 bars, trades held up to 7 days lose about 3% each before fees (n 5,987 trades), and only trades held over 20 days pay (+31.9% mean, n 1,131); flip days average −4.7 bp of book return against +23.8 bp on other days (805 vs 7,935 days).
- **F4:** Fees are not the cause: total commission (about 2,403 percentage points) is small next to the long side's gross 21,229, so the shortfall comes from the short side and from short trades.
- **F5:** Almost all the book's daily gain comes from being long while the 60-day return is positive: +53.3 bp per day (t 4.02, n 3,040 days), against +9.2 bp for long in a 60-day decline, +7.1 bp for short in a 60-day rise and +0.2 bp for short in a 60-day decline (all t < 0.8).
- **F6:** The slower trend selects better: on non-overlapping 20-bar cases a long signal in a 60-day rise is followed by +3.6% excess (t 1.63, n 141), and a long signal above the 100-day average by +3.2% (t 1.57, n 152); a long signal in a 60-day decline gets −3.7% (t −1.49, n 62).
- **F7:** The book lags holding the coin because it is short or flat in rising markets: in up windows it made +43.8% against +79.3% for holding (long share 0.64, n 68), and in down windows it lost −15.7% against −30.0% (n 76).

## Ideas
- `N1-08_twenty-day-momentum.d1_long-only-aligned-uptrend-persistence` (from F1, F5, F6, F7): In one coin's daily bars, when the coin's 60-day return is positive and its 20-day return is also positive, the following 20 days rise more than the coin's average 20-day return.
- `N1-08_twenty-day-momentum.d2_slow-trend-carries-the-drift` (from F2, F3, F4, F5): In one coin's daily bars, a positive 60-day return is followed by daily returns that stay above the coin's average for several weeks, so the gain lives in the slow trend rather than in the 20-day swings.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
