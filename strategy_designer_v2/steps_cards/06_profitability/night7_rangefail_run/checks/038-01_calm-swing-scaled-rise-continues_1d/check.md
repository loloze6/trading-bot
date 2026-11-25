---
backtest: 038-01_calm-swing-scaled-rise-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9096 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3569 | above 0 | yes |
| Mean daily return, on days in a position | 0.001289 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7702 | above 0 | yes |
| Calmar | 0.6985 | above 0.75 | no |
| Trades per day | 0.1676 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.269 % |
| Yearly return | +21.1 % (over 7.94 years) |
| Days in a position | 47 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/038-01_calm-swing-scaled-rise-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
