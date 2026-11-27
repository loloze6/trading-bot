---
backtest: 075-01.d3_heavy-volume-deep-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6338 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.02633 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007082 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4704 | above 0 | yes |
| Calmar | 0.5103 | above 0.75 | no |
| Trades per day | 0.3339 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.267 % |
| Yearly return | +13.2 % (over 7.94 years) |
| Days in a position | 59 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/075-01.d3_heavy-volume-deep-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
