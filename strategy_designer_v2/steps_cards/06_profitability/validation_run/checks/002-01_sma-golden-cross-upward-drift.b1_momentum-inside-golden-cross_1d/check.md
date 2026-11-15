---
backtest: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4881 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.07762 | above 0 | no |
| Mean daily return | 0.000316 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.307 | above 0 | yes |
| Calmar | 0.2291 | above 0.75 | no |
| Trades per bar | 0.2325 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/backtests/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
