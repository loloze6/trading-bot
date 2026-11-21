---
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9465 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3621 | above 0 | yes |
| Mean daily return | 0.0009813 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6941 | above 0 | yes |
| Calmar | 0.8054 | above 0.75 | yes |
| Trades per day | 0.1611 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
