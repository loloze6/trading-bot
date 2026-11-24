---
line: 7.d confirmed, not profitable
backtest: 031-01.b2.b1_long-up-streaks-ten-day-continuation_1d
idea tested: 031-01.b2.b1_long-up-streaks-ten-day-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4319 USD
---
## Findings
- **F1:** The book is in the market almost all the time even though the signal is not: 96.9 % of coin-bars carry a positive allocation, but the forecast is above 0 on only 50.9 % of them. The 10-bar minimum holding and the volatility sizing keep the long on after each streak ends (mean allocation 0.53 on bars with forecast 0, against 0.57 with forecast above 0).
- **F2:** Because of F1 the book's falls are the coins' own falls, scaled down. Its daily returns correlate 0.90 with holding the coins. Its deepest fall, -43.2 % over 276 days (w12–w14), came while holding fell -78.4 %. The next five falls (-42.9 %, -36.7 %, -35.4 %, -24.9 %, -23.7 %) each came with holding down -30 % to -67 %. This is why the Calmar fails (0.54 against 0.75) while the Sharpe passes (0.74).
- **F3:** The bars without the signal carry the losses but not the timing. Gain on forecast-0 bars was 11.1 summed, against 3.0 on forecast-positive bars, and those bars hold 45.7 % of all losing gain. They simply follow the coin's drift: mean gain 0.13 % a day against the coin's 0.28 %.
- **F4:** One-day streaks, the commonest case, are followed by a loss rather than a rise. Forecast 0–4 has a 10-day excess of -2.18 % (t -2.84, n 371). Streaks of two days or more rise: +1.57 % (t 1.33, n 260) at forecast 4–8, +2.01 % at 8–14, and +5.25 % (t 2.66, n 54) at 14+. Pooled, this gives the idea's unusual move of -0.21 % (t -0.34) against a cost of 0.19 %.
- **F5:** The continuation exists only when the coin is above its 100-day average. There, streaks of two or more days are followed by +4.60 % 10-day excess (t 2.38, n 120). Below that average the same streaks are followed by -2.65 % (t -2.05, n 100). Inside the above-average state the rise still grows with the forecast (slope 0.0046 per unit, t 1.49, n 218).
- **F6:** Being above the 100-day average is not the effect by itself. Grid cases above it with no streak signal have an excess of +0.32 % (t 0.31, n 188), against +4.60 % when a 2+ day streak is present. The condition belongs to the idea's own continuation theory: trend followers and late herders act when a visible run sits inside an established rise.
- **F7:** The coin's positive 30-day return works the same way. 2+ day streaks with a positive 30-day return are followed by +3.71 % excess (t 2.33, n 186). With a negative 30-day return they are followed by -0.79 % (t -0.76, n 135). Positive 30-day return without a streak signal gives -0.67 % (t -0.78, n 299), so that condition alone earns nothing.
- **F8:** Among the 10-day grid cells, the top quartile of 30-day return gives +3.89 % excess with a signal (t 2.26, n 162), against -1.50 % without one (n 145). The top quartile of distance above the 100-day average gives +3.24 % with a signal, against +0.96 % without. The rise after streaks is concentrated where the coin is already well up.

## Ideas
- `031-01.b2.b1.d1_up-streaks-inside-uptrend` (from F2, F3, F5, F6, F8): The more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it rises over the next 10 days, only while its close stands above its own 100-day average close, and the further above that average the larger the rise.
- `031-01.b2.b1.d2_up-streaks-after-monthly-rise` (from F1, F2, F7, F8): The more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it rises over the next 10 days, only while its 30-day return is positive, and the larger that 30-day return the larger the rise.
- `031-01.b2.b1.d3_multi-day-streaks-held-ten-days` (from F1, F3, F4): The more days beyond a single day a coin has kept closing higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it rises over the next 10 days, held only for the 10 days following the streak.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
