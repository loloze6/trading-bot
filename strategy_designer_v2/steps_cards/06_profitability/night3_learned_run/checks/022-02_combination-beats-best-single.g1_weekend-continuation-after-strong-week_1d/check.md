---
backtest: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.06 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5053 | above 0 | yes |
| Mean daily return | 0.0002882 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.9516 | above 0 | yes |
| Calmar | 0.9848 | above 0.75 | yes |
| Trades per day | 0.06072 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
