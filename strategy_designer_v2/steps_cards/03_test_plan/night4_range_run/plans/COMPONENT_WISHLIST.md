# Component wish list

One block per idea that needs components the catalogue does not have.

## 023-01_flat-range-top-reverts-down_1d
- Component: NetMoveToRangeRatio: abs(close[t] - close[t-30]) / (max(high[t-29..t]) - min(low[t-29..t])), from close, high and low; 0 to 1, larger as the 30-day net move takes up more of the range (small = flat market) | measures: situation
- Component: CloseVsHighLowRangeMid: (close[t] - (H + L) / 2) / ((H - L) / 2), with H = max(high[t-29..t]) and L = min(low[t-29..t]), from close, high and low; -1 to +1, growing as the close sits further above the range middle | measures: comparison

## 023-02_flat-range-bottom-reverts-up_1d
- Component: NetMoveToRangeRatio: abs(close[t] - close[t-30]) / (max(high[t-29..t]) - min(low[t-29..t])), from close, high and low; 0 to 1, growing as the 30-bar net move fills more of its high-low range (small means no trend) | measures: situation
- Component: HighLowRangeMidpointPosition: (close[t] - (H + L) / 2) / ((H - L) / 2), H and L being the 30-bar highest high and lowest low, bar t included; -1 to +1, more negative the further the close sits below the range's middle | measures: comparison
