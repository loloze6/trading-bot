---
backtest: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6597 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.106 | above 0 | yes |
| Mean daily return | 0.001395 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5222 | above 0 | yes |
| Calmar | 0.2849 | above 0.75 | no |
| Trades per day | 0.0129 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
