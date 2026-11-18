---
plan: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound_1d
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x next-day excess return on forecast > 0 bars: 0.00473387; ordinary t: 2.45182 (threshold: ordinary t >= 2.0 confirms (with top-minus-bottom > 0); t <= -2.0 rejects)
- Supporting check: top-half minus bottom-half mean excess next-day return (median forecast split): 0.00337586, passed: True
- Counts: bars with forecast > 0: 1192, top half bars: 596, bottom half bars: 596
- Decided by: The main measure's t is >= 2.0 and the top-minus-bottom difference is above 0.
- Reading: Situation = regime 'mean_reversion' (the detector's recorded decision, since its 20-day/100-day volatility ratio is not recorded and windows are too short to rebuild it) and a negative 1-day return, side long; supporting split puts forecasts >= the median in the top half and < the median in the bottom half, with unweighted mean excess returns; the minimum of 30 counts forecast > 0 bars with a next-day return in the same window.
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound_1d`
Measure: `measure.py`
