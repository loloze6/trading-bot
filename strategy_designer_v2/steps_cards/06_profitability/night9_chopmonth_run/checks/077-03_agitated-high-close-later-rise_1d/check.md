---
backtest: 077-03_agitated-high-close-later-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5854 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.03259 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009523 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3708 | above 0 | yes |
| Calmar | 0.4233 | above 0.75 | no |
| Trades per day | 0.08782 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.213 % |
| Yearly return | +11.5 % (over 7.94 years) |
| Days in a position | 39 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/077-03_agitated-high-close-later-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
