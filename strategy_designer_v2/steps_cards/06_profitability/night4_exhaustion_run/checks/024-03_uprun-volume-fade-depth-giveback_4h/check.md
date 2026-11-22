---
backtest: 024-03_uprun-volume-fade-depth-giveback_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.8293 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.383 | above 0 | no |
| Mean daily return | -0.001916 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9721 | above 0 | no |
| Calmar | -0.6543 | above 0.75 | no |
| Trades per day | 0.1266 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-03_uprun-volume-fade-depth-giveback_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
