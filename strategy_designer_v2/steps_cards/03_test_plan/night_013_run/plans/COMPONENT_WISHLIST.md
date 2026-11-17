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

## 013-06_breakout-volume-drives-continuation_1d
- Component: VolumeRatio: volume[t] / mean(volume over the last 90 bars, bar t included), from the `volume` column; it grows continuously as the bar's volume rises above its 90-day average (1 is an average day, above 1 is heavy) | measures: comparison

## 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d
- Component: VolumeRatioComponent: today's `volume` divided by the mean of the last 30 bars' `volume`, minus 1 (zero at average volume); it grows the heavier today's volume is against its 30-day average | measures: comparison

## 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d
- Component: RelativeVolumeComponent: the latest bar's volume divided by the mean volume of the last 20 bars (current bar included), minus 1, from the `volume` column; it is 0 at average volume and grows as volume rises above its 20-day average | measures: situation

## 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d3_nearness-strongest-when-calm_1d
- Component: CalmScaledDistanceFromHigh: closeness to the 365-bar high close (100 + (close - max close) / max close x 100), times the ratio of the 365-bar mean of the 20-bar std of daily returns to the current 20-bar std, all from closes; it grows as the close nears its high and as daily moves get calmer than their past year | measures: comparison

## 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d
- Component: RelativeVolumeComponent: log(volume[t] / mean of the last 30 bars' volume, bar t included), from the `volume` column; 0 at average volume, positive and growing as the day's volume gets heavier, negative on light days | measures: situation

## 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls.g1_rebound-grows-with-volatility_1d
- Component: VolRankedFallRebound: computes max(0, -(close[t]/close[t-1] - 1) / std of the last 20 daily returns) x (share of the last 120 values of 20-day return std that are at or below the current one), from closes only; it is zero on up days and grows with the depth of the fall and with how high volatility stands against its past 120 days | measures: comparison
