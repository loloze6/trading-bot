---
backtest: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5694 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.124 | above 0 | no |
| Mean daily return | -0.0003318 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6623 | above 0 | no |
| Calmar | -0.185 | above 0.75 | no |
| Trades per day | 0.07236 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
