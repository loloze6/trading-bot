---
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound_1h
idea tested: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3365 USD
---
## Findings
- **F1:** The book loses on costs. Its gross gain per day (0.106 % BTC, 0.075 % ETH) is about half its fees per day (0.211 %, 0.182 %), on a turnover of 4.1 and 3.3 times the book per day. Its 25808 trades, median 2 hours, average +0.093 % before fees against a 0.11 % trade cost, so −0.007 % after fees. The mean daily book return is −0.112 % on both coins, while the coins themselves averaged +0.12 % and +0.14 % a day.
- **F2:** The idea is too small for the cost. Per case over 2 hours the total move is +0.04 % (0.4 times the 0.11 % cost) and the unusual move +0.03 % (strength 0.025, half that of the real ideas measured so far), over 14913 cases.
- **F3:** The book is long on about 50 % of bars, mostly on weak forecasts that carry nothing. On the 2-hour grid, forecasts of 0.01–1 (10451 cases) give an unusual move of +0.016 % (t 1.49), and forecasts of 1–5 (2957) give +0.003 % (t 0.15). Only forecasts above 5 (7048) give +0.060 % (t 3.06), still about half the cost.
- **F4:** The rebound follows only the heaviest volume. Hourly falls beyond 2 typical moves rebound +0.21 % over 2 hours on volume 3–5 times average (t 2.15, 417 cases) and +0.29 % on volume above 5 times (t 2.16, 386). On volume 1–2 times they give −0.04 % (t −0.41, 393) and on 2–3 times −0.01 % (t −0.12, 344).
- **F5:** The largest falls rebound by more than a trade costs, but on few cases. Falls beyond 4 typical moves rebound +0.29 % over 2 hours (t 1.76, 260 cases), and the top fall×volume score bin gives a total move of +0.47 % (t 1.61, 109 cases). Intermediate scores do not grow monotonically: 10–20 gives +0.008 % and 20–40 gives −0.085%, hence the verdict's negative slope of −4.9e-6.
- **F6:** Among falls with a score above 10, the 2-hour rebound sits in high-volatility states: +0.27 % (t 1.30, 197 cases) when 30-day volatility is high against its 90-day average. In calm states it is +0.02 % (197) and in middle states −0.08 % (196). Only 58 % of windows have a positive mean.
- **F7:** Large hourly rises do not continue as the brief claimed. Every volume bin of rises beyond 2 typical moves shows a 2-hour unusual move between −0.11 % and −0.003 %, none with |t| above 1.1.

## Ideas
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound.d1_extreme-volume-crash-rebound` (from F1, F3, F4, F5): After an hour in which the coin falls far more than its typical hourly move over the past 30 days on volume several times its average hourly volume over the past 30 days, the price rebounds over the next two hours. The rebound grows with how many times that hour's volume exceeds its 30-day average, so that the falls on the heaviest volume carry most of it.
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound.d2_crash-rebound-in-turbulence` (from F1, F2, F6): After an hour in which the coin falls far more than its typical hourly move over the past 30 days on volume several times its average hourly volume over the past 30 days, the price rebounds over the next two hours. The rebound is larger the higher the coin's 30-day volatility stands against its 90-day average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
