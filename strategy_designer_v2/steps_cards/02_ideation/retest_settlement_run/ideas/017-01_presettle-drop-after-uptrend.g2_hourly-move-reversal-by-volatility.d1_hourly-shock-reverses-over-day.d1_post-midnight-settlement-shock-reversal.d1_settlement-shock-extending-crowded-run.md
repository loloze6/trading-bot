---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When the coin's return in the first hour after the 00:00 UTC funding settlement runs the same way as its return over the previous 23 hours, the larger that hour's return relative to its 24-hour volatility, the more the coin's return over the next 24 hours runs the opposite way.
Consequence: A trader would fade the post-midnight-settlement hour mainly when it extends the day's run, sized by the move, and take little or no position when the hour moves against the day's run, which leaves out the cases that carry the losses without the gain.
Why:
- F3: The reversal is stronger when the 01:00 hour moved the same way as the coin's prior 23 hours, so that the shock extends the side that was already crowded. In that case the large signals earn +0.57 % per case (t 6.8, 3867) and the small ones +0.33 % (t 4.1). When the hour runs against the prior 23 hours, the large signals earn +0.35 % (t 4.5) and the small ones +0.02 % (t 0.37, 4822 cases). Graded the same way, the quintile where the 24-hour move ran most in the shock's direction earns +0.78 % (t 7.2, 3380).
- F4: The crowded-run condition is not an effect of its own. Fading the 24-hour move at 13:00 UTC, a clock hour with no settlement, earns nothing at any size (every quintile between -0.18 % and +0.02 %, t between -1.98 and +0.19, about 3400 cases each). Fading the 13:00 one-hour move earns between -0.14 % and +0.10 % in every cell (|t| ≤ 1.3). So the gain belongs to the settlement hour, as the brief's theory of crowded-side funding flow says.
- F2: The effect grows with the size of the post-settlement hour's move. The drift-adjusted 24-hour reversal is +0.16 % (t 2.1, 4820 cases) for |forecast| 0–5, +0.18 % (t 2.5) for 5–10, +0.39 % (t 4.5) for 10–15 and +0.50 % (t 6.7, 4872 cases) for 15–20. The small signals carry little: even holding only the signals with |forecast| ≥ 10, at full weight, lifts a simulated book's Calmar from 0.26 to 0.61, with the deepest fall going from -75 % to -63 % and Sharpe from 0.60 to 0.93.
- F1: The check failed on the falls. The book's deepest fall was -47.0 % over 140 days in w12–w13, against a yearly return of +22.2 % (Calmar 0.47 against the 0.75 required). During that fall the coins barely drifted (-2.8 bp a day) but moved hard (346 bp mean absolute daily move), while the book lost 40 bp a day. In w12 the large signals (|forecast| ≥ 10) lost 0.49 % per case (t -2.04, 410 cases), and w12 alone fell 42 %.
