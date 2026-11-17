---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1525 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4292 | above 0 | no |
| Mean daily return | 0.0001251 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.0646 | above 0 | yes |
| Calmar | 0.001061 | above 0.75 | no |
| Trades per bar | 0.06278 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
