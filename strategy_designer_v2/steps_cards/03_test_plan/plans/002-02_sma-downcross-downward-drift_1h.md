---
idea: 002-02_sma-downcross-downward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA has crossed below long SMA -> adapted: "after the cross" becomes "while the short SMA is below the long SMA", graded by the size of the gap.
- Comparison: falls more often and further than after random points -> adapted: measured against the coin's unconditional forward return over the same windows, which is buy-and-hold.
- Outcome: price keeps falling over the following bars -> kept: the forward return after short bars is measured over a fixed horizon.
- Verdict transfer: yes. The bars after each down-cross are exactly the bars this forecast holds short, so a falling or not-falling result there carries over to the idea.
Forecast: The forecast uses the gap between the 50-bar and the 200-bar simple moving averages of the close, in percent of the 200-bar average (EMASpreadComponent with average "sma"). Brief settings are absent, so 50/200 is the common convention for this cross. The gap is standardised against its own past 200 values. It is then clipped at a maximum of 0, so the test covers only the downward-cross side. The forecast is zero while the 50-bar average is above the 200-bar average. It turns negative once the 50-bar average is below, starting at zero at the cross, and the short grows with the gap, up to -20.
Config: 002-02_sma-downcross-downward-drift_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The coin's forward 24-bar return after bars with forecast < 0, minus its unconditional forward 24-bar return over the same window. Sample one bar every 24 so that overlapping returns count once, pool the 6 windows, and compute a t-statistic.
- Supporting check: Among the short bars, the rank correlation between |forecast| and the forward 24-bar return should be negative, meaning a larger gap is followed by a deeper fall.
- Confirm: The excess forward return on short bars is negative with t ≤ -2. Short bars are followed by a fall more often than unconditional bars. At least 4 of the 6 windows show the same sign.
- Reject: The excess return has t > -1, which means no extra fall. A positive excess with t ≥ +2 counts as the reversal case that the brief names.
- Inconclusive: A t-statistic between -2 and -1, or a sign that agrees in fewer than 4 windows. At least 150 non-overlapping short samples and 20 distinct down-crosses across the windows are required; with fewer, the test is inconclusive.
