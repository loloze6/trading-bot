---
backtest: 024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues_4h
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 4h bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.985 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6994 | above 0 | yes |
| Mean daily return, on days in a position | 0.003118 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.832 | above 0 | yes |
| Calmar | 3.354 | above 0.75 | yes |
| Trades per day | 0.4322 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.647 % |
| Yearly return | +77.9 % (over 9.93 years) |
| Days in a position | 55 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_exhaustion_run/common/backtests/024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
