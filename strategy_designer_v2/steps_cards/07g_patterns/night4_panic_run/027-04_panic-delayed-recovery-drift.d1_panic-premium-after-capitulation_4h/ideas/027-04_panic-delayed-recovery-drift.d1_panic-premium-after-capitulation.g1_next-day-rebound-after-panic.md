---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation
line: 7.g patterns
backtest: 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a 24-hour fall, the coin earns more than its usual return over the next 24 hours. The more usual 24h moves the fall spans and the more times its usual size the 24-hour range is, the larger that next-day rebound.
Consequence: A trader would provide liquidity right at the close of a wide-range down day, holding for about one day, and refuse to buy narrow-range falls or to wait days for the premium.
Why:
- F2: The panic premium does exist, but only over the next day. On a non-overlapping 24h grid, the bottom decile of the coin's 24h return in usual 24h moves is followed by a 24h unusual move of +0.55 % (t 3.49, 1292 cases). The second decile is followed by +0.27 % (t 2.03). Deciles 3 to 10 lie between -0.26 % and 0 %, so the effect is graded with the depth of the fall.
- F3: The next-day rebound after the deepest falls is positive in all six coins. It runs from +0.19 % for BTC (t 0.68) to +0.81 % for ZEC (t 1.69), with XMR +0.67 % (t 1.98). It is positive in 7 of 8 years, with 2021 at +1.73 % (t 3.97) and 2018 at +1.19 % (t 2.51); 2020 is the only negative year, at -0.39 %.
- F4: The rebound comes from the falls with a wide range. In the bottom 24h-return decile, the next 24h unusual move is +0.66 % when the 24h range is in the top tercile of its 30-day-mean multiple, against -0.41 % in the middle tercile and -0.60 % in the low tercile. In the second decile it is +0.53 % in the top tercile against roughly 0 % in the other two.
- F5: The longer-horizon readings vanish on non-overlapping samples. The 6-day unusual move after the top 24h-range quintile is +1.02 % (t 1.51, 396 cases), and after the top 24h-return decile +0.88 % (t 0.98). The overlapping readings of t 3.76 and t 4.27 were inflated by counting the same moves several times.
- F1: The tested idea finds no move. Its 692 cases end -0.53 % below the coin's normal 78-bar drift (t -0.81). In every 24h-fall quintile, split by the sign of the prior 90-day return, the 13-day unusual move has |t| ≤ 1.27; the deepest-fall quintile with a negative 90-day return gives -3.1 % (t -1.27, 38 cases). The book is in position on 54 % of bars and trails holding by 0.11 Sharpe.
