---
backtest: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3773 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.931 | above 0 | no |
| Mean daily return | -0.0002061 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5028 | above 0 | no |
| Calmar | -0.1438 | above 0.75 | no |
| Trades per day | 3.448 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
