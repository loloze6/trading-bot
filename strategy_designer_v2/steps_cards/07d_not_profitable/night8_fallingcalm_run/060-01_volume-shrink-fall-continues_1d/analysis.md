---
line: 7.d confirmed, not profitable
backtest: 060-01_volume-shrink-fall-continues_1d
idea tested: 060-01_volume-shrink-fall-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3920 USD
---
## Findings
- **F1:** The effect sits almost entirely in the deepest volume shrinkage, not across the forecast scale. In-profile 5-day grid bars with a forecast below -15 had a mean excess 5-day return of -3.47 % (t -3.30, 113 cases), against -0.49 % (-15..-10, 62 cases), -0.47 % (-10..-5, 116 cases) and +0.69 % (-5..-2, 58 cases). On the raw log volume ratio, only the lowest quintile (-1.24 to -0.51) is clearly negative, at -2.06 % (t -2.11, 136 cases); the next quintile shows -0.97 % (t -1.17).
- **F2:** The book loses on its short holdings and earns on its long ones. Trades held 5.5 days or less (223 trades) lost a mean of -2.57 % net. Trades held 5.5 to 20 days (261 trades) netted about +0.05 %. Trades held 20 to 40 days (103 trades) earned +18.1 % net, and those held over 40 days (21 trades) earned +22.1 %. The fall's continuation pays when it is held for weeks; 5-day flips mostly pay fees and noise.
- **F3:** The size against cost explains the failed gain measures. All cases taken together give a total move of +0.13 % per case, 0.7 times the 0.19 % cost of a trade. The forecast-below-(-15) cases give a mean 5-day return of -2.95 % in the short's favour, about 15 times that cost. The book's mean daily return on days in a position was 0.028 %, against the 0.05 % rule.
- **F4:** The continuation lives after a moderate 20-day fall, not after a deep plunge or a shallow dip. Within the middle tertile of in-profile 20-day returns, shrinking-volume cases had a mean excess 5-day return of -4.31 % (t -5.02, 129 cases). On non-case bars in the same tertile it was +0.52 %, so the moderate fall alone does not carry the effect. After the deepest 20-day falls the cases returned -0.31 % (70 cases), and after the shallowest +1.23 % (94 cases).
- **F5:** A 5-day bounce breaks the continuation. Cases whose 5-day return was in the top tertile ("rose") had a mean excess 5-day return of -0.01 % (93 cases), against -1.93 % (fell, 107 cases) and -2.17 % (middle, 131 cases). Non-cases after a bounce returned +1.10 %, so the bounce condition is not an effect of its own on the short side.
- **F6:** The result rests on the years the downtrends persisted, which is why the leave-one-window-out Sharpe fell to -0.021.
- **F7:** Calm and agitated falling markets carried similar effects, so no agitation profile is singled out. Calm cases returned -1.44 % excess (t -1.99, 192 cases) and agitated cases -1.83 % (t -1.59, 101 cases).

## Ideas
- `060-01.d1_deep-dry-up-longer-fall` (from F1, F2, F3): In a falling market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 20 days, the fall coming mostly where the shrinkage is among the deepest of the coin's past two months.
- `060-01.d2_dry-up-in-moderate-declines` (from F4, F1, F6): In a falling market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days, and more so the more moderate its 20-day fall has been, the continuation fading as the 20-day fall turns into a plunge.
- `060-01.d3_dry-up-without-bounce` (from F5, F1, F3): In a falling market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days, and the larger still the lower its 5-day return, the continuation vanishing after a 5-day bounce.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
