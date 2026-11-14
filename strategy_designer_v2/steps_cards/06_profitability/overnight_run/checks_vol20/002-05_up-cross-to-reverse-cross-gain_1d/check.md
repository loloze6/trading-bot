---
backtest: 002-05_up-cross-to-reverse-cross-gain_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3762 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1934 | above 0 | no |
| Mean daily return | 0.0002062 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.03304 | above 0 | yes |
| Calmar | 0.141 | above 0.75 | no |
| Trades per bar | 0.04207 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/full_data_run/backtests/002-05_up-cross-to-reverse-cross-gain_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
