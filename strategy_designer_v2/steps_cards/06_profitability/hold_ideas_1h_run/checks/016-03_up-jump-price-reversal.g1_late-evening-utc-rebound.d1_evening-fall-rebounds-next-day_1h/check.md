---
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4216 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1322 | above 0 | no |
| Mean daily return | 0.00032 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2924 | above 0 | yes |
| Calmar | 0.1408 | above 0.75 | no |
| Trades per day | 0.7854 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/hold_ideas_1h_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
