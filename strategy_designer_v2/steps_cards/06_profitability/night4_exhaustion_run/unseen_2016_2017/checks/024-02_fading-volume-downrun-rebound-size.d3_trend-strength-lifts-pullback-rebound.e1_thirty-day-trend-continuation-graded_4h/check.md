---
backtest: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.481 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3577 | above 0 | no |
| Mean daily return | 0.00354 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.991 | above 0 | yes |
| Calmar | 10.78 | above 0.75 | yes |
| Trades per day | 0.4684 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night4_exhaustion_run/unseen_2016_2017/backtests/024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
