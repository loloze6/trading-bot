---
line: 7.d not profitable
backtest: 012-02_volume-burst-fall-reversal_1d
idea tested: 012-02_volume-burst-fall-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3465 USD
---
## Findings
- **F1:** The book earns 0.0082% a day against 0.118% for holding the coins, because it is invested on only 5.4% of coin-days; its 474 trades last 1.07 days on average and earn 0.55% each before fees (0.45% after, 56% winners), which is too small and too rare to lift the mean daily return.
- **F2:** After the 444 thinned sharp-fall bars, the excess return is +0.42% over 1 day (t 1.53) but turns to −0.42% over 3 days (t −1.13) and −1.05% over 5 days (t −2.14), so the rebound lasts one day and is then given back with more.
- **F3:** Volume ratio grades the next-day move: the top third by volume ratio gains +1.14% over 1 day (t 1.74, n 148) against −0.04% for the bottom third, but the same top third loses −1.78% over 5 days (t −1.94).
- **F4:** The wick works against the brief: falls that close nearest their low (bottom third of close-in-range, n 148) gain +1.64% over 1 day (t 3.46), while falls with the longest lower wick lose −0.41% over 1 day and −2.85% over 10 days (t −2.71).
- **F5:** The losses sit in bear years: falls in 2018 lose −2.66% over 3 days (t −2.24) and falls in 2022 lose −2.75% (t −2.73) and −3.88% over 5 days (t −3.32), while 2020 (+4.17% over 1 day, t 2.95) and 2021 (+1.96%, t 2.22) carry the rebound.
- **F6:** Falls that come after the strongest 30-day rise (top third of 30-day return, n 114) gain +0.95% over 1 day (t 2.30), while those in the middle third lose −1.77% over 5 days (t −1.98).

## Ideas
- `012-02_volume-burst-fall-reversal.d1_one-day-volume-burst-rebound` (from F2, F3, F1): Among bars that fall sharply, the larger the bar's volume relative to the coin's 30-day average volume, the larger the price rise over the next 1 day, a rebound that has faded by 3 days.
- `012-02_volume-burst-fall-reversal.d2_close-at-low-next-day-rebound` (from F4, F2): Among bars that fall sharply, the closer the bar closes to its own low, the larger the price rise over the next 1 day.
- `012-02_volume-burst-fall-reversal.d3_volume-burst-dip-in-uptrend` (from F5, F6, F3): Among bars that fall sharply, the larger the bar's volume relative to the coin's 30-day average volume, the larger the price rise over the next 1 day, only while the coin's 30-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
