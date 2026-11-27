---
backtest: 035-01.b1_calm-market-nearness-to-high_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.185 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2402 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006105 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.089 | above 0 | yes |
| Calmar | 0.7017 | above 0.75 | no |
| Trades per day | 0.1429 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.559 % |
| Yearly return | +12.9 % (over 10.59 years) |
| Days in a position | 57 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_rangefail_run/common/backtests/035-01.b1_calm-market-nearness-to-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
