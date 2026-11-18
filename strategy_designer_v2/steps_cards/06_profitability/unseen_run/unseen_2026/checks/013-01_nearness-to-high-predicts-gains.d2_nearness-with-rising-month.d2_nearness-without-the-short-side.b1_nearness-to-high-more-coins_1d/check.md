---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.001 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.9349 | above 0 | yes |
| Mean daily return | 0.0003718 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.4011 | above 0 | yes |
| Calmar | 2.085 | above 0.75 | yes |
| Trades per bar | 0.1072 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/unseen_run/unseen_2026/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
