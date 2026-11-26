---
backtest: 058-03.b1_calm-rise-continuation-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.944 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3912 | above 0 | yes |
| Mean daily return, on days in a position | 0.002674 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7765 | above 0 | yes |
| Calmar | 0.6337 | above 0.75 | no |
| Trades per day | 0.05944 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.885 % |
| Yearly return | +15.7 % (over 7.94 years) |
| Days in a position | 16 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/058-03.b1_calm-rise-continuation-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
