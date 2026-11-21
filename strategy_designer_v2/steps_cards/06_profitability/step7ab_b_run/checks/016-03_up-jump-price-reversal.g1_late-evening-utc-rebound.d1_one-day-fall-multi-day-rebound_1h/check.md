---
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5883 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.03453 | above 0 | yes |
| Mean daily return | 0.0009372 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4551 | above 0 | yes |
| Calmar | 0.2814 | above 0.75 | no |
| Trades per day | 0.4854 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
