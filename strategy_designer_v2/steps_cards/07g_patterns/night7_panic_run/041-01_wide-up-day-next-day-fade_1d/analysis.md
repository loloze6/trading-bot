---
line: 7.g patterns
backtest: 041-01_wide-up-day-next-day-fade_1d
idea tested: 041-01_wide-up-day-next-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3973 USD
---
## Findings
- **F1:** Down days with the widest range for the coin bounced the next day; down days in the top fifth of the swing-scaled range (high minus low over the close, in units of the 30-day daily-return swing) ended +1.16 % above drift (t 2.68, 822 cases on 262 days), while the other four fifths of down days were between -0.11 % and +0.22 % with |t| ≤ 0.64.
- **F2:** The bounce after wide down days points the same way everywhere I could split it, though no single split is strong on its own: positive in every year (2018 +1.28 %, 2019 +0.45 %, 2020 +1.57 %, 2021 +1.39 %), on every coin (BTC +0.71 % up to XMR +1.72 %, with ETH, XMR and ZEC at t ≥ 2.09) and in all 12 windows (+0.03 % to +4.32 %).
- **F3:** On down days the bounce grows with the width of the range and not with the size of the fall. In a regression of next-day excess on the swing-scaled range, the swing-scaled return and the close location, the range coefficient is +0.40 % per swing unit (t 2.77), while the return coefficient is -0.07 % (t -0.26).
- **F4:** Among wide days (the top two range fifths), the next-day excess falls steadily with where the day closed in its range: +1.07 % (t 2.41, 545 cases) for closes in the bottom fifth of the range, then +0.57 %, +0.37 %, -0.17 % and -0.29 % for closes in the top fifth. Combining both into the range times (1 − close location) gives +0.80 % (t 2.60, 1452 cases) in its top fifth, against -0.12 % to -0.23 % in the four other fifths.
- **F5:** The tested fade of up days is not graded by the range, which is why its supporting check failed (top third minus bottom third -0.07 %). Up days fall below drift most in the middle range fifth (-0.69 %, t -3.14), while the widest fifth gives only -0.49 % (t -1.39) and the narrowest +0.02 %. In rising markets, up days are followed by +0.36 % above drift (t 1.27), against the short.
- **F6:** The book is in effect a short on the coins and is never positioned for the bounce that works. Its daily returns correlate -0.65 with the coins', and it lost -1.23 % a day in the coins' best fifth of days. It held a position after only 60 down days against 4349 up days, and its 3726 trades lost -1.10 % each before fees.
- **F7:** The bounce after wide down days is large against what a trade costs: +1.16 % per case is about 6 times the 0.19 % round-trip cost. The 2-day excess on the 2-day grid is +1.28 %, but with t 1.46 the second day adds little that can be told from chance.

## Ideas
- `041-01.g1_wide-down-day-next-day-rebound` (from F1, F2, F3, F7): After a down-closing day, a coin rises over the next day, more so the wider that day's high-to-low range in units of its 30-day daily-return swing.
- `041-01.g2_wide-low-close-day-rebound` (from F4, F3, F1, F7): After a wide-range day that closes near its low, a coin rises over the next day, more so the wider the range in units of its 30-day daily-return swing and the closer the close sits to the day's low.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
