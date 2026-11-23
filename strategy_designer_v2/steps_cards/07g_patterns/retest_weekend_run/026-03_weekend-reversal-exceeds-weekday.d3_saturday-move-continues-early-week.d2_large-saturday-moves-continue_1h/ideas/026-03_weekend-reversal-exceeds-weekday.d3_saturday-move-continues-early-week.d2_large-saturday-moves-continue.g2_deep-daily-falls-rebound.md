---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour fall, measured against its usual 30-day 24-hour move, is followed by a rise over the next 24 hours that is larger the deeper the fall.
Consequence: A trader would buy after deep one-day falls, more the deeper the fall, rather than sell after one-day rallies.
Why:
- F3: Falls reverse more than rises. The graded slope is -0.079 (t -4.18, n 7356) after down days and -0.039 (t -2.56, n 7565) after up days. Over all volatilities, the most negative decile (mean -2.56 usual moves) is followed by +0.83 % excess over 24 hours (t 5.01, n 1495). The most positive decile (+2.75) is followed by -0.34 % (t -2.47).
- F2: In the higher-volatility 40 % of cases, the extreme quintiles reverse by more than a trade costs. After a mean past move of -1.70 usual moves the next 24 hours earn +1.10 % above drift (t 5.15, n 1196). After +1.84 usual moves they earn -0.63 % (t -3.40, n 1196). One trade costs 0.19 %.
- F4: The 24-hour reversal is persistent rather than one period's luck. The yearly slope is negative in 7 of 8 years, with t at or below -2 in 2018, 2019, 2020, 2021, 2023 and 2025, and near zero or positive only in 2022 (+0.001) and 2024 (+0.038, t 1.58). The coins agree in sign, from BTC at -0.009 (t -0.44) to XMR at -0.075 (t -3.63).
