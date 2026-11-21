---
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.023 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4383 | above 0 | yes |
| Mean daily return | 0.0006927 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7425 | above 0 | yes |
| Calmar | 0.7413 | above 0.75 | no |
| Trades per day | 0.1118 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
