# Component wish list

One block per idea that needs components the catalogue does not have.

## 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d
- Component: VolatilityScaledHighBreakComponent: (close[t] - H) / H / s, where H is the highest close of bars t-20 .. t-1 and s is the std (ddof 1) of the last 20 one-bar returns close[j]/close[j-1] - 1; signed, 0 at the prior high, growing as the close clears the high by more usual daily moves (clip at 0 for the break side) | measures: situation
