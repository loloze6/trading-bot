---
backtest: 075-01.g1_heavy-volume-down-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.687 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.07955 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006387 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5342 | above 0 | yes |
| Calmar | 0.5448 | above 0.75 | no |
| Trades per day | 0.3964 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.312 % |
| Yearly return | +15.1 % (over 7.94 years) |
| Days in a position | 74 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/075-01.g1_heavy-volume-down-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
