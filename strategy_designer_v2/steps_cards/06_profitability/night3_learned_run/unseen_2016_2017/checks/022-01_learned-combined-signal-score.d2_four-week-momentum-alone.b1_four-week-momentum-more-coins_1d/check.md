---
backtest: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.762 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.9892 | above 0 | no |
| Mean daily return | 0.003482 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.317 | above 0 | yes |
| Calmar | 7.048 | above 0.75 | yes |
| Trades per day | 0.3451 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2016_2017/backtests/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
