---
backtest: 059-01.b1.b1.d1.b1.b2.d3_held-rise-in-rising-month_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6972 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1444 | above 0 | yes |
| Mean daily return, on days in a position | 0.002213 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5325 | above 0 | yes |
| Calmar | 0.3817 | above 0.75 | no |
| Trades per day | 0.02042 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.501 % |
| Yearly return | +6.4 % (over 7.94 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b2.d3_held-rise-in-rising-month_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
