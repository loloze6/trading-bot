---
backtest: 016-03_up-jump-price-reversal_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.77 | above 0 | no |
| Sharpe minus holding's Sharpe | -3.323 | above 0 | no |
| Mean daily return | -0.002119 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.9 | above 0 | no |
| Calmar | -0.5577 | above 0.75 | no |
| Trades per day | 1.51 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-03_up-jump-price-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
