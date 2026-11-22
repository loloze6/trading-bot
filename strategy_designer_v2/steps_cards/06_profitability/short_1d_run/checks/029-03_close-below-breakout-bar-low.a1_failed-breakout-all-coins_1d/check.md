---
backtest: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.363 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2445 | above 0 | no |
| Mean daily return | 3.206e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1698 | above 0 | yes |
| Calmar | 0.151 | above 0.75 | no |
| Trades per day | 0.005288 | at least 0.01 | no |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar; Trades per day
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
