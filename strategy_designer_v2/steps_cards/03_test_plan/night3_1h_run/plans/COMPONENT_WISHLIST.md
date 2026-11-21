# Component wish list

One block per idea that needs components the catalogue does not have.

## 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high_1h
- Component: ProximityWeightedSurgeComponent: computed from closes as W x (close[t] / close[t-24] - 1) / mean over the last 720 bars of abs(close[i] / close[i-24] - 1), where W = (1 / (1 + D))^power and D is the percent distance of close[t] below the highest of the last 720 closes; it grows with the size of the 24-hour surge in usual daily moves and as the close nears its 30-day high, and it is 0 or small far below the high | measures: comparison

## 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds_1h
- Component: DropInMeanAbsDailyMoves: (close[t] / close[t-24] - 1) / mean over the last 720 bars of abs(close[i] / close[i-24] - 1), from closes; signed, and more negative the deeper the 24-hour fall in multiples of the 30-day average absolute daily return | measures: situation

## 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h
- Component: ReturnToMeanAbsReturnRatio: (close[t] / close[t-24] - 1) / mean over the last 720 bars of abs(close[i] / close[i-24] - 1), from closes only; it is signed and grows as the 24-bar rise becomes a larger multiple of the coin's usual daily move | measures: situation

## 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h
- Component: DailyDropToMeanAbsDailyReturn: (close[t] / close[t-24] - 1) divided by the mean of abs(close[i] / close[i-24] - 1) over the last 720 bars, from closes; signed, it is more negative the more times the usual daily move the coin fell over the last 24 hours (with a `drop_only` setting giving max(0, -value), which grows with the drop multiple) | measures: situation
