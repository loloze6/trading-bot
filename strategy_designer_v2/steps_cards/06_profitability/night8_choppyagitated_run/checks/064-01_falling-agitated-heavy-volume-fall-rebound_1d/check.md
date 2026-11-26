---
backtest: 064-01_falling-agitated-heavy-volume-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.091 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5382 | above 0 | yes |
| Mean daily return, on days in a position | 0.004537 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9179 | above 0 | yes |
| Calmar | 2.109 | above 0.75 | yes |
| Trades per day | 0.02488 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.378 % |
| Yearly return | +7.9 % (over 7.94 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/064-01_falling-agitated-heavy-volume-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
