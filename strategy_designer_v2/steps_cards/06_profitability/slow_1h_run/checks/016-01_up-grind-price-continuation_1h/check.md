---
backtest: 016-01_up-grind-price-continuation_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.016 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.57 | above 0 | no |
| Mean daily return | -0.000522 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.174 | above 0 | no |
| Calmar | -0.2294 | above 0.75 | no |
| Trades per day | 1.153 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-01_up-grind-price-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
