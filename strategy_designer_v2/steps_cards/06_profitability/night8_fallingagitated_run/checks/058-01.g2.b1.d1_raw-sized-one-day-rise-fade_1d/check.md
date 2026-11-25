---
backtest: 058-01.g2.b1.d1_raw-sized-one-day-rise-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.03477 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.5876 | above 0 | no |
| Mean daily return, on days in a position | -7.624e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1361 | above 0 | no |
| Calmar | -0.03951 | above 0.75 | no |
| Trades per day | 0.05925 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.562 % |
| Yearly return | -0.9 % (over 7.94 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d1_raw-sized-one-day-rise-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
