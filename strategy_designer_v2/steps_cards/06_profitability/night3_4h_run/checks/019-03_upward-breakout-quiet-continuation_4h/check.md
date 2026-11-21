---
backtest: 019-03_upward-breakout-quiet-continuation_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8977 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3439 | above 0 | yes |
| Mean daily return | 0.001049 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7595 | above 0 | yes |
| Calmar | 0.7487 | above 0.75 | no |
| Trades per day | 0.2764 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
