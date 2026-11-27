---
backtest: 075-01.d1_heavy-volume-down-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8618 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2543 | above 0 | yes |
| Mean daily return, on days in a position | 0.001499 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7373 | above 0 | yes |
| Calmar | 0.6715 | above 0.75 | no |
| Trades per day | 0.1459 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.914 % |
| Yearly return | +14.5 % (over 7.94 years) |
| Days in a position | 27 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/075-01.d1_heavy-volume-down-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
