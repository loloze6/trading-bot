---
backtest: 017-05_settlement-move-reverses-after_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -4.783 | above 0 | no |
| Sharpe minus holding's Sharpe | -5.337 | above 0 | no |
| Mean daily return | -0.002297 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -4.99 | above 0 | no |
| Calmar | -0.5753 | above 0.75 | no |
| Trades per day | 3.585 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-05_settlement-move-reverses-after_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
