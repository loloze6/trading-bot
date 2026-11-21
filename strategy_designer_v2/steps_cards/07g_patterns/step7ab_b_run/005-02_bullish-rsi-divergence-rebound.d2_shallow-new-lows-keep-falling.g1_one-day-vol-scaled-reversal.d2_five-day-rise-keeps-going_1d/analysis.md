---
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3767 USD
---
## Findings
- **F1:** When a coin's 20-day volatility is above its own median, a large one-day rise is followed by a fall the next day: the slope of the next day's unusual return on the day's return in units of 20-day volatility is −0.118 (t −5.0, 2,420 one-day cases). With volatility below its median the slope is +0.027 (t +1.8, 2,414 cases). The difference between the two slopes has a t of about −5.1, which stands out even after the many angles looked at.
- **F2:** Over all bars, the one-day reversal is graded. The day after the bottom fifth of vol-scaled one-day returns earns an unusual +0.21 % (raw +0.34 %). After the top two fifths it earns −0.23 % and −0.13 % (raw −0.10 % and −0.00 %). The pooled slope t is −2.86 on 4,834 cases, and both coins show it (BTC t −1.6, ETH t −2.4).
- **F3:** The one-day reversal is also stronger when 20-day volatility is high against 60-day volatility (t −3.6, 3,382 cases; t +0.4 otherwise). It is stronger when the coin's 60-day return is negative (t −3.3, 3,279 cases; t −0.4 when positive). Both conditions overlap with high volatility (F1).
- **F4:** The tested 5-day rise effect is carried by its top fifth. A vol-scaled 5-day return above about 0.87 is followed by an unusual +1.09 % over 3 days (t 3.2, 314 cases), while the fourth fifth is −0.66 % (t −1.9). The effect fades with the horizon: slope t is 2.2 at 3 days, 0.65 at 5 days and 1.1 at 10 days.
- **F5:** The 5-day rise effect looks larger at low volatility (t 2.27, 775 cases) than at high (t 0.96, 796 cases), but the interaction t is only 0.48. It looks larger in windows w13–w24 (t 2.3) than in w1–w12 (t 0.6). Neither split can be told apart from chance.
- **F6:** No weekday stands out among 7. Wednesday's next-day unusual return is −0.39 % (t −2.4, 830 cases), which is not distinct from chance across 7 tests. The bar's high-low range in volatility units predicts nothing at any horizon from 1 to 7 days (|t| ≤ 1.1).
- **F7:** The record holds only BTC and ETH, not the brief's BNB.
- **F8:** Trades lasting 8 days or more average +12.9 % after fees (437 trades), while trades of 0 to 4 days average −1.5 % and −2.2 %. This is mostly by construction, since a trade lasts while the rise continues. It supports no idea on its own.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going.g1_turbulent-one-day-move-reverses` (from F1, F2, F3): When a coin's 20-day daily volatility is high against its own usual level, the larger its last day's return relative to that volatility, the more of it the coin gives back over the next day, with a large one-day fall followed by a rebound and a large one-day rise by a decline.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
