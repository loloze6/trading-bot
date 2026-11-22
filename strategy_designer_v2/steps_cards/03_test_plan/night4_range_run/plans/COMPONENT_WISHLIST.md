# Component wish list

One block per idea that needs components the catalogue does not have.

## 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d
- Component: HighLowRangePosition: (close[t] - (H + L) / 2) / ((H - L) / 2), with H = max(high) and L = min(low) over the last 30 bars including bar t; it runs from -1 at the low to +1 at the high and is 0 at the middle (bounded, so it can sit in a regime rule "lt 0") | measures: situation

## 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins_1d
- Component: HighLowRangePosition: (close[t] − (H + L) / 2) / ((H − L) / 2), with H = max(high) and L = min(low) over the last `period` (30) bars, bar t included; 0 when H = L; runs from −1 at the range's low to +1 at its high and grows as the close rises toward the top | measures: situation

## 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d
- Component: ShareHumpWeightedMomentum: R x s x (1 - s) from close, high and low, where R = close[t] / close[t-30] - 1 and s = abs(close[t] - close[t-30]) / (max(high) - min(low)) over the last 30 bars, clipped to 0..1. It is signed like the 30-day return and grows with the size of that return. It peaks when the share is mid-scale and goes to 0 as the share nears 0 or 1. | measures: comparison

## 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.d1_reversion-only-near-zero-net-move_1d
- Component: FlatnessWeightedRangePositionHighLow: (2 x pos − 1) x (1 − abs(close[t] − close[t-30]) / (H − L)), with H = max(high) and L = min(low) over the last 30 bars and pos = (close[t] − L) / (H − L); signed, grows with the close's height above the range middle and with how near the 30-day net move is to zero (a `source` "high_low" option on `FlatnessWeightedRangePositionComponent`) | measures: situation

## 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.d1_young-trend-continues-further_1d
- Component: NetMoveRangeAgeComponent: reads the closes, highs and lows; counts the consecutive bars, ending at bar t, on which abs(close[t]-close[t-30]) / (max high - min low over 30 bars) has stayed at or above a level such as 0.5, capped at a maximum such as 30; signs the count by the 30-day return and gives 0 when the ratio is below the level; the count grows by one for each further bar, so its inverse grows as the trend gets fresher | measures: situation

## 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up.d1_flat-range-turn-nearing-middle_1d
- Component: RangeMidpointProximity: from the 30-bar high and low, mid = (max(high) + min(low)) / 2 and D = max(0, (mid − close[t]) / mid × 100); output 1 / (1 + D) while the close is below mid, 0 at or above it (or a `side` setting); never negative, rising continuously toward 1 as the close climbs back to the middle from below | measures: situation
