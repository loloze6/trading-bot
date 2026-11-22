# Component wish list

One block per idea that needs components the catalogue does not have.

## 024-01_fading-volume-uprun-giveback-size.g1_long-up-run-continues-rising_4h
- Component: UpStreakGainInUsualMovesComponent: n is the number of consecutive bars ending at bar t with close[i] > close[i-1] (0 if bar t is not up). Output is (close[t] / close[t-n] - 1) / m, where m is the mean of abs(close[j] / close[j-1] - 1) over the last `window` (180) one-bar returns. The output is 0 when there is no run, and grows with the run's gain counted in usual 4h moves, so it grows with both the run's length and its strength. | measures: comparison

## 024-04_downrun-volume-fade-depth-rebound.d1_rebound-in-expanding-volatility_4h
- Component: VolRatioScaledDownStreakLossComponent: (close[t-n] − close[t]) / close[t-n] / m x (std of the last 42 one-bar returns / std of the last 180 one-bar returns). Here n is the current run of consecutive down closes and m is the mean absolute one-bar return over 180 bars, all from closes. It is 0 when bar t did not close down, and grows with the streak's loss in usual moves and with the 7-day to 30-day volatility ratio. | measures: situation
- Component: ShortToLongVolatilityRatioComponent: std (ddof 1) of the last `short_period` (42) one-bar returns divided by the std of the last `long_period` (180) one-bar returns, from closes. It is 1 when recent volatility equals the 30-day level and grows as 7-day volatility expands above it. | measures: comparison
