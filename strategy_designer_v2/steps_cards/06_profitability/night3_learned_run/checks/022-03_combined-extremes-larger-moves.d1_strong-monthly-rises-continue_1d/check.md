---
backtest: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.037 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.483 | above 0 | yes |
| Mean daily return | 0.0008619 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8908 | above 0 | yes |
| Calmar | 1.047 | above 0.75 | yes |
| Trades per day | 0.1852 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
