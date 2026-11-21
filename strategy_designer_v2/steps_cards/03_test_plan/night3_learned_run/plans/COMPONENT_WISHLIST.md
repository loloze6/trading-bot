# Component wish list

One block per idea that needs components the catalogue does not have.

## 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls.d1_fall-rebound-in-volatility-bursts_1d
- Component: VolatilityBurstScaledFallComponent: max(0, -(close[t]/close[t-1]-1) / s30(t)) x (s7(t) / s30(t)), where sN is the ddof-1 standard deviation of the last N one-bar returns of the close; 0 on up bars, it grows with the depth of the fall in 30-day usual moves and with how far 7-day volatility sits above 30-day volatility | measures: situation

## 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d1_weighted-reversal-with-trend-agreement_1d
- Component: TrendAgreementWeightedTermComponent: computes term(t) x (1 + max(0, sign(term(t)) x R60(t) / s60(t))) from closes, where term is `PastPredictivePowerWeightedCompositeComponent`'s "single" term for the 1-day return (z over 365 bars times its correlation with the next 5 bars' return over 365 bars), R60 is close[t]/close[t-60]-1, and s60 is the standard deviation of 60-bar returns; it is signed like the term, grows with the term's size, and grows further as the 60-day return points more strongly the term's way | measures: comparison

## 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d1_volatility-reversal-with-trend_1d
- Component: VolatilityExcessPredictivePowerZ: from closes, -(w(t) - wbar(t)) x z(t), where w is the correlation over the past 365 days of s = -std of the 30 one-bar returns with the 5-day forward return, wbar is the mean of w over the prior 365 bars, and z is s's 365-bar z-score; it grows as the past power rises above its usual level and the signal is further from its mean | measures: situation
- Component: TrendAgreementWeightedBet: from closes, the reversed-volatility bet above times max(0, sign(bet) x the 28-day return in percent), or a smooth version of that weight; it is 0 against the trend and grows with the size of the 28-day return on the bet's side | measures: comparison

## 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls.d2_fall-rebound-after-strong-months_1d
- Component: FallTimesAbsMonthReturnComponent: max(0, -(close[t]/close[t-1]-1)/s30) x abs(close[t]/close[t-30]-1) x 100, where s30 is the std of the last 30 one-bar returns, from closes; 0 on up bars, grows with the depth of the fall and with the size of the 30-day move either way | measures: comparison

## 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d3_persistent-weighted-reversal-extremes_1d
- Component: ReversalTermPersistenceComponent: from closes only, computes the term w(i) x z(i) on each of the last 20 bars i. Here s(i) = -(close[i]/close[i-1] - 1), z(i) is its z-score over the 365 bars ending at i, and w(i) is the Pearson correlation of s with the next 5-bar return over the training rows ending at i-5. It outputs sign(term(t)) x (the number of those 20 bars on which the term had today's sign and an absolute size above its 365-bar mean absolute size) / 20, signed, from -1 to +1, growing in size with each further day the term stayed far out on the same side | measures: comparison
