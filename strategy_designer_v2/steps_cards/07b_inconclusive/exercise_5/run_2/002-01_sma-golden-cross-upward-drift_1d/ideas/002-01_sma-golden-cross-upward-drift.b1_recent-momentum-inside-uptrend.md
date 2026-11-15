---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, the coin rises more over the next 10 days the larger its own 20-day return.
Consequence: A trader should weigh the long by the coin's recent 20-day move inside an uptrend, not by the width of the 50/200 spread, and refuse it when the 20-day move has turned down.
Why:
- F1: The golden-cross spread forecast does not predict the coin's excess return at any horizon: the pooled slope t is 0.20 at 5 days (3349 cases), 0.37 at 10 days (1657), 0.55 at 20 days (811) and -0.06 at 40 days (388), and at 10 days the on-minus-off excess return is only 0.0005 versus -0.0005 (Welch t 0.14, 832 on and 825 off).
- F2: Within the bars where the 50-day SMA is above the 200-day, the coin's own 20-day return carries the effect: the slope of the 10-day excess return on the past 20-day return is 0.069 (t 3.26, 694 cases), against -0.020 (t -0.84, 681) while the 50-day is below.
- F3: The same split is clear by sign and by quintile on the forecast>0 bars: with a positive 20-day return the 10-day excess is +0.022 (t 2.07, 361), with a non-positive one -0.016 (t -2.28, 471); the top 20-day-return quintile gives +0.037 (t 1.85, 160) and the bottom one -0.029 (t -2.26, 131).
- F4: The off-cross bars show no such ordering, so the opposite-signed moves cancel inside the plan's test: the five 20-day-return quintiles give +0.016, -0.016, -0.002, +0.0004 and -0.008.
- F5: The longer 60-day return does not carry the effect on forecast>0 bars (slope 0.0067, t 0.75, 423 cases), so the information is in the recent 20-day move, not in the trend the 50/200 spread measures.
- F6: The forecast's own grading is not monotone: the 10-day excess is -0.0085 in forecast 0-5, +0.0023 in 5-10, +0.0105 in 10-15 and +0.00004 in 15-20, and the widest raw-spread quintile gives -0.0049 against +0.012 in the middle one (t 1.47).
- F7: The 20-day-return split on forecast>0 bars is mixed across coins and years: it is positive for XRP (+0.058 vs -0.042), ZEC (+0.088 vs -0.043), ETH (+0.017 vs -0.014) and BTC (+0.009 vs -0.0002), reversed for LTC and XMR, positive in 2020, 2021, 2024 and 2025, and negative in 2018, 2022 and 2023.
