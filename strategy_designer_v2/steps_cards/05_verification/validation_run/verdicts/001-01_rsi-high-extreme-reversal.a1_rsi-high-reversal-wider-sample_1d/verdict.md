---
plan: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample_1d
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean 5-bar excess return of extreme high-RSI cases: 0.0143993; ordinary t of the mean: 2.5761 (threshold: mean < 0 with t <= -2 on at least 30 cases (confirm); mean > 0 with t >= +2 on at least 30 cases (reject))
- Supporting check: coins with negative mean excess return (need >= 4 of 6): 1, passed: False
- Counts: cases: 595, coins with negative mean excess: 1, cases BTCUSD: 107, cases ETHUSD: 106, cases LTCUSD: 97, cases XMRUSD: 109, cases XRPUSD: 77, cases ZECUSD: 99
- Decided by: Pooled mean excess return is above 0 with t >= +2 on at least 30 cases: price rises more than usual after extreme high RSI.
- Reading: Situation RSI>50 with a short forecast, RSI read as 'fifty_minus_rsi' from the component column's scale (recomputed as 14-bar Wilder RSI inside each window if it looks standardised); cases are grid bars 0,5,10,... of each window with forecast <= -5 and a 5-bar forward return inside the window; the coin mean is the mean 5-bar return on the same grid over all its windows; a coin with no case does not count as negative in the 4-of-6 check; fewer than 30 cases is reported as not observable.
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample_1d`
Measure: `measure.py`
