---
line: 7.d not profitable
backtest: 002-02_sma-death-cross-downward-drift_1d
idea tested: 002-02_sma-death-cross-downward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4686 USD
---
## Findings
- **F1:** The book loses before fees, not because of them: the gross daily return is -0.000496 against fees of only 0.000028 a day, giving a book return of -0.000524 a day, and the 1273 short trades lose a mean -11.2% before fees with only 23.9% winners.
- **F2:** The death-cross state carries no downward drift: coins rise 0.001303 a day while the forecast is short and 0.001271 while it is flat, against 0.001287 overall.
- **F3:** A larger forecast loses more because it adds size without adding edge: the top |forecast| tercile loses -0.002588 a day gross at a mean allocation of -1.52, against -0.000487 for the bottom tercile at -0.27, even though forward 10-bar coin returns are similar (0.0150 vs 0.0199).
- **F4:** The book pays only when the whole market falls: it gains in 2018 (+2.62 summed daily gross, coin -0.0035 a day, 79% short) and 2022 (+0.93, coin -0.0018 a day, 89% short), and loses in 2020 (-5.35, coin +0.0042 a day) and 2024 (-2.96, coin +0.0024 a day), with window w16 alone at -4.66.
- **F5:** Short losses come from volatile bars: short bars in the calm volatility tercile earn +0.000051 a day gross, against -0.001138 in the middle tercile and -0.001446 in the volatile tercile, where coins rise 0.001786 a day.
- **F6:** The short works only when price sits below its 50-day SMA while the 50-day SMA is climbing back toward the 200-day: there the short's 10-bar excess gain is +0.0173 on non-overlapping cases (n=107, t 1.39) and positive in every volatility tercile (+0.017 calm t 2.9, +0.035 mid t 4.7, +0.043 volatile t 5.0, overlapping). This rests mostly on 2018 (+0.104) and turns negative in 2024 (-0.038) and 2025 (-0.025), so it is fragile.
- **F7:** Shorting a deepening decline loses: with price below its 50-day SMA and the spread still widening, the short's 10-bar excess gain is -0.0102 non-overlapping (n=247, t -1.14), and -0.0147 (t -3.29) in the volatile tercile.
- **F8:** Shorting while price is already above its 50-day SMA and the spread is still widening loses -0.0416 per 10 bars in the mid-volatility tercile (n=253, t -4.54, overlapping).
- **F9:** Young death crosses lose and mature ones hold up better: shorts at most 60 bars into the state have a non-overlapping short gain of -0.0067 (n=398, t -1.05), against +0.0118 (n=212, t 1.27) for states older than 60 bars.

## Ideas
- `002-02_sma-death-cross-downward-drift.d1_failed-rebound-in-downtrend` (from F6, F2, F1): In one coin, while the 50-day SMA is below the 200-day SMA, a bar that closes below its 50-day SMA after the 50-day SMA has risen toward the 200-day over the last 10 bars is followed by a 10-bar fall larger than the coin's usual 10-bar move. The failed recovery inside the downtrend is where the late sellers act.
- `002-02_sma-death-cross-downward-drift.d2_volatile-deepening-selloff-rebounds` (from F7, F5, F3): In one coin, while the 50-day SMA is below the 200-day SMA and the gap between them has widened over the last 10 bars, a close below the 50-day SMA in high 20-day volatility is followed by a 10-bar rise larger than the coin's usual 10-bar move. An extended, accelerating decline exhausts itself and rebounds.
- `002-02_sma-death-cross-downward-drift.d3_fresh-cross-already-recovering` (from F8, F9, F4): In one coin, when the 50-day SMA has just crossed below the 200-day SMA and price closes back above its 50-day SMA, price rises over the next 10 bars by more than the coin's usual 10-bar move. A fresh cross with price already recovering marks a low that has passed, not the start of a downtrend.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
