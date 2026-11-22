---
backtest: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2667 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2874 | above 0 | no |
| Mean daily return | 0.0002201 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1199 | above 0 | yes |
| Calmar | 0.07057 | above 0.75 | no |
| Trades per day | 0.4701 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
