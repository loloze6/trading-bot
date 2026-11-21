# Component wish list

One block per idea that needs components the catalogue does not have.

## 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_volume-burst-move-reverses_1h
- Component: VolumeConcentrationWeightedMove: (sum of the top_k largest volumes among the last `period` bars / sum of the `period` volumes) x (close[t] - close[t-period]) / close[t-period] x 100, from volume and close; signed like the move, and its size grows with both the move and the share of volume in the busiest hours (period 72, top_k 1; `negate` gives the lean against the move) | measures: situation
