---
backtest: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.444 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3075 | above 0 | no |
| Mean daily return | 0.00413 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.026 | above 0 | yes |
| Calmar | 12.89 | above 0.75 | yes |
| Trades per day | 0.2148 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2016_2017/backtests/022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
