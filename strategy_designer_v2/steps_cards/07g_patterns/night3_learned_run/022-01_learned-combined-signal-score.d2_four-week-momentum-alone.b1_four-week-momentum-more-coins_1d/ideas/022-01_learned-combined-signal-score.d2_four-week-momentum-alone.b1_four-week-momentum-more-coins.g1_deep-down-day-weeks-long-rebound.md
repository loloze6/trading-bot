---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's fall on its last day, the higher its return over the next 20 days, the gain growing with the depth of the day's fall.
Consequence: After a coin's sharp one-day drop, lean long for the following weeks in proportion to the drop rather than short it, and refuse shorts taken right after a deep down day.
Why:
- F1: Over the next 20 days, a coin's one-day return points the other way, and strongly. The slope of the 20-day excess return (in units of the coin's usual 20-day move) on the ranked one-day return is -0.157 per standard deviation (t -6.1, 1456 non-overlapping cases). It holds when returns are clipped (t -6.3) and when the day's return is scaled by its 20-day volatility (t -5.4).
- F2: The book's gain is all on the long side. Long bars earned +0.21 % per bar (17987 bars, sum 38.0), short bars -0.0085 % (18868 bars, sum -1.6). Shorts paid only in falling years (2018 +0.14 %, 2022 +0.11 % per bar) and lost in 2020, 2023 and 2024 (-0.11 % to -0.14 % per bar).
- F3: The deepest falls are not where the losses continue, which fits F1. In the forecast's quintiles:
