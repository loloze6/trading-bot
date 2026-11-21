---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is positive, a sharp fall over one four-hour bar is followed by a rise over the next three days. The larger that fall compared with the coin's typical four-hour move over the past 30 days, the larger the rise.
Consequence: In a coin that has risen over the past month, buy a sharp four-hour fall for a three-day hold rather than sell it, and lean in more the deeper the fall was against the coin's usual moves.
Why:
- F1: A sharp four-hour fall in a coin whose 30-day return is positive is followed by a rise over the next three days. Falls were taken as a bar's return of at most -2 times the coin's 30-day standard deviation of four-hour returns, de-overlapped to one per three days in each window. They are followed by a mean 18-bar return of +1.06 % above the coin's drift (t 2.61, 606 cases). The same falls when the 30-day return is negative give +0.14 % (t 0.37, 636 cases). Given the many angles examined, this t is only borderline.
- F2: Over all de-overlapped sharp falls, the deepest falls are followed by the largest three-day excess rise, and the grading is weak and uneven. Falls of -4 standard deviations or more give +1.36 % (t 2.26, 167 cases), against +0.45 % to +0.72 % for -4 to -2.5 and +0.35 % (t 0.80, 568 cases) for -2.5 to -2. The Spearman correlation between fall size and the excess return is 0.039 (p 0.17, 1243 cases). The mean strength is 0.067 (t 2.05).
- F3: The rebound after sharp falls does not come from one coin. Five of 6 coins have a positive mean excess (XRP +1.23 %, ZEC +0.93 %, XMR +0.75 %, LTC +0.47 %, BTC +0.23 %; ETH -0.08 %), but none reaches t 1.5 alone. By year, 2021 carries the most (+3.56 %, t 2.91), while 2018 and 2022 are negative (-0.42 %, -0.67 %).
- F4: On the 4h grid, the break below the prior two-day low in an uptrend gains more after a wider broken stretch. The narrow, middle and wide terciles give -0.24 % (36 cases), +3.84 % (t 2.19, 24 cases) and +7.15 % (t 2.22, 16 cases) of 18-bar excess return. These samples are small and much smaller than the verdict's 1182 cases.
