---
backtest: 058-01.g2.b1.d2.b1.d2.d2_modest-bounce-in-slide-fades_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7585 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2058 | above 0 | yes |
| Mean daily return, on days in a position | 0.001752 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5988 | above 0 | yes |
| Calmar | 0.6658 | above 0.75 | no |
| Trades per day | 0.02987 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.254 % |
| Yearly return | +3.6 % (over 7.94 years) |
| Days in a position | 6 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2.b1.d2.d2_modest-bounce-in-slide-fades_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
