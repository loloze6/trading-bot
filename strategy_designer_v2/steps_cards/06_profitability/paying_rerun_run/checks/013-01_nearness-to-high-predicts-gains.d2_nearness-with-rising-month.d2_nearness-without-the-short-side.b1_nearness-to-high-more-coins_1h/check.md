---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.078 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5292 | above 0 | yes |
| Mean daily return | 0.0007008 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9242 | above 0 | yes |
| Calmar | 1.072 | above 0.75 | yes |
| Trades per day | 0.8253 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
