---
backtest: 067-01.b1.g1.b1.g1.d1_deepest-choppy-slides-continue_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2236 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7713 | above 0 | no |
| Mean daily return, on days in a position | -0.0003267 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4981 | above 0 | no |
| Calmar | -0.0682 | above 0.75 | no |
| Trades per day | 0.000194 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.003 % |
| Yearly return | -0.0 % (over 7.94 years) |
| Days in a position | 0 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1.b1.g1.d1_deepest-choppy-slides-continue_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
