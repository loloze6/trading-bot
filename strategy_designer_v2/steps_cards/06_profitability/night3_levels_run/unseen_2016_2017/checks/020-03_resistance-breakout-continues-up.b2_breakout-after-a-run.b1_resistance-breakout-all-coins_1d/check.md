---
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.111 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5334 | above 0 | no |
| Mean daily return | 0.003602 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.816 | above 0 | yes |
| Calmar | 10.81 | above 0.75 | yes |
| Trades per day | 0.1488 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night3_levels_run/unseen_2016_2017/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
