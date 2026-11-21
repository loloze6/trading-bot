# Component wish list

One block per idea that needs components the catalogue does not have.

## 022-01_learned-combined-signal-score_1d
- Component: PastPredictivePowerWeightedCompositeComponent: from closes only, on bar t computes four signals. They are the 28-bar return, the negated 1-bar return, the 90-bar closing-high proximity and the negated 30-bar return volatility, each z-scored over the past 365 bars. For each signal it takes its weight w_k, the correlation over bars i in t-365..t-5 between signal_k(i) and close[i+5]/close[i]-1, so only completed returns are used and the weights are relearned every bar. It outputs sum_k w_k x z_k(t) / sum_k |w_k|. The output is signed and grows as the signals that predicted well point more strongly the same way. | measures: comparison

## 022-02_combination-beats-best-single_1d
- Component: RelearnedCombinationScore: at each bar, regresses the past 5-day returns (close[i+5]/close[i]-1, only for i+5 <= t) over a rolling window on the four standardised signals from the closes (28-day return, 1-day return, 90-day-high proximity, 30-day volatility), then outputs the fitted combination of today's signals; signed, and it grows with the predicted 5-day return | measures: situation
- Component: PastBestSingleSignalScore: at each bar, ranks the four signals by the rolling correlation of each signal with the realised 5-day return (only returns already known at t), then outputs today's value of the top-ranked signal, signed by that correlation; signed, and it grows with that signal's strength | measures: comparison

## 022-03_combined-extremes-larger-moves_1d
- Component: PerformanceWeightedSignal: one effect's value (momentum, 1-day reversal, distance from high, or volatility level, from closes) times its trailing correlation with the realised 5-bar forward return. The correlation is computed from closes only over a past window, and includes only returns fully realised by bar t. The output grows with both the signal's strength and its recent predictive success, and its sign flips when the effect has recently worked in reverse. | measures: situation
