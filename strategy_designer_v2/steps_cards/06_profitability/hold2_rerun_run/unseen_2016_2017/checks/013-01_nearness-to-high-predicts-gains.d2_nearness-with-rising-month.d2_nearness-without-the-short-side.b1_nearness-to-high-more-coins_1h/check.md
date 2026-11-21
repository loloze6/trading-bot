---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.696 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4478 | above 0 | no |
| Mean daily return | 0.004298 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.321 | above 0 | yes |
| Calmar | 13.76 | above 0.75 | yes |
| Trades per day | 0.2392 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/hold2_rerun_run/unseen_2016_2017/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
