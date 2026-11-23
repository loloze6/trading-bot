---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-hour return in the first hour after the 00:00 UTC funding settlement relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way, and more so the higher its 24-hour volatility stands against its 30-day volatility.
Consequence: A trader would weight the daily post-settlement fade toward days when the coin's short-term volatility is raised against its month, where the reversal per case is largest.
Why:
- F5: The reversal is larger when the coin's 24-hour volatility is high against its 30-day volatility. Large signals earn +0.61 % (t 4.4, 1702) in the top third of that ratio against +0.24 % (t 2.6, 2224) in the bottom third. The same high-volatility condition at 13:00 earns only +0.10 % (t 0.7) for large moves, so it is not an effect alone. It also raises the spread per case (std 5.7 % against 4.4 %), so it does not cut the falls by itself.
- F4: The crowded-run condition is not an effect of its own. Fading the 24-hour move at 13:00 UTC, a clock hour with no settlement, earns nothing at any size (every quintile between -0.18 % and +0.02 %, t between -1.98 and +0.19, about 3400 cases each). Fading the 13:00 one-hour move earns between -0.14 % and +0.10 % in every cell (|t| ≤ 1.3). So the gain belongs to the settlement hour, as the brief's theory of crowded-side funding flow says.
- F2: The effect grows with the size of the post-settlement hour's move. The drift-adjusted 24-hour reversal is +0.16 % (t 2.1, 4820 cases) for |forecast| 0–5, +0.18 % (t 2.5) for 5–10, +0.39 % (t 4.5) for 10–15 and +0.50 % (t 6.7, 4872 cases) for 15–20. The small signals carry little: even holding only the signals with |forecast| ≥ 10, at full weight, lifts a simulated book's Calmar from 0.26 to 0.61, with the deepest fall going from -75 % to -63 % and Sharpe from 0.60 to 0.93.
