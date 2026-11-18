# Component wish list

One block per idea that needs components the catalogue does not have.

## 012-03_lower-wick-flush-recovery_1d
- Component: LowerWickShareComponent: (close - low) / (high - low) of the current bar, from the high, low and close columns (0.5 if high equals low), 0 to 1, growing as the close sits further above the bar's low | measures: comparison
- Component: VolumeRatioComponent: volume / mean volume of the last `period` bars, current bar included, from the volume column, 0 and up, growing with the size of the volume burst | measures: situation

## 012-04_flush-depth-retracement-size_1d
- Component: VolumeRatioComponent: the bar's volume divided by its mean over the prior N bars (for example 20), from `volume`; it grows as the bar's volume exceeds its usual level | measures: situation
- Component: LowerWickShareComponent: (min(open, close) - low) / (high - low), from `open`, `high`, `low` and `close`, from 0 to 1; it grows as the low sits further below the bar's body | measures: situation
- Component: OpenToLowDropComponent: (open - low) / open x 100, from `open` and `low`, never negative; it grows with the depth of the bar's intrabar fall | measures: comparison
