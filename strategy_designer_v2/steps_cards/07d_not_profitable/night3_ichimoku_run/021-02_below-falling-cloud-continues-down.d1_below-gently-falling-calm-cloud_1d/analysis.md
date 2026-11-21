---
line: 7.d not profitable
backtest: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud_1d
idea tested: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3878 USD
---
## Findings
- **F1:** The book loses because it shorts coins that drift upward, and the effect does not cover that drift. The cases' unusual move is +2.33 % per 26 days in the short's favour, but the coins' normal drift is −4.06 % against it, so the total move is −1.73 % per case. On active days the book's −1.61 bps a day splits into −2.24 bps from the market's own rise and only +0.63 bps from timing (Sharpe −0.38, holding's Sharpe higher by 0.94).
- **F2:** The cost of a trade is not the cause. A round trip costs 0.19 %, and each case moves 9 to 12 times that, so no change of holding or turnover repairs the book; the loss comes from the sign of the total move.
- **F3:** The losses come from a few violent rebounds. The worst 5 % of active days sum to −8.40, while the other 95 % earn +7.14. The quarter of cases whose coin rose most inside the 26 days (mean peak +46 %) lose 35.6 % each, against +20.3 % for the quarter that barely rose.
- **F4:** Those rebounds follow a recent rise while the coin is still below the falling cloud. Cases whose coin was up over its past 26 days (mean +3.2 %) lose 15.4 % on the short, against +8.7 % and +4.4 % for coins down 16 % and 8 %. Trades entered in the top quarter of the 26-day return lose 9.2 % on average. Active days in the top fifth of the 10-day return (mean +19.9 %) lose 6.3 bps a day (t −2.06, 1495 days), and 54 % of the worst days follow a 10-day rise, against 46 % of all active days.
- **F5:** The losses gather in bull years and in the strongest-drifting coins. The cases of 2020 and 2021 lose 37.4 % and 39.0 % per case (7 and 12 cases), while 2018 gains 16.0 % (34 cases). XRP and ZEC trades lose 15.0 % and 7.3 % on average (drift +6.3 % and +7.4 % per 26 days).
- **F6:** The idea's grading does hold. The quarter of cases with the most negative forecast (mean −5.0) gains 3.1 % total and 7.4 % unusual on the short, while the least negative quarter (−1.9) loses 8.0 % total and 3.7 % unusual. That is not enough to overcome the drift on most cases (F1).
- **F7:** By trades, the calmest coins do worst, against the idea's calm term. Trades entered in the lowest quarter of 30-day volatility (2.2 % a day) lose 10.5 % on average, against +0.3 % and +3.9 % in the two middle quarters.

## Ideas
- `021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.d1_below-cloud-short-still-falling` (from F1, F3, F4, F6): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the slower the cloud has fallen over the past 26 days and the calmer the coin's daily moves have been over the past 30 days, only while the coin's own 26-day return is negative, and more negative the larger that past 26-day fall.
- `021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.d2_rebound-under-falling-cloud` (from F3, F4, F5): When a coin below a falling Ichimoku cloud has risen over its past 10 days, it keeps rising over the next 26 days, and the larger its 10-day rise, the larger the rise that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
