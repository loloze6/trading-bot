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
