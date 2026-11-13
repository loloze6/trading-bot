---
brief: 002_moving-average-cross-trend-persistence
source-idea: N7-01_drift-only-near-high
line: 7.e profitable but not proven
backtest: N7-01_drift-only-near-high_1d_oos
instruments: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ
bar: 1d
period: folds A, D
---
Idea: In one coin, when the daily close sits at or very near the top of its last 20 closes and a new 20-day closing high was made within the last few bars, the next day's return is above the coin's average. The edge fades once the high is more than about five bars old or the close has slipped down its range.
Consequence: Take or keep a long only while the close is pinned to a fresh 20-day high, and drop it as soon as the high ages or the close falls back in its range, rather than holding through the whole 20-bar gate.
Why:
- F5: Inside the gate, next-day excess grows with closeness to the 20-day high. In-market coin-days in the top quartile of the raw near-high value have next-day excess +0.0047 (t = 2.41, n = 1132). The bottom quartile has −0.0011 (t = −0.82, n = 1132). These are 1-day returns; same-day coins are correlated, so the t is optimistic.
- F6: Next-day excess also depends on how recent the high is. With the high 0–5 bars old (raw recency 15–20), excess is +0.0027 (t = 2.76, n = 3200). With the high 5–10 bars old (raw 10–15), excess is −0.0024 (t = −1.39, n = 851).
- F7: Being above SMA20 without a recent 20-day high earns nothing. Those coin-days have next-day excess −0.0016 (t = −1.02, n = 1005). By contrast, all coin-days below SMA20 have −0.0014 (t = −2.25, n = 5780), and all coin-days above it have +0.0010 (t = 1.31, n = 5009).
- F2: The gain rests on a few days. The top 10 of 1449 book days sum to 1.32 of the book's total 1.84 in summed daily returns. The remaining 1439 days average only 0.00036. Trades show the same pattern: 2024 trades, median −1.6 %, 41 % winners, and the 10 best of 2024 make 2175 of the 9784 summed trade percent.
