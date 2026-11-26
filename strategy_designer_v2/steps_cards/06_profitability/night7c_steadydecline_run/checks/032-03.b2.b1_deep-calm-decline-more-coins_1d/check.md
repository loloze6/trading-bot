---
backtest: 032-03.b2.b1_deep-calm-decline-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.007421 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.5918 | above 0 | no |
| Mean daily return, on days in a position | -7.581e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2175 | above 0 | no |
| Calmar | -0.04313 | above 0.75 | no |
| Trades per day | 0.1118 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.065 % |
| Yearly return | -2.2 % (over 7.94 years) |
| Days in a position | 55 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-03.b2.b1_deep-calm-decline-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
