---
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4381 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1156 | above 0 | no |
| Mean daily return | 0.0004404 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3135 | above 0 | yes |
| Calmar | 0.1819 | above 0.75 | no |
| Trades per day | 0.6462 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/step7ab_bp_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
