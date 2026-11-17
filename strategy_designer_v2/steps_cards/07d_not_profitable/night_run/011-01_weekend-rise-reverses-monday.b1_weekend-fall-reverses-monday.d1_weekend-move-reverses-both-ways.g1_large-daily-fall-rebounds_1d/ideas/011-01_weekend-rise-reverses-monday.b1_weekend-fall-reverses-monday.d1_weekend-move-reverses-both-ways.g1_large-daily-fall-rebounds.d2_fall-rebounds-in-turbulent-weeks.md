---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's own daily fall that is large against its 20-day volatility, the coin rises over the next 1 day, and the larger the fall in units of its usual daily move, the larger the rebound, only while the coin's 5-day volatility is high against its 20-day volatility, the rebound being larger the higher that ratio.
Consequence: A trader would keep the dip-buying for turbulent days, when the recent swings are wider than usual, and stay flat after falls in quiet weeks.
Why:
- F5: The rebound is also concentrated where short-term volatility is high. Bars whose 5-day volatility is in the top quintile against 20-day volatility (ratio 1.28–2.04) earn +0.0067 mean excess (t 3.10, gain 3.08). The other four quintiles together are near zero (between -0.0037 and +0.0001).
- F4: The book does not keep up with holding, and its daily return and Calmar fall short. Its mean daily return is 0.000289 (Sharpe 0.48) against holding's 0.00118 (Sharpe 0.55), and its deepest fall is -32.8%. Fees take 3.73 of 8.82 summed gross gain (42%), and the market's own rise adds only 0.000141 per bar against 0.000366 of timing.
- F6: Positions carried after the forecast has gone to zero earn nothing: 1612 bars, mean excess -0.0022 (t -1.77), gain -0.02. Fresh signal bars earn +0.0024 (t 3.44, gain 8.84).
