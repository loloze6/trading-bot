---
backtest: 031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.483 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4078 | above 0 | yes |
| Mean daily return, on days in a position | 0.001827 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.326 | above 0 | yes |
| Calmar | 1.418 | above 0.75 | yes |
| Trades per day | 0.3595 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.560 % |
| Yearly return | +48.9 % (over 10.59 years) |
| Days in a position | 66 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/common/backtests/031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
