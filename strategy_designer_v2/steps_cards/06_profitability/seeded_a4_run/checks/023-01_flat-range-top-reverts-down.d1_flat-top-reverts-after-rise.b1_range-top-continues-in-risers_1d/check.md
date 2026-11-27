---
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d
data: XRP, TRX, ZEC, CRV, FIL, TAO, PEPE, BTC as XRPUSD, TRXUSD, ZECUSD, CRVUSD, FILUSD, TAOUSD, PEPEUSD, BTCUSD; 1d bars; windows research_2016, data use 2
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.239 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3284 | above 0 | yes |
| Mean daily return, on days in a position | 0.001938 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.089 | above 0 | yes |
| Calmar | 1.002 | above 0.75 | yes |
| Trades per day | 0.2322 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.637 % |
| Yearly return | +40.4 % (over 10.59 years) |
| Days in a position | 55 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/seeded_a4_run/backtests/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
