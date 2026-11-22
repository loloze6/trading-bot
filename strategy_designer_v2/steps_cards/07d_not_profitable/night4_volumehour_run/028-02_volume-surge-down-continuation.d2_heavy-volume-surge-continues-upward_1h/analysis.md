---
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward_1h
idea tested: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3702 USD
---
## Findings
- **F1:** The tested effect is too small to pay for a trade: per case the total 6-hour move is +0.01 % and the unusual move is −0.03 % (strength −0.015, t −1.38, 11507 cases), against a cost of 0.11 % per trade. As a result the book fails every gain and fall measure: Sharpe −0.26, mean daily return −0.037 %, Calmar −0.25, and the lowest Sharpe with one window left out is −0.39.
- **F2:** The fees eat everything the book gains before costs. The forecast is positive on 49 % of all hours, and the book trades 3.6 times a day. Per bar, the gain before costs is 0.24 bp on BTC against 0.53 bp of fees, and 0.46 bp on ETH against 0.45 bp. So the signal fires on ordinary up-hours, not on rare surges.
- **F3:** The book is mostly a half-sized holding of the coin, and its timing loses. Its daily returns track the coins with correlation 0.73 and beta 0.51. It is long on 74–75 % of bars, still holds 0.36–0.45 of the book when the forecast is 0, and earns −3.7 bp a day while the coins earn +12.7 bp. About +6.4 bp a day comes from the market's rise, so timing costs about −10 bp a day.
- **F4:** Strong up-hours do not continue as a group. Hours of 2.5–4 hourly standard deviations up are followed by +0.2 bp unusual move over 6 hours (n 222). Strong up-hours on more than 3 times the usual volume give +20 bp (t 0.88, n 167), while those on 1–2 times the usual volume give −55 bp (t −1.41, n 53).
- **F5:** Whether a strong up-hour continues depends on the 24 hours before it. When the prior 24-hour return was at or below zero, the 6-hour unusual move after the up-hour is +23 bp (t 0.68, n 146) and the 1-hour move is +22 bp (t 1.71). When the prior 24 hours had already risen more than 2 day-scaled standard deviations, the up-hour is followed by −43 bp over 6 hours (t −1.72) and −84 bp over 24 hours (t −1.73, n 109).
- **F6:** Heavy-volume falls are followed by rises, not continuation. Hours with a volume-weighted scaled return of −10 to −3 are followed by +19.7 bp over 2 hours (t 2.71, n 607) and +36.5 bp over 24 hours (t 1.67). Strong down-hours (below −2 standard deviations) that come after a prior 24-hour fall of more than 2 day-scaled standard deviations are followed by +111 bp over 2 hours (t 2.65), +100 bp over 6 hours and +252 bp over 24 hours (t 2.66, n 95). That 6-hour move is about nine times the cost of a trade.

## Ideas
- `028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.d1_volume-surge-after-falling-day` (from F4, F5, F1): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next six hours, only while the coin's 24-hour return before that hour was flat or falling, and the larger that hour's rise relative to its typical 30-day hourly move and the deeper the prior 24-hour fall, the larger the further rise.
- `028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.d2_heavy-volume-selloff-rebounds` (from F6, F2, F1): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rises over the next two hours to one day, and the larger that hour's fall in typical hourly moves and the deeper the coin's 24-hour fall before it, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
