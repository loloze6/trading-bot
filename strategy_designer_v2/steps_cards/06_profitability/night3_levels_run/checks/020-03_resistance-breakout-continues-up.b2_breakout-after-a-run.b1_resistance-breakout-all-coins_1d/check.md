---
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.134 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5498 | above 0 | yes |
| Mean daily return | 0.0008091 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9379 | above 0 | yes |
| Calmar | 1.121 | above 0.75 | yes |
| Trades per day | 0.1215 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
