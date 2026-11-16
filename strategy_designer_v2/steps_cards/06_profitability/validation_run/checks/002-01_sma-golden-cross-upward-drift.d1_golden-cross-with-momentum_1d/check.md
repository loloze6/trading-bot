---
backtest: 002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-momentum_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8505 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2963 | above 0 | yes |
| Mean daily return | 0.0004504 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6429 | above 0 | yes |
| Calmar | 0.7164 | above 0.75 | no |
| Trades per bar | 0.1105 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/backtests/002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-momentum_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
