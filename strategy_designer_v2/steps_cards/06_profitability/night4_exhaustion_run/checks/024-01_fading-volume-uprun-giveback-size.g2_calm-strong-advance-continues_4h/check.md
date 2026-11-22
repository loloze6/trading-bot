---
backtest: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9422 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3885 | above 0 | yes |
| Mean daily return | 0.0009559 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7738 | above 0 | yes |
| Calmar | 1.014 | above 0.75 | yes |
| Trades per day | 0.6643 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
