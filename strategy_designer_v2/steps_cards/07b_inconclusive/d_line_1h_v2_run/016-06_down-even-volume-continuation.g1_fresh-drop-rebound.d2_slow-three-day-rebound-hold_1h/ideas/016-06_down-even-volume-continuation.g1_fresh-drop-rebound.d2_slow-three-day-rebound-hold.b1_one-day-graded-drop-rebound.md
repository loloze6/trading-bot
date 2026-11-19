---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.b inconclusive
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 1 day, with the rise showing between about 6 and 24 hours after the drop rather than in the first hours.
Consequence: Take the rebound when a deep 1-day drop comes inside a 3-day fall and hold it for about one day, not three, because the extra two days give part of the gain back.
Why:
- F1: The tested slope is on the idea's side (72-bar excess return on the forecast: t = 3.93 over 1,891 grid cases). The result is inconclusive only because the later leg fails: the forecast-weighted excess return from bar t+24 to t+72 is -0.00125, and its slope t is only 1.64.
- F2: The graded rebound is carried by the first day after the drop. On the 72-bar grid, the next-24-bar excess return has slope t = 4.11 (n = 1,928) and a forecast-weighted mean of +0.0041. On a non-overlapping 24-bar grid it holds with t = 3.91 over 5,640 cases and a forecast-weighted mean of +0.0021.
- F3: Inside that first day the rebound is not immediate. It builds from hours 6 to 24: on the 24-bar grid the next-6-bar slope t is 0.37 (fw mean +0.00007), the next-12-bar t is 2.37 (fw mean +0.0015) and the next-24-bar t is 3.91.
- F4: Days two and three add nothing, even in the strongest cases. In the top half of forecasts the 24-to-72-bar excess return is -0.0014, against +0.0059 over the first 24 bars. Across all situation cases the 24-to-72-bar mean excess is -0.0028, so a 3-day fall keeps drifting down after the first day.
- F5: The first-day rebound is broad across coins. The 24-bar slope t is 2.18 for ETH, 2.16 for XRP, 2.21 for ZEC, 1.98 for XMR and 1.59 for LTC; BTC is the exception at -0.53. By period it is 3.38 in w1-8, 0.87 in w9-16 and 3.33 in w17-24.
- F6: The grading is clear at 72 bars. The lowest forecast quartile (mean forecast 2.7) has a 72-bar excess return of -0.0093, while the top half (mean forecast 17.8) has +0.0043.
