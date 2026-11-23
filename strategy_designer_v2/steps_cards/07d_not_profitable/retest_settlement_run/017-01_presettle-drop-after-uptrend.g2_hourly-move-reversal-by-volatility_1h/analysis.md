---
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h
idea tested: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5700 USD
---
## Findings
- **F1:** The book loses on costs it can never cover: 364,283 trades with a median length of 60 minutes lose 0.20 % each before fees and 0.30 % after, and the idea's one-hour move per case is +0.01 % against a 0.19 % round-trip cost. Even the strongest one-hour bucket (moves of 1–2 usual moves) gives only +0.036 % (t 9.2, 83,732 cases), so the Sharpe of -13.77 and Calmar of -0.99 come from turnover (20.77 trades a day), not from a missing effect.
- **F2:** The same reversal grows with the horizon up to a day. For hourly moves of 1–3 usual moves, the unusual move on non-overlapping grids is +0.030 % at 6 h (t 1.6), +0.124 % at 12 h (t 3.4, 9,382 cases) and +0.326 % at 24 h (t 4.5, 4,877 cases). The 24 h strength is 0.064 and the total move is +0.326 %, which covers the 0.19 % cost. By 48 h it fades to +0.12 % (t 0.85), and the 24 h slope t is 4.18 against -0.20 at 48 h.
- **F3:** Within the 24-hour horizon the effect is graded, but only up to about three usual moves. At 24 h the unusual move is +0.120 % for moves of 0–1 usual moves, +0.299 % for 1–2 and +0.445 % for 2–3; moves of 3–4 give -0.002 % and moves above 4 give -0.53 %. At 12 h, 3–4 gives -0.16 % and above 4 gives -0.60 %. So the largest shocks do not reverse, yet the uncapped linear forecast bets hardest on them.
- **F4:** At 24 h both sides reverse and no single coin carries the result. Long after a down hour gives +0.253 % (t 2.55, 2,588 cases) and short after an up hour gives +0.348 % (t 3.46, 2,593 cases). Five of six coins give +0.21 % to +0.58 % (ZEC t 2.58, XRP t 2.37); ETH is weakest at +0.031 % (t 0.19). By window group, w1–w18 give +0.30 % to +0.54 % (t 2.7–3.1) and w19–w24 give -0.05 % (t -0.39).
- **F5:** The cumulative move does not carry the reversal; the single-hour shock does. A 6-hour summed scaled move of 2–3 usual moves continues instead of reversing: -0.195 % at 6 h (t -3.4) and -0.377 % at 12 h (t -3.5).
- **F6:** High volatility is mostly an effect of its own and is not a repair. With a 24 h hold and one case per grid cell (17,089 cases, +0.112 %, t 2.9), cases in the top-third volatility regime give +0.281 % (t 3.37), but bars there with no signal (|z| ≤ 1) already give +0.154 % (t 2.07). The signal adds about the same in every regime: +0.14 % in low volatility, +0.05 % in mid and +0.13 % in high.
- **F7:** The funding-settlement clock does not strengthen the effect. With a 24 h hold, cases at the pre-settlement hours (23, 07 and 15 UTC) give +0.013 % (t 0.08, 1,344 cases) against +0.121 % (t 3.0) at other hours. At one hour, large pre-settlement moves give -0.058 % against +0.026 % elsewhere.

## Ideas
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day` (from F1, F2, F4): The larger a coin's last 1-hour return relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily` (from F2, F3, F5): Among hourly moves of up to a few times a coin's 24-hour volatility, the larger its last 1-hour return relative to that volatility, the more its return over the next 24 hours runs the opposite way.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
