---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Config: 002-05_sma-up-regime-positive-drift_config.json
Confirm: On bars with a positive forecast (SMA50 above SMA200), the mean next-bar BTC return is clearly higher than the mean over all bars, with a higher share of up bars. Bar gains also rise with the size of the forecast (top-tercile forecast bars gain more than bottom-tercile ones). Before costs, the portfolio's return per unit of exposure beats buy-and-hold.
Reject: Next-bar returns on positive-forecast bars are no higher than the all-bar mean, or are lower, which would show reversal after crosses. Gains do not grow with forecast size, or the portfolio does not beat buy-and-hold per unit of exposure before costs.
Deviation: The config uses the continuous, standardised SMA50−SMA200 spread on every bar, not the cross event and the stretch between crosses. The position therefore scales with the spread, is not constant between crosses, and tapers toward zero as the averages converge before a cross. The spread also turns negative after a downward cross, giving a short position. The idea as written only claims upward stretches rise, and treats a downward cross as the end of the trend. The test therefore also requires downward stretches to fall.
