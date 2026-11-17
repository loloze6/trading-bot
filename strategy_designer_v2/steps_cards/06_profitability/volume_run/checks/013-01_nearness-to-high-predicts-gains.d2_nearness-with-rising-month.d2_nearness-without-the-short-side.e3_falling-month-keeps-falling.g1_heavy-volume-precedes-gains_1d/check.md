---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5016 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.05256 | above 0 | no |
| Mean daily return | 0.0001046 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2793 | above 0 | yes |
| Calmar | 0.2661 | above 0.75 | no |
| Trades per bar | 0.3876 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/volume_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
