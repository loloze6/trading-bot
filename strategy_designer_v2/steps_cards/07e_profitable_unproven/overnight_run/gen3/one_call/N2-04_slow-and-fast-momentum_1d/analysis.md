---
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum_1d
idea tested: N2-04_slow-and-fast-momentum
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3348 USD
---
## Findings
- **F1:** The book earns from timing, not only from the coins' drift: it held about 30–38% of bars, and its return while held beat drift × exposure on all six coins (timing excess ZEC 5.73, ETH 4.01, BTC 3.57, XRP 2.63, LTC 0.78, XMR 0.66). Held days returned 0.00176 per day above each coin's mean (t 2.56, n 5886 daily bars). Over non-overlapping 5-bar blocks, held blocks returned +0.0081 above the coin mean (t 2.21, n 1164) and flat blocks returned −0.0039 (t −1.80, n 2255).
- **F2:** The edge sits in the strongest third of the signal: held-day excess rises from 0.0005 (t 0.52, n 1962) in the lowest forecast tercile to 0.0016 (t 1.41, n 1960) in the middle and 0.0031 (t 2.31, n 1964) in the highest. The verdict's own slope of 20-bar excess on forecast is also positive (0.0040).
- **F3:** The edge is strongest in high volatility: held-day excess is 0.0035 (t 2.30, n 1689) in the coin's top 20-day-volatility tercile, against 0.0013 (t 1.34, n 1546) in the bottom tercile and 0.0016 (t 1.48, n 1799) in the middle.
- **F4:** The profit comes from a few long, large trades: the top 10 of 2559 trades give 7290 of 14618 summed net percent (50%), and 21 of the top 25 are ZEC (11 trades, 7407) or XRP (10 trades, 1871). The win rate is 42% and the median trade is −1.14%.
- **F5:** By duration, trades held 20 days or more earn 18578 summed percent over 398 trades, while trades shorter than 10 days lose 5534 over 1765 trades. The book cuts many false starts and rides a few long runs.
- **F6:** The edge depends on the market state: held-day excess is positive in 2019 (0.0040, t 2.12, n 695) and 2020 (0.0047, t 3.11, n 1048), but negative in the falling years 2018 (−0.0083, t −2.23, n 352) and 2022 (−0.0046, t −2.29, n 388). Book gains cluster in windows w11, w21, w17 and w24 (5.22, 5.10, 4.25, 4.54).

## Ideas
- `N2-04_slow-and-fast-momentum.e1_strong-volatile-momentum-persists` (from F1, F2, F3): When a coin is up over both 20 and 60 days and its 20-day return is unusually large against its own recent history, while its 20-day volatility is in its upper range, its next days rise more than its average.
- `N2-04_slow-and-fast-momentum.e2_rare-long-runs-pay` (from F4, F5, F1): In a coin whose 20- and 60-day returns are both positive, the rise above its average comes mostly from a few runs that last more than 20 days. These runs are larger in the more speculative coins such as ZEC and XRP.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
