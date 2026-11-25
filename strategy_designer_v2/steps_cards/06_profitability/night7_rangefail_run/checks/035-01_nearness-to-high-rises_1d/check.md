---
backtest: 035-01_nearness-to-high-rises_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.29 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6827 | above 0 | yes |
| Mean daily return, on days in a position | 0.0004662 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 1.11 | above 0 | yes |
| Calmar | 1.284 | above 0.75 | yes |
| Trades per day | 0.233 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.685 % |
| Yearly return | +17.4 % (over 7.94 years) |
| Days in a position | 99 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/035-01_nearness-to-high-rises_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
