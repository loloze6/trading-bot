---
backtest: N1-07_fresh-death-cross-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5131 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.05264 | above 0 | no |
| Mean daily return | 0.0002811 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3301 | above 0 | yes |
| Calmar | 0.2864 | above 0.75 | no |
| Trades per bar | 0.04275 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-07_fresh-death-cross-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
