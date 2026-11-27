---
line: 7.d confirmed, not profitable
backtest: 081-01.d1_deep-up-day-five-day-fade_1d
idea tested: 081-01.d1_deep-up-day-five-day-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4396 USD
---
## Findings
- **F1:** The fade lives only in the deepest up days. On non-overlapping 5-day cases (folds B, C), up days closing more than 4 usual 20-day swings below the 20-day high are followed by a short-side unusual move of +4.04 % (t 1.96, 141 cases on 54 days), and their total move is +3.15 %, about 14 times the 0.22 % trade cost. Up days 3 to 4 swings below give +0.96 % (t 0.70). Those 2 to 3, 1 to 2 and 0 to 1 swings below give -0.22 %, -1.09 % and -0.96 %, with total moves of -1.6 % to -2.6 %. The book shorts all of them and loses before costs.
- **F2:** The forecast's linear grading does not separate the paying cases from the losing ones. Split by tercile of the forecast, the strongest third earns +3.63 % unusual over 5 days (t 2.59, 234 cases, 73 days). The middle third earns -1.42 % (t -1.38) and the weakest -0.85 % (t -0.89). The weakest third loses -3.93 % over 10 days (t -2.28). Two thirds of the shorts cancel the gain of the first, which leaves the book's Sharpe at -0.003 and its mean daily return on days in a position at -0.0003 %.
- **F3:** The book stays short far beyond the signal. It is in a position on 83 % of coin-days, and 1,175 of its short 5-day cases fall on bars with no deep up-day signal. Those cases earn +0.26 % unusual (t 0.27) and -1.13 % total, so carrying the short past the signal pays the coin's drift (-0.82 % per 5 days against the short) for nothing. Trades last 10.6 days on average, and 1,112 trades of 5.5 days or less lose -7.1 % net each.
- **F4:** The deep cases keep fading after five days. Up days more than 4 swings below the high give +5.25 % unusual over 10 days (t 1.88), against +4.04 % over 5 days. The strongest forecast third gives +5.30 % over 10 days (t 2.13). The shallow up days, 0 to 1 swing below, turn to -3.67 % over 10 days (t -2.11).
- **F5:** The fade is concentrated in up days whose 20-day return is below -10 %. These earn +2.71 % unusual over 5 days (t 3.53, 241 cases), and the deep ones among them (more than 2.5 swings below the high) earn +3.22 % (t 1.99, 207 cases, 62 days). Up days with a 20-day return between 0 and +10 % lose -3.77 % (t -3.31, 138 cases). The condition alone carries no effect: non-signal bars with a 20-day return below -10 % earn +0.20 % unusual (t 0.19, 400 cases). Down days at the same depth do not fade either: at more than 4 swings below the high they give +0.71 % (t 0.40, 304 cases). The effect therefore belongs to relief days after a monthly fall, as the theory of under-water holders selling into relief says.
- **F6:** The 60-day trend is not where the effect lives, so no profile is named. The signal's unusual move is -0.08 % in falling markets (199 cases), +2.71 % in choppy markets (t 2.26, 77 cases) and +0.57 % in rising markets (167 cases). The deepest tercile does not fade in any trend, because these trend groups mix the depths and the 20-day falls. The book's losses come from rising stretches, where it averages -0.16 % a day against +0.12 % in falling ones. Those are the stretches where it is short shallow up days into a rising coin, against a drift of +0.60 % a day.

## Ideas
- `081-01.d1.d1_deepest-up-days-fade-steeply` (from F1, F2): In any market, a day that closes up while sitting deeper below the coin's 20-day high, measured in the coin's own usual daily swing over the last 20 days, is followed by a larger fall over the next five days, a fall that grows faster than the depth and is carried by the up days sitting several usual swings below the high.
- `081-01.d1.d2_deep-up-day-five-day-fade-only` (from F3, F1): In any market, a day that closes up while sitting deeper below the coin's 20-day high, measured in the coin's own usual daily swing over the last 20 days, is followed by a larger fall over the next five days, and the short is held for those five days only, closed unless a new deep up day renews it.
- `081-01.d1.d3_deep-up-day-ten-day-fade` (from F4, F1): In any market, a day that closes up while sitting deeper below the coin's 20-day high, measured in the coin's own usual daily swing over the last 20 days, is followed by a larger fall over the next ten days, the fall growing with the depth.
- `081-01.d1.d4_relief-day-fade-after-monthly-fall` (from F5, F6): In any market, a day that closes up while sitting deeper below the coin's 20-day high, measured in the coin's own usual daily swing over the last 20 days, is followed by a larger fall over the next five days while its 20-day return is negative, the fall growing with both the depth and the size of that 20-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
