---
backtest: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.599 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.04527 | above 0 | yes |
| Mean daily return | 0.0008293 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4503 | above 0 | yes |
| Calmar | 0.3309 | above 0.75 | no |
| Trades per day | 0.4494 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
