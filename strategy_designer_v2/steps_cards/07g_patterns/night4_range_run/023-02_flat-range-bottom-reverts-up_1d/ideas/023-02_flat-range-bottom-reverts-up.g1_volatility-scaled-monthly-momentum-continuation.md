---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up
line: 7.g patterns
backtest: 023-02_flat-range-bottom-reverts-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return relative to its own 30-day daily volatility, the more its price continues in that same direction over the next 5 days. This holds even when the past month looks flat next to its high-low range.
Consequence: A trader should trade with a coin's volatility-scaled 30-day move rather than fade it toward the middle of the range. Recent strength is a reason to be long and recent weakness a reason to refuse a long.
Why:
- F1: The tested idea runs the wrong way. In flat coins (30-day net move at most 0.3 of the 30-day range), closes in the lower range quintiles show 5-day excess returns of −0.02 % (n 105, t −0.03) and −0.70 % (n 197, t −1.20). The flat and trending cases look alike: trending quintile 1 is −1.06 % (n 314, t −1.99). So being below the middle in a flat month predicts no rebound, and the step-5 size (−0.61 % per case, −3.2× the 0.19 % cost) confirms it.
- F2: The 30-day return scaled by 30-day volatility predicts the next 5 days in its own direction. Its correlation with the 5-day excess move, in units of the usual move, is 0.056 (2,555 non-overlapping cases, t 2.84). Ranked by coin, the top 30-day-return quintile earns +1.18 % excess (n 510, t 1.99, strength 0.10) and the second-lowest −1.07 % (n 510, t −2.76, strength −0.10).
- F3: The continuation holds inside flat coins too, the regime the brief says should revert. Flat cases in the highest scaled 30-day-return group gain +2.33 % excess over 5 days (n 114, t 2.57, strength 0.22). Trending cases in the top quintile gain +1.09 % (n 511, t 1.93). The highest range-position quintile in trending coins gains +1.32 % (n 433, t 2.11, strength 0.11).
- F4: Measured in the direction of the past 30-day move, continuation grows from the smallest scaled moves to the larger ones. By size quartile it is −0.19 % (t −0.54), then +0.94 % (t 2.52), +0.80 % (t 1.90) and +0.63 % (t 1.25), with 639 cases each.
- F5: The continuation in F4 is positive in 5 of 6 coins, with ETH strongest at +1.11 % (t 2.42) and XMR the exception at −0.18 % (t −0.41). It is uneven across years: it is concentrated in 2020 (+1.76 %, t 2.67) and 2021 (+2.53 %, t 3.59), and negative in 2022 (−0.97 %, t −1.88). Its reliability outside the 2020–2021 bull years is therefore weak.
