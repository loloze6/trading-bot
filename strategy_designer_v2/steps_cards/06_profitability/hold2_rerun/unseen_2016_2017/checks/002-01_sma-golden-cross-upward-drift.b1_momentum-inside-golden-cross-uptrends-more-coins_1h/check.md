---
backtest: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1h bars; windows unseen_2016_2017
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.505 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1694 | above 0 | yes |
| Mean daily return | 0.005005 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.272 | above 0 | yes |
| Calmar | 17.89 | above 0.75 | yes |
| Trades per day | 0.2282 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/hold2_rerun/unseen_2016_2017/backtests/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
