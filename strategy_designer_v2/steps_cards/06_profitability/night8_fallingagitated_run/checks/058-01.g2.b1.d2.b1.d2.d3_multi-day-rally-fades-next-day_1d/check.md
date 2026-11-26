---
backtest: 058-01.g2.b1.d2.b1.d2.d3_multi-day-rally-fades-next-day_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3967 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.156 | above 0 | no |
| Mean daily return, on days in a position | 0.0007228 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2416 | above 0 | yes |
| Calmar | 0.2764 | above 0.75 | no |
| Trades per day | 0.03006 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.193 % |
| Yearly return | +1.4 % (over 7.94 years) |
| Days in a position | 6 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2.b1.d2.d3_multi-day-rally-fades-next-day_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
