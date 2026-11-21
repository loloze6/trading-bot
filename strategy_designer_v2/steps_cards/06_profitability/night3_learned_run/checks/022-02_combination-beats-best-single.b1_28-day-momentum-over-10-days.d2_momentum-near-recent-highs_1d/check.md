---
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.081 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.527 | above 0 | yes |
| Mean daily return | 0.0009956 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9223 | above 0 | yes |
| Calmar | 0.7651 | above 0.75 | yes |
| Trades per day | 0.1552 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
