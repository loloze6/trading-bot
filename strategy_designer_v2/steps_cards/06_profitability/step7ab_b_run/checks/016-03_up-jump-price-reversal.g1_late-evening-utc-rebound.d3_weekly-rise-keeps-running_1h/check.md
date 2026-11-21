---
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.902 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3483 | above 0 | yes |
| Mean daily return | 0.0008947 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7142 | above 0 | yes |
| Calmar | 0.8512 | above 0.75 | yes |
| Trades per day | 0.6516 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
