# Component wish list

One block per idea that needs components the catalogue does not have.

## 060-02_falling-calm-low-to-close-fade_1d
- Component: CloseAboveLowInUsualMoves: (close[t] - low[t]) / close[t] / s, where s is the std (ddof 1) of the last 30 one-bar returns close[j]/close[j-1] - 1 including bar t; it reads high, low and close, is 0 with the close at the low, and grows linearly as the close stands further above the low in usual daily moves | measures: comparison
