---
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 4h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.988 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.8506 | above 0 | no |
| Mean daily return | 0.002028 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.629 | above 0 | yes |
| Calmar | 7.358 | above 0.75 | yes |
| Trades per day | 0.2051 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night3_4h_run/unseen_2016_2017/backtests/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
