---
backtest: 075-01.d2_heavy-volume-fall-two-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7775 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1701 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007554 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.644 | above 0 | yes |
| Calmar | 0.6556 | above 0.75 | no |
| Trades per day | 0.5326 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.537 % |
| Yearly return | +20.3 % (over 7.94 years) |
| Days in a position | 83 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/075-01.d2_heavy-volume-fall-two-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
