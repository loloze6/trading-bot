---
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1007 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4535 | above 0 | no |
| Mean daily return | 0.0001028 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.08107 | above 0 | no |
| Calmar | -0.04833 | above 0.75 | no |
| Trades per bar | 0.8085 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
