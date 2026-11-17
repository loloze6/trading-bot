---
backtest: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5817 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.02753 | above 0 | yes |
| Mean daily return | 0.0004459 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.4346 | above 0 | yes |
| Calmar | 0.4268 | above 0.75 | no |
| Trades per bar | 0.3957 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_013_run/backtests/013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
