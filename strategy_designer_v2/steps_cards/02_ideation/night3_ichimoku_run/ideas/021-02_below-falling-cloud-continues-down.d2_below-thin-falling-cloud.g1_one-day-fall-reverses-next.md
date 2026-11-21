---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud
line: 7.g patterns
backtest: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return over the next day is higher the larger its fall over the past day was, measured against its usual daily move. After a large rise the next day's return is lower, more weakly.
Consequence: A trader would lean against a coin's sharp one-day falls, more the sharper the fall, and refuse to chase them with a short.
Why:
- F1: Daily moves reverse the next day, in proportion to the size of the move. Moves are measured in units of the coin's daily standard deviation within its window. After a fall larger than 2 of these units, the next day's return averaged +0.348 units (410 days, a rough t near 7). After a fall of 1 to 2 units it averaged +0.107 (1460 days), and after a fall of 0 to 1 unit +0.026 (6174 days). After a rise of 1 to 2 units it averaged -0.020 (1512 days), and after a rise larger than 2 units -0.098 (505 days). A third of a daily move is several times a round trip of 0.19 %, but the window-level scaling uses each window's whole history, so this needs a test on causal volatility.
