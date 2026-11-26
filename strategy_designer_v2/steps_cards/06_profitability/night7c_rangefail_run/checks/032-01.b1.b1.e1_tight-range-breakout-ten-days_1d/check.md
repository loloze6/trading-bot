---
backtest: 032-01.b1.b1.e1_tight-range-breakout-ten-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9904 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.39 | above 0 | yes |
| Mean daily return, on days in a position | 0.000928 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8038 | above 0 | yes |
| Calmar | 0.6642 | above 0.75 | no |
| Trades per day | 0.01341 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.305 % |
| Yearly return | +5.8 % (over 7.94 years) |
| Days in a position | 17 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-01.b1.b1.e1_tight-range-breakout-ten-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
