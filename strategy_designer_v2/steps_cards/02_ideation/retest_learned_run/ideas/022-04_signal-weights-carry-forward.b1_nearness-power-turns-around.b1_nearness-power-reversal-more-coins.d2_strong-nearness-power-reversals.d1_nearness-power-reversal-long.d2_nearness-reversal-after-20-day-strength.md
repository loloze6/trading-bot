---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin's nearness to its 90-day high, the larger both the excess of its past 365-day predictive power for 5-day returns and today's deviation of nearness from its usual level, when the reading points against a past relation that implies a fall, the larger the coin's rise over the next 5 days. This rise is larger the higher the coin's 20-day return.
Consequence: A trader should weight the long nearness-power reversal by the coin's 20-day return and refuse it after a 20-day fall, where the book lost with a Sharpe of -1.8.
Why:
- F1: The check failed on Calmar alone (0.615 against 0.75): the yearly return of +20.7 % sits against a deepest fall of -33.7 %. That fall is one episode lasting 850 days across w1–w8, while the coins in the book fell -53.6 % and the book chained -5.8 %. The year of that fall, 2022, is the book's worst (book -32.0 %, coin -63.5 %), and 2018 also ends flat (book -2.0 %, coin -83.1 %).
- F2: The book's falls come from staying long while the coin is in a downtrend. On days in a position, the book's mean daily return in the coin's lowest third of 20-day return is -0.220 % (Sharpe -1.81, 4449 coin-days), against +0.393 % (Sharpe 3.29) in its highest third. By price against its 100-day mean the pattern is the same: -0.181 % (Sharpe -1.42) below, +0.396 % (Sharpe 3.25) above. On the book's worst 5 % of days, 77.6 % of coins were in a position (63.4 % on all days), with a mean price 6.5 % below the 100-day mean (+3.7 % on all days).
- F4: The 20-day return separates the cases the same way. With the signal, the unusual move is +0.70 % in the top third (t 2.81, 565 cases) against +0.03 % in the bottom third (781 cases). Without the signal, the top third earns +0.17 %, so here too the condition alone carries little.
