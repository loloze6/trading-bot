---
backtest: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9643 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3568 | above 0 | yes |
| Mean daily return | 0.0009261 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8076 | above 0 | yes |
| Calmar | 1.029 | above 0.75 | yes |
| Trades per day | 0.3815 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
