---
backtest: 002-05_up-cross-to-reverse-cross-gain_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3762 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1934 | above 0 | no |
| Mean daily return | 0.0007398 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.03304 | above 0 | yes |
| Calmar | 0.0009771 | above 0.1811 | no |
| Trades per bar | 0.04207 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/full_data_run/backtests/002-05_up-cross-to-reverse-cross-gain_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
