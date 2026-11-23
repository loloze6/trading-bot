# Component wish list

One block per idea that needs components the catalogue does not have.

## 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d2_calm-up-saturday-continues-higher_1h
- Component: LaggedRiseTimesCalmness: max(0, close[t-lag] / close[t-lag-period] - 1) x mean(s over the last vol_lookback bars) / s(t), with s(i) the std of the vol_period hourly close-to-close returns ending at bar i (period 24, lag 24, vol_period 720, vol_lookback 8760), from closes only. It is 0 after a flat or down Saturday and grows with Saturday's rise and with how far current volatility sits below its past-year average | measures: situation

## 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d1_sunday-reversal-grows-with-volatility_1h
- Component: MeanAbsScaledReturnTimesVolatilityComponent: from closes, (close[t] / close[t-24] - 1) / m x s. Here m is the mean of abs(close[i] / close[i-24] - 1) over the last 720 bars, and s is the std (ddof 1) of the last 720 one-bar returns. It is signed like the 24-bar return, and its size grows with that move in usual 24h moves and with the coin's hourly volatility | measures: comparison
