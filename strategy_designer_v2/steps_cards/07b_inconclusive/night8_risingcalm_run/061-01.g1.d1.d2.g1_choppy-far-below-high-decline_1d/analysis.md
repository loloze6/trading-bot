---
line: 7.b inconclusive
backtest: 061-01.g1.d1.d2.g1_choppy-far-below-high-decline_1d
idea tested: 061-01.g1.d1.d2.g1_choppy-far-below-high-decline
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3585 USD
---
## Findings
- **F1:** In folds B and C, the cases do not grade overall the way step 5 reads them. Splitting by gap over all cases, the larger-gap half earns +4.2 % excess short against +0.4 % for the smaller half (Welch t 3.16). Step 5's own check on all four folds, however, gave a larger-gap half minus smaller-gap half of −0.07 %. The grading is mixed across the data, and that is part of why the result is unclear.
- **F2:** The grading lives in calm bars only. In calm choppy cases, the larger-gap half earns +3.6 % excess short over 5 days and the smaller half −0.3 % (difference +3.9 %, Welch t 2.98; Spearman of gap vs excess −0.20). In agitated choppy cases the halves are +4.6 % vs +3.4 % by gap (Welch t 0.45), and by forecast the order flips (−0.7 %, t −0.24). There, large and small gaps fall alike, with no grading.
- **F3:** Calm cases ranked by gap rise steadily across gap quintiles: excess short +9.2 % (t 2.15, 12 cases), +4.4 % (t 3.07, 29), +0.9 % (t 0.61), −1.3 % (t −0.97) and +0.8 % (t 0.64), from the largest gap to the smallest. The gap-weighted mean excess short over calm cases is +3.5 % with day-clustered t 2.57 (159 cases, 85 days). Here "calm" means the coin's 30-day swing is at or below its median over the explored windows, an approximation of the profile's past-year median.
- **F4:** In calm bars, the largest-gap third is positive in every year: +6.4 % (2018, t 2.26), +2.1 % (2019, t 1.91), +4.6 % (2020, t 1.21) and +7.4 % (2021, t 1.29). The middle and smallest-gap thirds are near zero or negative from 2019 on (for example −1.9 % and −5.7 % in 2020 and 2021). The calm-side effect is therefore not carried by one year. By contrast, the pooled effect over all cases is mostly 2018 (+6.2 %, t 3.61, against −0.005 % in 2021).
- **F5:** The tested result is on the predicted side but short of the bar: weighted mean excess short +1.02 % with t 1.68 (721 cases, 352 days). The unusual move is +0.61 % per case (t 1.87), which is 3.1 times the 0.19 % trade cost. The total move is only +0.04 %, because the coin's normal drift is −0.57 % in the short direction. A short on this signal can only beat holding; it cannot earn much on its own. The test used only the six default coins, while six more (ADA, DOGE, LINK, TRX, UNI, AAVE) have data in folds A and D and part of B and C.
- **F6:** In folds B and C, five of six coins carry the effect: BTC +2.6 % (t 2.10), ETH +3.7 % (t 2.46), LTC +2.5 %, XMR +2.5 % and XRP +1.9 % (t 1.37 to 1.68). ZEC is flat (−0.06 %, t −0.04).

## Ideas
- `061-01.g1.d1.d2.g1.b1_choppy-calm-far-below-high-decline` (from F2, F3, F4, F6): In a choppy, calm market, the further a coin's close sits below its highest close of the past 20 days, the further it keeps falling over the next 5 days.
- `061-01.g1.d1.d2.g1.b2_choppy-far-below-high-more-coins` (from F5, F6): In a choppy market, the further a coin's close sits below its highest close of the past 20 days, the further it keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
