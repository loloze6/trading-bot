---
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6524 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.09825 | above 0 | yes |
| Mean daily return | 0.0006555 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.518 | above 0 | yes |
| Calmar | 0.309 | above 0.75 | no |
| Trades per day | 0.2925 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
