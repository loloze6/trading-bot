# Component wish list

One block per idea that needs components the catalogue does not have.

## 060-02_falling-calm-low-to-close-fade_1d
- Component: CloseAboveLowInUsualMovesComponent: (close[t] − low[t]) / close[t] / s, where s is the std (ddof 1) of the last 30 one-bar returns close[j]/close[j-1] − 1, bar t included; read from high, low and close; 0 with the close at the low, growing linearly as the close stands further above the day's low in usual daily moves | measures: situation

## 086-02_down-up-volume-ratio-drift_1d
- Component: DownUpVolumeSkewComponent: over the last `period` bars (20), the mean volume of bars with close[i] < close[i-1] divided by the mean volume of bars with close[i] > close[i-1], minus 1 (or the log of that ratio), from close and volume; signed, 0 when the two averages are equal, growing as down days get heavier and up days get thinner | measures: situation
