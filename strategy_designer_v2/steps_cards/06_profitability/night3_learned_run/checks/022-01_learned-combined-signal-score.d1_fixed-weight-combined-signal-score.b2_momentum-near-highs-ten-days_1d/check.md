---
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7062 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.152 | above 0 | yes |
| Mean daily return | 0.0003425 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.5891 | above 0 | yes |
| Calmar | 0.4424 | above 0.75 | no |
| Trades per day | 0.1561 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
