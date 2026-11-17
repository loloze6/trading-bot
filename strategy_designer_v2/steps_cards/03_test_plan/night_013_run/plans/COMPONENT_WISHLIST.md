# Component wish list

One block per idea that needs components the catalogue does not have.

## 013-01_nearness-to-high-predicts-gains.d1_gain-concentrated-at-the-high_1d
- Component: ConvexHighProximityComponent: from closes, closeness = 1 / (1 + depth), where depth is the percent distance of the close below the highest of the last 365 closes, raised to a power above 1; it reaches 1 at the high and rises faster the nearer the close is to the high | measures: situation
- Component: HighProximityMomentumComponent: from closes, the convex closeness above times the 30-bar percent return of the close; it is positive and grows when the close is pressed against its 365-bar high after a strong month, and is small far below the high or after a weak month | measures: situation

## 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g2_rising-volume-precedes-gains_1d
- Component: VolumeRatioComponent: the mean of `volume` over the last `short_period` (5) bars divided by its mean over the last `long_period` (30) bars, minus 1, current bar included; it is positive and grows as recent volume rises above the longer average, and negative when recent volume is thin | measures: situation

## 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d
- Component: VolumeRatioComponent: volume[t] / mean(volume over the last 20 bars, bar t included) - 1, from the `volume` column; 0 at average volume, positive and growing as the day's volume rises above its 20-day average, negative down to -1 as it thins | measures: situation

## 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g2_break-of-30-day-high_1d
- Component: PriorHighBreakoutDistance: (close[t] - H) / H x 100, where H is the highest `high` of the `period` bars before bar t (bar t excluded); positive and growing as the close clears that high further, negative below it (a clip at 0 keeps only the break) | measures: situation

## 013-02_follow-through-stronger-near-high_1d
- Component: HighAnchoredMomentumComponent: from closes, (close[t] / close[t-30] - 1) x 100 x (close[t] / highest close of the last 365 bars), so it is signed by the 30-bar return and its size grows with both the return and closeness to the 52-week high (full weight at the high, shrinking towards 0 far below it) | measures: comparison

## 013-03_breakout-above-high-continues_1d
- Component: DistanceAbovePriorHighComponent: (close[t] - H) / H x 100, where H is the highest of the `period` closes before bar t (bar t excluded); read from closes; positive above the prior high, negative below, and grows with the distance above it | measures: situation

## 013-04_heavy-volume-below-high-breakout_1d
- Component: VolumeRatioComponent: the mean of `volume` over the last `short_period` bars (10) divided by the mean of `volume` over the last `long_period` bars (90), minus 1. It comes from the `volume` column, is 0 when recent volume equals its average, and grows as recent volume gets heavier. | measures: comparison

## 013-05_longer-stall-bigger-breakout_1d
- Component: StallUnderHighCountComponent: from closes, the number of the last 60 bars whose close was below the highest of the 365 closes before it and within a set percent band of that high; the value rises from 0 to 60 as the stall under the high lasts longer | measures: comparison

## 013-06_breakout-volume-drives-continuation_1d
- Component: VolumeRatio: volume[t] / mean(volume over the last 90 bars, bar t included), from the `volume` column; it grows continuously as the bar's volume rises above its 90-day average (1 is an average day, above 1 is heavy) | measures: comparison

## 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d
- Component: VolumeRatioComponent: today's `volume` divided by the mean of the last 30 bars' `volume`, minus 1 (zero at average volume); it grows the heavier today's volume is against its 30-day average | measures: comparison

## 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d
- Component: RelativeVolumeComponent: the latest bar's volume divided by the mean volume of the last 20 bars (current bar included), minus 1, from the `volume` column; it is 0 at average volume and grows as volume rises above its 20-day average | measures: situation
