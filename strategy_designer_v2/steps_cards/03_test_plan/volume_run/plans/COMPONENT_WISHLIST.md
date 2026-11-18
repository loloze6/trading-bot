# Component wish list

One block per idea that needs components the catalogue does not have.

## 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g2_rising-volume-precedes-gains_1d
- Component: VolumeMeanRatio: mean of `volume` over the last `short_period` bars (5) divided by mean of `volume` over the last `long_period` bars (30), current bar included; 1 at normal participation, rising above 1 as recent volume grows relative to its 30-day level, falling toward 0 when recent volume is thin | measures: situation

## 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g2_heavy-volume-fall-rebounds_1d
- Component: VolumeToMedianRatio: volume[t] divided by the median of the `volume` column over the prior `period` bars (default 20, bar t excluded); 1 at a typical day, growing as the day's volume exceeds its recent median | measures: comparison

## 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal.g1_high-volume-weekend-moves-reverse_1d
- Component: VolumeWeightedScaledReturnComponent: computes (close[t]/close[t-1] - 1) / (std of the last 20 one-bar returns) x volume[t] / mean(volume over the last 20 bars), from the close and volume columns; it is signed, and its size grows with both the move in usual moves and the volume relative to its 20-day average | measures: comparison
