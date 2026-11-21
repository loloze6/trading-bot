---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin's 30-day volatility, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower the same signal's predictive power for that coin's 5-day returns over the following 90 days. This reversal is larger the more the side it points to agrees with the coin's own 28-day return.
Consequence: A trader would take the reversed-volatility bet mainly when it runs with the coin's 4-week trend, and refuse it against the trend, which cuts the losing shorts in rising stretches.
Why:
- F1: The book fails on its falls and not on its trading costs: its deepest fall is 54.5 % over 556 days in w14–w18, where the book summed −0.73 while holding the coins summed +0.83, and its fees are only 0.002 % to 0.006 % of the book per bar.
- F3: The book's gain comes from its longs only. Long bars earn +0.118 % per bar (7497 bars); short bars earn −0.009 % (8190 bars), although the book is short about half the time in every stretch (46 % to 51 %).
- F4: In w14–w18 both sides lose, shorts −0.165 % per bar (1609 bars) and longs −0.051 % (1872 bars), while in w1–w13 both earn (+0.068 % and +0.172 %). The book's deepest fall is therefore a period in which the reversed volatility relation did not hold.
- F5: The book's gain sits in the bets that agree with the coin's 28-day return:
