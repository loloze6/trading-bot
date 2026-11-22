---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size
line: 7.b inconclusive
backtest: 024-02_fading-volume-downrun-rebound-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, only when the streak's loss is several times the coin's typical four-hour move over the past 30 days. Beyond that, the larger the loss relative to that typical move, the larger the rise.
Consequence: A trader buys only the down-streaks that are extreme against the coin's usual four-hour move, and refuses the common short ones, which give nothing back.
Why:
- F1: The tested measure is zero, not merely short of the bar. The mean 18-bar unusual move of the 4537 long cases is +0.0003 % with t 0.002. At 6 bars it is +0.066 % (t 0.98) and at 12 bars +0.013 % (t 0.13), so no horizon from one to three days shows the pooled effect.
- F2: The rebound appears only in the largest losses relative to the usual move. The top decile of the streak's loss in usual moves (mean 5.9 usual moves, 422 cases) has a mean 18-bar unusual move of +2.03 % (t 4.18), and the ninth decile (3.3 usual moves) has +0.75 % (t 1.95). Deciles 0 to 6 (0.4 to 2.0 usual moves) are all at or below zero, between −0.32 % and −0.93 %, with the second decile at t −2.80. Over the whole set, the forecast's above-median minus below-median difference is +1.07 %.
- F3: The top quintile of relative loss (at least 2.8 usual moves, 843 cases) gives a clear and stable result. Its mean 18-bar unusual move is +1.39 % (t 4.48), a strength of 0.165. It is also positive at 6 bars (+0.71 %, t 3.93) and at 12 bars (+0.97 %, t 3.61). It is positive in all six coins, from LTC's +0.32 % (t 0.53) to ZEC's +2.37 % (t 2.31). It is positive in 6 of 8 years; the exceptions are 2018 (−0.34 %) and 2022 (−1.06 %).
- F4: In the pooled cases, the market's own moves drown the effect. The cases' 18-bar unusual move swings by year, from −1.46 % (t −3.47) in 2018 and −1.25 % (t −3.95) in 2022 to +1.40 % (t 3.25) in 2021. The top quintile, by contrast, holds in both 30-day trends: +1.49 % (t 3.51, 500 cases) after a falling month and +1.25 % (t 2.79, 343 cases) after a rising one.
- F6: Most cases are small streaks that carry nothing. 3747 of the 4537 cases are two-bar streaks, with a mean of −0.04 % (t −0.29). The forecast ranks the outcome no better than the raw loss does (Spearman correlation with the 18-bar move 0.076 against 0.083 for the raw loss in usual moves), because it standardises against its own recent values.
- F7: In its large-loss part, the idea's move covers the cost of a trade many times over. The top quintile's total 18-bar move per case is +1.80 %, about 9 times the 0.19 % a trade cost, against 0.41 % (2.1 times) for all cases.
