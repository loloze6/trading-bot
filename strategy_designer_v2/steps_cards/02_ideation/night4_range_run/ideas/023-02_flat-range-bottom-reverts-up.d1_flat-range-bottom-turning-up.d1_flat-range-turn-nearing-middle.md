---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the larger its rise over the past 10 days and the closer that rise has carried its close back to the middle, the more it rises over the next 5 days.
Consequence: In a flat market, favour dips that have already climbed most of the way back to the middle on a strong 10-day rise, and give little weight to small turns or turns still deep in the range.
Why:
- F3: The tested forecast does not grade the next 5 days. On 168 independent grid cases its unusual move is 0.81 % (t 1.02), strength 0.083, and the slope's t is 1.20. Its quartiles are U-shaped rather than rising: drift-removed 5-day returns are +2.78 %, −0.66 %, −0.94 % and +2.07 % from weakest to strongest.
- F6: In flat coins below the middle, only the strongest turns carry the effect. By 10-day-return quintile the drift-removed 5-day returns are +0.25 %, −2.53 %, −0.40 %, −0.00 % and +1.95 % (strength 0.20 for the top quintile, mean 10-day rise +7.8 %), giving a slope t of 2.41 on 467 cases.
- F9: Within flat coins below the middle, closes nearest the middle do best. By range-position quartile the drift-removed 5-day returns are +0.18 %, −1.43 %, −0.25 % and +0.94 % from deepest to nearest the middle (strength 0.10 for the nearest).
