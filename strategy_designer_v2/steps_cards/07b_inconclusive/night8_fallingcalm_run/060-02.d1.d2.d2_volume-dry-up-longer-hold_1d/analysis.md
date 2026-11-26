---
line: 7.b inconclusive
backtest: 060-02.d1.d2.d2_volume-dry-up-longer-hold_1d
idea tested: 060-02.d1.d2.d2_volume-dry-up-longer-hold
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2275 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but well short of the bar: the main measure is +0.0238 with a day-pooled t of 0.61 from 150 grid cases on only 54 days. The idea's size, measured on more cases, is +3.28 % unusual move per 20 days (strength 0.164, t 2.02 over 200 days, 292 cases), so the evidence is too thin rather than absent.
- **F2:** The cases bunch on few days. In folds B and C, 89 active 20-day grid cases fall on only 29 days, because the six coins enter falling markets together. Each pooled day carries about three coins, and day-clustering turns 89 cases into roughly 29 pieces of evidence.
- **F3:** The effect is graded in the predicted direction. The coin's 20-day unusual return rises from -4.9 % (second-lowest volume-growth quintile) to +3.6 % (fourth) and +12.6 % (highest, log ratio +0.82). The Spearman correlation of volume growth with the unusual return is +0.23 (forecast with it: +0.25). The strongest third of forecasts earns +13.6 % per case against -1.5 % and -4.8 % for the two weaker thirds.
- **F4:** The effect is mostly on the growth side. Long cases (volume grew) gain +6.7 % unusual return over 20 days (41 cases), while short cases (volume dried up) lose -1.1 % (48 cases). The most dried-up quintile still ended +5.8 % above the coin's normal drift, so the dry-up continuation is weak where the growth rebound is strong.
- **F5:** The effect is uneven across periods and coins. By year, the cases earn +3.9 % (2018), +2.8 % (2019), +11.1 % (2020) and -7.9 % (2021). By coin, BTC (-5.2 %) and ETH (-4.4 %) are negative, while LTC, XMR, XRP and ZEC are positive (+3.3 % to +7.8 %). With 12 to 34 cases per group, these groups are small enough to be noise.
- **F6:** The plan's 20-day horizon is not where the measure is clearest. On the same grid in folds B and C, the main measure's t is 1.09 at 5 days, 1.61 at 10 days, 1.27 at 20 days and 0.16 at 40 days. This is a hint, but too weak and too small to amend the horizon on.
- **F7:** More data is available than the test used. The test ran only the six core coins, while ADA, DOGE, LINK, TRX, UNI, AAVE (folds A and D and part of B and C), AVAX, SOL, INJ (folds A and D) and NEAR, SUI, TAO, ONDO (fold D) also have daily bars. Their falling markets do not always fall on the core coins' days, so they would add independent days to the pooled t.

## Ideas
- `060-02.d1.d2.d2.b1_volume-growth-fall-more-coins` (from F1, F2, F3, F7): In a falling market, while the coin's 20-day return is clearly negative, the more its trading volume over the past 30 days has grown against the 30 days before, the smaller its fall, or the larger its rise, over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
