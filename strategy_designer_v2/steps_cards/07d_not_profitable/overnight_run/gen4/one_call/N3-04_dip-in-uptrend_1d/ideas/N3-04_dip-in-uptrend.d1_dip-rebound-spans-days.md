---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-04_dip-in-uptrend
line: 7.d not profitable
backtest: N3-04_dip-in-uptrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day and 60-day returns are both positive, a sharp daily drop is followed by a rise over the next two to three days, larger than the rise on the first day alone.
Consequence: A trader buying the dip should hold the rebound for a few days rather than one bar, which captures more of the move per entry.
Why:
- F6: The rebound lasts beyond the one-bar horizon. On non-overlapping dip signals (n=1362), the coin gains +0.24% on day 1 (t=1.78) and a further +0.63% over days 2–3 (t=3.06). A second consecutive dip day is followed by +0.63% (n=826, t=3.42), against +0.33% (n=1557, t=2.68) after a first dip.
- F7: Fees are not the problem; trade selection is. The 1613 trades are all long, with a median hold of 1 day. Their gross mean is -0.03% per trade (t=-0.16) against about 0.10% in fees. One-day trades gain +1.25% gross (n=1127), but trades held 1.5–3.5 days lose -3.37% (n=342) and those held 3.5–7.5 days lose -3.74% (n=79): these are the dips that kept falling.
