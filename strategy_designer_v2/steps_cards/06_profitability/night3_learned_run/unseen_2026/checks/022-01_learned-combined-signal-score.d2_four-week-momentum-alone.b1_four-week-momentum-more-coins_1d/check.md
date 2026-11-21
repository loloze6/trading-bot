---
backtest: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.022 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.9559 | above 0 | yes |
| Mean daily return | 0.001051 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5206 | above 0 | yes |
| Calmar | 1.923 | above 0.75 | yes |
| Trades per day | 0.3717 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2026/backtests/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
