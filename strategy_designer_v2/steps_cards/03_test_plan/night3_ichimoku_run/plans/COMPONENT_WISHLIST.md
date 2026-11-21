# Component wish list

One block per idea that needs components the catalogue does not have.

## 021-03_thin-cloud-upward-breakout_1d
- Component: CloudCrossUpAgeComponent: from high, low and close with the standard Ichimoku spans (9, 26, 52, displacement 26), +n while the close has stayed above the cloud top for n bars since its last move out of the cloud whose previous outside side was below the bottom, else 0 or -n for the mirror case, capped at a max_bars; it grows by one each bar the close stays above after a cross from below | measures: situation

## 021-04_thin-cloud-downward-breakdown_1d
- Component: CloudThinnessBreakBelowComponent: on bars where close[t] is below the cloud bottom, it computes the distance below the bottom (percent of close) divided by (1 + cloud width in percent of close), from high, low and close with the standard Ichimoku spans (9/26/52, displaced 26). It is 0 inside or above the cloud and continuous at the edge, and it grows in size as the close falls further below a thinner cloud | measures: comparison

## 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d
- Component: CloudFallGentlenessComponent: from high and low, takes the cloud mid level C(i) as in `IchimokuCloudSlopeComponent` (tenkan 9, kijun 26, senkou 52, displacement 26) and its fall D = max(0, -(C(t) - C(t-26)) / C(t-26) x 100), and outputs 1 / (1 + D), from 0 to 1, never negative; it equals 1 when the cloud is flat or rising and shrinks toward 0 as the cloud falls faster over 26 bars, so standardised and negated it gives a short that grows as the fall slows | measures: comparison
