---
backtest: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7623 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.8321 | above 0 | yes |
| Mean daily return | 0.0002711 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6435 | above 0 | yes |
| Calmar | 1.033 | above 0.75 | yes |
| Trades per bar | 0.1358 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/unseen_run/unseen_2026/backtests/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
