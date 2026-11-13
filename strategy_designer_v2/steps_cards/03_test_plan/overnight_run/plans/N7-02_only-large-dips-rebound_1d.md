---
idea: N7-02_only-large-dips-rebound
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: an uptrending coin has a one-day drop of about one standard deviation or more against its last 60 daily moves -> adapted: the uptrend (SMA50 above SMA200) is a regime, and the one-day drop, scaled by the mean size of the 60 previous daily moves, sets a graded position instead of a one-std threshold.
- Comparison: milder down days, which are followed only by the coin's ordinary drift -> adapted: milder drops are damped to almost zero by a graded dead zone, and are judged against holding the coin.
- Outcome: the price rises over the next three days -> adapted: the three-day hold is dropped, the position lasts while the drop is the latest bar, and the 3-bar forward return is measured from the record.
- Verdict transfer: yes: a large-drop long in an uptrend that beats holding over the next 3 bars is exactly the idea, and one that loses to holding contradicts it.
Forecast: The regime is "trending" when SMA50 is above SMA200; on every other bar the forecast is flat. In the trending regime the forecast starts from the latest one-day percent move. It is divided by the mean absolute size of the 60 previous daily moves (standardise, target 10, cap 20), so an ordinary move is about 10 and a one-std drop is about 12.5. The value is then negated and clipped at 0, so only down days give a long position. Last, it goes through signed_power with exponent 3 and pivot 20, the strongest graded dead zone the guide allows: - a mild drop of 0.5 std (about 6) gives about 0.5, below the rebalance minimum; - a one-std drop gives about 5, an allocation of 0.5; - a drop of 1.6 std or more (at the cap of 20) gives 20. The forecast is never negative. It grows with the size of the drop and returns to near zero on the next bar unless another large drop occurs.
Config: N7-02_only-large-dips-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Take the bars where the forecast is 5 or more (a drop of about one std or more in an uptrend). On each, measure the coin's forward 3-bar return minus that coin's mean 3-bar return over all 24 windows together. Pool the results across coins, counting events within 3 bars of each other as one case.
- Supporting check: The same excess return on mild uptrend down days (forecast above 0 but below 2) should be close to zero. Its 95% interval should include 0.
- Confirm: The mean excess 3-bar return after forecast-5-or-more bars is positive with t ≥ 2 over the de-overlapped cases.
- Reject: The mean excess 3-bar return after those bars is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a pool of fewer than 30 de-overlapped cases across all coins and windows.
