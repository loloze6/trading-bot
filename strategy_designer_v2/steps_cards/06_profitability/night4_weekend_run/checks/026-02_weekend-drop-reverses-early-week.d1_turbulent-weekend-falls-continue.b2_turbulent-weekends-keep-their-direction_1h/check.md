---
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7264 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1726 | above 0 | yes |
| Mean daily return | 0.0002824 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6138 | above 0 | yes |
| Calmar | 0.4452 | above 0.75 | no |
| Trades per day | 0.1764 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
