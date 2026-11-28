# Component wish list

One block per idea that needs components the catalogue does not have.

## 089-02_calm-decline-up-down-volume-ratio_1d
- Component: UpDownDayMeanVolumeRatio: over bars t-19 .. t, (mean volume of bars with close[i] > close[i-1]) / (mean volume of bars with close[i] < close[i-1]), from close and volume; it grows as up days trade heavier per day than down days, and a log or centred form is 0 when the two are equal | measures: comparison

## 089-03_calm-decline-thinning-down-volume_1d
- Component: DownDayVolumeFadeRatio: ln(B / A), where A is the mean volume of the bars i in t-9 .. t with close[i] < close[i-1], and B is the mean volume of such bars in t-29 .. t-10; it is 0 when either window has no down bar, positive and growing as recent down days get lighter than before, negative when they get heavier (params short_period 10, base_period 20) | measures: situation
- Component: DownDayVolumeFadeRatio (the same component; its base window B is the comparison) | measures: comparison

## 089-01.c1_calm-decline-down-volume-exhaustion_1d
- Component: DownToUpDayMeanVolumeRatio: ln of (mean volume on bars closing below the prior close / mean volume on bars closing above it) over the last 20 bars, from close and volume, 0 when the two averages are equal and growing as the average down-day volume rises above the average up-day volume | measures: situation

## 089-04.c1_heavy-up-day-volume-rebounds_1d
- Component: UpDayVolumeToUsualVolumeComponent: the sum of volume[i] over bars i in t-`period`+1 .. t with close[i] > close[i-1] (`period` 20), divided by mean(volume) over the last `base_period` bars (60), from close and volume; never negative, 0 when no up day, grows as up days carry more volume against usual daily volume | measures: situation
