---
line: 7.g patterns
backtest: N2-01_weekday-of-coming-bar_1d
idea tested: N2-01_weekday-of-coming-bar
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2790 USD
---
## Findings
- **F1:** After a down bar that falls more than one 20-bar standard deviation, the next bar beats the coin's mean daily return: +0.0048 (t 3.29, n 1302) for z in (-2,-1] and +0.0069 (t 2.58, n 476) for z ≤ -2. After a small up bar (z in (0,1]) the next bar lags the mean by -0.0021 (t -3.36, n 5275), and all six coins show that lag.
- **F2:** Heavy volume sharpens the rebound. A down bar of z ≤ -1 with volume above 1.5x its 20-bar average is followed by +0.0097 excess (t 4.05, n 677), against +0.0027 (t 1.86, n 1101) without the surge. Any down bar on a volume surge gives +0.0083 (t 4.82, n 1218), while an up bar on a surge gives -0.0007 (t -0.45, n 1282).
- **F3:** Where the bar closes within its range orders the next bar's excess return almost monotonically. A close in the bottom fifth gives +0.0038 (t 3.80, n 2631); a close in the top fifth gives -0.0021 (t -2.64, n 3716). A z ≤ -1 down bar that also closes in the bottom fifth gives +0.0079 (t 4.54, n 944).
- **F4:** Weekday sessions differ from each other, and Saturday is not the only one that stands out. Saturday is +0.0034 (t 4.07, n 2467) and Friday is +0.0021 (t 2.23, n 2462). Tuesday is -0.0025 (t -2.60, n 2472), negative in 5 of 6 coins. Thursday is -0.0030 (t -2.69, n 2472), negative in all 6 coins, but 2019 alone carries t -6.99 (n 312).
- **F5:** The Saturday premium and the down-bar rebound do not add up. After a z ≤ -1 down bar the coming Saturday shows -0.0002 (t -0.10, n 256), while other coming days show +0.0063 (t 4.32, n 1522). So the Saturday-only book misses most of the rebound in F1.
- **F6:** The book is long-only and earns from a thin edge. It made 1361 trades with a mean net P&L of +0.25% and a median of -0.01%. Its Sharpe of 0.478 trails holding the coin by 0.09, and Saturday is the only weekday with a non-trivial book return (+0.0024, t 2.59).
- **F7:** The rebound comes and goes by year: z ≤ -1 rebounds were strongest in 2020 (+0.0137, t 3.05) and 2021 (+0.0145, t 3.36) and near zero in 2019, 2024 and 2025. By coin it ranges from XMR at +0.0102 (t 3.51) to BTC at +0.0022 (t 0.89).

## Ideas
- `N2-01_weekday-of-coming-bar.g1_high-volume-selloff-bounce` (from F1, F2, F7): When a coin's daily bar falls more than its usual one-day move on volume well above its recent average, the next daily bar returns more than the coin's average day, because forced or panicked sellers exhaust themselves and price snaps back.
- `N2-01_weekday-of-coming-bar.g2_close-near-low-reversal` (from F3, F1): When a coin's daily bar closes in the lowest part of its high-low range, the next daily bar returns more than the coin's average day.
- `N2-01_weekday-of-coming-bar.g3_quiet-up-close-fades` (from F1, F3): After a modest up day that closes near its high, a coin's next daily bar returns less than its average day, as small gains fade rather than persist.
- `N2-01_weekday-of-coming-bar.g4_midweek-session-weakness` (from F4): A coin's Tuesday and Thursday daily sessions return less than its average day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
