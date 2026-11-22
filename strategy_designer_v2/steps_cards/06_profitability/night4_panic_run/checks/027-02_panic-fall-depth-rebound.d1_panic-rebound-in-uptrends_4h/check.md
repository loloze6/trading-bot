---
backtest: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.008 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4545 | above 0 | yes |
| Mean daily return | 0.0004648 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.8533 | above 0 | yes |
| Calmar | 1.13 | above 0.75 | yes |
| Trades per day | 0.009415 | at least 0.01 | no |

- Decided by: failed: Mean daily return; Trades per day
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
