---
backtest: 038-02_agitated-fall-vs-swing-rebound_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6686 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2763 | above 0 | no |
| Mean daily return, on days in a position | 0.001207 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5077 | above 0 | yes |
| Calmar | 0.3878 | above 0.75 | no |
| Trades per day | 0.07421 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.448 % |
| Yearly return | +5.5 % (over 10.59 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/common/backtests/038-02_agitated-fall-vs-swing-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
