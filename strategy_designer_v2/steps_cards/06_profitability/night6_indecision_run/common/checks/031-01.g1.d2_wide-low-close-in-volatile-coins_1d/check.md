---
backtest: 031-01.g1.d2_wide-low-close-in-volatile-coins_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.051 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.01369 | above 0 | no |
| Mean daily return, on days in a position | 0.007642 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9938 | above 0 | yes |
| Calmar | 1.081 | above 0.75 | yes |
| Trades per day | 0.01661 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.470 % |
| Yearly return | +9.5 % (over 10.59 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_indecision_run/common/backtests/031-01.g1.d2_wide-low-close-in-volatile-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
