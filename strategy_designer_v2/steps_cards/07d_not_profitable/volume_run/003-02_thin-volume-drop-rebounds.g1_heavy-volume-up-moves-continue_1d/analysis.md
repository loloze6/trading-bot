---
line: 7.d not profitable
backtest: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d
idea tested: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3268 USD
---
## Findings
- **F1:** The book holds its full position only on the day after the rise, when the coin earns nothing extra; the continuation comes on the following days, when the book has mostly left. After bars with forecast ≥ 10 (n≈1,600), the coin's excess over its mean is 0.00077 on day 1 (t 0.56) at a mean position of 1.02. It is 0.0053 on day 2 (t 4.0), 0.0045 on day 4 (t 3.3) and 0.0036 on day 6 (t 2.7), while the mean position is only 0.15–0.23.
- **F2:** Because the forecast follows each bar, the book trades in and out around one-day holds, and fees eat the gain. There are 2,988 trades with a median length of 1 day and a mean of 3.3 days. Fees cost 0.00016–0.00023 of the book per bar, against a timing gain of −0.00034 to +0.00051 per coin. The book's mean daily return is 4.9e-05 and its Sharpe is 0.10, while holding gives Sharpe 0.26–0.65 per coin.
- **F3:** The continuation lives in coins already rising over the past 20 days and fails in falling ones. Active bars in the lowest quarter of 20-day return have a 5-day excess of −0.0115 and a held gain of −0.0021 per bar (318 bars), against +0.0215 in the top quarter (850 bars). On the 5-bar grid, cases with a positive 20-day return have an excess of 0.0238 (t 2.79, 277 cases), against 0.0087 (t 1.22, 234 cases) for a negative one.
- **F4:** The book's gain is spread thin and fragile across periods. Its mean gain is negative in 11 of 24 windows. The chained daily book has a deepest fall of −43.6%, which gives a Calmar of 0.0057. With one window left out, the lowest Sharpe is −0.09.
- **F5:** What edge there is sits in the strongest readings, and it grows with the horizon. The forecast bucket 10–20 carries 91% of the summed position gain. Its excess over the coin's mean rises from 0.0008 at 1 day to 0.0130 at 5 days and 0.0230 at 10 days.

## Ideas
- `003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue.d1_delayed-heavy-volume-continuation` (from F1, F2, F5): When a coin rises sharply over one day relative to its own 20-day volatility, it keeps rising over the next 5 days, and the larger the volatility-scaled rise and the heavier its volume against the coin's 30-day average, the larger the further gain, with that further gain coming from the second to the sixth day after the rise rather than the first day.
- `003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue.d2_continuation-inside-uptrends-only` (from F3, F4): When a coin rises sharply over one day relative to its own 20-day volatility, it keeps rising over the next 5 days, and the larger the volatility-scaled rise and the heavier its volume against the coin's 30-day average, the larger the further gain, only while the coin's 20-day return is positive, the gain growing with that 20-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
