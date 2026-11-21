---
backtest: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9139 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.296 | above 0 | yes |
| Mean daily return | 0.0005395 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7396 | above 0 | yes |
| Calmar | 0.9263 | above 0.75 | yes |
| Trades per day | 0.229 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
