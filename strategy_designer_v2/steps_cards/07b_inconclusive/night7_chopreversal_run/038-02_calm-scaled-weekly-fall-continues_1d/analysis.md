---
line: 7.b inconclusive
backtest: 038-02_calm-scaled-weekly-fall-continues_1d
idea tested: 038-02_calm-scaled-weekly-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3266 USD
---
## Findings
- **F1:** The tested result is on the side the idea predicts but short of the bar. Step 5 measured an unusual 5-day move of +0.55 % in the short direction, t 1.53, over 1093 cases on 616 days. On folds B and C the calm-fall grid cases give +1.32 % at t 1.59 (375 cases, 135 days). Five of six coins are positive (XRP +2.04 % t 1.97, XMR +1.99 % t 1.83, LTC +1.66 % t 1.46, ETH +1.59 % t 1.16, BTC +0.72 % t 0.84), and only ZEC is about 0 (-0.21 %, t -0.14).
- **F2:** The effect is graded with the fall's size, as the idea says. Over 5 days the calm-fall terciles of the scaled 7-day fall give -0.66 % (t -0.68), +1.23 % (t 1.18) and +3.40 % (t 2.11, 125 cases, 55 days). The slope of the short-direction unusual move on the absolute scaled fall is +0.028 per unit (correlation 0.18, 375 cases).
- **F3:** The continuation lives in calm markets only. Agitated falls give -0.68 % over 5 days (t -0.49, 318 cases) against +1.32 % in calm markets. The same holds over 2 days (calm +0.60 % t 1.72, agitated +0.01 % t 0.02) and over 10 days (calm +2.10 % t 1.24, agitated -1.28 % t -0.52).
- **F4:** The effect varies over time, which is why a single test on six coins stays under t 2. Calm falls give +3.56 % (t 1.98) in 2018 and +2.30 % (t 1.99) in 2019, but -2.60 % (t -1.88) in 2020 and -0.54 % (t -0.25) in 2021. Windows range from +5.04 % (w14) to -4.45 % (w17, t -2.20).
- **F5:** The effect is not clearly confined to one trend.
- **F6:** More data is available than the test used. The test ran the six default coins only, while folds A and D also hold ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL and INJ, and fold D also holds NEAR, SUI, TAO and ONDO. That would add independent calm-fall cases to a result that falls short through too few cases relative to its variance (F1, F4).

## Ideas
- `038-02.b1_calm-scaled-fall-more-coins` (from F1, F2, F3, F4, F6): In a calm market, the larger a coin's 7-day fall measured against its 30-day daily swing, the larger its further fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
