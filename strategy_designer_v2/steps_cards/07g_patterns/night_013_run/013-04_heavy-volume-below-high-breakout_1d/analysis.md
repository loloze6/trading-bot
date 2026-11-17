---
line: 7.g patterns
backtest: 013-04_heavy-volume-below-high-breakout_1d
idea tested: 013-04_heavy-volume-below-high-breakout
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3397 USD
---
## Findings
- **F1:** Heavy recent volume is followed by higher returns. Coins were ranked by their 5-day mean volume over their 30-day mean volume and cut into quintiles within each coin. The top quintile beat the bottom over the next 5 days by +1.93 % excess (Welch t 2.77, non-overlapping 5-day samples; Spearman 0.057 over n=2503). The bottom quintile alone averaged −1.18 % (t −2.74).
- **F2:** The same volume ranking separates the next day's return at both ends. The bottom quintile averaged −0.268 % excess (t −3.14, n=2591) and the top quintile +0.278 % (t 2.44, n=2587), with the middle quintiles near zero.
- **F3:** Split by the sign of the past 5-day return, the volume effect follows the direction of the move. Light volume after a 5-day fall gives the worst next 5 days, −1.64 % (t −2.55, n=265). Heavy volume after a 5-day rise gives the best, +1.36 % (t 1.75, n=278). Heavy volume after a fall is flat (−0.02 %).
- **F4:** The volume effect is uneven across coins and years. It is significant only in XRP (top−bot +4.9 %, t 2.25) and ZEC (+5.3 %, t 2.35); it is negative in BTC (−1.0 %, t −0.79). By year, 2024 carries most of it (+8.0 %, t 4.50), while 2018 and 2019 are mildly negative. Given the many angles examined, F1–F3 should be read as a candidate, not a settled effect.
- **F5:** The tested breakout book barely trades. Breakout ("trending") bars are only 0.7–2.4 % of bars per coin, and the mean allocation is 0.004–0.021. Its Sharpe of 0.51 over 2898 days comes from a mean daily return of 0.0000591, and 9 of 24 windows show a zero mean book return. The 30 trending 10-day samples averaged +7.7 % excess, but at t 1.46.
- **F6:** Closeness to the 30-day high showed only a weak, borderline pattern. The top quintile of close / 30-day high was followed by +2.53 % excess over 10 days (t 2.28, n=248), but top minus bottom was t 2.01 and not monotone. Weekday effects (Friday +0.30 %, t 3.66; Wednesday −0.30 %, t −2.75 next-day excess) were not consistent across years. Neither stands out enough given the number of looks.

## Ideas
- `013-04_heavy-volume-below-high-breakout.g1_volume-confirmed-short-term-continuation` (from F1, F2, F3, F4): The heavier a coin's volume over the last 5 days relative to its own 30-day average, the larger its return over the next 5 days. This holds most strongly when that volume comes with a rise over the same 5 days, and light volume during a 5-day fall is followed by the weakest returns.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
