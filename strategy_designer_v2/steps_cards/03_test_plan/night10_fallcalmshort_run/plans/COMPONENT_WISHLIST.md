# Component wish list

One block per idea that needs components the catalogue does not have.

## 086-01_down-day-volume-share-drift_1d
- Component: DownDayVolumeShareComponent: from the close and volume columns, sum(volume[i] for i in t-9 .. t with close[i] < close[i-1]) / sum(volume[t-9 .. t]); 0 to 1, rising as more of the 10-bar volume falls on down days (a "centred" form, share − 0.5, would be signed: positive when down-day volume dominates, 0 when balanced) | measures: situation
