---
backtest: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.954 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3809 | above 0 | no |
| Mean daily return | 0.003696 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.697 | above 0 | yes |
| Calmar | 12.37 | above 0.75 | yes |
| Trades per day | 1.299 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/retest_1h_run/unseen_2016_2017/backtests/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
