# Component wish list

One block per idea that needs components the catalogue does not have.

## 037-01_falling-market-wide-day-decline_1d
- Component: RangeInReturnStdComponent: (high[t] − low[t]) / close[t] / s, where s is the std (ddof 1) of the last 30 one-bar returns close[j] / close[j-1] − 1 ending at bar t; built from high, low and close; never negative, it grows as the day's range widens against the 30-day return swing | measures: situation

## 041-01_wide-up-day-next-day-fade_1d
- Component: RangeInUsualMovesComponent: ((high[t] − low[t]) / close[t]) / s, where s is the standard deviation (ddof 1) of the last `vol_period` (30) one-bar returns close[j] / close[j-1] − 1, bar t's included; it reads high, low and close; it is 0 and up, never negative, and grows as the day's range widens against the coin's usual daily swing | measures: situation
