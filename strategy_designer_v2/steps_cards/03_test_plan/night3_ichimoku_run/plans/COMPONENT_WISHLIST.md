# Component wish list

One block per idea that needs components the catalogue does not have.

## 021-04_thin-cloud-downward-breakdown_1d
- Component: IchimokuCloudPositionComponent: the signed distance of close[t] from the nearer edge of the cloud, in percent of the close. It is 0 inside the cloud, negative below it and positive above it, and its size grows with the distance from the cloud. Span A is the mean of the 9-bar and 26-bar (highest high + lowest low) / 2, and span B is the 52-bar (highest high + lowest low) / 2, both on windows ending at bar t-26. It reads high, low and close. | measures: situation
- Component: IchimokuCloudWidthComponent: abs(span A - span B) / close[t] x 100, with the spans as above, from high, low and close. It is never negative and grows as the cloud thickens. A config would centre it against its usual level to weight falls through a thin cloud. | measures: comparison

## 021-03_thin-cloud-upward-breakout_1d
- Component: CloudCrossUpAgeComponent: from high, low and close with the standard Ichimoku spans (9, 26, 52, displacement 26), +n while the close has stayed above the cloud top for n bars since its last move out of the cloud whose previous outside side was below the bottom, else 0 or -n for the mirror case, capped at a max_bars; it grows by one each bar the close stays above after a cross from below | measures: situation
