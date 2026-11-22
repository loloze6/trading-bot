# Component wish list

One block per idea that needs components the catalogue does not have.

## 027-01_panic-range-multiple-rebound_4h
- Component: PanicRangeMultipleComponent: on 4h bars, (max(high) − min(low) over the last 6 bars) divided by the mean of that same 6-bar range over the last 180 bars, bar t included; it is set to 0 unless close[t] < close[t−6]; it is 0 or above, never negative, and grows with the multiple (1 when the stretch's range equals the 30-day average) | measures: situation

## 027-04_panic-delayed-recovery-drift_4h
- Component: LaggedPanicStretchIntensity: over the 6 bars ending `lag` (6) bars before bar t, max(0, -(the stretch's close-to-close return) / the coin's usual 6-bar move over a long window) x ((max high - min low over those bars) / the mean of the usual 6-bar range over the same long window), from close, high and low; 0 unless the stretch fell, and growing with the depth of the fall and with how many usual ranges the stretch spanned | measures: situation
