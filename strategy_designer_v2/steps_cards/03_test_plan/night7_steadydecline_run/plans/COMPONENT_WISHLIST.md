# Component wish list

One block per idea that needs components the catalogue does not have.

## 035-02_swing-wide-low-close-rebounds_1d
- Component: LowCloseRangeInUsualMovesComponent: (high[t] − low[t]) / close[t] / s x (high[t] − close[t]) / (high[t] − low[t]), which equals (high[t] − close[t]) / close[t] / s, where s is the std (ddof 1) of the last 20 one-bar returns close[j] / close[j-1] − 1; reads high, low and close; 0 with the close at the high, growing as the day widens against the coin's recent swing and as the close nears the low | measures: situation

## 036-02_fall-vs-range-next-day-rebound_1d
- Component: FallInMeanBarRanges: max(0, close[t-1] − close[t]) / mean(high[i] − low[i], i = t-30 .. t-1), from close, high and low; 0 on up days, and it grows linearly as the day's close-to-close fall gets larger against the prior 30 days' mean daily range (above 1 when the fall exceeds the usual range) | measures: comparison

## 037-02_fall-range-beyond-loss-rebound_1d
- Component: FallTimesRangeExcessComponent: max(0, close[t-1] − close[t]) / close[t-1] x 100 x max(0, (high[t] − low[t]) − max(0, close[t-1] − close[t])) / close[t-1] x 100, from close, high and low; 0 on up days, never negative, growing with both the fall and the range travelled beyond the closing loss | measures: situation
