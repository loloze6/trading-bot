---
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
idea tested: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5333 USD
---
## Findings
- **F1:** In the top third of each coin's 7-day hourly volatility, the 1-day return reverses over the next 1 day. The slope of the next-24h excess return on the standardised 1-day return is -0.0070 per sd (t -11.2, n 5413 non-overlapping cases). It holds in both halves of the windows (t -5.2 in w1-12, t -9.7 in w13-24) and in every coin when split on 1-day volatility (t -2.8 to -5.2). It is still -0.0066 per sd over the next 3 days (t -3.8, n 1751).
- **F2:** In the bottom third of 7-day hourly volatility, the sign flips: moves continue. The 1-day return predicts the next 3 days at +0.0066 per sd (t 2.3, n 1751) and the next 1 day at +0.0021 per sd (t 2.3, n 5414). The 3-day return predicts the next 1 day at +0.0038 per sd (t 4.2, n 5414). In the middle volatility third, the 3-day return predicts the next 3 days at +0.0074 per sd (t 3.1, n 1749). By coin over 3 days, five of six slopes are positive, but only XMR reaches t 2.8, so this is less firm than F1.
- **F3:** The tested rebound after a fresh drop in a 3-day fall is real but front-loaded, which is why the supporting check failed (-0.00125). After a 3-day fall:
- **F4:** The way a fall was built shows the opposite of the brief. Falls whose 1-day path is dominated by one hour (top third of max|hourly|/sum|hourly|) lag over the next 3 days (excess -0.0028 against +0.0018 for grinding falls). The jump share predicts the 24-to-72-hour return negatively among falls (t -2.0). This is weak given how many angles were tried.
- **F5:** Volume concentration weakens the 1-day reversal. The interaction of the standardised 1-day return with the top-hour volume share is +0.019 (t 4.5, n 16814) over the next 1 day, but it vanishes over 3 days (t 0.6).
- **F6:** The book barely earns. Its Sharpe is 0.14 and its mean daily return 0.00011, against holding at about 0.0012. ETH (-0.00021) and LTC (-0.00041) lose, consistent with a 3-day hold that misses a reversal finished within 1 day.

## Ideas
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.g1_high-volatility-one-day-reversal` (from F1, F3): When a coin's hourly volatility over the past 7 days is high, the larger its 1-day return, the more it moves the opposite way over the next 1 day, with most of that move inside those 24 hours.
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.g2_calm-market-three-day-continuation` (from F2): When a coin's hourly volatility over the past 7 days is low, the larger its 3-day return, the further it keeps moving in the same direction over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
