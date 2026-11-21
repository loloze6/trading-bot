---
backtest: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8964 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.7984 | above 0 | yes |
| Mean daily return | 0.0006207 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.132 | above 0 | yes |
| Calmar | 1.493 | above 0.75 | yes |
| Trades per day | 0.1791 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2026/backtests/022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
