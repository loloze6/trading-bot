---
backtest: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.963 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.788 | above 0 | no |
| Mean daily return | 0.001447 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.581 | above 0 | yes |
| Calmar | 3.133 | above 0.75 | yes |
| Trades per day | 0.05917 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night4_fallingbounce_run/unseen_2016_2017/backtests/025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
