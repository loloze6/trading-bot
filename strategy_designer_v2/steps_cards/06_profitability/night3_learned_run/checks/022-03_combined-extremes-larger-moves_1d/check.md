---
backtest: 022-03_combined-extremes-larger-moves_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.7213 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.276 | above 0 | no |
| Mean daily return | -0.0004697 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8647 | above 0 | no |
| Calmar | -0.2209 | above 0.75 | no |
| Trades per day | 0.2353 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-03_combined-extremes-larger-moves_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
