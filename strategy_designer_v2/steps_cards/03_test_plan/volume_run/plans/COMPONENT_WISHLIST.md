# Component wish list

One block per idea that needs components the catalogue does not have.

## 012-03_lower-wick-flush-recovery_1d
- Component: LowerWickShareComponent: (close[t] - low[t]) / (high[t] - low[t]) from the bar's high, low and close (0.5 if high equals low); 0 when the close is at the low, rising to 1 when the close is at the high, so it grows with the length of the lower wick below the close | measures: comparison

## 012-04_flush-depth-retracement-size_1d
- Component: LowerWickComponent: (min(open, close) - low) / (high - low) of the current bar, 0 to 1 (0 when high = low), from open, high, low and close; it grows as the low sits further below the bar's body | measures: situation
- Component: OpenToLowDropComponent: (open - low) / open x 100 of the current bar, from open and low, never negative; it grows with the depth of the bar's fall from its open to its low (optionally divided by the coin's usual one-bar move) | measures: comparison

## 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g2_rising-volume-precedes-gains_1d
- Component: VolumeMeanRatio: mean of `volume` over the last `short_period` bars (5) divided by mean of `volume` over the last `long_period` bars (30), current bar included; 1 at normal participation, rising above 1 as recent volume grows relative to its 30-day level, falling toward 0 when recent volume is thin | measures: situation

## 013-04_heavy-volume-below-high-breakout_1d
- Component: VolumeMeanRatio: the mean of `volume` over the last 10 bars divided by the mean of `volume` over the last 90 bars, both ending at the current bar; it is 1 at usual volume and grows as recent volume gets heavier | measures: comparison

## 003-03_heavy-volume-rise-continues_1d
- Component: volume-weighted rise: one-day return of the close over the 20-bar standard deviation of one-bar returns, times volume[t] / mean(volume over the last 30 bars), from close and volume; signed, zero for no move, and larger as the rise is larger and the volume heavier | measures: situation

## 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g2_heavy-volume-fall-rebounds_1d
- Component: VolumeToMedianRatio: volume[t] divided by the median of the `volume` column over the prior `period` bars (default 20, bar t excluded); 1 at a typical day, growing as the day's volume exceeds its recent median | measures: comparison

## 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal.g1_high-volume-weekend-moves-reverse_1d
- Component: VolumeWeightedScaledReturnComponent: computes (close[t]/close[t-1] - 1) / (std of the last 20 one-bar returns) x volume[t] / mean(volume over the last 20 bars), from the close and volume columns; it is signed, and its size grows with both the move in usual moves and the volume relative to its 20-day average | measures: comparison
