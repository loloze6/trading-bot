---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the 50-day average is above the 200-day average, the coin's forward drift is concentrated in the late part of the run: returns over bars 30 to 120 after the up-cross are higher than returns over bars 10 to 30.
Consequence: A trader should weight a long position by how long the 50-day average has stayed above the 200-day average, not by how wide the spread is, and should expect the first weeks after the cross to carry little or negative drift.
Why:
- F4: The trade-length split decides the book. The 632 trades lasting at most 40 days lose −8.6% to −12.0% each before fees, summing to −6461% net. The 456 trades held over 40 days gain +16.1% each, summing to +7297% net.
- F6: Within a long position, bars 10–30 of the run lose: coin mean −0.00075 and book −0.00102 over 2088 bars, a book sum of −2.13. Bars 30–60 earn coin 0.002326 (t 2.49) and bars 60–120 earn coin 0.002046 (t 2.66), book sums +5.42 and +9.15.
- F5: Trades opened at a high forecast lose and those opened at a low one win. The 774 trades entered with forecast 10–20 average −1.42% gross with a 30.6% win rate. The 150 trades entered at forecast 2–5 average +9.15% gross and are held longer (56.7 against 38.6 days).
- F1: The forecast's size does not grade the coin's next-day return: the coin's mean next return rises only from 0.000942 (forecast 0–5, t 0.90) to 0.001549 (forecast 15–20, t 1.37), and across quintiles of the raw 50/200 spread it is highest in the lowest quintile (0.002726) and only 0.001443 in the highest. This matches the verdict's slope t of 0.37 and its share-positive gap of −0.021.
