# Component wish list

One block per idea that needs components the catalogue does not have.

## 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d
- Component: CloudFallGentlenessComponent: from high and low, takes the cloud mid level C(i) as in `IchimokuCloudSlopeComponent` (tenkan 9, kijun 26, senkou 52, displacement 26) and its fall D = max(0, -(C(t) - C(t-26)) / C(t-26) x 100), and outputs 1 / (1 + D), from 0 to 1, never negative; it equals 1 when the cloud is flat or rising and shrinks toward 0 as the cloud falls faster over 26 bars, so standardised and negated it gives a short that grows as the fall slows | measures: comparison

## 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d
- Component: IchimokuCloudThinness: 1 / (1 + abs(span A - span B) / close x 100), using the same displaced spans as IchimokuCloudWidthComponent, from high, low and close; always positive, at most 1 when the spans meet, and growing smoothly as the cloud thins against the price | measures: comparison
