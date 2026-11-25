---
backtest: 035-01_wide-low-close-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7638 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2096 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008122 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6117 | above 0 | yes |
| Calmar | 0.5577 | above 0.75 | no |
| Trades per day | 0.7454 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.024 % |
| Yearly return | +24.6 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/035-01_wide-low-close-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
