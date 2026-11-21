---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 30-day hourly volatility stands above its own 90-day norm, the more of its last 24 hours' move, scaled by that volatility, it gives back over the next 24 hours.
Consequence: A trader fading a coin's daily move should do it mainly when the coin is unusually volatile for itself, and leave it alone in calm stretches.
Why:
- F1: Measured on the 30-day-volatility-scaled 24-hour return at every bar (non-overlapping grid, 15,950 cases), the 24-hour reversal is three times stronger in the top tercile of volatility relative to its own 90-day median (−60.6 bp of next-24h excess return per unit z, t −8.2) than in the middle tercile (−22.7 bp, t −3.1), and absent in the bottom tercile (−2.0 bp, t −0.3); the top-tercile slope is negative in all 8 years, with t at or below −2.1 in 6 of them.
- F5: The book fails mainly because it holds too little of the market's rise rather than because the signal is wrong: Sharpe 0.50 sits 0.057 below holding, and its mean daily return of 0.000368 is under the 0.0005 bar, while the reversal it trades is only a mid-strength slice (F2) of a broader effect that is strongest in high-volatility stretches (F1).
