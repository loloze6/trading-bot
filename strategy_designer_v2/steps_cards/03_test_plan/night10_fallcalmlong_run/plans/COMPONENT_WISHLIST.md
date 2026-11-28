# Component wish list

One block per idea that needs components the catalogue does not have.

## 089-02_calm-decline-up-down-volume-ratio_1d
- Component: UpDownDayMeanVolumeRatio: over bars t-19 .. t, (mean volume of bars with close[i] > close[i-1]) / (mean volume of bars with close[i] < close[i-1]), from close and volume; it grows as up days trade heavier per day than down days, and a log or centred form is 0 when the two are equal | measures: comparison

## 089-03_calm-decline-thinning-down-volume_1d
- Component: DownDayVolumeFadeRatio: ln(B / A), where A is the mean volume of the bars i in t-9 .. t with close[i] < close[i-1], and B is the mean volume of such bars in t-29 .. t-10; it is 0 when either window has no down bar, positive and growing as recent down days get lighter than before, negative when they get heavier (params short_period 10, base_period 20) | measures: situation
- Component: DownDayVolumeFadeRatio (the same component; its base window B is the comparison) | measures: comparison
