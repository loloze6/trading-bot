---
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.564 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4994 | above 0 | yes |
| Mean daily return, on days in a position | 0.00207 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.375 | above 0 | yes |
| Calmar | 2.079 | above 0.75 | yes |
| Trades per day | 0.221 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.301 % |
| Yearly return | +43.0 % (over 10.59 years) |
| Days in a position | 51 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/seeded_a4_run/common/backtests/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
