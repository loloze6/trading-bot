# Component wish list

One block per idea that needs components the catalogue does not have.

## 043-01_falling-agitated-intraday-drop-rebound_1d
- Component: OpenToCloseDropComponent: max(0, (open[t] - close[t]) / open[t] x 100), from open and close of bar t; 0 on bars closing at or above their open, growing linearly with the percent fall from open to close | measures: situation
