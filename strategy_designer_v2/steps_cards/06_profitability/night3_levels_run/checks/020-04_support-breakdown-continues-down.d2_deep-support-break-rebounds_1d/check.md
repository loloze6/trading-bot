---
backtest: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4034 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1508 | above 0 | no |
| Mean daily return | 0.0003793 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2729 | above 0 | yes |
| Calmar | 0.1744 | above 0.75 | no |
| Trades per day | 0.135 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
