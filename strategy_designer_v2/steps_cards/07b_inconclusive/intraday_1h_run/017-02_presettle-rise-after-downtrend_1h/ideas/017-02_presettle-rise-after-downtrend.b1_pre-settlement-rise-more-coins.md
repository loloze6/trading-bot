---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend
line: 7.b inconclusive
backtest: 017-02_presettle-rise-after-downtrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a strong 3-day run down, the return over the 2 hours before each funding settlement time (00:00, 08:00 and 16:00 UTC) is positive, and the stronger the 3-day fall, the larger that pre-settlement rise.
Consequence: Before settlement, crowded shorts close to avoid paying funding and basis traders adjust, so spot leans up against a downtrend.
Why:
- F1: The test's result leans the way the idea predicts but is weak: slope t is 1.30 and the mean-excess t is 0.36 over 25,569 cases. My recomputed cases show the same pattern, with forecast quintiles rising only from -0.2 bp (t -0.11) to +2.5 bp (t 0.95).
- F6: The effect is mixed across years and coins. The case slope t is 3.20 in 2018 but -3.25 in 2020. Only ZEC has a slope t above 2 (3.11); the other five coins range from -0.25 to 1.31.
