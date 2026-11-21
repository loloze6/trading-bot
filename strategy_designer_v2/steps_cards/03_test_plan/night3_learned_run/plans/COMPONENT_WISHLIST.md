# Component wish list

One block per idea that needs components the catalogue does not have.

## 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d
- Component: centred-power counter-bet: -(w(t) - mean of w over the prior 365 bars) x z(t). Here w(t) is the Pearson correlation, over the past 365 days, of nearness to the 90-day high (close / max of the last 90 closes - 1) with the following 5-day return, and z(t) is that nearness's 365-bar z-score, both from closes. It grows as past power rises further above its usual level and as the nearness signal is more extreme. | measures: comparison
