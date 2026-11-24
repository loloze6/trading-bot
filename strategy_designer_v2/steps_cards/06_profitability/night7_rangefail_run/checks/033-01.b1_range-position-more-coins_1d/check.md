---
backtest: 033-01.b1_range-position-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7841 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1767 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007159 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6599 | above 0 | yes |
| Calmar | 0.6099 | above 0.75 | no |
| Trades per day | 0.4884 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.743 % |
| Yearly return | +22.9 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/033-01.b1_range-position-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
