# Component wish list

One block per idea that needs components the catalogue does not have.

## 054-01_deep-reclaimed-low-pierce-rebound_1d
- Component: PriorLowPierceDepth: max(0, L − low[t]) / L × 100, with L = min(low[t-30 .. t-1]) (bar t excluded), set to 0 unless close[t] ≥ L (the low is reclaimed); reads `low` and `close`, is 0 when the day did not pierce or did not reclaim, and grows linearly with how deep the day's low went under the prior 30-day low | measures: situation
