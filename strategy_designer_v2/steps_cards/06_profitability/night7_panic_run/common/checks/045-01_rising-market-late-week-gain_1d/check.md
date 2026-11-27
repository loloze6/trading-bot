---
backtest: 045-01_rising-market-late-week-gain_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.256 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1921 | above 0 | yes |
| Mean daily return, on days in a position | 0.003287 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.087 | above 0 | yes |
| Calmar | 1.22 | above 0.75 | yes |
| Trades per day | 0.06758 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.768 % |
| Yearly return | +19.0 % (over 10.59 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_panic_run/common/backtests/045-01_rising-market-late-week-gain_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
