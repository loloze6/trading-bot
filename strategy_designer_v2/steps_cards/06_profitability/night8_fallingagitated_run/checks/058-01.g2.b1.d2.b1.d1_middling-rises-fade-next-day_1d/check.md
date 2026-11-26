---
backtest: 058-01.g2.b1.d2.b1.d1_middling-rises-fade-next-day_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4425 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1103 | above 0 | no |
| Mean daily return, on days in a position | 0.0004232 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2475 | above 0 | yes |
| Calmar | 0.2731 | above 0.75 | no |
| Trades per day | 0.05587 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.194 % |
| Yearly return | +1.6 % (over 7.94 years) |
| Days in a position | 11 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2.b1.d1_middling-rises-fade-next-day_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
