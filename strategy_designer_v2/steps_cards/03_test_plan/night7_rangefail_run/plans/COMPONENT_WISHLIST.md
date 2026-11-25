# Component wish list

One block per idea that needs components the catalogue does not have.

## 033-01.b2_beyond-range-close-drift_1d
- Component: PriorRangePositionComponent: 2 x (close[t] − L) / (H − L) − 1, with H = max(high[t-20..t-1]) and L = min(low[t-20..t-1]), from the high, low and close columns; −1 at the prior low, +1 at the prior high, rising continuously with the close and growing past +1 above the prior high (below −1 under the prior low) | measures: situation

## 033-02.d2_fresh-upside-break-rises_1d
- Component: PriorBreakoutCloseCountComponent: the number of bars i in t-`window` .. t-1 (bar t excluded) whose close[i] is above the highest of the `period` closes before it (close[i-`period`] .. close[i-1]), with `window` 20 and `period` 20, from closes only; it is 0 to `window` and grows by one for each earlier breakout close, so fewer earlier breaks give a smaller value | measures: situation
