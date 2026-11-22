---
backtest: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.053 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4989 | above 0 | yes |
| Mean daily return | 0.0003193 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.873 | above 0 | yes |
| Calmar | 0.9049 | above 0.75 | yes |
| Trades per day | 0.1101 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
