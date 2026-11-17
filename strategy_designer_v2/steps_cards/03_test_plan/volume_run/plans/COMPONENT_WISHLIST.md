# Component wish list

One block per idea that needs components the catalogue does not have.

## 012-01_liquidation-flush-rebound_1d
- Component: LowerWickComponent: (min(open, close) - low) / (high - low), or divided by the coin's ATR, from the open, high, low and close columns; 0 with no lower wick, growing as the low sits further below the close | measures: situation

## 012-03_lower-wick-flush-recovery_1d
- Component: LowerWickShareComponent: (close[t] - low[t]) / (high[t] - low[t]) from the bar's high, low and close (0.5 if high equals low); 0 when the close is at the low, rising to 1 when the close is at the high, so it grows with the length of the lower wick below the close | measures: comparison

## 012-04_flush-depth-retracement-size_1d
- Component: LowerWickComponent: (min(open, close) - low) / (high - low) of the current bar, 0 to 1 (0 when high = low), from open, high, low and close; it grows as the low sits further below the bar's body | measures: situation
- Component: OpenToLowDropComponent: (open - low) / open x 100 of the current bar, from open and low, never negative; it grows with the depth of the bar's fall from its open to its low (optionally divided by the coin's usual one-bar move) | measures: comparison
