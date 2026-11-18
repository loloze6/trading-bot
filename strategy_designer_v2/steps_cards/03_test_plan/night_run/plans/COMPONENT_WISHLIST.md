# Component wish list

One block per idea that needs components the catalogue does not have.

## 003-03_heavy-volume-rise-continues_1d
- Component: VolumeRatioComponent: volume[t] divided by the mean of the last `period` (30) bars' volume, from the `volume` column; it is 1 at average volume and grows as the day's volume gets heavier against that average | measures: comparison

## 003-04_heavy-volume-drop-continues_1d
- Component: VolumeRatioComponent: the current bar's volume divided by the mean volume of the prior `period` bars (period 30), from the `volume` column; it rises continuously as the day's volume grows against its own average (1 at the average, 3 at three times it) | measures: comparison

## 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d
- Component: volume_ratio: the bar's volume divided by the mean volume of the last 60 bars (from `volume`); about 1 on an ordinary day, growing as that day's volume grows heavier | measures: comparison
- Component: volume_weighted_fall: the negated one-bar return in usual moves (from `close`) multiplied by the volume ratio above (from `volume`); positive after a fall, growing with both the size of the fall and how heavy its volume was | measures: situation

## 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next.g1_falls-closing-near-low-bounce_1d
- Component: CloseLocationComponent: computes (high - close) / (high - low) of the current bar, from the high, low and close columns, 0 to 1 (0.5 when high equals low); it grows as the close nears the day's low | measures: comparison
- Component: DownMoveCloseLocationComponent: computes max(0, -(close[t]/close[t-1] - 1) / s) x (high - close) / (high - low), s being the 60-bar standard deviation of one-bar returns, from the close, high and low columns; it is 0 on up days and grows with both the size of the fall in usual moves and the closeness of the close to the low | measures: situation

## 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g2_heavy-volume-fall-rebounds_1d
- Component: RelativeVolumeToMedian: volume[t] / median(volume of the past 20 bars), from the volume column; it is 1 at usual volume and grows without bound as the day's volume gets heavier | measures: situation

## 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.b1_weekend-move-reverses-three-days_1d
- Component: LaggedVolatilityScaledReturnComponent: the one-bar return of the bar `lag` bars before the current one (close[t-lag]/close[t-lag-1] - 1), divided by the standard deviation of the `vol_period` one-bar returns ending at that bar; read from closes only; signed, grows with the size of that past move in usual moves (lag 0, 1, 2 on the Sunday, Monday, Tuesday closes gives the weekend move) | measures: situation

## 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
- Component: VolumeWeightedScaledReturn: (close[t]/close[t-1] - 1) / std of the last 20 one-bar returns, times volume[t] / mean of the last 20 volumes. It is read from the close and volume columns. It is signed, and its size grows with both the move in usual-move units and the relative volume. | measures: comparison
- Component: RelativeVolume: volume[t] / mean of the last `period` volumes, from the volume column. It is one-sided, about 1 at usual volume and grows as volume rises above its average. | measures: comparison

## 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal.g1_high-volume-weekend-moves-reverse_1d
- Component: VolumeWeightedScaledReturn: (close[t]/close[t-1] - 1) / std(last 20 one-bar returns) x volume[t] / mean(volume over the last 20 bars), from close and volume; signed, and its size grows with both the move in usual moves and the relative volume | measures: comparison

## 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal.g1_high-vol-down-day-rebound_1d
- Component: VolatilityRatioToAverageComponent: the standard deviation of the last 20 one-bar close returns divided by the mean of that 20-bar standard deviation over the last 60 bars (bar t included), from closes; 1 at the average, it grows as the current volatility rises above its 60-day mean | measures: comparison
