---
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1997 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3541 | above 0 | no |
| Mean daily return | 5.234e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.05774 | above 0 | no |
| Calmar | 0.06876 | above 0.75 | no |
| Trades per day | 0.07709 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
