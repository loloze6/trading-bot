---
backtest: 037-01.b1_choppy-extended-fall-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.005469 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.602 | above 0 | no |
| Mean daily return, on days in a position | 8.488e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2131 | above 0 | no |
| Calmar | -0.02365 | above 0.75 | no |
| Trades per day | 0.06018 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.711 % |
| Yearly return | -0.8 % (over 7.94 years) |
| Days in a position | 24 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/037-01.b1_choppy-extended-fall-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
