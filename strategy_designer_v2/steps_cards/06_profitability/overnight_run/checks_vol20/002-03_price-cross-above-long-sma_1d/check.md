---
backtest: 002-03_price-cross-above-long-sma_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5051 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.06455 | above 0 | no |
| Mean daily return | 0.0002767 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1867 | above 0 | yes |
| Calmar | 0.2436 | above 0.75 | no |
| Trades per bar | 0.1105 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/full_data_run/backtests/002-03_price-cross-above-long-sma_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
