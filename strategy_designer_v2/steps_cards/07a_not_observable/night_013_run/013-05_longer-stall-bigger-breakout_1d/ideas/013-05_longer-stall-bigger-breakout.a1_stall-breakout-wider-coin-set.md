---
brief: 013_anchoring-to-recent-high
source-idea: 013-05_longer-stall-bigger-breakout
line: 7.a not observable
backtest: 013-05_longer-stall-bigger-breakout_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 52-week high, the more days of the past 60 it spent closing just under that high, the larger its return over the next 30 days.
Consequence: The under-reaction builds up while selling holds the price below the high, so a longer stall under the high leads to a larger catch-up after the break.
Why:
- F1: The idea's situation, a close above the prior 365-day closing high, is rare in this data: only 2.6% of all bars are in the trending regime, and only 18 of the 518 non-overlapping 30-bar grid bars that have a full forward return fall in it (3.5%), against the plan's minimum of 30.
- F3: The windows are short for the 30-day horizon: they last about 122 bars (119 to 123), so each coin-window gives only 3.75 full grid bars, and the 6 coins over 138 coin-windows give just 518 cases.
- F4: The cases cluster in a few bull years: 2022 gives 0 trending grid bars, 2018 and 2019 give 0 together, and 2020 gives 5, 2021 3, 2023 2, 2024 4 and 2025 4; the fold-D windows w19–w24 alone give 8 of the 18.
- F5: Few coins reach the situation: BTC and ETH give 5 grid cases each, XMR and ZEC 3 each, and LTC and XRP 1 each, so each extra coin in the recent folds adds about 1–2 cases.
