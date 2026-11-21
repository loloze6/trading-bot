---
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
idea tested: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3734 USD
---
## Findings
- **F1:** The book barely earns while simply holding the coins earns far more. Its mean daily return is 5.6e-05 against roughly 0.0007–0.0016 a day for holding each coin. Its chained yearly return is -0.7%, with a deepest fall of -49%. Its 3761 trades average -1.35% before fees and -1.45% after, with a 48.8% win rate.
- **F2:** The book's worst windows are the ones where the coins themselves fell. In w2 the book returned -0.0029 a day while the coins returned -0.0038; in w14 it was -0.0019 against -0.0043, in w7 -0.0014 against -0.0047, in w1 -0.0014 against -0.0015, and in w9 -0.0010 against -0.0026. So the rebound bet keeps buying falls that continue when the larger trend is down, and these windows carry the falls and the one-window-left-out weakness.
- **F3:** On the 72-bar grid, the active cases with a 30-day (720-bar) return in the top third returned +0.0081 over the next 3 days (t 2.56, n 679). Those in the bottom third returned only +0.0003 (t 0.09, n 678), and the middle third returned -0.0016 (n 678). The highest forecast tercile inside the rising-month group returned +0.0197, against +0.0010 in the falling-month group.
- **F4:** Only the strongest forecasts pay. Active cases in the forecast's top third had a mean excess 3-day return of +0.0047 (t 1.71, n 921). The low third had -0.0035 (t -1.30, n 921) and the middle third -0.0057 (t -2.09, n 920), yet the book holds a position on all of them.
- **F5:** The rebound is carried by agitated markets. Active cases where the 3-day hourly volatility was high against the 30-day volatility returned +0.0086 over the next 3 days (t 2.58, n 679). The calm third returned -0.0019 (n 678).
- **F6:** Being in the fall regime costs the book the market's rise. Grid bars with a positive forecast returned +0.0026 over the next 3 days, against +0.0055 on the 2921 bars the book sat flat. Window fees of 0.014–0.020 per coin eat about half of the window gross of -0.003 to +0.071, and ETH's gross is negative.

## Ideas
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.d1_rebound-inside-monthly-uptrend` (from F2, F3, F1): When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, and the deeper its 3-day fall, the larger that rebound, only while the coin has risen over the past 30 days, with the rebound larger the stronger that 30-day rise.
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.d2_rebound-after-volatile-drops` (from F5, F4, F1): When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, and the deeper its 3-day fall, the larger that rebound, only while its hourly volatility over the past 3 days is high against its hourly volatility over the past 30 days, with the rebound larger the higher that ratio.
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.d3_dip-in-rising-month` (from F3, F6): When a coin has risen over the past 30 days, the deeper its fall over the past 3 days, the more it rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
