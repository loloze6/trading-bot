---
backtest: 023-01_flat-range-top-reverts-down_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1643 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3898 | above 0 | no |
| Mean daily return | 7.523e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.02818 | above 0 | yes |
| Calmar | 0.02719 | above 0.75 | no |
| Trades per day | 0.2018 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
