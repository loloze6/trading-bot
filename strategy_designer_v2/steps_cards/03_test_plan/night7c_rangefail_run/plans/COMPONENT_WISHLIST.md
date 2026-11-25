# Component wish list

One block per idea that needs components the catalogue does not have.

## 032-01.b1.b1.e2_small-breaks-follow-through_1d
- Component: BreakProximityAboveHigh: computes (1 / (1 + D))^power with D = (close[t] − H) / H x 100 and H = max(close[t-60 .. t-1]); it is 0 when close[t] ≤ H, equals 1 at a break of zero size, and falls smoothly toward 0 as the break grows. It reads closes only and is graded, rising as the break gets smaller. | measures: comparison
