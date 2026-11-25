---
line: 7.d confirmed, not profitable
backtest: 040-01_agitated-fall-size-next-day-rebound_1d
idea tested: 040-01_agitated-fall-size-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4103 USD
---
## Findings
- **F1:** The check failed only on Calmar (0.7469 against the 0.75 rule), and the book's deepest fall, -20.8 % over 27 days, lies entirely in w16, where the book's daily returns summed -0.32 on XRP, -0.30 on ETH, -0.30 on LTC, -0.23 on XMR, -0.19 on ZEC and only -0.02 on BTC.
- **F2:** During that deepest fall the book lost on positions taken outside a falling market. On its 32 held bars in a rising 60-day trend the next day's excess return was -4.6 % (t -2.28, summed gain -0.53), and on its 11 held bars in a choppy trend it was -10.9 % (t -2.08, summed gain -0.27). Its 6 held bars in a falling trend earned +17.7 % (t 6.44, summed gain +0.62).
- **F3:** Across folds B and C the effect lives in the falling agitated market. There, the slope of the next-day excess return on the forecast is +0.00169 (t 3.94, 377 signal bars) and the mean excess return per signal is +1.40 % (t 4.72). In a rising agitated market the slope is +0.00002 (t 0.04, 358 bars) and the mean is +0.01 %. In a choppy agitated market the mean is -2.19 % (t -1.67, 61 bars).
- **F4:** In the falling agitated market the effect is graded by the size of the fall. The forecast's terciles give next-day excess returns of +0.29 % (t 0.58, 122 cases), +1.07 % (t 2.44, 121) and +2.71 % (t 4.90, 134). The book's summed gain in the top tercile is +2.25 of the profile's +2.62.
- **F5:** The falling trend is not an effect of its own, so it repairs this idea rather than replacing it. Agitated falling bars without the signal (up days) are followed by -1.05 % excess (t -3.94, 361 bars), against +1.40 % after down days. Calm falling markets show no rebound after down days (-0.44 %, t -2.48, 622 bars). This matches the brief's forced-selling reason, which ties the overshoot to agitation and to down days.
- **F6:** Keeping only the falling-trend positions roughly halves the fall. A before-cost replay of the book's own positions gives a deepest fall of -7.7 % against -20.3 %, Calmar 1.46 against 1.16 and Sharpe 1.24 against 1.21, at a yearly return of +11.2 % against +23.6 %. In that profile a signal's next-day move is +1.55 % on average, about 8 times the 0.19 % cost of a trade, against +0.46 % (2.4 times) for the whole book.
- **F7:** A longer holding does not help. In the falling trend the 2-day excess return per signal falls to +0.38 % (t 0.72, 157 non-overlapping cases), so the effect is a one-day rebound.

## Ideas
- `040-01.d1_falling-agitated-fall-rebound` (from F1, F2, F3, F4, F5, F6, F7): In a falling, agitated market, the larger a coin's one-day fall, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
