---
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.306 | above 0 | yes |
| Sharpe minus holding's Sharpe | 2.208 | above 0 | yes |
| Mean daily return | 0.001517 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.734 | above 0 | yes |
| Calmar | 7.851 | above 0.75 | yes |
| Trades per day | 0.1485 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2026/backtests/022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
