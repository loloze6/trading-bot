---
backtest: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2166 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3371 | above 0 | no |
| Mean daily return | 4.703e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.01505 | above 0 | yes |
| Calmar | 0.0971 | above 0.75 | no |
| Trades per day | 0.05016 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
