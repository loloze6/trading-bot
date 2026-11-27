---
backtest: 031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.254 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1788 | above 0 | yes |
| Mean daily return, on days in a position | 0.002838 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.1 | above 0 | yes |
| Calmar | 1.01 | above 0.75 | yes |
| Trades per day | 0.08965 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.762 % |
| Yearly return | +18.8 % (over 10.59 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_yearlow_run/common/backtests/031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
