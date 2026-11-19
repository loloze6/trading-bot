# Component wish list

One block per idea that needs components the catalogue does not have.

## 016-02_down-grind-price-continuation_1h
- Component: GrindShareOfFallComponent: over the last `period` (72) one-bar close returns, 1 minus (the sum of the `k` largest hourly losses, e.g. k = 3) / (the sum of all hourly losses), signed by the period's net return so a fall reads negative; it grows toward 1 in size as the fall is spread over many small losses and shrinks toward 0 as the few biggest hours carry it | measures: comparison

## 016-03_up-jump-price-reversal_1h
- Component: TopGainsShareOfRiseComponent: over the last `period` (72) one-bar close returns close[j]/close[j-1]-1, the sum of the `k` (e.g. 3) largest positive returns divided by the net rise close[t]/close[t-72]-1 (0 when the net move is not above 0, capped at 1). It is computed from closes, and its value grows from near 0 for a grind toward 1 as the rise comes from fewer, bigger hours. | measures: situation

## 016-04_down-jump-price-reversal_1h
- Component: FallConcentrationShare: over the last `period` (72) one-bar close changes, the sum of the `k` (3) largest one-bar losses divided by the net fall close[t-period] - close[t], when that net fall is above 0, else 0. It reads closes only, is never negative, and grows from near 0 (a grind spread over many hours) towards 1 and above (a fall made by a few violent hours). A variant times the net fall in percent, so that size and concentration combine into one graded long-only reading. | measures: comparison

## 016-05_up-even-volume-continuation_1h
- Component: VolumeEvenness: the median of the last `period` (72) bar volumes divided by their mean (or 1 minus their Gini coefficient), from the volume column; it runs from 0 to 1 and rises toward 1 as the hourly volume is spread more evenly. | measures: situation

## 016-07_up-volume-burst-reversal_1h
- Component: VolumeConcentrationComponent: the sum of the `top_k` largest hourly volumes among the last `period` bars (for example 72 and 3), divided by the total volume of those bars, read from the volume column; it grows from `top_k`/`period` (even volume) towards 1 as the volume bunches into a few hours | measures: situation

## 016-08_down-volume-burst-reversal_1h
- Component: VolumeTopShareComponent: over the last `period` bars (72), the sum of the `top_k` largest hourly volumes (for example 3) divided by the sum of all `period` volumes, read from the volume column; ranges from top_k/period (volume spread evenly) up to 1, and grows as the period's volume concentrates in fewer hours | measures: comparison

## 016-01_up-grind-price-continuation_1h
- Component: GrindShareOfRise: from the closes over the last 72 bars, R = close[t] / close[t-72] - 1 and T = the sum of the k largest one-bar gains (k = 3); outputs 1 - min(T / R, 1) when R > 0, else 0, so it is 0 at a small or negative rise and grows towards 1 as the rise is carried by many small hourly gains | measures: comparison
