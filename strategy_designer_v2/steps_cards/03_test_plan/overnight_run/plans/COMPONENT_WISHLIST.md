# Component wish list

One block per idea that needs components the catalogue does not have.

## N1-03_mature-trend-carries-drift_1d
- Component: MaEpisodeAgeComponent: the number of consecutive bars, ending at the current bar, on which the close is above its SMA(`period`, default 200), computed from closes; positive while above, negative count while below, reset to ±1 at each cross; its size grows by one with each bar the episode lasts | measures: situation

## N1-05_friday-to-saturday-rise_1d
- Component: WeekdaySeasonalReturnComponent: from `timestamp` and `close`, takes the weekday of the next bar. It then computes the trailing mean close-to-close return of past bars on that weekday (Saturday, when the current bar is Friday), minus the trailing mean of all daily returns over the same lookback. The output is signed and continuous, and grows as that weekday's past returns exceed the average day's. | measures: situation

## N1-09_below-falling-long-average_1d
- Component: MovingAverageSlope: (MA_period[t] - MA_period[t-k]) / MA_period[t-k] x 100, the SMA or EMA of closes compared with itself k bars earlier, from the close column; signed, more negative the more steeply the average has fallen over k bars | measures: situation

## N1-02_above-rising-long-average_1d
- Component: SmaSlopeComponent: (SMA_period(close)[t] - SMA_period(close)[t-k]) / SMA_period(close)[t-k] x 100 from closes (period 200, k 20); signed, grows as the long average rises faster | measures: situation
- Component: SmaSlopeComponent (same as above): its sign separates rising from falling 200-day SMA trades | measures: comparison

## N1-07_fresh-death-cross-rebound_1d
- Component: SmaCrossRecency: from closes, the number of bars since SMA(50) last crossed below SMA(200) (0 on the cross bar), or a freshness score of max(0, 20 - bars since the cross) that is largest on the cross bar and falls to 0 after 20 bars or once SMA50 is back above SMA200 | measures: situation

## N2-01_weekday-of-coming-bar_1d
- Component: coming-bar weekday: the UTC weekday (0 to 6) of the current bar's timestamp plus one bar's spacing, read from `timestamp`; a categorical value, used as a regime measure so that a rule can select the bar before Saturday | measures: situation

## N5-04_clustered-new-highs_1d
- Component: NewHighCountComponent: the number of bars among the last `window` (10) whose close was above every one of its prior `lookback` (20) closes, read from closes; it runs 0 to `window` and grows as the run prints more new highs close together (1 at a first break, more in an established run) | measures: situation
