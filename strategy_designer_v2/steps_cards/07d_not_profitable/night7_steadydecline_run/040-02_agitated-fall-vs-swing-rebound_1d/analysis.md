---
line: 7.d confirmed, not profitable
backtest: 040-02_agitated-fall-vs-swing-rebound_1d
idea tested: 040-02_agitated-fall-vs-swing-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4228 USD
---
## Findings
- **F1:** The check failed on Calmar alone (0.686 against 0.75), and the falls behind it come from the weak, frequent part of the signal. In folds B and C the book's deepest fall is -19.5 %, in w16, and w13 (-14.6 %) and w17 (-13.6 %) come next. Over those three falls the held bars lost in every bucket of the day's scaled fall. Bars with z between -1 and -0.5 lost the most (sum -0.675, mean next day -9.8 %, 21 bars).
- **F2:** The gain sits in the strongest case of the signal. Held bars with the day's fall at or below -2.5 of the 30-day swing returned +6.4 % the next day (t 3.4, 27 bars). Bars from -2.5 to -1.5 returned +1.3 % (t 2.4, 109 bars). Bars from -1.5 to 0 returned only +0.3 % to +0.7 % (1062 bars). The top forecast quartile holds 3.55 of the 4.72 summed gain.
- **F3:** Holding only on falls of -1.5 swings or more cuts the deepest fall from -19.5 % to -5.9 %. Calmar rises from 0.83 to 1.31 and Sharpe from 0.97 to 1.01, with a yearly return of 7.7 % against 16.2 %. This is an approximate rebuild at 0.095 % per side.
- **F4:** On agitated bars, a fall of at least 1 swing after a 7-day return below -10 % is followed by +2.29 % excess the next day (t 3.42, 132 cases). The same fall without a prior 7-day decline gives +0.10 % (t 0.21, 161 cases).
- **F5:** The 7-day decline is not an effect of its own, because without the signal it loses. Up days after the same 7-day decline give -1.18 % excess the next day (t -2.24, 186 cases), and small down days give +0.15 % (t 0.26, 222 cases). This fits the brief's theory: forced selling (liquidations, stops, volatility cuts) builds over several down days before it exhausts.
- **F6:** The rebound after a large fall following a 7-day decline lasts two days: +2.48 % excess over 2 days (t 3.24, 132 cases). That is about 13 times the 0.19 % cost of a trade.
- **F7:** Keeping the book only while the coin's 7-day return is below -10 % brings the deepest fall to -10.0 % and Calmar to 1.39, with Sharpe 1.12 and a yearly return of 13.9 %. This is an approximate rebuild.
- **F8:** The effect lives in falling agitated markets.

## Ideas
- `040-02.d1_agitated-fall-after-weekly-decline` (from F1, F4, F5, F7): In an agitated market, the larger a coin's one-day fall against the standard deviation of its daily returns over the past 30 days, the larger its rise over the next day, only while the coin's 7-day return is a fall.
- `040-02.d2_two-day-rebound-after-selling` (from F4, F6): In an agitated market, the larger a coin's one-day fall against the standard deviation of its daily returns over the past 30 days, the larger its rise over the next two days, when the fall ends a 7-day decline.
- `040-02.d3_largest-scaled-falls-rebound` (from F1, F2, F3): In an agitated market, the larger a coin's one-day fall against the standard deviation of its daily returns over the past 30 days, the larger its rise over the next day, among falls of more than one and a half times that swing.
- `040-02.d4_falling-agitated-fall-rebound` (from F5, F8): In a falling, agitated market, the larger a coin's one-day fall against the standard deviation of its daily returns over the past 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
