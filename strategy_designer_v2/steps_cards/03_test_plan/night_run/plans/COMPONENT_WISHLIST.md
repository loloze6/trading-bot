# Component wish list

One block per idea that needs components the catalogue does not have.

## 003-01_thin-volume-rise-reverses_1d
- Component: RelativeVolumeComponent: the bar's volume divided by the mean volume of the last `period` bars (30 here), from the `volume` column; above 1 on heavy days, below 1 on thin days, and it falls as the day gets thinner (a log form, signed around 0, would suit a graded forecast) | measures: comparison

## 003-02_thin-volume-drop-rebounds_1d
- Component: VolumeRatioComponent: log(mean volume over the last 30 bars, current bar included / volume[t]), from the `volume` column; positive and growing the thinner the bar's volume is against its 30-day average, negative on heavy-volume bars | measures: comparison

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
