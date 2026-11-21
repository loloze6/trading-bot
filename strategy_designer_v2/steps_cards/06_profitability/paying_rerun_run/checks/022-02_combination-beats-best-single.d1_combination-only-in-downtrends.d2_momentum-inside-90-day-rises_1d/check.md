---
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.184 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6294 | above 0 | yes |
| Mean daily return | 0.000881 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.058 | above 0 | yes |
| Calmar | 1.484 | above 0.75 | yes |
| Trades per day | 0.1957 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
