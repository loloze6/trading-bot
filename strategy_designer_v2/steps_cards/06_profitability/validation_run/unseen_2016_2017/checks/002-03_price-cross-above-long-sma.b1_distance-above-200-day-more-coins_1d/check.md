---
backtest: 002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.344 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.7449 | above 0 | no |
| Mean daily return, on days in a position | 0.00351 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.798 | above 0 | yes |
| Calmar | 5.085 | above 0.75 | yes |
| Trades per day | 0.1021 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.346 % |
| Yearly return | +159.4 % (over 1.99 years) |
| Days in a position | 82 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/validation_run/unseen_2016_2017/backtests/002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
