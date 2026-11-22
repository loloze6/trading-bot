---
backtest: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.815 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2613 | above 0 | yes |
| Mean daily return | 0.0007888 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.666 | above 0 | yes |
| Calmar | 0.4897 | above 0.75 | no |
| Trades per day | 0.1244 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
