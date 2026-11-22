---
backtest: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.022 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.9244 | above 0 | yes |
| Mean daily return | 0.0002925 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.7163 | above 0 | yes |
| Calmar | 1.862 | above 0.75 | yes |
| Trades per day | 0.05244 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/night4_fallingbounce_run/unseen_2026/backtests/025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
