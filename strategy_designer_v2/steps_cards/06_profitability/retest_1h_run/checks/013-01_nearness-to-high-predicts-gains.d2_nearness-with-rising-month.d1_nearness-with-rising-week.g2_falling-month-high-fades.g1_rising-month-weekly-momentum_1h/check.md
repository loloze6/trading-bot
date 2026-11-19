---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7273 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1735 | above 0 | yes |
| Mean daily return | 0.0004514 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.5696 | above 0 | yes |
| Calmar | 0.4219 | above 0.75 | no |
| Trades per day | 1.49 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/retest_1h_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
