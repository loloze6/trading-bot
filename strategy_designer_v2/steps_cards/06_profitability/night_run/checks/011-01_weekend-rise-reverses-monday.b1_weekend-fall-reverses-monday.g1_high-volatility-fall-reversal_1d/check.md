---
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8912 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3371 | above 0 | yes |
| Mean daily return | 0.0004482 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.7974 | above 0 | yes |
| Calmar | 0.7006 | above 0.75 | no |
| Trades per bar | 0.1869 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
