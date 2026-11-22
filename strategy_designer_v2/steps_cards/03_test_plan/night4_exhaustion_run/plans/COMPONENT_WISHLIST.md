# Component wish list

One block per idea that needs components the catalogue does not have.

## 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
- Component: DownStreakScaledLoss: n = the number of consecutive bars ending at t with close[i] < close[i-1]; the output is (close[t-n] / close[t] - 1) divided by the mean absolute one-bar return close[j] / close[j-1] - 1 over the last 180 bars, and 0 when bar t is not a down bar; it grows with the streak's loss in typical 4h moves | measures: situation
- Component: DownStreakVolumeFade: over the same current down streak of n >= 2 bars, minus the least-squares slope of ln(volume) against the bar index, from the volume column; 0 when there is no streak; it grows as volume declines faster across the streak | measures: situation

## 024-01_fading-volume-uprun-giveback-size.g1_long-up-run-continues-rising_4h
- Component: UpStreakGainInUsualMovesComponent: n is the number of consecutive bars ending at bar t with close[i] > close[i-1] (0 if bar t is not up). Output is (close[t] / close[t-n] - 1) / m, where m is the mean of abs(close[j] / close[j-1] - 1) over the last `window` (180) one-bar returns. The output is 0 when there is no run, and grows with the run's gain counted in usual 4h moves, so it grows with both the run's length and its strength. | measures: comparison
