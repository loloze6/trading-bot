---
backtest: 020-01_resistance-retest-turns-down_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.8127 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.367 | above 0 | no |
| Mean daily return | -0.0008463 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9417 | above 0 | no |
| Calmar | -0.3334 | above 0.75 | no |
| Trades per day | 0.2437 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
