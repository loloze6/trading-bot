---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is low relative to its own past year, a daily move is followed by a move the same way over the next day, and the larger the move measured in units of the 20-day volatility, the larger the continuation.
Consequence: A trader would follow, not fade, a coin's daily move during its calm stretches, sizing with the move's size in volatility units.
Why:
- F3: Next-day reversal exists only in the volatile state. In the top 20-day-volatility tercile, the next day's vol-scaled return regressed on today's vol-scaled move has slope -0.070 (t -5.78). In the bottom tercile the slope is +0.049 (t 3.46) and the lag-1 correlation is +0.034, so in calm stretches a daily move continues and the fade loses.
- F4: Volatility measured against the coin's own past year sorts the same way. The top quintile of 20-day vol over 250-day vol has timing +0.001457 and net +0.000562, with reversal slope -0.047 (t -2.85). The bottom quintile has net -0.000848 (t -2.76), with continuation slope +0.068 (t 2.90).
- F2: The fade only works when the coin's own 20-day volatility is high. In each coin's top tercile of 20-day volatility, timing is +0.001570 against fees of 0.000578, net +0.000971 (t 2.91, n 10049, Sharpe 0.56). In the bottom tercile, timing is -0.000611, net -0.001353 (t -5.89, n 10043, Sharpe -1.12). In the middle tercile, net is -0.000710 (t -2.73).
