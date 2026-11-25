---
backtest: 049-01_wide-day-low-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7966 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2424 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008561 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6456 | above 0 | yes |
| Calmar | 0.6048 | above 0.75 | no |
| Trades per day | 0.7361 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.046 % |
| Yearly return | +26.4 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/049-01_wide-day-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
