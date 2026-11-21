---
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9039 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.8375 | above 0 | yes |
| Mean daily return | 0.0005231 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.004459 | above 0 | no |
| Calmar | 1.762 | above 0.75 | yes |
| Trades per day | 0.114 | at least 0.01 | yes |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night3_levels_run/unseen_2026/backtests/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
