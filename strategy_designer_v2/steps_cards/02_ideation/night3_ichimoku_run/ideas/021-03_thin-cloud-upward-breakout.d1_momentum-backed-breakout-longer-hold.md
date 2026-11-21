---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-03_thin-cloud-upward-breakout
line: 7.d not profitable
backtest: 021-03_thin-cloud-upward-breakout_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close that crosses up from below a coin's Ichimoku cloud to above it, the coin rises over the next 40 days, and the larger the coin's 60-day return before the cross, the larger the rise.
Consequence: A trader would keep an upward cloud breakout for about 40 days rather than 26, and lean harder on breakouts that come after a strong two-month rise, which are the ones that carry the gain.
Why:
- F2: The move after an upward cloud cross outlasts the 26-day hold. The mean rise from the cross is +8.7 % at 26 days and +12.6 % at 39 days (181 and 161 crosses). On trades, the mean is +10.1 % at 26 days and +13.6 % at 52 days (287 and 210). The position's gain per bar is largest at ages 25 to 40 days, at 0.00586 (t 3.28, 485 bar-cases), against 0.0015 to 0.0024 at ages 0 to 25. It turns to -0.00038 beyond 40 days. The book exits just before its best stretch.
- F3: The cloud-thinness grading points the wrong way in the book. Thinner clouds at entry give slightly lower net trade returns (Spearman rho -0.125, p 0.02, 336 trades), and the forecast size does the same (rho -0.136, p 0.012). The verdict's thin-minus-thick difference is only +0.23 %. The sizing therefore adds risk without adding gain.
- F4: The coin's 60-day return before the cross sorts the outcome. Trades in its top tercile net +18.7 % against +2.0 % in its bottom tercile (161 trades). Their 26-day forward return is +27.0 % against -0.1 %. The 40-day return sorts the same way more weakly (+10.2 % against +5.8 %, rho 0.155, 208 trades).
- F5: The losses that pull Calmar to 0.68 (deepest fall 23 %) fall in the bear years. Trades lost -7.8 % on average in 2018 (26 trades) and -1.0 % in 2022 (40 trades), against +17.5 % to +18.5 % in 2020 and 2021. In those two years the book's mean daily return was -0.00033 and -0.00039, while the coins fell -0.0033 and -0.0019 a day. Within a trade, the mean worst point of the path is -7.5 %, and the 10th percentile is -22.6 %.
