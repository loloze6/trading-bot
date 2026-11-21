---
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7151 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6171 | above 0 | yes |
| Mean daily return | 0.0005307 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.005656 | above 0 | yes |
| Calmar | 0.9976 | above 0.75 | yes |
| Trades per day | 0.1381 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2026/backtests/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
