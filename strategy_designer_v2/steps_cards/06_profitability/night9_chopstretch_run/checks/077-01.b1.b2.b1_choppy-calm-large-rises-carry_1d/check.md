---
backtest: 077-01.b1.b2.b1_choppy-calm-large-rises-carry_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.314 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2388 | above 0 | no |
| Mean daily return, on days in a position | 0.001907 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.05547 | above 0 | yes |
| Calmar | 0.1152 | above 0.75 | no |
| Trades per day | 0.004586 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.212 % |
| Yearly return | +1.2 % (over 7.94 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar; Trades per day
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/077-01.b1.b2.b1_choppy-calm-large-rises-carry_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
