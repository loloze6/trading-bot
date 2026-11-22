---
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h
idea tested: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3674 USD
---
## Findings
- **F1:** The tested effect is not in the data. Thin-volume hours (volume at or below its 30-day mean) that rise are not followed by a fall. Rises of 1–2 typical moves are followed by +4.4 bp unusual return over 4 hours (t 1.39, n 2156). Rises of 2–3 typical moves are followed by −10.9 bp (t −1.30, n 348). Step 5 measured a strength of only 0.003 over 11108 cases, so there is no fade for a short to capture.
- **F2:** Fees cause most of the book's loss. It made 19464 trades, all short, with a median holding of 4 hours. Each trade averaged −0.25 % gross and −0.35 % net, against a cost of 0.11 % per buy and sell. Per day, turnover was 1.73, fees took −0.091 % and the gross gain was only −0.016 %. That explains the −0.105 % mean daily return and the Sharpe of −1.93.
- **F3:** Being short against the coins' rise costs the book further. The market part of its gain is −0.027 % a day, while its timing part is only +0.011 % a day. Holding the coins earned +0.128 % a day, which leaves the book's Sharpe 2.57 below holding's.
- **F4:** Heavy-volume falls are followed by a rebound, not by the continuation the brief expects. After hours falling more than 2 typical moves on volume more than twice the 30-day mean (n 926), the unusual return in the fall's direction was −30 bp over 2 hours (t −4.22) and −65 bp over 24 hours (t −3.47). Heavy-volume rises of the same size show nothing comparable: −1.4 bp over 4 hours (t −0.16) and +24 bp over 24 hours (t 1.48, n 874).
- **F5:** The rebound grows with the size of the fall times the log of its volume ratio, but only in the top quintile. That quintile (n 1014, mean score 6.8) is followed by +27 bp over 6 hours (t 2.61, strength 0.14) and +62 bp over 24 hours (t 3.41). The four lower quintiles lie between −8 and +8 bp over 6 hours, none with |t| above 1.
- **F6:** The rebound is strongest at the extreme and holds in every sub-period of both coins. Falls over 5 typical moves on volume over 4 times the mean are followed by +48 bp over 4 hours (t 1.61) and +130 bp over 24 hours (t 2.41, n 184). After heavy falls, the 24-hour unusual return is positive in all 8 coin × window-group cells, from +11 bp (BTC w1–6) to +152 bp (BTC w13–18). At 24 hours the move is about 5–12 times the 0.11 % cost of a trade.

## Ideas
- `028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back.d1_heavy-volume-selloffs-rebound-daily` (from F4, F5, F6, F2): After an hour in which the coin falls far more than its typical hourly move over the past 30 days on volume several times its 30-day average, the price rises back over the next 24 hours, and the larger that hour's fall in typical moves and the higher its volume against its 30-day average, the larger the rise.
- `028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back.d2_heavy-volume-drops-bounce-intraday` (from F4, F5): After an hour in which the coin falls far more than its typical hourly move over the past 30 days on volume several times its 30-day average, the price rises over the next six hours, and the larger the fall in typical moves times the log of its volume ratio, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
