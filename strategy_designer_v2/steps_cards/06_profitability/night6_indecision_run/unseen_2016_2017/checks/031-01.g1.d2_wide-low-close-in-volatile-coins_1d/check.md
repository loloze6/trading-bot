---
backtest: 031-01.g1.d2_wide-low-close-in-volatile-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.116 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.665 | above 0 | no |
| Mean daily return, on days in a position | 0.008779 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8151 | above 0 | yes |
| Calmar | 1.972 | above 0.75 | yes |
| Trades per day | 0.01605 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.520 % |
| Yearly return | +11.2 % (over 1.99 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-01.g1.d2_wide-low-close-in-volatile-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
