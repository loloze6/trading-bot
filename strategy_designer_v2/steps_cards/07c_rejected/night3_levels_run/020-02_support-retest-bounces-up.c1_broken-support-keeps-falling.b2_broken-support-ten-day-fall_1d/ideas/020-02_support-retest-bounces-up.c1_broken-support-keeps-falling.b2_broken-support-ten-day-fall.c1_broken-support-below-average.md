---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall
line: 7.c rejected
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while the close is below its 50-day average.
Consequence: Below its 50-day average, a close just under a support that held several times is a reason to be short for the next ten days, the larger the cluster the stronger; above that average, it is a reason to refuse the short.
Why:
- F1: The verdict's sign reads the wrong way. On these closes the coin fell beyond its drift, as the idea says: −0.64 % over 10 days on 1164 non-overlapping cases (t −1.54). Recomputing the plan's own measure, −(forecast/10) × drift-adjusted return, gives −0.0118 (t −2.30), but with a negative forecast that product is a long's gain. The short's sized gain beyond drift is +0.0118 (t +2.30, n 1164). Read as the plan describes it ("the short's gain beyond holding the coin"), the measure confirms the idea and the supporting check also passed (+1.09 %, Welch t 1.31).
- F2: The fall is graded with the size of the forecast. By quartile of |forecast|, the 10-day drift-adjusted return runs +0.45 %, −0.64 %, −0.75 %, −1.62 % (t −2.24, n 291 each). On the 5-day horizon it runs +0.44 %, −0.13 %, −0.73 %, −0.98 % (t −2.61, n 590). At 20 days it is noisy: −0.90 %, −1.57 %, +2.20 %, −3.77 %.
- F3: The idea is small and the book shorts against the coins' rise. Its strength is only 0.026 of a usual 10-day move (14.49 %). The signal is active on 69 % of grid bars, and its cases rose +0.55 % in total over 10 days because the normal drift is +1.19 %. So the always-short book lost: Sharpe −0.55, mean daily return −0.07 %. This fits F8 and F11: in a total move against the short, no holding rule pays.
- F4: The idea holds below the 50-day average. There, larger forecasts are followed by a 10-day drift-adjusted fall of −2.65 % (t −2.91, n 228) and a total fall of −1.45 %, about 7.6 times the 0.19 % cost of a round trip. Smaller forecasts below the average give +0.42 % (n 251). Above the 50-day average there is no gradient: −0.79 % (n 73) and −0.81 % (n 96), both with |t| < 0.6.
- F6: The effect swings with the year. The 10-day drift-adjusted return on active cases is −4.53 % in 2018 (t −3.44), −2.49 % in 2019, and −2.22 % in 2022. It is +3.06 % in 2020, +3.13 % in 2021 and +1.96 % in 2023. The falls come in the bear years, which agrees with the trend condition in F4 and F5.
