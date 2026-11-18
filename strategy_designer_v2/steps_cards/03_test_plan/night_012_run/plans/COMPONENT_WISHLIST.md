# Component wish list

One block per idea that needs components the catalogue does not have.

## 012-04_flush-depth-retracement-size_1d
- Component: VolumeRatioComponent: the bar's volume divided by its mean over the prior N bars (for example 20), from `volume`; it grows as the bar's volume exceeds its usual level | measures: situation
- Component: LowerWickShareComponent: (min(open, close) - low) / (high - low), from `open`, `high`, `low` and `close`, from 0 to 1; it grows as the low sits further below the bar's body | measures: situation
- Component: OpenToLowDropComponent: (open - low) / open x 100, from `open` and `low`, never negative; it grows with the depth of the bar's intrabar fall | measures: comparison
