---
line: 7.a not observable
backtest: 013-05_longer-stall-bigger-breakout_1d
idea tested: 013-05_longer-stall-bigger-breakout
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2625 USD
---
## Findings
- **F1:** The idea's situation, a close above the prior 365-day closing high, is rare in this data: only 2.6% of all bars are in the trending regime, and only 18 of the 518 non-overlapping 30-bar grid bars that have a full forward return fall in it (3.5%), against the plan's minimum of 30.
- **F2:** The breaks are short, so a 30-bar grid rarely lands on one: there are 208 trending episodes with a mean length of 2.1 bars, a median of 2 and a maximum of 8, which gives 527 trending bars but only 22 trending grid bars.
- **F3:** The windows are short for the 30-day horizon: they last about 122 bars (119 to 123), so each coin-window gives only 3.75 full grid bars, and the 6 coins over 138 coin-windows give just 518 cases.
- **F4:** The cases cluster in a few bull years: 2022 gives 0 trending grid bars, 2018 and 2019 give 0 together, and 2020 gives 5, 2021 3, 2023 2, 2024 4 and 2025 4; the fold-D windows w19–w24 alone give 8 of the 18.
- **F5:** Few coins reach the situation: BTC and ETH give 5 grid cases each, XMR and ZEC 3 each, and LTC and XRP 1 each, so each extra coin in the recent folds adds about 1–2 cases.
- **F6:** The outcome varies widely from case to case, which makes the slope noisy: the 18 cases have a 30-bar forward return with a mean of 0.17, a median of 0.055, a standard deviation of 0.58 and a maximum of 2.37, against a standard deviation of 0.31 over all grid bars.

## Ideas
- `013-05_longer-stall-bigger-breakout.a1_stall-breakout-wider-coin-set` (from F1, F3, F4, F5): When a coin closes above its prior 52-week high, the more days of the past 60 it spent closing just under that high, the larger its return over the next 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
