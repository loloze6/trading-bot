---
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.906 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.876 | above 0 | no |
| Mean daily return | 0.003404 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.444 | above 0 | yes |
| Calmar | 7.037 | above 0.75 | yes |
| Trades per day | 0.2703 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2016_2017/backtests/022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
