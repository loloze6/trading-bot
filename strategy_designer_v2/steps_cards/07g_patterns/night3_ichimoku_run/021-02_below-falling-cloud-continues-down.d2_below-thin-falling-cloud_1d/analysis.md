---
line: 7.g patterns
backtest: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud_1d
idea tested: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3843 USD
---
## Findings
- **F1:** Daily moves reverse the next day, in proportion to the size of the move. Moves are measured in units of the coin's daily standard deviation within its window. After a fall larger than 2 of these units, the next day's return averaged +0.348 units (410 days, a rough t near 7). After a fall of 1 to 2 units it averaged +0.107 (1460 days), and after a fall of 0 to 1 unit +0.026 (6174 days). After a rise of 1 to 2 units it averaged -0.020 (1512 days), and after a rise larger than 2 units -0.098 (505 days). A third of a daily move is several times a round trip of 0.19 %, but the window-level scaling uses each window's whole history, so this needs a test on causal volatility.
- **F2:** The book's losses run through every coin and most windows. Its 938 trades lasted 28.6 days on average and lost 4.99 % each after fees (median -3.80 %), and only 34 % won. Every coin lost per trade, from -1.05 % on LTC to -13.46 % on XRP. 13 of 23 windows had a negative mean daily book return.
- **F3:** Below a falling cloud, the coin's past 26-day return orders what follows over the next 26 days, which the cloud's thinness does not explain. Among the 156 cases in the regime, the next 26-day return in excess of drift was:
- **F4:** Across all bars, a high close relative to recent prices goes with a higher next 26 days.
- **F5:** Some angles showed nothing that stands out from chance:

## Ideas
- `021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud.g1_one-day-fall-reverses-next` (from F1): A coin's return over the next day is higher the larger its fall over the past day was, measured against its usual daily move. After a large rise the next day's return is lower, more weakly.
- `021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud.g2_below-cloud-momentum-keeps-falling` (from F3, F4, F2): When a coin closes below a falling Ichimoku cloud, its return over the next 26 days is lower the lower its 26-day return has been.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
