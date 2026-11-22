---
backtest: 024-04_downrun-volume-fade-depth-rebound_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6995 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1457 | above 0 | yes |
| Mean daily return | 0.001381 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5503 | above 0 | yes |
| Calmar | 0.3497 | above 0.75 | no |
| Trades per day | 0.08576 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-04_downrun-volume-fade-depth-rebound_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
