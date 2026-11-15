---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's own 20-day return, the more that coin rises over the next 10 days.
Consequence: A trader should lean long in proportion to a coin's recent 20-day gain rather than on its 50/200-day average spread, which by itself carried no edge.
Why:
- F5: What does carry the next 10 days is the coin's own recent move. The slope of the 10-day excess return on the coin's 20-day past return has t 2.80 over 1375 non-overlapping cases. Inside the top past-20-day tercile, the up-cross state also earns 0.0326 against -0.0067 off (t 2.34). Inside the bottom tercile it earns -0.0209 against 0.0097 (t -2.39). The moving-average state only matters through the recent move it partly overlaps with.
- F1: The tested effect is close to zero at every horizon. The 10-day slope of forward return (less the coin's mean) on the forecast is 0.000202 with t 0.37 over 1657 non-overlapping cases. At the other horizons the t is 0.20 at 5 days (3349 cases), 0.55 at 20 days (811) and -0.06 at 40 days (388). Using the raw 50/200 spread instead of the forecast gives t between -0.76 and 0.02.
- F4: The effect does not grow with the spread or with how fresh the cross is. By forecast bucket, the 10-day excess is -0.0085, 0.0023, 0.0105 and 0.00004 for (0,5], (5,10], (10,15] and (15,20]. In the first 10 days after the cross it is 0.0038 (58 cases), against -0.037 at 10–30 days (89 cases).
