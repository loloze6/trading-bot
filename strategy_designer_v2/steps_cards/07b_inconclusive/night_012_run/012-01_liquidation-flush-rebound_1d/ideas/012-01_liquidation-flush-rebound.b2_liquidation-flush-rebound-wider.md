---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-01_liquidation-flush-rebound
line: 7.b inconclusive
backtest: 012-01_liquidation-flush-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a bar closes sharply lower on volume far above its own 30-day average volume and leaves a long lower wick below its close, price rises over the next 3 days. The more extreme the volume burst and the longer the wick, the larger that rise.
Consequence: Liquidation flushes overshoot and are partly retraced once forced selling is exhausted.
Why:
- F1: The pooled flush-bar result is on the side the idea predicts, a 3-day excess return of +0.0163 (t 2.11, 158 cases, hit rate 55.7%), but it rests on the volume burst alone, because the wick works against the grading: the Spearman correlation of the 3-day excess return is +0.157 with volume ratio, +0.014 with the fall and −0.061 with the wick, so the combined forecast correlation is −0.009.
- F5: The effect varies widely from year to year and coin to coin: flush 3-day excess is −0.0243 (t −2.05) in 2019 and −0.0202 (t −1.42) in 2021 but +0.0687 in 2020 and +0.0395 (t 2.68) in 2024, and no single coin reaches t 2 (BTC +0.0204, t 1.82; ZEC +0.0046, t 0.22).
