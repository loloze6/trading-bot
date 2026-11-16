---
backtest: 002-01_sma-golden-cross-upward-drift.b2_fresh-golden-cross-fades_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.0393 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5264 | above 0 | no |
| Mean daily return | 5.292e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3697 | above 0 | no |
| Calmar | 0.00716 | above 0.75 | no |
| Trades per bar | 0.007412 | at least 0.01 | no |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar; Trades per bar
Record: `steps_cards/04_backtest/backtests/002-01_sma-golden-cross-upward-drift.b2_fresh-golden-cross-fades_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
