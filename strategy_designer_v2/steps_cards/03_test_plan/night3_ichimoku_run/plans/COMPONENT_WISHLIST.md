# Component wish list

One block per idea that needs components the catalogue does not have.

## 021-03_thin-cloud-upward-breakout_1d
- Component: IchimokuCloudPositionComponent: (close[t] − cloud top) / close[t] x 100 above the cloud, (close[t] − cloud bottom) / close[t] x 100 below it, 0 inside. Span A = (midpoint of high/low over 9 bars + midpoint over 26 bars) / 2, and span B = midpoint of high/low over 52 bars, both taken 26 bars back. It is signed and grows as the close moves further above the top or below the bottom. | measures: situation
- Component: IchimokuCloudWidthComponent: abs(span A − span B) / close[t] x 100, from high, low and close with the same spans and 26-bar displacement. It is never negative and grows as the cloud thickens; a `form` giving its inverse would make it grow as the cloud thins. | measures: comparison

## 021-04_thin-cloud-downward-breakdown_1d
- Component: IchimokuCloudPositionComponent: the signed distance of close[t] from the nearer edge of the cloud, in percent of the close. It is 0 inside the cloud, negative below it and positive above it, and its size grows with the distance from the cloud. Span A is the mean of the 9-bar and 26-bar (highest high + lowest low) / 2, and span B is the 52-bar (highest high + lowest low) / 2, both on windows ending at bar t-26. It reads high, low and close. | measures: situation
- Component: IchimokuCloudWidthComponent: abs(span A - span B) / close[t] x 100, with the spans as above, from high, low and close. It is never negative and grows as the cloud thickens. A config would centre it against its usual level to weight falls through a thin cloud. | measures: comparison
