---
backtest: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7693 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2151 | above 0 | yes |
| Mean daily return | 0.000611 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6064 | above 0 | yes |
| Calmar | 0.7312 | above 0.75 | no |
| Trades per day | 0.331 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
