---
backtest: 032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.791 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.7261 | above 0 | yes |
| Mean daily return, on days in a position | 0.00351 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.604 | above 0 | yes |
| Calmar | 1.893 | above 0.75 | yes |
| Trades per day | 0.01096 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.660 % |
| Yearly return | +24.3 % (over 10.59 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_rangefail_run/common/backtests/032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
