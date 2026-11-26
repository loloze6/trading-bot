---
backtest: 032-03.b1.b2_violent-decline-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1642 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4859 | above 0 | no |
| Mean daily return, on days in a position | 0.0001934 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.0755 | above 0 | yes |
| Calmar | 0.05481 | above 0.75 | no |
| Trades per day | 0.05811 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.646 % |
| Yearly return | +1.3 % (over 7.94 years) |
| Days in a position | 29 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-03.b1.b2_violent-decline-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
