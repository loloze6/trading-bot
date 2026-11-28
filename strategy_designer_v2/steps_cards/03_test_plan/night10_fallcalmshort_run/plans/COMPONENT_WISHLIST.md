# Component wish list

One block per idea that needs components the catalogue does not have.

## 086-01_down-day-volume-share-drift_1d
- Component: DownDayVolumeShareComponent: from the close and volume columns, sum(volume[i] for i in t-9 .. t with close[i] < close[i-1]) / sum(volume[t-9 .. t]); 0 to 1, rising as more of the 10-bar volume falls on down days (a "centred" form, share − 0.5, would be signed: positive when down-day volume dominates, 0 when balanced) | measures: situation

## 060-02_falling-calm-low-to-close-fade_1d
- Component: CloseAboveLowInUsualMovesComponent: (close[t] − low[t]) / close[t] / s, where s is the std (ddof 1) of the last 30 one-bar returns close[j]/close[j-1] − 1, bar t included; read from high, low and close; 0 with the close at the low, growing linearly as the close stands further above the day's low in usual daily moves | measures: situation

## 086-02_down-up-volume-ratio-drift_1d
- Component: DownUpVolumeSkewComponent: over the last `period` bars (20), the mean volume of bars with close[i] < close[i-1] divided by the mean volume of bars with close[i] > close[i-1], minus 1 (or the log of that ratio), from close and volume; signed, 0 when the two averages are equal, growing as down days get heavier and up days get thinner | measures: situation
