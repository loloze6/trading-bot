---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 7-day return is negative, the further its latest 1-day move falls relative to its 60-day volatility, the more the coin rises over the next 2 days. The effect is stronger the deeper the coin's 7-day fall relative to its volatility.
Consequence: In a falling coin, a sharp down day is a reason to lean long and a strong up day is a reason to lean short for the next two to three days.
Why:
- F1: When a coin is in the bottom fifth of its 7-day return scaled by its 60-day volatility, its next 2-day excess return falls as its signed 1-day move rises: slope −0.0100 per unit of z, t −8.98, n 3004 non-overlapping cases; at 3 days the slope is −0.0127, t −8.84, n 2005; the middle and top fifths have flat or positive slopes (+0.0003 t 0.25, +0.0068 t 3.01, +0.0022 t 1.81, +0.0013 t 1.13).
- F2: Split by the sign of the prior 7-day return, the 1-day move's sign reverses in falling coins and persists in rising ones: down-trend slope −0.0040 (t −4.11, n 7580) against up-trend slope +0.0025 (t 3.19, n 7440), and −0.0063 (t −5.61) against +0.0049 (t 4.24) at 3 days.
- F3: In falling coins, days down by more than one usual move are followed by +0.0080 excess over 2 days (t 3.11, n 923), while up days of 0.3 to 1 usual moves are followed by −0.0070 (t −4.41, n 1755); in rising coins, up days of more than one usual move are followed by +0.0093 (t 3.40, n 1056).
- F5: The move-against-the-7-day-trend measure keeps its effect when the tested idea's absolute move size is in the same regression (t −4.86 against absz t 2.58), so the tested idea misses most of the pattern.
- F6: The against-trend slope is negative in 15 of 19 coins and in 7 of 8 years, with t at or below −2.7 in 2021, 2023, 2024 and 2025; 2020 goes the other way (t +3.87), and so do the down-trend reversals in that year (t +2.16).
