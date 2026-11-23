---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday close-to-close move is undone over the next 2 days (Monday and Tuesday), more strongly the higher the coin's past 20-day volatility stands relative to its usual 60-day volatility, with the larger moves reversing the most, only while the 20-day volatility stands clearly above the 60-day volatility.
Consequence: A trader would lean against Sunday's move only in turbulent stretches, and graded by how turbulent, and stay out on calm and middling Sundays where the reversal does not show.
Why:
- F1: The check failed on Calmar alone (0.51 against the 0.75 rule). The rebuilt book shows the same, with a yearly return of +12.3 % over a deepest fall of -23.9 %. That fall lasted 908 days through windows w1 to w9 (years 2018, 2019, 2022 and 2023). The coins' mean daily return in it was -0.0004 %, so the book lost 23 % summed while the market stood flat.
- F2: The reversal is carried by the most turbulent Sundays. Split into quintiles of the 20-day to 60-day volatility ratio (about 520 Sunday cases each), the mean 2-day move against Sunday, net of drift, is +0.74 % (t 2.6), +0.12 % (t 0.4), -0.20 % (t -0.5), +0.81 % (t 2.4) and +2.10 % (t 5.0). The two middle quintiles earn nothing and are where the book's position-days cost fees for no reversal.
- F3: Trading the same book only when Sunday's volatility ratio is in its top 40 % lifts Calmar from 0.51 to 0.84 and Sharpe from 0.74 to 0.91. It also cuts the deepest fall from -23.9 % to -10.0 %, while the yearly return goes from +12.3 % to +8.4 %. This is the only change tried that passes the failed measure: short only reaches 0.21, long only 0.45, and dropping longs against the 20-day trend 0.47.
- F4: The volatility condition is not an effect of its own. On non-Sunday bars, the same 2-day bet against the day's move earns +0.21 % (t 1.0, 1543 cases) in the top volatility-ratio quintile, against +2.10 % (t 5.0, 520 cases) on Sundays. The condition only strengthens the Sunday liquidity reversal: per the brief's theory, a turbulent market leaves thin weekend books moved further by imbalance.
- F6: The effect is weakest exactly in the fall's years. The mean 2-day move against Sunday was +0.17 % (t 0.7) in 2022 and +0.28 % (t 1.6) in 2023, against +0.55 % to +1.33 % in the other years. The book's mean daily return was -0.007 % in 2022 and +0.009 % in 2023, against +0.03 % to +0.07 % in the other years.
- F7: Size is not the obstacle. The total move per case is +0.74 % against a 0.22 % round-trip cost, 3.3 times, and in the top volatility quintile the reversal is about 2.1 %, near ten times the cost.
