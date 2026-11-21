---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more evenly a coin's volume was spread across the hours of its last 24 hours, the larger the share of that 24-hour move it gives back over the next 24 hours.
Consequence: A steady, evenly traded daily move is a stronger reason to lean against it than a move made in one volume burst.
Why:
- F3: Against the brief, moves made with volume spread evenly across the 24 hours reverse more than moves made in a volume burst: the grid slope is −49.0 bp per z (t −6.0) in the lowest tercile of max-hour volume share versus −14.2 bp (t −2.3) in the highest, and the z × volume-concentration interaction is positive on all 6 coins (t 0.5 to 2.7, 4 of 6 above 1.8).
- F1: Measured on the 30-day-volatility-scaled 24-hour return at every bar (non-overlapping grid, 15,950 cases), the 24-hour reversal is three times stronger in the top tercile of volatility relative to its own 90-day median (−60.6 bp of next-24h excess return per unit z, t −8.2) than in the middle tercile (−22.7 bp, t −3.1), and absent in the bottom tercile (−2.0 bp, t −0.3); the top-tercile slope is negative in all 8 years, with t at or below −2.1 in 6 of them.
