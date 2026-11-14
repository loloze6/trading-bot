---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.d not profitable
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, while the 50-day SMA is below the 200-day SMA, a bar that closes below its 50-day SMA after the 50-day SMA has risen toward the 200-day over the last 10 bars is followed by a 10-bar fall larger than the coin's usual 10-bar move. The failed recovery inside the downtrend is where the late sellers act.
Consequence: A trader would take shorts only on a failed rebound inside a death-cross regime, and stand aside for the rest of the regime.
Why:
- F6: The short works only when price sits below its 50-day SMA while the 50-day SMA is climbing back toward the 200-day: there the short's 10-bar excess gain is +0.0173 on non-overlapping cases (n=107, t 1.39) and positive in every volatility tercile (+0.017 calm t 2.9, +0.035 mid t 4.7, +0.043 volatile t 5.0, overlapping). This rests mostly on 2018 (+0.104) and turns negative in 2024 (-0.038) and 2025 (-0.025), so it is fragile.
- F2: The death-cross state carries no downward drift: coins rise 0.001303 a day while the forecast is short and 0.001271 while it is flat, against 0.001287 overall.
- F1: The book loses before fees, not because of them: the gross daily return is -0.000496 against fees of only 0.000028 a day, giving a book return of -0.000524 a day, and the 1273 short trades lose a mean -11.2% before fees with only 23.9% winners.
