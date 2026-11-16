---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day rise relative to its usual daily move over the past 20 days, the larger its further rise over the next five days.
Consequence: A trader would add to a long after a sharp up day instead of fading it, sized by how large the day was against the usual move.
Why:
- F2: The second half of the tested idea is wrong in this data: in the top decile of one-day rises (mean move 1.91 usual daily moves), the next day's return is +0.18% rather than a fall, so the short loses -0.00185 gross and -0.00295 net per bar; the next-day slope on the size of rises is positive (0.0012, t 1.55, n 8,087), the opposite of reversal.
- F5: Large one-day rises continue rather than reverse over several days: the slope of the excess return on rise size is 0.0047 (t 2.11, n 2,687) over 3 days and 0.0149 (t 3.65, n 1,490 non-overlapping) over 5 days, and it is positive both above (t 2.06) and below (t 2.80) the 50-day average.
