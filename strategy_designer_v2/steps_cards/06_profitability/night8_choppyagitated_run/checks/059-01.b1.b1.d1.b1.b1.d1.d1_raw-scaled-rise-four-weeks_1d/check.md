---
backtest: 059-01.b1.b1.d1.b1.b1.d1.d1_raw-scaled-rise-four-weeks_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3706 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9234 | above 0 | no |
| Mean daily return, on days in a position | -0.0005616 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5153 | above 0 | no |
| Calmar | -0.1439 | above 0.75 | no |
| Trades per day | 0.04813 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.330 % |
| Yearly return | -11.9 % (over 7.94 years) |
| Days in a position | 46 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b1.d1.d1_raw-scaled-rise-four-weeks_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
