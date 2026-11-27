---
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.495 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4198 | above 0 | yes |
| Mean daily return, on days in a position | 0.002549 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.354 | above 0 | yes |
| Calmar | 1.041 | above 0.75 | yes |
| Trades per day | 0.05138 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.034 % |
| Yearly return | +31.8 % (over 10.59 years) |
| Days in a position | 32 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
