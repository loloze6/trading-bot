---
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.356 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2914 | above 0 | yes |
| Mean daily return, on days in a position | 0.001318 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.185 | above 0 | yes |
| Calmar | 1.16 | above 0.75 | yes |
| Trades per day | 0.2215 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.663 % |
| Yearly return | +46.4 % (over 10.59 years) |
| Days in a position | 90 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_range_run/common/backtests/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
