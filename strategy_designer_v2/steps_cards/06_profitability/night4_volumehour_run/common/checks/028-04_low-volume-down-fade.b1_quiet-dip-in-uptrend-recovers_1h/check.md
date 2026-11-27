---
backtest: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1h bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4864 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.6133 | above 0 | no |
| Mean daily return, on days in a position | 0.0005517 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2807 | above 0 | yes |
| Calmar | 0.1208 | above 0.75 | no |
| Trades per day | 1.271 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.930 % |
| Yearly return | +7.3 % (over 10.59 years) |
| Days in a position | 43 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/common/backtests/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
