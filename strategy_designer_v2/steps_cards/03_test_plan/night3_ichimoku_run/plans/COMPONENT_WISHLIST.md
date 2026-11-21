# Component wish list

One block per idea that needs components the catalogue does not have.

## 021-01_above-rising-cloud-continues-up_1d
- Component: IchimokuCloudPositionComponent: (close[t] - cloud top) / cloud top x 100, where cloud top = max(span A, span B) at bar t; span A = mean of the 9- and 26-bar (max high + min low)/2, span B = the 52-bar (max high + min low)/2, both read from bars ending 26 bars earlier; signed, and grows as the close sits further above the cloud | measures: situation
- Component: IchimokuCloudSlopeComponent: percent change over 26 bars of the cloud's level at bar t, the cloud level being the mean of span A and span B as displaced above (from high and low); signed, positive and larger the faster the cloud rises | measures: comparison

## 021-02_below-falling-cloud-continues-down_1d
- Component: IchimokuCloudDistanceComponent: (close[t] - cloud edge) / cloud edge x 100, using the lower edge when the close is below the cloud. Span A = (midpoint of 9-bar high/low + midpoint of 26-bar high/low) / 2 and span B = midpoint of the 52-bar high/low, both from high and low taken 26 bars before t. Signed, 0 inside the cloud, and growing in size the further the close sits outside it. | measures: situation
- Component: IchimokuCloudSlopeComponent: percent change of the cloud (the mean of span A and span B, displaced 26 bars) over the last 26 bars, from high and low. Signed: negative and larger in size the faster the cloud has fallen. | measures: comparison
