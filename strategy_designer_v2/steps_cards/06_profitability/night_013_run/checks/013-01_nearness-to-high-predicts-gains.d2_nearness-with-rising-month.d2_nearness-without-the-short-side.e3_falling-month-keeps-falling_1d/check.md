---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2692 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8234 | above 0 | no |
| Mean daily return | -0.0001861 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4683 | above 0 | no |
| Calmar | -0.1399 | above 0.75 | no |
| Trades per bar | 0.1823 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
