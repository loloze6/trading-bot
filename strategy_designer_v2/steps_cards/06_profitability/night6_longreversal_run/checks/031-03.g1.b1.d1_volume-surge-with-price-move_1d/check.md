---
backtest: 031-03.g1.b1.d1_volume-surge-with-price-move_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7377 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1302 | above 0 | yes |
| Mean daily return, on days in a position | 0.0005994 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5816 | above 0 | yes |
| Calmar | 0.3443 | above 0.75 | no |
| Trades per day | 0.1862 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.392 % |
| Yearly return | +17.4 % (over 7.94 years) |
| Days in a position | 90 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d1_volume-surge-with-price-move_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
