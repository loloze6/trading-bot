---
brief: 002_moving-average-cross-trend-persistence
source-idea: N7-01_drift-only-near-high
line: 7.d not profitable
backtest: N7-01_drift-only-near-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A close that slips back from a fresh 20-day high to just under the top of its range, or below its middle, is followed by below-average 5-bar returns. The rise continues only while the close stays at the high itself.
Consequence: Hold the long only while the close sits at its 20-day high, and step out as soon as it slips back into the range.
Why:
- F4: Where the close sits in its 20-day range adds held exposure with no gain outside the very top. Blocks with the close in the lower half of the range earn −117 bp (n=41, t=−0.78). Blocks with the close at 0.9–0.99 of the range earn only +18 bp (n=175, t=0.19), yet 13.7% of them lose more than 10%.
- F3: The gain is concentrated right after a fresh high and fades as the high ages, while the crash risk does not fade.
