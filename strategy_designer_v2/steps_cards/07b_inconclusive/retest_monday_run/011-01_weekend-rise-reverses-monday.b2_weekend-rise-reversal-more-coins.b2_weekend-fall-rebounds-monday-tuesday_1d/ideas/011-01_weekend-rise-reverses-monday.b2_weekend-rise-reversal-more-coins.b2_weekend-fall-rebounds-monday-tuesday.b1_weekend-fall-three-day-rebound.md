---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), and the larger the weekend fall, the larger the rise.
Consequence: Large weekend falls are a reason to buy at Sunday's close and hold through Wednesday, sized by how far the coin fell, rather than exiting on Tuesday.
Why:
- F1: The main t is negative even though the pooled mean is positive, because coins fall and rebound together on the same Sundays: across 2,235 Sunday-fall cases the pooled excess 2-day return is +0.36 % (t 2.21), but the mean of per-Sunday cross-coin means is −0.33 % (t −0.87, 292 Sundays), and the case-level correlation between fall size and the 2-day excess return is only 0.018.
- F3: Over 3 days the rebound grows with the size of the weekend fall: the per-Sunday mean 3-day excess return by fall quintile is −0.11 %, +0.16 %, +0.75 %, +1.67 % (t 2.12, 146 Sundays) and +1.25 % (t 1.47, 122 Sundays). The same quintiles over 2 days follow no order (pooled −0.48 %, +0.37 %, −0.02 %, +1.66 %, +0.23 %).
- F4: The rebound arrives on the third day rather than on Monday: Wednesday's own excess return after a Sunday fall averages +0.53 % per Sunday (t 1.92, 288 Sundays), while Monday's averages −0.24 % (t −0.81, 294 Sundays) and the 2-day return −0.33 %.
