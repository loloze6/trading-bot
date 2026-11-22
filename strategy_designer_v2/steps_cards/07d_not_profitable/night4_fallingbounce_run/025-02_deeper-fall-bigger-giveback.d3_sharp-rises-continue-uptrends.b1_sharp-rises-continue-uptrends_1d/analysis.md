---
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends_1d
idea tested: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3910 USD
---
## Findings
- **F1:** The book fails on its falls, not on its gain. Its deepest fall is -51.0 % against a yearly return of +25.4 %, which gives a Calmar of 0.50 against the required 0.75. The next deepest falls are -44.8 %, -36.2 %, -32.4 % and -29.5 %, and in each one the coins themselves fell 42 %, 46 %, 76 %, 40 % and 39 % (w15–w17, w1–w6, w12–w15, w18–w19, w21–w22).
- **F2:** The book holds no edge of its own that could cushion these falls. The idea's unusual move is -0.16 % per case over 10 days (t -0.27, 930 cases, strength -0.016). Its +1.01 % total move is almost entirely the coins' +1.17 % normal drift, so the book is a part-time long that rides the coins down in their falls. Cost is not the issue: the total move is 5.2 times the 0.19 % cost of a trade.
- **F3:** How far the coin sits below its 60-day high, in usual 20-day moves, separates winning long bars from losing ones.
- **F4:** The coin's 20-day return, in usual moves, grades the outcome the same way, while the 90-day return used as the regime does not.
- **F5:** The book loses in recovering-but-damaged coins, mainly by holding positive 90-day-return coins that are already deep below their recent high.

## Ideas
- `025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends.d1_sharp-rises-near-highs` (from F1, F3, F5): In a coin whose 90-day return is positive, the larger the day's rise measured against the standard deviation of its last 20 daily returns, the larger its rise over the next 10 days, only while the coin closes near its highest close of the past 60 days. The closer it closes to that high, measured in its usual 20-day moves, the larger the rise that follows; the further below it, the more the rise is given back.
- `025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends.d2_distance-from-60-day-high` (from F2, F3, F5): The closer a coin's close is to its highest close of the past 60 days, measured in its usual 20-day moves, the larger its rise over the next 10 days; the further below that high it closes, the larger its fall over the next 10 days.
- `025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends.d3_sharp-rises-in-strong-months` (from F1, F4): In a coin whose 90-day return is positive, the larger the day's rise measured against the standard deviation of its last 20 daily returns, the larger its rise over the next 10 days, the more so the larger its 20-day return measured in its usual 20-day moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
