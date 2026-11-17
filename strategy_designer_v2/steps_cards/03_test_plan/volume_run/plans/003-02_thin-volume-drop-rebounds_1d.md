---
idea: 003-02_thin-volume-drop-rebounds
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp one-day fall on volume well below its 30-day average, graded by fall size and thinness -> adapted: "sharp" and "well below" are regime thresholds (fall of 2 usual moves or more, volume ratio 0.5 or less); inside the regime the position grows with both fall size and thinness, added rather than multiplied.
- Comparison: the bar's volume against its own 30-day average daily volume -> kept
- Outcome: the price wins back part of the fall over the next 5 days (up) -> adapted: the position is held only on the fall bar, not for 5 days, so the 5-day hold is dropped and measured in the criterion.
- Verdict transfer: yes: the test measures the 5-day rebound after thin-volume sharp falls, and whether it grows with the forecast, which reads the fall size and the thinness.
Forecast: The regime is active only on a bar whose one-day return is at least 2 usual moves down and whose volume is at most half its 30-bar average. On every other bar the forecast is 0. Inside the regime the forecast is long and is the mean of three parts: - Fall size: the one-day volatility-scaled return (20-bar volatility), standardised, negated and clipped at 0, so a bigger fall gives a bigger value. - Thinness: a constant +10 minus the standardised 30-bar volume ratio, so thinner volume gives a bigger value. - The two thinness pieces (the constant and the negated volume ratio) count as two of the three equal weights, so the forecast is (F + 10 - V) / 3. It is never negative. It typically lands near 7 to 10 and grows with a deeper fall and with thinner volume.
Config: 003-02_thin-volume-drop-rebounds_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: For each bar with forecast above 0, take the 5-bar forward return minus the coin's mean 5-bar return over all windows. Pool coins and windows. Drop any event within 5 bars of the previous counted event in the same window. Test the mean with a one-sample t.
- Supporting check: Across those events, the slope of excess 5-bar return on the forecast is positive.
- Confirm: Mean excess return above 0 with t ≥ 2, and the supporting slope above 0, with at least 20 independent events.
- Reject: Mean excess return below 0 with t ≤ -2, with at least 20 independent events.
- Inconclusive: Any t between -2 and 2, a confirming mean with a slope of 0 or below, or fewer than 20 independent events.
