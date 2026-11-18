---
backtest: 012-01_liquidation-flush-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5572 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.003018 | above 0 | yes |
| Mean daily return | 0.0003866 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3642 | above 0 | yes |
| Calmar | 0.4029 | above 0.75 | no |
| Trades per bar | 0.1486 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/volume_run/backtests/012-01_liquidation-flush-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
