---
backtest: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9496 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3958 | above 0 | yes |
| Mean daily return | 0.00119 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7851 | above 0 | yes |
| Calmar | 0.839 | above 0.75 | yes |
| Trades per day | 0.08131 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
