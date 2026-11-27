---
backtest: 070-01.g1.d1.b1_deep-slide-run-break-fade-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5222 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.03157 | above 0 | no |
| Mean daily return, on days in a position | 0.003303 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1829 | above 0 | yes |
| Calmar | 0.3492 | above 0.75 | no |
| Trades per day | 0.01237 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.306 % |
| Yearly return | +2.9 % (over 7.94 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.g1.d1.b1_deep-slide-run-break-fade-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
