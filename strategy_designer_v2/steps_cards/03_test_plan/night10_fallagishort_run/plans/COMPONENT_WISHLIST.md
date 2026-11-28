# Component wish list

One block per idea that needs components the catalogue does not have.

## 048-01_falling-agitated-wide-rise-giveback_1d
- Component: ScaledRiseRangeMultiple: max(0, (close[t]/close[t-1] - 1) / s30) x (high[t] - low[t]) / mean(high[i] - low[i], i = t-29 .. t), where s30 is the std (ddof 1) of the last 30 one-bar returns, read from close, high and low; it is 0 on down and flat days and grows with both the scaled rise and the range multiple (the up-side mirror of `ScaledFallRangeMultipleComponent` with `period` 1, `lag` 0, `window` 30, `scale` "std") | measures: situation

## 086-01_upper-shadow-further-fall_1d
- Component: UpperWickInMeanRangesComponent: (high[t] − max(open[t], close[t])) / mean(high[i] − low[i]) over the last 30 bars (`base_period`, bar t included or excluded by setting), from open, high, low and close; 0 for no upper shadow, growing linearly as the shadow lengthens against the usual daily range | measures: situation

## 086-02_rejected-rise-share-fall_1d
- Component: OpenRiseGivebackShare: (high[t] − close[t]) / (high[t] − open[t]) from open, high and close of bar t when high > open, else 0; 0 when the close is at the high, 1 when the whole rise above the open is given back, above 1 when the close ends below the open (optionally capped at 1); it grows with the share of the rejected rise | measures: situation
