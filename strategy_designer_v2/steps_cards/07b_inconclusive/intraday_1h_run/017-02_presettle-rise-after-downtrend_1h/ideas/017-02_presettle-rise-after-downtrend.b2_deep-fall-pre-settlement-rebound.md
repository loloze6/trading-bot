---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend
line: 7.b inconclusive
backtest: 017-02_presettle-rise-after-downtrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a 3-day run down, the return over the 2 hours before each funding settlement time (00:00, 08:00 and 16:00 UTC) is positive, and the deeper the coin's 3-day percentage fall, the larger that pre-settlement rise.
Consequence: A trader would lean long into settlement only after deep 3-day falls, since shallow falls show no rise.
Why:
- F2: The rise appears only after the deepest raw 3-day falls. Settlement-bar cases in the deepest fall decile (mean fall -13.8%) gain +9.2 bp over 2h (t 2.70, n 5,065), while deciles 2 to 5 are all negative (-1.0 to -2.4 bp). The raw-fall quintiles show the same: the deepest is +9.5 bp (t 2.73), and the next four range from -0.3 to -3.6 bp.
- F3: Measured on the raw size of the fall instead of the plan's z-score against its own past 72 values, the pre-settlement 2h excess return grows with the fall depth at 136 bp per unit of fall (t 7.32, n 25,072). The plan's standardised forecast mostly measures how the fall changed recently, not how deep it is.
- F4: The rebound after falls is not tied to the funding clock. Over all hours the slope on raw fall is 110 bp (t 16.9, overlapping bars). Inside the deepest decile, settlement bars beat other hours only modestly (+9.2 vs +1.3 bp, Welch t 2.16), and non-settlement hours such as 04 (+14.4 bp, t 2.87) and 11 (+21.8 bp, t 3.28) are as strong as the settlement hours 05/13/21 (+6.2, +11.2, +10.2 bp, t 1.26 to 1.72).
