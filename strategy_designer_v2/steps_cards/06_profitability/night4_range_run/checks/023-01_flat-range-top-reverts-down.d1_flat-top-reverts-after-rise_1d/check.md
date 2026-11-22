---
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.08 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.634 | above 0 | no |
| Mean daily return | -0.0005842 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.182 | above 0 | no |
| Calmar | -0.2425 | above 0.75 | no |
| Trades per day | 0.1458 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
